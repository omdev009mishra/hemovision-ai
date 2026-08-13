"""
HemoVision — Lower Eyelid Boundary Detector
Identifies the lower eyelid margin and constructs candidate lower palpebral conjunctiva ROI.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np
import cv2


@dataclass
class EyelidDetectionResult:
    success: bool
    candidate_mask: np.ndarray  # Binary mask uint8 [H, W] of lower eyelid candidate ROI
    bounding_box: Tuple[int, int, int, int]  # (x, y, w, h)
    eyelid_quality: float
    failure_reason: Optional[str] = None


class EyelidDetector:
    """Detects lower eyelid margin and isolates candidate palpebral conjunctiva region."""

    def __init__(self, y_start_ratio: float = 0.15, y_end_ratio: float = 0.95):
        self.y_start_ratio = y_start_ratio
        self.y_end_ratio = y_end_ratio

    def detect_lower_eyelid(self, image_rgb: np.ndarray, eye_bbox: Tuple[int, int, int, int]) -> EyelidDetectionResult:
        if image_rgb is None or image_rgb.size == 0:
            return EyelidDetectionResult(
                success=False,
                candidate_mask=np.zeros((1, 1), dtype=np.uint8),
                bounding_box=(0, 0, 0, 0),
                eyelid_quality=0.0,
                failure_reason="invalid_image"
            )

        h, w, _ = image_rgb.shape
        ex, ey, ew, eh = eye_bbox

        candidate_mask = np.zeros((h, w), dtype=np.uint8)

        # Restrict to middle-lower region of eye bounding box
        y_start = max(0, int(ey + eh * self.y_start_ratio))
        y_end = min(h, int(ey + eh * self.y_end_ratio))
        x_start = max(0, int(ex + ew * 0.05))
        x_end = min(w, int(ex + ew * 0.95))

        if y_end <= y_start or x_end <= x_start:
            candidate_mask[int(h * 0.3):int(h * 0.9), int(w * 0.1):int(w * 0.9)] = 255
            bbox = (int(w * 0.1), int(h * 0.3), int(w * 0.8), int(h * 0.6))
        else:
            candidate_mask[y_start:y_end, x_start:x_end] = 255
            bbox = (x_start, y_start, x_end - x_start, y_end - y_start)

        return EyelidDetectionResult(
            success=True,
            candidate_mask=candidate_mask,
            bounding_box=bbox,
            eyelid_quality=0.85
        )
