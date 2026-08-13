"""
HemoVision — Phase 12: Comprehensive End-to-End Integration Tests

Validates the full system flow from image input, quality gating, ROI segmentation,
color calibration, feature extraction, ML estimation, conformal prediction interval,
FastAPI endpoints, preset samples, and report generation.
"""

import numpy as np
import pytest
from fastapi.testclient import TestClient

from ml.src.quality.quality_assessment import ResearchQualityAssessor
from ml.src.segmentation.conjunctiva_segmenter import ConjunctivaSegmenter
from ml.src.preprocessing.color_calibration import ColorCalibrator
from ml.src.models.feature_extractor import FeatureExtractor
from ml.src.models.hb_estimator import HbEstimator
from ml.src.inference.pipeline import InferencePipeline
from backend.app.main import app

client = TestClient(app)


def test_full_pipeline_usable_image():
    """Verify full end-to-end execution on valid synthetic conjunctiva image."""
    pipeline = InferencePipeline()

    # 1. Create synthetic conjunctiva image
    h, w = 200, 200
    img_rgb = np.zeros((h, w, 3), dtype=np.uint8)
    img_rgb[:, :] = [210, 175, 155]  # Skin
    img_rgb[120:160, 50:150] = [220, 65, 75]  # Red conjunctiva patch
    img_rgb[::2, ::2] += 8  # Texture

    # 2. Process through pipeline
    result = pipeline.process(img_rgb)

    assert result.is_usable is True
    assert result.quality_score > 0.0
    assert result.estimated_hb_g_dl is not None
    assert 5.0 <= result.estimated_hb_g_dl <= 20.0
    assert result.prediction_interval[0] < result.prediction_interval[1]
    assert 0.0 <= result.reliability_score <= 1.0
    assert "Research" in result.research_category
    assert result.visual_overlay_b64 != ""


def test_full_pipeline_blurry_rejection():
    """Verify pipeline rejects out-of-focus blurry input image."""
    pipeline = InferencePipeline()

    # Blurry uniform image
    img_rgb = np.full((150, 150, 3), 200, dtype=np.uint8)

    result = pipeline.process(img_rgb)

    assert result.is_usable is False
    assert result.estimated_hb_g_dl is None
    assert "rejected_blur" in result.rejection_reasons
    assert result.research_category == "Quality Gate Failure"


def test_api_integration_preset_demo_samples():
    """Verify FastAPI preset samples end-to-end endpoint execution."""
    presets_res = client.get("/api/v1/demo-samples")
    assert presets_res.status_code == 200
    presets = presets_res.json()["presets"]

    # Test Normal Preset
    norm_preset = presets[0]
    res_norm = client.post("/api/v1/analyze", json={"image_b64": norm_preset["image_b64"]})
    assert res_norm.status_code == 200
    data_norm = res_norm.json()
    assert data_norm["is_usable"] is True
    assert data_norm["prediction"]["estimated_hb_g_dl"] > 11.0

    # Test Blurry Preset Rejection
    blur_preset = presets[3]
    res_blur = client.post("/api/v1/analyze", json={"image_b64": blur_preset["image_b64"]})
    assert res_blur.status_code == 200
    data_blur = res_blur.json()
    assert data_blur["is_usable"] is False
    assert "rejected_blur" in data_blur["quality"]["rejection_reasons"]


def test_api_report_generation():
    """Verify clinical research summary report endpoint output."""
    presets_res = client.get("/api/v1/demo-samples")
    image_b64 = presets_res.json()["presets"][0]["image_b64"]

    res_report = client.post("/api/v1/reports/markdown", json={"image_b64": image_b64})
    assert res_report.status_code == 200
    data = res_report.json()
    assert "session_id" in data
    assert "# HemoVision — Research Screening Summary Report" in data["markdown"]
    assert "INVESTIGATIONAL RESEARCH NOTICE" in data["markdown"]
