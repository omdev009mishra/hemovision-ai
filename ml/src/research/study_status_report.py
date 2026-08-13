"""Generate a non-clinical aggregate status file for a future study dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from ml.src.research.study_status import DEFAULT_STUDY_STATUS


def build_study_status_report(metrics: Mapping[str, Any] | None = None) -> dict:
    values = dict(metrics or {})
    return {
        "study_status": DEFAULT_STUDY_STATUS.value,
        "approval_status": "NOT_APPROVED_FOR_HUMAN_COLLECTION",
        "participant_count": int(values.get("participant_count", 0)),
        "session_count": int(values.get("session_count", 0)),
        "usable_images": int(values.get("usable_images", 0)),
        "rejected_images": int(values.get("rejected_images", 0)),
        "segmentation_success_rate": float(values.get("segmentation_success_rate", 0.0)),
        "lab_linkage_rate": float(values.get("lab_linkage_rate", 0.0)),
        "metadata_completeness": float(values.get("metadata_completeness", 0.0)),
        "withdrawals": int(values.get("withdrawals", 0)),
        "protocol_deviations": int(values.get("protocol_deviations", 0)),
        "clinical_collection": "BLOCKED",
        "clinical_training": "BLOCKED",
        "clinical_validation": "NOT_PERFORMED",
    }


def write_study_status_report(path: str = "research/reports/study_status.json") -> dict:
    report = build_study_status_report()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
