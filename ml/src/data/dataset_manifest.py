"""
HemoVision Dataset Manifest Generator
Generates dataset_manifest.json declaring dataset type (clinical vs synthetic), counts, seeds, and split stats.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
import json

from ml.src.data.dataset_loader import DatasetRecord
from ml.src.data.split_dataset import DatasetSplitter


class DatasetManifestGenerator:

    def __init__(self, dataset_version: str = "1.0.0", dataset_type: str = "synthetic", seed: int = 42):
        self.dataset_version = dataset_version
        self.dataset_type = dataset_type
        self.seed = seed

    def generate_manifest(self, records: List[DatasetRecord], output_file: str) -> Dict[str, Any]:
        splitter = DatasetSplitter(random_seed=self.seed)
        split_records = splitter.split_records(records)
        split_pts = splitter.split_participants([r.participant_id for r in records])

        manifest = {
            "dataset_version": self.dataset_version,
            "dataset_type": self.dataset_type,
            "creation_timestamp": datetime.now(timezone.utc).isoformat(),
            "random_seed": self.seed,
            "counts": {
                "participant_count": len(set(r.participant_id for r in records)),
                "session_count": len(set(r.session_id for r in records)),
                "image_count": len(records),
                "lab_measurement_count": len(set(r.lab_measurement_id for r in records if r.lab_measurement_id != "UNKNOWN")),
                "annotation_count": sum(1 for r in records if r.annotation_mask_path),
            },
            "splits": {
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
                "clinical_training_allowed": self.dataset_type == "clinical",
            }
        }

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest
