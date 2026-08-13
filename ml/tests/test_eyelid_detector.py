"""
Tests for EyelidDetector
"""

import pytest
import numpy as np
from ml.src.segmentation.eyelid_detector import EyelidDetector


def test_eyelid_detector_bounds():
    detector = EyelidDetector(y_start_ratio=0.15, y_end_ratio=0.95)
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    eye_bbox = (50, 50, 400, 400)

    res = detector.detect_lower_eyelid(img, eye_bbox)
    assert res.success is True
    assert res.candidate_mask.shape == (512, 512)
    assert np.sum(res.candidate_mask > 0) > 0
