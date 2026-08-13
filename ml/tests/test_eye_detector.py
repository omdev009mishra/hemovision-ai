"""
Tests for EyeDetector
"""

import pytest
import numpy as np
from ml.src.segmentation.eye_detector import EyeDetector, EyeDetectionResult


def test_eye_detector_success():
    detector = EyeDetector()
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    # Add contrasting pattern
    img[100:400, 100:400] = [200, 180, 160]
    img[200:300, 200:300] = [50, 50, 50]

    res = detector.detect(img)
    assert res.success is True
    assert res.eye_region_quality > 0.0
    assert len(res.bounding_box) == 4


def test_eye_detector_empty_or_low_contrast_failure():
    detector = EyeDetector()
    blank = np.full((512, 512, 3), 40, dtype=np.uint8)
    res = detector.detect(blank)
    assert res.success is False
    assert res.failure_reason == "eye_not_detected"
