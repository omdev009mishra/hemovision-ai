"""
HemoVision — Eye Region Detector
Detects the ocular/eyelid region from an eye image using edge density, intensity contrast, and reticle constraints.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
import numpy as np
import cv2


@dataclass
class EyeDetectionResult:
    success: bool
    bounding_box: Tuple[int, int, int, int]  # (x, y, w, h)
    eye_region_quality: float
    cropped_eye_rgb: Optional[np.ndarray] = None
    failure_reason: Optional[str] = None


class EyeDetector:
    """Detects and localizes the eye/ocular region in smartphone images."""

    def __init__(self, min_contrast: float = 5.0, min_edge_density: float = 0.001):
        self.min_contrast = min_contrast
        self.min_edge_density = min_edge_density

    def detect(self, image_rgb: np.ndarray) -> EyeDetectionResult:
        if image_rgb is None or image_rgb.size == 0 or len(image_rgb.shape) != 3:
            return EyeDetectionResult(
                success=False,
                bounding_box=(0, 0, 0, 0),
                eye_region_quality=0.0,
                failure_reason="invalid_image_dimensions"
            )

        h, w, _ = image_rgb.shape
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        # Calculate contrast (standard deviation of gray intensity)
        contrast = float(np.std(gray))
        if contrast < self.min_contrast:
            return EyeDetectionResult(
                success=False,
                bounding_box=(0, 0, w, h),
                eye_region_quality=0.0,
                failure_reason="eye_not_detected"
            )

        # Canny edge density check
        edges = cv2.Canny(gray, 30, 120)
        edge_density = float(np.sum(edges > 0) / (h * w))

        if edge_density < self.min_edge_density:
            return EyeDetectionResult(
                success=False,
                bounding_box=(0, 0, w, h),
                eye_region_quality=0.0,
                failure_reason="eye_not_detected"
            )

        # Find ocular bounding region
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours and any(cv2.contourArea(c) > 10 for c in contours):
            valid_c = [c for c in contours if cv2.contourArea(c) > 10]
            pts = np.vstack(valid_c)
            x, y, bw, bh = cv2.boundingRect(pts)
            pad_x = int(bw * 0.1)
            pad_y = int(bh * 0.1)
            x_min = max(0, x - pad_x)
            y_min = max(0, y - pad_y)
            x_max = min(w, x + bw + pad_x)
            y_max = min(h, y + bh + pad_y)
            bbox = (x_min, y_min, max(1, x_max - x_min), max(1, y_max - y_min))
        else:
            bbox = (0, 0, w, h)

        bx, by, bw, bh = bbox
        cropped = image_rgb[by:by+bh, bx:bx+bw].copy() if bw > 0 and bh > 0 else image_rgb.copy()
        quality_score = min(1.0, max(0.5, float((contrast / 50.0) * 0.5 + (edge_density / 0.05) * 0.5)))

        return EyeDetectionResult(
            success=True,
            bounding_box=bbox,
            eye_region_quality=round(quality_score, 4),
            cropped_eye_rgb=cropped
        )
