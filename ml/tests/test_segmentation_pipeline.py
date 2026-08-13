"""
Tests for Segmentation Pipeline Integration
"""

import pytest
import cv2
import numpy as np
from pathlib import Path
from ml.src.segmentation.conjunctiva_segmenter import create_segmenter


def test_classical_cv_segmenter_synthetic_fixture():
    fixture_path = Path("dataset/samples/segmentation/synthetic_eye_001.png")
    assert fixture_path.exists()

    bgr = cv2.imread(str(fixture_path))
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    segmenter = create_segmenter("classical_cv")
    res = segmenter.segment(rgb)

    assert res.success is True
    assert res.roi_area_pixels > 0
    assert res.roi_image.size > 0
    assert res.processing_time_ms > 0.0
    assert res.visual_overlay is not None
