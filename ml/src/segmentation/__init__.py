"""
HemoVision Segmentation Package — Phase 3
Palpebral conjunctiva ROI localization, color-space semantic segmentation, and evaluation metrics.
"""

from ml.src.segmentation.conjunctiva_segmenter import (
    ConjunctivaSegmenter,
    SegmentationResult,
    calculate_iou,
    calculate_dice,
)

__all__ = [
    "ConjunctivaSegmenter",
    "SegmentationResult",
    "calculate_iou",
    "calculate_dice",
]
