"""
HemoVision — Morphological Refinements & Connected Component Filtering
Applies morphological opening/closing and filters contours by area, aspect ratio, and spatial position.
"""

from typing import Dict, Any, Tuple
import numpy as np
import cv2


class MorphologicalRefiner:
    """Applies morphological operations and connected-component spatial filtering."""

    def __init__(
        self,
        kernel_size: int = 5,
        min_component_area: int = 100,
        max_component_area_ratio: float = 0.35,
        min_aspect_ratio: float = 0.5,
        max_aspect_ratio: float = 6.0,
    ):
        self.kernel_size = kernel_size
        self.min_component_area = min_component_area
        self.max_component_area_ratio = max_component_area_ratio
        self.min_aspect_ratio = min_aspect_ratio
        self.max_aspect_ratio = max_aspect_ratio

    def refine(self, raw_mask: np.ndarray) -> np.ndarray:
        """
        Applies morphological opening, closing, and connected-component filtering.

        Args:
            raw_mask: Binary uint8 mask [H, W] with values {0, 255}

        Returns:
            Refined uint8 binary mask [H, W]
        """
        if raw_mask is None or raw_mask.size == 0:
            return raw_mask

        h, w = raw_mask.shape
        total_pixels = h * w

        # 1. Morphological Kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.kernel_size, self.kernel_size))

        # Opening (noise removal) followed by Closing (gap filling)
        opened = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

        # 2. Connected Component Filtering
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        refined_mask = np.zeros((h, w), dtype=np.uint8)

        if not contours:
            return refined_mask

        valid_contours = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < self.min_component_area or area > (total_pixels * self.max_component_area_ratio):
                continue

            x, y, bw, bh = cv2.boundingRect(c)
            if bh == 0:
                continue
            aspect_ratio = float(bw / bh)

            if self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio:
                valid_contours.append(c)

        if valid_contours:
            # Keep largest valid contour (palpebral conjunctiva main region)
            largest = max(valid_contours, key=cv2.contourArea)
            cv2.drawContours(refined_mask, [largest], -1, 255, thickness=cv2.FILLED)
        else:
            # If no single contour meets aspect ratio constraints, keep largest raw contour if area > min
            largest_raw = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_raw) >= self.min_component_area:
                cv2.drawContours(refined_mask, [largest_raw], -1, 255, thickness=cv2.FILLED)

        return refined_mask
