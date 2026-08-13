"""
Tests for Segmentation Evaluation Metrics (IoU, Dice, Precision, Recall, Pixel Accuracy)
"""

import pytest
import numpy as np
from ml.src.evaluation.segmentation_metrics import (
    calculate_iou,
    calculate_dice,
    calculate_precision,
    calculate_recall,
    calculate_pixel_accuracy,
    calculate_segmentation_metrics,
)


def test_perfect_mask_overlap():
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[20:80, 20:80] = 255

    assert calculate_iou(mask, mask) == 1.0
    assert calculate_dice(mask, mask) == 1.0
    assert calculate_precision(mask, mask) == 1.0
    assert calculate_recall(mask, mask) == 1.0
    assert calculate_pixel_accuracy(mask, mask) == 1.0


def test_empty_masks_and_zero_denominators():
    empty_mask = np.zeros((100, 100), dtype=np.uint8)
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[20:80, 20:80] = 255

    # Empty vs Empty
    assert calculate_iou(empty_mask, empty_mask) == 1.0
    assert calculate_dice(empty_mask, empty_mask) == 1.0
    assert calculate_precision(empty_mask, empty_mask) is None
    assert calculate_recall(empty_mask, empty_mask) is None

    # Predicted Empty vs Non-empty Ground Truth
    assert calculate_iou(empty_mask, mask) == 0.0
    assert calculate_dice(empty_mask, mask) == 0.0
    assert calculate_precision(empty_mask, mask) is None
    assert calculate_recall(empty_mask, mask) == 0.0


def test_partial_overlap():
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask1[0:50, 0:50] = 255  # Area 2500

    mask2 = np.zeros((100, 100), dtype=np.uint8)
    mask2[25:75, 0:50] = 255  # Area 2500, Intersection 1250, Union 3750

    iou = calculate_iou(mask1, mask2)
    dice = calculate_dice(mask1, mask2)

    assert iou == pytest.approx(1250.0 / 3750.0)
    assert dice == pytest.approx(2.0 * 1250.0 / 5000.0)
