"""
Unit tests for HemoVision Phase 4: Image Quality & Preprocessing
Tests Laplacian blur variance, exposure analysis, specularity detection, and color calibration.
"""

import numpy as np
import pytest
from ml.src.quality.quality_assessment import (
    ResearchQualityAssessor,
    QualityAssessmentResult,
    calculate_laplacian_variance,
)
from ml.src.preprocessing.color_calibration import (
    ColorCalibrator,
    CalibrationResult,
    rgb_to_chromaticity,
    rgb_to_cielab,
)


def test_laplacian_variance_uniform_vs_textured():
    # Uniform image has zero variance
    uniform = np.full((100, 100), 128, dtype=np.uint8)
    var_uniform = calculate_laplacian_variance(uniform)
    assert var_uniform == pytest.approx(0.0)

    # Checkerboard/textured image has high variance
    textured = np.zeros((100, 100), dtype=np.uint8)
    textured[::2, ::2] = 255
    var_textured = calculate_laplacian_variance(textured)
    assert var_textured > 100.0


def test_quality_assessor_usable_image():
    # Synthetic optimal image (mixed values centered near 128)
    img_rgb = np.zeros((100, 100, 3), dtype=np.uint8)
    img_rgb[:, :] = [130, 120, 110]
    img_rgb[::2, ::2] = [200, 50, 50]  # Texture for focus score

    assessor = ResearchQualityAssessor(min_focus_score=10.0)
    result = assessor.assess(img_rgb)

    assert isinstance(result, QualityAssessmentResult)
    assert result.is_usable is True
    assert result.quality_score > 0.0
    assert len(result.rejection_reasons) == 0


def test_quality_assessor_blurry_and_overexposed_image():
    # Blurry uniform overexposed image
    img_rgb = np.full((100, 100, 3), 250, dtype=np.uint8)

    assessor = ResearchQualityAssessor(min_focus_score=50.0)
    result = assessor.assess(img_rgb)

    assert result.is_usable is False
    assert "rejected_blur" in result.rejection_reasons
    assert "rejected_overexposure" in result.rejection_reasons


def test_rgb_to_chromaticity():
    img_rgb = np.zeros((10, 10, 3), dtype=np.uint8)
    img_rgb[:, :] = [100, 50, 50]  # R=100, G=50, B=50 => Total = 200 => r=0.5, g=0.25, b=0.25

    r_norm, g_norm, b_norm = rgb_to_chromaticity(img_rgb)
    assert r_norm == pytest.approx(0.5, abs=0.01)
    assert g_norm == pytest.approx(0.25, abs=0.01)
    assert b_norm == pytest.approx(0.25, abs=0.01)


def test_color_calibrator_gray_world():
    img_rgb = np.zeros((50, 50, 3), dtype=np.uint8)
    img_rgb[:, :] = [180, 90, 45]  # Unbalanced lighting

    calibrator = ColorCalibrator(method="gray_world")
    result = calibrator.calibrate(img_rgb)

    assert isinstance(result, CalibrationResult)
    assert result.calibrated_image.shape == (50, 50, 3)
    # Calibrated channels should move closer to balance
    cal_mean_r, cal_mean_g, cal_mean_b = result.mean_rgb
    assert abs(cal_mean_r - cal_mean_g) < abs(180 - 90)


def test_rgb_to_cielab_conversion():
    img_rgb = np.zeros((10, 10, 3), dtype=np.uint8)
    img_rgb[:, :] = [200, 50, 50]  # Strong red

    lab = rgb_to_cielab(img_rgb)
    assert lab.shape == (10, 10, 3)
    # Red should produce positive a* value
    a_star_mean = np.mean(lab[:, :, 1])
    assert a_star_mean > 20.0
