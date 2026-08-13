"""
Tests for SegmentationResult dataclass
"""

import pytest
import numpy as np
from ml.src.segmentation.segmentation_result import SegmentationResult


def test_segmentation_result_serialization():
    mask = np.zeros((100, 100), dtype=np.uint8)
    roi = np.zeros((20, 20, 3), dtype=np.uint8)
    res = SegmentationResult(
        success=True,
        mask=mask,
        bounding_box=(10, 10, 20, 20),
        roi_image=roi,
        roi_area_pixels=400,
        roi_area_ratio=0.04,
        segmentation_quality=0.88,
        failure_reason=None,
        method="classical_cv",
        quality_flags={"has_roi": True},
        processing_time_ms=12.5
    )

    d = res.to_dict()
    assert d["success"] is True
    assert d["method"] == "classical_cv"
    assert d["bounding_box"] == [10, 10, 20, 20]
    assert d["roi_area_pixels"] == 400
    assert d["confidence"] == 0.88
    assert res.confidence == 0.88
    assert res.roi_crop.shape == (20, 20, 3)
    assert res.coverage_ratio == 0.04
