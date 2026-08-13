"""
HemoVision Dataset Manifest Generator
Generates dataset_manifest.json declaring dataset type (clinical vs synthetic), counts, seeds, and split stats.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

from ml.src.data.dataset_loader import DatasetRecord
from ml.src.data.split_dataset import DatasetSplitter


class DatasetManifestGenerator:

    def __init__(
        self,
        dataset_version: str = "1.0.0",
        dataset_type: str = "synthetic",
        seed: int = 42,
        research_context: Optional[Dict[str, Any]] = None,
    ):
        self.dataset_version = dataset_version
        self.dataset_type = dataset_type
        self.seed = seed
        self.research_context = research_context or {}

    def generate_manifest(self, records: List[DatasetRecord], output_file: str) -> Dict[str, Any]:
        splitter = DatasetSplitter(random_seed=self.seed)
        split_records = splitter.split_records(records)
        split_pts = splitter.split_participants([r.participant_id for r in records])
        all_pts = [r.participant_id for r in records]
        sufficient = splitter.is_sufficient_for_ml_eval(all_pts)

        usable_records = [
            r for r in records
            if str(getattr(r, "quality_status", "")).upper() in {"USABLE", "USABLE_IMAGE", "USABLE"}
        ]
        segmentation_success_count = sum(
            1
            for r in records
            if str(getattr(r, "segmentation_status", "")).upper() in {"SUCCEEDED", "SUCCESS"}
            or getattr(r, "segmentation_success", False) is True
        )
        lab_linked_count = sum(
            1
            for r in records
            if getattr(r, "lab_measurement_id", "UNKNOWN") not in {None, "", "UNKNOWN"}
        )
        context = self.research_context
        manifest = {
            "dataset_version": self.dataset_version,
            "dataset_type": self.dataset_type,
            "study_id": context.get("study_id", "STUDY_ID_REQUIRED"),
            "protocol_version": context.get("protocol_version", "PROTOCOL_VERSION_REQUIRED"),
            "consent_version": context.get("consent_version", "CONSENT_VERSION_REQUIRED"),
            "participant_count": len(set(all_pts)),
            "session_count": len(set(r.session_id for r in records)),
            "image_count": len(records),
            "usable_image_count": len(usable_records),
            "segmentation_success_count": segmentation_success_count,
            "lab_linked_image_count": lab_linked_count,
            "withdrawn_participant_count": int(context.get("withdrawn_participant_count", 0)),
            "excluded_image_count": int(context.get("excluded_image_count", len(records) - len(usable_records))),
            "freeze_status": context.get("freeze_status", "OPEN"),
            "freeze_timestamp": context.get("freeze_timestamp"),
            "creation_timestamp": datetime.now(timezone.utc).isoformat(),
            "random_seed": self.seed,
            "counts": {
                "participant_count": len(set(all_pts)),
                "session_count": len(set(r.session_id for r in records)),
                "image_count": len(records),
                "lab_measurement_count": len(set(r.lab_measurement_id for r in records if r.lab_measurement_id != "UNKNOWN")),
                "annotation_count": sum(1 for r in records if r.annotation_mask_path),
            },
            "splits": {
                "is_sufficient_for_ml_eval": sufficient,
                "train": {
                    "participant_count": len(split_pts["train"]),
                    "image_count": len(split_records["train"]),
                },
                "val": {
                    "participant_count": len(split_pts["val"]),
                    "image_count": len(split_records["val"]),
                },
                "test": {
                    "participant_count": len(split_pts["test"]),
                    "image_count": len(split_records["test"]),
                },
            },
            "governance": {
                "has_governed_clinical_declaration": self.dataset_type == "clinical",
                "clinical_training_allowed": False,
                "clinical_validation_status": "NOT_PERFORMED",
            }
        }

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest
