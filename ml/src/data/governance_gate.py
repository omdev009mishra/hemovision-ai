"""
HemoVision — Clinical Data Governance Gate
Evaluates dataset governance evidence and determines dataset classification:
SYNTHETIC, UNVERIFIED_CLINICAL, or GOVERNED_CLINICAL.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional
import json


class GovernanceState(str, Enum):
    SYNTHETIC = "SYNTHETIC"
    UNVERIFIED_CLINICAL = "UNVERIFIED_CLINICAL"
    GOVERNED_CLINICAL = "GOVERNED_CLINICAL"


@dataclass
class GovernanceCheckResult:
    state: GovernanceState
    is_clinical_training_allowed: bool
    rejection_reasons: Tuple[str, ...] if 'Tuple' in globals() else list
    metadata: Dict[str, Any]


from typing import Tuple


class GovernanceGate:
    """Evaluates dataset governance evidence and enforces clinical data compliance."""

    def __init__(self, dataset_dir: str):
        self.dataset_dir = Path(dataset_dir)

    def evaluate(self) -> GovernanceCheckResult:
        gov_file = self.dataset_dir / "dataset_governance.json"
        
        # 1. If no governance file exists or is synthetic
        if not gov_file.exists():
            return GovernanceCheckResult(
                state=GovernanceState.SYNTHETIC,
                is_clinical_training_allowed=False,
                rejection_reasons=("No governance declaration file found — defaulting to synthetic mode.",),
                metadata={"dataset_type": "synthetic"}
            )

        try:
            with open(gov_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return GovernanceCheckResult(
                state=GovernanceState.SYNTHETIC,
                is_clinical_training_allowed=False,
                rejection_reasons=(f"Failed to parse governance file: {str(e)}",),
                metadata={"dataset_type": "synthetic"}
            )

        dtype = str(data.get("dataset_type", "synthetic")).lower()
        if dtype == "synthetic":
            return GovernanceCheckResult(
                state=GovernanceState.SYNTHETIC,
                is_clinical_training_allowed=False,
                rejection_reasons=("Declared dataset_type is synthetic.",),
                metadata=data
            )

        rejections = []
        if not data.get("consent_verified", False):
            rejections.append("Participant consent not verified.")
        
        ref = str(data.get("ethics_approval_reference", ""))
        if not ref or "REQUIRED" in ref or ref == "...":
            rejections.append("Missing or placeholder ethics approval reference.")

        if not data.get("deidentification_verified", False):
            rejections.append("De-identification status not verified.")

        if str(data.get("governance_status", "")).lower() != "approved":
            rejections.append("Governance status is not approved.")

        if rejections:
            return GovernanceCheckResult(
                state=GovernanceState.UNVERIFIED_CLINICAL,
                is_clinical_training_allowed=False,
                rejection_reasons=tuple(rejections),
                metadata=data
            )

        return GovernanceCheckResult(
            state=GovernanceState.GOVERNED_CLINICAL,
            is_clinical_training_allowed=True,
            rejection_reasons=(),
            metadata=data
        )
