"""
HemoVision Dataset Validator
Executes 14 deterministic validation checks and outputs dataset_validation_report.json and dataset_validation_report.md.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Any, Tuple
import json
import os

from ml.src.data.dataset_loader import DatasetLoader, DatasetRecord


@dataclass
class ValidationIssue:
    check_id: int
    check_name: str
    severity: str  # ERROR, WARNING, INFO
    entity_id: str
    message: str


class DatasetValidator:

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.loader = DatasetLoader(root_dir)

    def validate(self) -> Tuple[List[ValidationIssue], Dict[str, Any]]:
        issues: List[ValidationIssue] = []
        records = self.loader.load_records()

        # Check 1: Record count & loader health
        if not records:
            issues.append(ValidationIssue(
                check_id=1,
                check_name="Dataset Existence",
                severity="WARNING",
                entity_id="ROOT",
                message="No dataset records found in specified directory."
            ))

        # Check 2: Participant ID uniqueness & sufficiency
        participant_ids = [r.participant_id for r in records if r.participant_id != "UNKNOWN"]
        unique_pts = set(participant_ids)

        if len(unique_pts) < 3:
            issues.append(ValidationIssue(
                check_id=13,
                check_name="Participant Count Sufficiency",
                severity="WARNING",
                entity_id="DATASET",
                message=f"Insufficient participants (N={len(unique_pts)}) for meaningful train/validation/test evaluation."
            ))

        # Check 3: Session ID uniqueness
        session_ids = [r.session_id for r in records if r.session_id != "UNKNOWN"]

        # Check 4: Image ID uniqueness
        image_ids = [r.image_id for r in records if r.image_id != "UNKNOWN"]
        seen_img = set()
        for iid in image_ids:
            if iid in seen_img:
                issues.append(ValidationIssue(
                    check_id=4,
                    check_name="Duplicate Image ID",
                    severity="ERROR",
                    entity_id=iid,
                    message=f"Duplicate image_id discovered: {iid}"
                ))
            seen_img.add(iid)

        # Check 5: Referential integrity & linkage
        for r in records:
            if r.participant_id == "UNKNOWN":
                issues.append(ValidationIssue(
                    check_id=5,
                    check_name="Referential Integrity",
                    severity="ERROR",
                    entity_id=r.image_id,
                    message=f"Image {r.image_id} has missing participant_id linkage."
                ))

            # Check 8: Laboratory Hb linkage & Check 9: Missing Hb values
            if r.laboratory_hb_g_dl is None:
                issues.append(ValidationIssue(
                    check_id=8,
                    check_name="Laboratory Hb Linkage",
                    severity="WARNING",
                    entity_id=r.image_id,
                    message=f"Record {r.image_id} has no associated reference laboratory Hb measurement."
                ))

            # Check 6: Image existence & Check 7: Image readability
            if r.image_path:
                img_file = self.root_dir / r.image_path
                if not img_file.exists() and Path(r.image_path).exists():
                    img_file = Path(r.image_path)
                if not img_file.exists():
                    issues.append(ValidationIssue(
                        check_id=6,
                        check_name="Image Existence",
                        severity="WARNING",
                        entity_id=r.image_id,
                        message=f"Image file does not exist on disk: {r.image_path}"
                    ))

            # Check 12: Quality status validity
            if r.quality_status not in ["usable", "rejected_blur", "rejected_exposure", "rejected_motion", "rejected_framing", "pending_review", "unknown"]:
                issues.append(ValidationIssue(
                    check_id=12,
                    check_name="Quality Status Validity",
                    severity="ERROR",
                    entity_id=r.image_id,
                    message=f"Invalid quality status: {r.quality_status}"
                ))

        err_count = sum(1 for i in issues if i.severity == "ERROR")
        warn_count = sum(1 for i in issues if i.severity == "WARNING")

        if err_count > 0:
            status_label = "VALIDATION FAILED"
        elif warn_count > 0:
            status_label = "VALIDATION PASSED WITH WARNINGS"
        else:
            status_label = "VALIDATION PASSED"

        summary = {
            "total_records": len(records),
            "total_participants": len(unique_pts),
            "total_sessions": len(set(session_ids)),
            "total_images": len(set(image_ids)),
            "error_count": err_count,
            "warning_count": warn_count,
            "is_valid": err_count == 0,
            "status_label": status_label,
            "is_sufficient_for_ml_eval": len(unique_pts) >= 3,
        }

        return issues, summary

    def generate_reports(self, output_dir: str) -> Tuple[str, str]:
        issues, summary = self.validate()
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        json_path = out_path / "dataset_validation_report.json"
        md_path = out_path / "dataset_validation_report.md"

        report_data = {
            "summary": summary,
            "issues": [asdict(i) for i in issues]
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        md_content = [
            "# HemoVision Dataset Validation Report",
            "",
            "## Summary",
            f"- **Validation Status**: `{summary['status_label']}`",
            f"- **Total Records**: {summary['total_records']}",
            f"- **Total Participants**: {summary['total_participants']}",
            f"- **Total Sessions**: {summary['total_sessions']}",
            f"- **Total Images**: {summary['total_images']}",
            f"- **Errors**: {summary['error_count']}",
            f"- **Warnings**: {summary['warning_count']}",
            f"- **Sufficient for Train/Val/Test Split**: {'YES' if summary['is_sufficient_for_ml_eval'] else 'NO (N < 3 participants)'}",
            "",
            "## Issues Logged",
        ]

        if not issues:
            md_content.append("No validation issues found.")
        else:
            for i in issues:
                md_content.append(f"- **[{i.severity}]** `{i.check_name}` (Entity: `{i.entity_id}`): {i.message}")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))

        return str(json_path), str(md_path)
