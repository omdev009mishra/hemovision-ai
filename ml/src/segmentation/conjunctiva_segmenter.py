"""
HemoVision — Phase 3: Palpebral Conjunctiva Localization & Segmentation

Implements classical baseline computer vision algorithms (HSV/LAB color-space thresholding,
morphological operations, and spatial region constraints) for isolating the palpebral
conjunctiva (inner lower eyelid) from ocular/facial images.

Output format supports binary masks, bounding boxes, cropped ROIs, segmentation metrics (IoU, Dice),
and color visual overlays. Designed to easily interface with future deep learning (U-Net) backends.
"""

from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional
import numpy as np
import cv2


@dataclass
class SegmentationResult:
    """Container for palpebral conjunctiva segmentation outputs."""
    mask: np.ndarray  # Binary mask uint8 [H, W], values {0, 255}
    roi_crop: np.ndarray  # Bounding-box cropped RGB image [H_roi, W_roi, 3]
    bounding_box: Tuple[int, int, int, int]  # (x, y, width, height)
    roi_area_pixels: int  # Count of foreground conjunctiva pixels
    coverage_ratio: float  # Fraction of image occupied by conjunctiva ROI
    quality_metrics: Dict[str, float]  # Metrics dictionary (compactness, aspect ratio, mean red intensity)
    visual_overlay: np.ndarray  # RGB visualization with green mask contour and red ROI bounding box


def calculate_iou(mask_pred: np.ndarray, mask_true: np.ndarray) -> float:
    """Calculate Intersection over Union (IoU / Jaccard Index) between binary masks."""
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    intersection = np.logical_and(pred_bool, true_bool).sum()
    union = np.logical_or(pred_bool, true_bool).sum()
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return float(intersection / union)


def calculate_dice(mask_pred: np.ndarray, mask_true: np.ndarray) -> float:
    """Calculate Dice Similarity Coefficient (DSC) between binary masks."""
    pred_bool = (mask_pred > 127)
    true_bool = (mask_true > 127)
    intersection = np.logical_and(pred_bool, true_bool).sum()
    total_pixels = pred_bool.sum() + true_bool.sum()
    if total_pixels == 0:
        return 1.0
    return float(2.0 * intersection / total_pixels)


class ConjunctivaSegmenter:
    """
    Palpebral conjunctiva localization and semantic segmentation engine.
    Uses adaptive color-space segmentation (HSV + LAB a* channel) and spatial constraints.
    """

    def __init__(
        self,
        min_hue: int = 0,
        max_hue: int = 25,
        min_sat: int = 30,
        max_sat: int = 255,
        min_val: int = 40,
        max_val: int = 255,
        min_a_star: int = 135,
        morph_kernel_size: int = 5,
        min_roi_area: int = 100,
    ):
        self.min_hue = min_hue
        self.max_hue = max_hue
        self.min_sat = min_sat
        self.max_sat = max_sat
        self.min_val = min_val
        self.max_val = max_val
        self.min_a_star = min_a_star
        self.morph_kernel_size = morph_kernel_size
        self.min_roi_area = min_roi_area

    def segment(self, image_rgb: np.ndarray) -> SegmentationResult:
        """
        Segment the palpebral conjunctiva from an RGB input image.

        Args:
            image_rgb: RGB image numpy array of shape [H, W, 3], uint8.

        Returns:
            SegmentationResult object containing mask, cropped ROI, bounding box, and metrics.
        """
        if image_rgb is None or image_rgb.size == 0 or len(image_rgb.shape) != 3:
            raise ValueError("Input image must be a non-empty 3-channel uint8 array.")

        height, width, _ = image_rgb.shape
        total_pixels = height * width

        # 1. Convert to HSV color space for hue/saturation filtering of mucosal red/pink tones
        hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        
        # Lower and upper bounds for red/pink mucosa in HSV
        lower_red1 = np.array([0, self.min_sat, self.min_val], dtype=np.uint8)
        upper_red1 = np.array([self.max_hue, self.max_sat, self.max_val], dtype=np.uint8)
        
        lower_red2 = np.array([160, self.min_sat, self.min_val], dtype=np.uint8)
        upper_red2 = np.array([180, self.max_sat, self.max_val], dtype=np.uint8)

        mask_hsv1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_hsv2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_hsv = cv2.bitwise_or(mask_hsv1, mask_hsv2)

        # 2. Convert to CIELAB color space for redness emphasis (a* channel)
        lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
        a_channel = lab[:, :, 1]
        _, mask_lab = cv2.threshold(a_channel, self.min_a_star, 255, cv2.THRESH_BINARY)

        # Combined color mask
        raw_mask = cv2.bitwise_and(mask_hsv, mask_lab)

        # 3. Apply Morphological Cleanup (Opening then Closing)
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (self.morph_kernel_size, self.morph_kernel_size)
        )
        opened_mask = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, kernel)
        closed_mask = cv2.morphologyEx(opened_mask, cv2.MORPH_CLOSE, kernel)

        # 4. Spatial ROI Constraint (Prioritize lower portion of image where lower eyelid palpebral conjunctiva rests)
        spatial_mask = np.zeros_like(closed_mask)
        # Eyelid region constraint: middle-to-lower region [20% to 90% height]
        y_start = int(height * 0.15)
        y_end = int(height * 0.95)
        x_start = int(width * 0.05)
        x_end = int(width * 0.95)
        spatial_mask[y_start:y_end, x_start:x_end] = 255

        constrained_mask = cv2.bitwise_and(closed_mask, spatial_mask)

        # 5. Extract Contours and select largest valid palpebral conjunctiva ROI
        contours, _ = cv2.findContours(constrained_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        final_mask = np.zeros((height, width), dtype=np.uint8)
        bbox = (0, 0, width, height)
        roi_area = 0

        if contours:
            # Filter contours by area and sort descending
            valid_contours = [c for c in contours if cv2.contourArea(c) >= self.min_roi_area]
            if valid_contours:
                largest_contour = max(valid_contours, key=cv2.contourArea)
                cv2.drawContours(final_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
                x, y, w, h = cv2.boundingRect(largest_contour)
                bbox = (int(x), int(y), int(w), int(h))
                roi_area = int(cv2.contourArea(largest_contour))
            else:
                # Fallback to constrained mask if no contour passes minimum area
                final_mask = constrained_mask
                roi_area = int(np.sum(final_mask > 0))
                x, y, w, h = cv2.boundingRect(final_mask) if roi_area > 0 else (0, 0, width, height)
                bbox = (int(x), int(y), int(w), int(h))
        else:
            final_mask = constrained_mask
            roi_area = int(np.sum(final_mask > 0))
            if roi_area > 0:
                x, y, w, h = cv2.boundingRect(final_mask)
                bbox = (int(x), int(y), int(w), int(h))

        # Crop ROI image
        bx, by, bw, bh = bbox
        if bw > 0 and bh > 0:
            roi_crop = image_rgb[by:by+bh, bx:bx+bw].copy()
        else:
            roi_crop = image_rgb.copy()

        coverage_ratio = float(roi_area / total_pixels)

        # Calculate quality metrics
        aspect_ratio = float(bw / bh) if bh > 0 else 1.0
        compactness = float(4.0 * np.pi * roi_area / (perimeter ** 2)) if (contours and (perimeter := cv2.arcLength(max(contours, key=cv2.contourArea), True)) > 0) else 0.0

        quality_metrics = {
            "roi_area_pixels": float(roi_area),
            "coverage_ratio": coverage_ratio,
            "aspect_ratio": aspect_ratio,
            "compactness": compactness,
        }

        # 6. Generate Visual Overlay
        visual_overlay = image_rgb.copy()
        # Draw semi-transparent green mask overlay over detected ROI
        green_overlay = visual_overlay.copy()
        green_overlay[final_mask > 0] = [0, 220, 100]
        cv2.addWeighted(green_overlay, 0.4, visual_overlay, 0.6, 0, visual_overlay)

        # Draw red bounding box contour
        if bw > 0 and bh > 0:
            cv2.rectangle(visual_overlay, (bx, by), (bx + bw, by + bh), (255, 30, 30), 2)

        return SegmentationResult(
            mask=final_mask,
            roi_crop=roi_crop,
            bounding_box=bbox,
            roi_area_pixels=roi_area,
            coverage_ratio=coverage_ratio,
            quality_metrics=quality_metrics,
            visual_overlay=visual_overlay,
        )
