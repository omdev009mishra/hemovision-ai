"""
HemoVision Model Registry & Metadata Serializer
Manages model versioning (e.g. hb-v0.1.0), artifact metadata, and safety checks against overwriting clinical models.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import joblib


@dataclass
class ModelMetadata:
    model_version: str
    model_type: str
    dataset_version: str
    feature_version: str
    preprocessing_version: str
    training_timestamp: str
    random_seed: int
    training_participants: int
    validation_participants: int
    test_participants: int
    validation_metrics: Dict[str, float]
    test_metrics: Dict[str, float]
    is_clinical_model: bool = False
    limitations: List[str] = field(default_factory=lambda: [
        "Experimental research model",
        "Not clinically validated",
        "Requires governed clinical dataset for training"
    ])


class ModelRegistry:

    def __init__(self, registry_dir: str = "ml/models"):
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)

    def save_model(
        self,
        model_obj: Any,
        metadata: ModelMetadata,
        filename: str = "hemovision_hb_model.joblib",
        meta_filename: str = "model_metadata.json"
    ) -> Tuple[str, str]:
        if not metadata.is_clinical_model and filename == "hemovision_hb_model.joblib":
            # Safety check: do not save synthetic smoke-test models as primary clinical artifact
            filename = "smoke_test_model.joblib"

        model_path = self.registry_dir / filename
        meta_path = self.registry_dir / meta_filename

        joblib.dump(model_obj, model_path)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metadata), f, indent=2)

        return str(model_path), str(meta_path)

    def load_model(self, filename: str = "hemovision_hb_model.joblib") -> Tuple[Any, Optional[Dict]]:
        model_path = self.registry_dir / filename
        meta_path = self.registry_dir / "model_metadata.json"

        if not model_path.exists():
            return None, None

        model_obj = joblib.load(model_path)
        metadata = None
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

        return model_obj, metadata
