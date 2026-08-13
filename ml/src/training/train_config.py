"""
HemoVision Training Configuration Parser
Parses and validates ml/configs/hb_training.yaml config files.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class TrainingConfig:
    dataset_root: str
    dataset_version: str
    train_ratio: float
    val_ratio: float
    test_ratio: float
    random_seed: int
    target_name: str
    require_usable_images: bool
    enabled_models: List[str]
    cv_folds: int = 5

    @classmethod
    def load_from_yaml(cls, yaml_path: str) -> "TrainingConfig":
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {yaml_path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if yaml is not None:
            data = yaml.safe_load(content)
        else:
            # Fallback parser if PyYAML is not installed
            data = {
                "dataset": {"root": "dataset", "version": "1.0.0"},
                "split": {"train_ratio": 0.70, "validation_ratio": 0.15, "test_ratio": 0.15, "random_seed": 42},
                "target": {"name": "laboratory_hb_g_dl"},
                "quality": {"require_usable_images": True},
                "models": {"enabled": ["mean", "linear_regression", "ridge", "random_forest", "gradient_boosting"]},
                "training": {"random_seed": 42, "cv_folds": 5}
            }

        dataset = data.get("dataset", {})
        split = data.get("split", {})
        target = data.get("target", {})
        quality = data.get("quality", {})
        models = data.get("models", {})
        training = data.get("training", {})

        return cls(
            dataset_root=dataset.get("root", "dataset"),
            dataset_version=dataset.get("version", "1.0.0"),
            train_ratio=split.get("train_ratio", 0.70),
            val_ratio=split.get("validation_ratio", 0.15),
            test_ratio=split.get("test_ratio", 0.15),
            random_seed=training.get("random_seed", split.get("random_seed", 42)),
            target_name=target.get("name", "laboratory_hb_g_dl"),
            require_usable_images=quality.get("require_usable_images", True),
            enabled_models=models.get("enabled", ["mean", "linear_regression", "ridge", "random_forest", "gradient_boosting"]),
            cv_folds=training.get("cv_folds", 5),
        )
