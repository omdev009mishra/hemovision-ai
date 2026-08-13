"""Dataset-freeze checks for governed research datasets.

This module produces integrity reports only. A frozen dataset is not clinically
validated, and this workflow never enables clinical model training.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from ml.src.data.exif_sanitizer import EXIFSanitizer
from ml.src.data.withdrawal import WithdrawalManager
from ml.src.research.privacy import find_direct_identifier_keys


class FreezeStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    FROZEN = "FROZEN"
    RELEASED_FOR_RESEARCH = "RELEASED_FOR_RESEARCH"


class DatasetFreezeAuthorizationError(PermissionError):
    """Raised when a caller without authorization tries to freeze or mutate data."""


class DatasetFreezeValidationError(ValueError):
    """Raised after a freeze candidate fails a required integrity check."""


def _to_dict(record: Any) -> Dict[str, Any]:
    if isinstance(record, Mapping):
        return dict(record)
    if is_dataclass(record):
        return asdict(record)
    if hasattr(record, "__dict__"):
        return dict(vars(record))
    raise TypeError("Research records must be mappings or dataclass-like objects.")


class DatasetFreezeManager:
    """Validates and freezes a controlled research snapshot with explicit authority."""

    def __init__(self, report_dir: str = "research/reports/freeze") -> None:
        self.report_dir = Path(report_dir)
        self.status = FreezeStatus.OPEN

    def assert_modifiable(self) -> None:
        if self.status in {FreezeStatus.FROZEN, FreezeStatus.RELEASED_FOR_RESEARCH}:
            raise DatasetFreezeAuthorizationError("Frozen datasets cannot be modified by this workflow.")

    def begin_review(self, *, authorized: bool) -> None:
        if not authorized:
            raise DatasetFreezeAuthorizationError("Authorized workflow is required to begin freeze review.")
        self.assert_modifiable()
        self.status = FreezeStatus.UNDER_REVIEW

    def freeze(
        self,
        records: Sequence[Any],
        consent_records: Sequence[Mapping[str, Any]],
        *,
        authorized: bool,
        dataset_type: str = "synthetic",
        governance_status: str = "synthetic",
        schema_valid: bool = True,
        splits: Optional[Mapping[str, Iterable[str]]] = None,
    ) -> Dict[str, Any]:
        """Freeze a reviewed snapshot and write JSON/Markdown integrity reports.

        Rejected images, segmentation failures, unaligned laboratory references,
        and withdrawn participants are excluded from the research-ready subset.
        They are counted in the report, not silently converted into usable data.
        """
        if not authorized:
            raise DatasetFreezeAuthorizationError("Only an authorized workflow can transition a dataset to FROZEN.")
        self.assert_modifiable()
        self.status = FreezeStatus.UNDER_REVIEW

        all_records = [_to_dict(record) for record in records]
        checks: Dict[str, Any] = {
            "governance": self._governance_ok(dataset_type, governance_status),
            "consent": self._consent_ok(consent_records),
            "schema_validation": bool(schema_valid),
            "duplicate_detection": self._duplicate_image_ids(all_records),
            "pii_scan": self._pii_ok(all_records, consent_records),
            "exif_privacy": self._exif_ok(all_records),
            "participant_level_split": self._split_ok(splits or {}),
        }
        hard_failures = [
            name for name, outcome in checks.items()
            if outcome is False or (isinstance(outcome, dict) and not outcome.get("ok", False))
        ]

        active_records, withdrawn_records, withdrawn_ids = WithdrawalManager.filter_active_records(
            all_records, list(consent_records)
        )
        eligible_records: List[Dict[str, Any]] = []
        quality_excluded = segmentation_excluded = alignment_excluded = 0
        for record in active_records:
            if not self._is_usable(record):
                quality_excluded += 1
                continue
            if not self._segmentation_succeeded(record):
                segmentation_excluded += 1
                continue
            if not self._lab_aligned(record):
                alignment_excluded += 1
                continue
            eligible_records.append(record)

        checks.update(
            {
                "image_quality": {"ok": True, "excluded": quality_excluded},
                "segmentation_status": {"ok": True, "excluded": segmentation_excluded},
                "lab_alignment": {"ok": True, "excluded": alignment_excluded},
                "withdrawal_status": {"ok": True, "excluded": len(withdrawn_records)},
            }
        )
        report = self._build_report(
            all_records=all_records,
            eligible_records=eligible_records,
            withdrawn_ids=withdrawn_ids,
            checks=checks,
            hard_failures=hard_failures,
            excluded_count=len(all_records) - len(eligible_records),
        )
        self._write_report(report)
        if hard_failures:
            self.status = FreezeStatus.UNDER_REVIEW
            raise DatasetFreezeValidationError(
                "Dataset cannot be frozen until checks pass: " + ", ".join(hard_failures)
            )

        self.status = FreezeStatus.FROZEN
        report["freeze_status"] = self.status.value
        self._write_report(report)
        return report

    @staticmethod
    def _governance_ok(dataset_type: str, governance_status: str) -> bool:
        # Synthetic validation can be frozen. Any clinical candidate needs an
        # explicit external governance record; this code never supplies one.
        return dataset_type.lower() == "synthetic" or governance_status.lower() == "approved"

    @staticmethod
    def _consent_ok(consent_records: Sequence[Mapping[str, Any]]) -> bool:
        return all(
            str(record.get("consent_status", "")).lower() in {"given", "verified_active", "withdrawn"}
            for record in consent_records
        )

    @staticmethod
    def _duplicate_image_ids(records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
        ids = [str(record.get("image_id")) for record in records if record.get("image_id")]
        duplicates = sorted({image_id for image_id in ids if ids.count(image_id) > 1})
        return {"ok": not duplicates, "duplicate_count": len(duplicates)}

    @staticmethod
    def _pii_ok(
        records: Sequence[Mapping[str, Any]], consent_records: Sequence[Mapping[str, Any]]
    ) -> Dict[str, Any]:
        findings: List[str] = []
        for index, record in enumerate([*records, *consent_records]):
            findings.extend(f"record[{index}].{key}" for key in find_direct_identifier_keys(record))
        return {"ok": not findings, "finding_count": len(findings)}

    @staticmethod
    def _exif_ok(records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
        violations = 0
        for record in records:
            exif = record.get("exif_metadata")
            if isinstance(exif, Mapping):
                _, had_forbidden = EXIFSanitizer.sanitize_metadata(dict(exif))
                violations += int(had_forbidden)
        return {"ok": violations == 0, "forbidden_metadata_records": violations}

    @staticmethod
    def _split_ok(splits: Mapping[str, Iterable[str]]) -> Dict[str, Any]:
        seen: set[str] = set()
        overlaps: set[str] = set()
        for participant_ids in splits.values():
            current = set(participant_ids)
            overlaps.update(seen.intersection(current))
            seen.update(current)
        return {"ok": not overlaps, "overlap_count": len(overlaps)}

    @staticmethod
    def _is_usable(record: Mapping[str, Any]) -> bool:
        value = str(record.get("quality_status", record.get("image_quality_status", "USABLE"))).upper()
        return value == "USABLE"

    @staticmethod
    def _segmentation_succeeded(record: Mapping[str, Any]) -> bool:
        value = record.get("segmentation_status", record.get("segmentation_success", "SUCCEEDED"))
        return value is True or str(value).upper() in {"SUCCEEDED", "SUCCESS", "TRUE"}

    @staticmethod
    def _lab_aligned(record: Mapping[str, Any]) -> bool:
        value = record.get("alignment_status", "aligned")
        return str(value).lower() == "aligned"

    def _build_report(
        self,
        *,
        all_records: Sequence[Mapping[str, Any]],
        eligible_records: Sequence[Mapping[str, Any]],
        withdrawn_ids: set[str],
        checks: Mapping[str, Any],
        hard_failures: Sequence[str],
        excluded_count: int,
    ) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        return {
            "freeze_status": self.status.value,
            "freeze_timestamp": timestamp,
            "clinical_validation_status": "NOT_PERFORMED",
            "clinical_training_status": "BLOCKED",
            "record_count": len(all_records),
            "research_ready_image_count": len(eligible_records),
            "excluded_image_count": excluded_count,
            "withdrawn_participant_count": len(withdrawn_ids),
            "checks": dict(checks),
            "hard_failures": list(hard_failures),
        }

    def _write_report(self, report: Mapping[str, Any]) -> Tuple[Path, Path]:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        json_path = self.report_dir / "freeze_report.json"
        markdown_path = self.report_dir / "freeze_report.md"
        json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        checks_md = "\n".join(
            f"- `{name}`: {'PASS' if outcome is True or (isinstance(outcome, dict) and outcome.get('ok')) else 'FAIL'}"
            for name, outcome in report["checks"].items()
        )
        markdown_path.write_text(
            "# Dataset Freeze Report\n\n"
            f"- Freeze status: `{report['freeze_status']}`\n"
            f"- Clinical validation: `{report['clinical_validation_status']}`\n"
            f"- Clinical training: `{report['clinical_training_status']}`\n"
            f"- Research-ready images: `{report['research_ready_image_count']}`\n"
            f"- Excluded images: `{report['excluded_image_count']}`\n\n"
            "## Integrity checks\n\n"
            f"{checks_md}\n",
            encoding="utf-8",
        )
        return json_path, markdown_path
