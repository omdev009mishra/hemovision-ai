"""
HemoVision — Phase 7: Palpebral Conjunctiva Localization & Segmentation

Modular architecture supporting classical computer vision baselines (ClassicalCVSegmenter / ConjunctivaSegmenter)
and extensible interfaces for future deep learning segmentation models (UNet, MobileNet).
"""

from abc import ABC, abstractmethod
from pathlib import Path
import time
from typing import Dict, Any, Optional, Tuple
try:
    import yaml
except ImportError:
    yaml = None
import numpy as np
import cv2

from ml.src.segmentation.segmentation_result import SegmentationResult
from ml.src.segmentation.eye_detector import EyeDetector
from ml.src.segmentation.eyelid_detector import EyelidDetector
from ml.src.segmentation.morphological_refinement import MorphologicalRefiner
from ml.src.segmentation.roi_extractor import ROIExtractor
from ml.src.segmentation.visualization import SegmentationVisualizer


def calculate_iou(mask_pred: np.ndarray, mask_true: np.ndarray) -> float:
    """Calculate Intersection over Union (IoU / Jaccard Index) between binary masks."""
    from ml.src.evaluation.segmentation_metrics import calculate_iou as calc_iou
    val = calc_iou(mask_pred, mask_true)
    return float(val) if val is not None else 0.0


def calculate_dice(mask_pred: np.ndarray, mask_true: np.ndarray) -> float:
    """Calculate Dice Similarity Coefficient (DSC) between binary masks."""
    from ml.src.evaluation.segmentation_metrics import calculate_dice as calc_dice
    val = calc_dice(mask_pred, mask_true)
    return float(val) if val is not None else 0.0


class AbstractSegmenter(ABC):
    """Abstract base interface for palpebral conjunctiva segmentation models."""

    @abstractmethod
    def segment(self, image_rgb: np.ndarray) -> SegmentationResult:
        pass


class ClassicalCVSegmenter(AbstractSegmenter):
    """
    Classical Computer Vision baseline for lower palpebral conjunctiva segmentation.
    Combines multi-colorspace thresholding (CIELAB a*, HSV H/S/V), morphological operations,
    and connected-component spatial filtering.
    """

    def __init__(
        self,
        config_path: Optional[str] = "ml/configs/segmentation.yaml",
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
        self.config = {}
        if config_path and Path(config_path).exists() and yaml is not None:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f) or {}
            except Exception:
                self.config = {}

        cs_cfg = self.config.get("color_space", {})
        hsv1_cfg = cs_cfg.get("hsv_red1", {})
        hsv2_cfg = cs_cfg.get("hsv_red2", {})
        morph_cfg = self.config.get("morphology", {})
        comp_cfg = self.config.get("component_filtering", {})
        roi_cfg = self.config.get("roi_constraints", {})
        q_cfg = self.config.get("quality_gate", {})

        # Color Space bounds (override with explicit init arguments if non-default)
        self.min_a_star = min_a_star if min_a_star != 135 else cs_cfg.get("lab_a_min", 135)

        self.min_hue1 = min_hue if min_hue != 0 else hsv1_cfg.get("hue_min", 0)
        self.max_hue1 = max_hue if max_hue != 25 else hsv1_cfg.get("hue_max", 25)
        self.min_sat1 = min_sat if min_sat != 30 else hsv1_cfg.get("sat_min", 30)
        self.max_sat1 = max_sat if max_sat != 255 else hsv1_cfg.get("sat_max", 255)
        self.min_val1 = min_val if min_val != 40 else hsv1_cfg.get("val_min", 40)
        self.max_val1 = max_val if max_val != 255 else hsv1_cfg.get("val_max", 255)

        self.min_hue2 = hsv2_cfg.get("hue_min", 160)
        self.max_hue2 = hsv2_cfg.get("hue_max", 180)
        self.min_sat2 = hsv2_cfg.get("sat_min", self.min_sat1)
        self.max_sat2 = hsv2_cfg.get("sat_max", self.max_sat1)
        self.min_val2 = hsv2_cfg.get("val_min", self.min_val1)
        self.max_val2 = hsv2_cfg.get("val_max", self.max_val1)

        # Detectors & Refiners
        self.eye_detector = EyeDetector()
        self.eyelid_detector = EyelidDetector(
            y_start_ratio=roi_cfg.get("y_start_ratio", 0.15),
            y_end_ratio=roi_cfg.get("y_end_ratio", 0.95)
        )
        self.morph_refiner = MorphologicalRefiner(
            kernel_size=morph_cfg.get("kernel_size", morph_kernel_size),
            min_component_area=comp_cfg.get("min_component_area_pixels", min_roi_area),
            max_component_area_ratio=comp_cfg.get("max_component_area_ratio", 0.35),
            min_aspect_ratio=comp_cfg.get("min_aspect_ratio", 0.5),
            max_aspect_ratio=comp_cfg.get("max_aspect_ratio", 6.0),
        )
        self.roi_extractor = ROIExtractor(
            min_area_pixels=q_cfg.get("min_roi_area_pixels", min_roi_area),
            max_area_ratio=q_cfg.get("max_roi_area_ratio", 0.45)
        )

    def segment(self, image_rgb: np.ndarray) -> SegmentationResult:
        """
        Executes classical CV segmentation pipeline and measures runtime.
        """
        start_time = time.perf_counter()

        if image_rgb is None or image_rgb.size == 0 or len(image_rgb.shape) != 3:
            raise ValueError("Input image must be a non-empty 3-channel uint8 array.")

        height, width, _ = image_rgb.shape

        # 1. Eye Region Detection
        eye_res = self.eye_detector.detect(image_rgb)
        if not eye_res.success:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return SegmentationResult(
                success=False,
                mask=np.zeros((height, width), dtype=np.uint8),
                bounding_box=(0, 0, width, height),
                roi_image=image_rgb.copy(),
                roi_area_pixels=0,
                roi_area_ratio=0.0,
                segmentation_quality=0.0,
                failure_reason=eye_res.failure_reason or "eye_not_detected",
                method="classical_cv",
                quality_flags={"eye_detected": False},
                processing_time_ms=elapsed_ms
            )

        # 2. Lower Eyelid Candidate Localization
        eyelid_res = self.eyelid_detector.detect_lower_eyelid(image_rgb, eye_res.bounding_box)

        # 3. Colorspace Analysis (HSV + CIELAB a*)
        hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        lower_red1 = np.array([self.min_hue1, self.min_sat1, self.min_val1], dtype=np.uint8)
        upper_red1 = np.array([self.max_hue1, self.max_sat1, self.max_val1], dtype=np.uint8)
        lower_red2 = np.array([self.min_hue2, self.min_sat2, self.min_val2], dtype=np.uint8)
        upper_red2 = np.array([self.max_hue2, self.max_sat2, self.max_val2], dtype=np.uint8)

        mask_hsv1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_hsv2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_hsv = cv2.bitwise_or(mask_hsv1, mask_hsv2)

        lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
        a_channel = lab[:, :, 1]
        _, mask_lab = cv2.threshold(a_channel, self.min_a_star, 255, cv2.THRESH_BINARY)

        color_mask = cv2.bitwise_and(mask_hsv, mask_lab)
        candidate_color_mask = cv2.bitwise_and(color_mask, eyelid_res.candidate_mask)

        # 4. Morphological Refinement & Component Filtering
        refined_mask = self.morph_refiner.refine(candidate_color_mask)

        # 5. ROI Extraction & Quality Gate Evaluation
        roi_res = self.roi_extractor.extract(image_rgb, refined_mask)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        if not roi_res.success:
            return SegmentationResult(
                success=False,
                mask=refined_mask,
                bounding_box=roi_res.bounding_box,
                roi_image=roi_res.roi_image,
                roi_area_pixels=roi_res.roi_area_pixels,
                roi_area_ratio=roi_res.roi_area_ratio,
                segmentation_quality=0.0,
                failure_reason=roi_res.failure_reason or "segmentation_failed",
                method="classical_cv",
                quality_flags=roi_res.quality_flags,
                processing_time_ms=elapsed_ms
            )

        # Generate Visual Overlay
        overlay = SegmentationVisualizer.create_overlay(image_rgb, refined_mask, roi_res.bounding_box)

        # Algorithmic Segmentation Quality Score
        quality_score = min(1.0, float(0.4 * eye_res.eye_region_quality + 0.6 * min(1.0, roi_res.roi_area_ratio / 0.15)))

        return SegmentationResult(
            success=True,
            mask=refined_mask,
            bounding_box=roi_res.bounding_box,
            roi_image=roi_res.roi_image,
            roi_area_pixels=roi_res.roi_area_pixels,
            roi_area_ratio=roi_res.roi_area_ratio,
            segmentation_quality=round(quality_score, 4),
            failure_reason=None,
            method="classical_cv",
            quality_flags=roi_res.quality_flags,
            processing_time_ms=elapsed_ms,
            visual_overlay=overlay
        )


# Alias ConjunctivaSegmenter to ClassicalCVSegmenter for backward compatibility
ConjunctivaSegmenter = ClassicalCVSegmenter


def create_segmenter(method: str = "classical_cv", config_path: str = "ml/configs/segmentation.yaml") -> ClassicalCVSegmenter:
    """Factory function creating a segmenter instance."""
    if method == "classical_cv":
        return ClassicalCVSegmenter(config_path=config_path)
    else:
        raise ValueError(f"Unknown segmentation method: '{method}'. Supported methods: ['classical_cv']")
