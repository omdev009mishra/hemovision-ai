"""
Tests for Feature Extraction Schema & Calculation
"""

import json
import pytest
import numpy as np
from ml.src.models.feature_extractor import FeatureExtractor


def test_feature_schema_json():
    with open("ml/models/feature_schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)

    assert schema["feature_count"] == 28
    assert len(schema["features"]) == 28
    names = [feat["name"] for feat in schema["features"]]
    assert "mean_R" in names
    assert "mean_a" in names
    assert "specularity_ratio" in names


def test_feature_extractor_returns_valid_features():
    extractor = FeatureExtractor()
    # Create a reddish ROI image
    roi = np.zeros((50, 50, 3), dtype=np.uint8)
    roi[:, :, 0] = 200  # R
    roi[:, :, 1] = 100  # G
    roi[:, :, 2] = 100  # B
    mask = (np.ones((50, 50)) * 255).astype(np.uint8)

    feat_vec = extractor.extract(roi, mask)
    assert feat_vec is not None
    assert feat_vec.redness_index > 0.0
