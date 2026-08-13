"""
Tests for Model Registry & Safety Metadata Checks
"""

import pytest
import numpy as np
from ml.src.models.baseline_models import BaselineModelFactory
from ml.src.models.model_registry import ModelRegistry, ModelMetadata


def test_model_registry_saves_smoke_test():
    registry = ModelRegistry("research/test_models")
    model = BaselineModelFactory.create_model("ridge")
    X = np.random.randn(10, 5)
    y = np.random.randn(10)
    model.fit(X, y)

    meta = ModelMetadata(
        model_version="smoke-v0.1.0",
        model_type="Ridge",
        dataset_version="1.0.0",
        feature_version="1.0.0",
        preprocessing_version="1.0.0",
        training_timestamp="2026-08-13T00:00:00Z",
        random_seed=42,
        training_participants=10,
        validation_participants=2,
        test_participants=2,
        validation_metrics={"mae": 1.0},
        test_metrics={"mae": 1.0},
        is_clinical_model=False,
    )

    m_path, meta_path = registry.save_model(model, meta, filename="hemovision_hb_model.joblib")
    assert "smoke_test_model.joblib" in m_path  # Safety override for non-clinical models
