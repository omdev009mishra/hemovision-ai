"""
Unit tests for HemoVision Phase 6 & Phase 8: Models & End-to-End Inference Pipeline
Tests FeatureExtractor, HbEstimator, and InferencePipeline.
"""

import numpy as np
import pytest
from ml.src.models.feature_extractor import FeatureExtractor, FeatureVector
from ml.src.models.hb_estimator import HbEstimator, ModelPrediction
from ml.src.inference.pipeline import InferencePipeline, InferenceResult


def test_feature_extractor_returns_valid_vector():
    img_rgb = np.zeros((100, 100, 3), dtype=np.uint8)
    img_rgb[:, :] = [210, 80, 80]  # Reddish conjunctiva patch

    extractor = FeatureExtractor()
    feat_vec = extractor.extract(img_rgb)

    assert isinstance(feat_vec, FeatureVector)
    arr = feat_vec.to_array()
    assert len(arr) == 28
    assert feat_vec.redness_index > 0.0
    assert feat_vec.red_green_ratio > 1.0


def test_hb_estimator_prediction():
    estimator = HbEstimator()
    img_rgb = np.zeros((100, 100, 3), dtype=np.uint8)
    img_rgb[:, :] = [210, 80, 80]
    feat_vec = FeatureExtractor().extract(img_rgb)

    pred = estimator.predict(feat_vec)

    assert isinstance(pred, ModelPrediction)
    assert 5.0 <= pred.estimated_hb_g_dl <= 20.0
    assert len(pred.prediction_interval) == 2
    assert pred.prediction_interval[0] < pred.prediction_interval[1]
    assert 0.0 <= pred.reliability_score <= 1.0
    assert "Research" in pred.research_category
    assert "investigational" in pred.disclaimer.lower()


def test_inference_pipeline_usable_image():
    pipeline = InferencePipeline()

    # Create synthetic usable eye image
    h, w = 150, 150
    img_rgb = np.zeros((h, w, 3), dtype=np.uint8)
    img_rgb[:, :] = [200, 160, 140]
    img_rgb[80:120, 30:120] = [220, 70, 75]
    img_rgb[::2, ::2] += 10  # Texture for focus

    res = pipeline.process(img_rgb)

    assert isinstance(res, InferenceResult)
    assert res.is_usable is True
    assert res.estimated_hb_g_dl is not None
    assert res.visual_overlay_b64 != ""
    assert res.roi_crop_b64 != ""
    assert "redness_index" in res.feature_summary


def test_inference_pipeline_rejected_image():
    pipeline = InferencePipeline()

    # Create uniform overexposed image (fails blur & exposure)
    img_rgb = np.full((100, 100, 3), 252, dtype=np.uint8)

    res = pipeline.process(img_rgb)

    assert isinstance(res, InferenceResult)
    assert res.is_usable is False
    assert res.estimated_hb_g_dl is None
    assert len(res.rejection_reasons) > 0
    assert res.research_category == "Quality Gate Failure"
