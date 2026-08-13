"""
HemoVision — Segmentation Evaluation Metrics
Calculates IoU, Dice Coefficient, Precision, Recall, and Pixel Accuracy for binary segmentation masks.
Handles zero denominators and empty masks safely by returning None or 0.0.
"""

from typing import Dict, Any, Optional
import numpy as np


def calculate_iou(mask_pred: np.ndarray, mask_true: np.ndarray) -> Optional[float]:
    """Calculate Intersection over Union (IoU / Jaccard Index)."""
    if mask_pred is None or mask_true is None or mask_pred.size == 0 or mask_true.size == 0:
        return None
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    intersection = float(np.logical_and(pred_bool, true_bool).sum())
    union = float(np.logical_or(pred_bool, true_bool).sum())
    if union == 0.0:
        return 1.0 if intersection == 0.0 else None
    return float(intersection / union)


def calculate_dice(mask_pred: np.ndarray, mask_true: np.ndarray) -> Optional[float]:
    """Calculate Dice Similarity Coefficient (DSC)."""
    if mask_pred is None or mask_true is None or mask_pred.size == 0 or mask_true.size == 0:
        return None
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    intersection = float(np.logical_and(pred_bool, true_bool).sum())
    total = float(pred_bool.sum() + true_bool.sum())
    if total == 0.0:
        return 1.0
    return float(2.0 * intersection / total)


def calculate_precision(mask_pred: np.ndarray, mask_true: np.ndarray) -> Optional[float]:
    """Calculate Precision (True Positives / Predicted Positives)."""
    if mask_pred is None or mask_true is None or mask_pred.size == 0 or mask_true.size == 0:
        return None
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    intersection = float(np.logical_and(pred_bool, true_bool).sum())
    pred_area = float(pred_bool.sum())
    if pred_area == 0.0:
        return None
    return float(intersection / pred_area)


def calculate_recall(mask_pred: np.ndarray, mask_true: np.ndarray) -> Optional[float]:
    """Calculate Recall / Sensitivity (True Positives / Ground Truth Positives)."""
    if mask_pred is None or mask_true is None or mask_pred.size == 0 or mask_true.size == 0:
        return None
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    intersection = float(np.logical_and(pred_bool, true_bool).sum())
    gt_area = float(true_bool.sum())
    if gt_area == 0.0:
        return None
    return float(intersection / gt_area)


def calculate_pixel_accuracy(mask_pred: np.ndarray, mask_true: np.ndarray) -> Optional[float]:
    """Calculate Pixel Accuracy ((TP + TN) / Total Pixels)."""
    if mask_pred is None or mask_true is None or mask_pred.size == 0 or mask_true.size == 0:
        return None
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    correct = float((pred_bool == true_bool).sum())
    total = float(pred_bool.size)
    if total == 0.0:
        return None
    return float(correct / total)


def calculate_segmentation_metrics(mask_pred: np.ndarray, mask_true: np.ndarray) -> Dict[str, Optional[float]]:
    """Calculates all binary segmentation evaluation metrics."""
    iou = calculate_iou(mask_pred, mask_true)
    dice = calculate_dice(mask_pred, mask_true)
    prec = calculate_precision(mask_pred, mask_true)
    rec = calculate_recall(mask_pred, mask_true)
    acc = calculate_pixel_accuracy(mask_pred, mask_true)

    return {
        "iou": round(iou, 4) if iou is not None else None,
        "dice": round(dice, 4) if dice is not None else None,
        "precision": round(prec, 4) if prec is not None else None,
        "recall": round(rec, 4) if rec is not None else None,
        "pixel_accuracy": round(acc, 4) if acc is not None else None,
    }
