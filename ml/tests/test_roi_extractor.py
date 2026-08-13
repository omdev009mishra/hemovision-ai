"""
Tests for ROIExtractor
"""

import pytest
import numpy as np
from ml.src.segmentation.roi_extractor import ROIExtractor


def test_roi_extractor_valid_mask():
    extractor = ROIExtractor(min_area_pixels=50, max_area_ratio=0.5)
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    img[200:300, 200:300] = [200, 50, 50]
    mask = np.zeros((512, 512), dtype=np.uint8)
    mask[200:300, 200:300] = 255

    res = extractor.extract(img, mask)
    assert res.success is True
    assert res.roi_area_pixels == 10000
    assert res.roi_image.shape == (100, 100, 3)
    assert res.bounding_box == (200, 200, 100, 100)


def test_roi_extractor_too_small_fails():
    extractor = ROIExtractor(min_area_pixels=500, max_area_ratio=0.5)
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    mask = np.zeros((512, 512), dtype=np.uint8)
    mask[200:210, 200:210] = 255  # 100 pixels < 500

    res = extractor.extract(img, mask)
    assert res.success is False
    assert res.failure_reason == "segmentation_failed"
