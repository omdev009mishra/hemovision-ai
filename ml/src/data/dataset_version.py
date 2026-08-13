"""
HemoVision — Dataset Versioning Engine
Manages semantic dataset versioning (vMAJOR.MINOR.PATCH) and generates manifest declarations.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import json


class DatasetVersionManager:
    """Handles semantic versioning and manifest generation for research datasets."""

    def __init__(self, version: str = "1.0.0", dataset_type: str = "synthetic"):
        self.version = version
        self.dataset_type = dataset_type

    def create_manifest(
        self,
        governance_status: str,
        total_participants: int,
        total_sessions: int,
        total_images: int,
        usable_images: int,
        excluded_images: int,
        withdrawn_participants: int,
        train_count: int,
        val_count: int,
        test_count: int,
        output_path: str = "dataset/dataset_manifest.json"
    ) -> Dict[str, Any]:
        manifest = {
            "dataset_version": f"v{self.version.lstrip('v')}",
            "dataset_type": self.dataset_type,
            "governance_status": governance_status,
            "creation_timestamp": datetime.now(timezone.utc).isoformat(),
            "counts": {
                "participant_count": total_participants,
                "session_count": total_sessions,
                "image_count": total_images,
                "usable_image_count": usable_images,
                "excluded_image_count": excluded_images,
                "withdrawn_participant_count": withdrawn_participants,
            },
            "splits": {
                "train_image_count": train_count,
                "val_image_count": val_count,
                "test_image_count": test_count,
            },
            "governance": {
                "has_governed_clinical_declaration": governance_status == "approved" and self.dataset_type == "clinical",
                "clinical_training_allowed": governance_status == "approved" and self.dataset_type == "clinical",
            }
        }

        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest
