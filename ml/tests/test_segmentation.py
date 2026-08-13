"""
Unit tests for HemoVision Phase 3: Palpebral Conjunctiva Segmentation
Tests segmenter color thresholding, ROI extraction, metrics (IoU, Dice), and visual overlay.
"""

import numpy as np
import pytest
from ml.src.segmentation.conjunctiva_segmenter import (
    ConjunctivaSegmenter,
    SegmentationResult,
    calculate_iou,
    calculate_dice,
)


def test_calculate_iou_and_dice_perfect_overlap():
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask1[20:60, 20:60] = 255
    mask2 = mask1.copy()

    iou = calculate_iou(mask1, mask2)
    dice = calculate_dice(mask1, mask2)

    assert iou == pytest.approx(1.0)
    assert dice == pytest.approx(1.0)


def test_calculate_iou_and_dice_zero_overlap():
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask1[0:20, 0:20] = 255
    mask2 = np.zeros((100, 100), dtype=np.uint8)
    mask2[50:80, 50:80] = 255

    iou = calculate_iou(mask1, mask2)
    dice = calculate_dice(mask1, mask2)

    assert iou == pytest.approx(0.0)
    assert dice == pytest.approx(0.0)


def test_calculate_iou_and_dice_partial_overlap():
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask1[0:50, 0:50] = 255  # area 2500
    mask2 = np.zeros((100, 100), dtype=np.uint8)
    mask2[25:75, 0:50] = 255  # area 2500, overlap 25x50 = 1250

    iou = calculate_iou(mask1, mask2)
    dice = calculate_dice(mask1, mask2)

    # Intersection = 1250, Union = 3750 => IoU = 1/3
    assert iou == pytest.approx(1250.0 / 3750.0)
    # Dice = 2*1250 / (2500+2500) = 2500/5000 = 0.5
    assert dice == pytest.approx(0.5)


def test_conjunctiva_segmenter_synthetic_eye_image():
    # Create synthetic RGB eye image with red/pink lower eyelid region
    h, w = 200, 200
    image_rgb = np.zeros((h, w, 3), dtype=np.uint8)
    # Background skin tone (light beige/tan)
    image_rgb[:, :] = [210, 180, 160]

    # Palpebral conjunctiva red/pink mucosal patch in lower region
    image_rgb[120:160, 50:150] = [220, 60, 80]

    segmenter = ConjunctivaSegmenter(
        min_hue=0, max_hue=30, min_sat=30, min_val=30, min_a_star=130, min_roi_area=50
    )
    result = segmenter.segment(image_rgb)

    assert isinstance(result, SegmentationResult)
    assert result.mask.shape == (h, w)
    assert np.array_equal(np.unique(result.mask), np.array([0, 255])) or np.array_equal(np.unique(result.mask), np.array([0]))
    assert result.roi_area_pixels > 0
    assert result.coverage_ratio > 0.0
    assert len(result.bounding_box) == 4
    
    # Verify bounding box bounds
    bx, by, bw, bh = result.bounding_box
    assert bx >= 0 and by >= 0
    assert bw > 0 and bh > 0
    assert result.roi_crop.shape == (bh, bw, 3)
    assert result.visual_overlay.shape == (h, w, 3)


def test_conjunctiva_segmenter_invalid_input():
    segmenter = ConjunctivaSegmenter()
    with pytest.raises(ValueError):
        segmenter.segment(None)

    with pytest.raises(ValueError):
        segmenter.segment(np.array([]))
