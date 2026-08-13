"""
HemoVision — Segmentation Visualizer Utilities
Generates multi-panel diagnostic figures and visual overlays for palpebral conjunctiva segmentation.
"""

from pathlib import Path
from typing import Optional
import numpy as np
import cv2
import matplotlib.pyplot as plt

from ml.src.segmentation.segmentation_result import SegmentationResult


class SegmentationVisualizer:
    """Utility class for drawing and saving segmentation visual overlays and multi-panel figures."""

    @staticmethod
    def create_overlay(image_rgb: np.ndarray, mask: np.ndarray, bbox: Optional[tuple] = None) -> np.ndarray:
        """
        Draws semi-transparent green mask overlay and red ROI bounding box on input RGB image.
        """
        if image_rgb is None or image_rgb.size == 0:
            return np.zeros((1, 1, 3), dtype=np.uint8)

        overlay = image_rgb.copy()
        if mask is not None and mask.shape[:2] == image_rgb.shape[:2]:
            green_layer = overlay.copy()
            green_layer[mask > 127] = [0, 220, 100]
            cv2.addWeighted(green_layer, 0.45, overlay, 0.55, 0, overlay)

        if bbox is not None and len(bbox) == 4 and bbox[2] > 0 and bbox[3] > 0:
            bx, by, bw, bh = bbox
            cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), (255, 30, 30), 2)

        return overlay

    @staticmethod
    def save_diagnostic_panel(
        image_rgb: np.ndarray,
        seg_result: SegmentationResult,
        output_path: str,
        title: str = "HemoVision Segmentation Diagnostic Panel"
    ):
        """
        Generates and saves a 4-panel diagnostic figure (Original, Raw/Candidate, Refined Mask, Overlay + ROI).
        """
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle(title, fontsize=14, fontweight='bold')

        # 1. Original Image
        axes[0, 0].imshow(image_rgb)
        axes[0, 0].set_title("1. Input RGB Image")
        axes[0, 0].axis("off")

        # 2. Mask
        axes[0, 1].imshow(seg_result.mask, cmap="gray")
        axes[0, 1].set_title(f"2. Refined Mask (Area: {seg_result.roi_area_pixels} px)")
        axes[0, 1].axis("off")

        # 3. Cropped ROI
        axes[1, 0].imshow(seg_result.roi_image)
        axes[1, 0].set_title("3. Extracted Conjunctiva ROI")
        axes[1, 0].axis("off")

        # 4. Visual Overlay
        overlay = seg_result.visual_overlay if seg_result.visual_overlay is not None else SegmentationVisualizer.create_overlay(image_rgb, seg_result.mask, seg_result.bounding_box)
        axes[1, 1].imshow(overlay)
        axes[1, 1].set_title(f"4. Overlay (Quality: {seg_result.segmentation_quality:.2f})")
        axes[1, 1].axis("off")

        plt.tight_layout()
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_p, dpi=150, bbox_inches='tight')
        plt.close(fig)
