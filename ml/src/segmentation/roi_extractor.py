"""
HemoVision — ROI Extractor & Quality Gate Evaluator
Extracts cropped ROI image, bounding box metadata, and evaluates segmentation quality heuristics.
"""

from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional
import numpy as np
import cv2


@dataclass
class ROIExtractionResult:
    success: bool
    roi_image: np.ndarray  # Cropped RGB ROI
    roi_mask: np.ndarray  # Cropped binary ROI mask
    bounding_box: Tuple[int, int, int, int]  # (x, y, w, h)
    roi_area_pixels: int
    roi_area_ratio: float
    quality_flags: Dict[str, bool]
    failure_reason: Optional[str] = None


class ROIExtractor:
    """Extracts cropped conjunctiva ROI and validates segmentation quality."""

    def __init__(self, min_area_pixels: int = 100, max_area_ratio: float = 0.45):
        self.min_area_pixels = min_area_pixels
        self.max_area_ratio = max_area_ratio

    def extract(self, image_rgb: np.ndarray, mask: np.ndarray) -> ROIExtractionResult:
        if image_rgb is None or mask is None or image_rgb.size == 0 or mask.size == 0:
            return ROIExtractionResult(
                success=False,
                roi_image=np.zeros((1, 1, 3), dtype=np.uint8),
                roi_mask=np.zeros((1, 1), dtype=np.uint8),
                bounding_box=(0, 0, 0, 0),
                roi_area_pixels=0,
                roi_area_ratio=0.0,
                quality_flags={"has_roi": False},
                failure_reason="segmentation_failed"
            )

        h, w, _ = image_rgb.shape
        total_pixels = h * w

        roi_area = int(np.sum(mask > 127))
        area_ratio = float(roi_area / total_pixels) if total_pixels > 0 else 0.0

        # Quality Checks
        has_roi = roi_area >= self.min_area_pixels
        valid_area = area_ratio <= self.max_area_ratio

        quality_flags = {
            "has_roi": has_roi,
            "valid_area": valid_area,
            "connected_structure": True,
        }

        if not has_roi:
            return ROIExtractionResult(
                success=False,
                roi_image=image_rgb.copy(),
                roi_mask=mask.copy(),
                bounding_box=(0, 0, w, h),
                roi_area_pixels=roi_area,
                roi_area_ratio=area_ratio,
                quality_flags=quality_flags,
                failure_reason="segmentation_failed"
            )

        if not valid_area:
            return ROIExtractionResult(
                success=False,
                roi_image=image_rgb.copy(),
                roi_mask=mask.copy(),
                bounding_box=(0, 0, w, h),
                roi_area_pixels=roi_area,
                roi_area_ratio=area_ratio,
                quality_flags=quality_flags,
                failure_reason="segmentation_failed"
            )

        # Calculate bounding box
        y_indices, x_indices = np.where(mask > 127)
        if len(x_indices) == 0 or len(y_indices) == 0:
            return ROIExtractionResult(
                success=False,
                roi_image=image_rgb.copy(),
                roi_mask=mask.copy(),
                bounding_box=(0, 0, w, h),
                roi_area_pixels=0,
                roi_area_ratio=0.0,
                quality_flags=quality_flags,
                failure_reason="segmentation_failed"
            )

        x_min, x_max = int(np.min(x_indices)), int(np.max(x_indices))
        y_min, y_max = int(np.min(y_indices)), int(np.max(y_indices))
        bw = max(1, x_max - x_min + 1)
        bh = max(1, y_max - y_min + 1)

        bbox = (x_min, y_min, bw, bh)
        roi_image = image_rgb[y_min:y_min+bh, x_min:x_min+bw].copy()
        roi_mask = mask[y_min:y_min+bh, x_min:x_min+bw].copy()

        return ROIExtractionResult(
            success=True,
            roi_image=roi_image,
            roi_mask=roi_mask,
            bounding_box=bbox,
            roi_area_pixels=roi_area,
            roi_area_ratio=area_ratio,
            quality_flags=quality_flags,
            failure_reason=None
        )
