"""
HemoVision — Phase 8: Unified End-to-End Inference Pipeline

Executes Quality Assessment -> Segmentation -> Color Preprocessing -> Feature Extraction
-> ML Hb Estimation -> Conformal Interval Gating -> Visual Overlay Generation.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Tuple
import base64
import cv2
import numpy as np

from ml.src.quality.quality_assessment import ResearchQualityAssessor, QualityAssessmentResult
from ml.src.segmentation.conjunctiva_segmenter import ConjunctivaSegmenter, SegmentationResult
from ml.src.preprocessing.color_calibration import ColorCalibrator, CalibrationResult
from ml.src.models.feature_extractor import FeatureExtractor, FeatureVector
from ml.src.models.hb_estimator import HbEstimator, ModelPrediction


@dataclass
class InferenceResult:
    """Complete container for HemoVision research analysis results."""
    is_usable: bool
    quality_score: float
    rejection_reasons: Tuple[str, ...]
    quality_details: Dict[str, Any]
    segmentation_details: Dict[str, Any]
    feature_summary: Dict[str, float]
    estimated_hb_g_dl: Optional[float]
    prediction_interval: Optional[Tuple[float, float]]
    confidence_level: Optional[float]
    reliability_score: Optional[float]
    research_category: str
    disclaimer: str
    visual_overlay_b64: str  # Base64 encoded JPEG image of visual overlay
    roi_crop_b64: str  # Base64 encoded JPEG image of cropped ROI


def _array_to_b64_jpeg(arr_rgb: np.ndarray) -> str:
    """Helper to convert RGB uint8 numpy array to base64 JPEG string."""
    if arr_rgb is None or arr_rgb.size == 0:
        return ""
    bgr = cv2.cvtColor(arr_rgb, cv2.COLOR_RGB2BGR)
    success, buffer = cv2.imencode(".jpg", bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    if not success:
        return ""
    return base64.b64encode(buffer).decode("utf-8")


class InferencePipeline:
    """
    Unified end-to-end research inference pipeline for HemoVision.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.quality_assessor = ResearchQualityAssessor()
        self.segmenter = ConjunctivaSegmenter()
        self.calibrator = ColorCalibrator(method="gray_world")
        self.feature_extractor = FeatureExtractor()
        self.hb_estimator = HbEstimator(model_path=model_path)

    def process(self, image_rgb: np.ndarray) -> InferenceResult:
        """
        Process an input RGB conjunctival image through the entire research pipeline.

        Args:
            image_rgb: RGB uint8 numpy array [H, W, 3]

        Returns:
            InferenceResult object with analysis metrics, predictions, and base64 visuals.
        """
        if image_rgb is None or image_rgb.size == 0:
            raise ValueError("Input image must be a non-empty 3-channel uint8 array.")

        # 1. Quality Assessment
        quality_res: QualityAssessmentResult = self.quality_assessor.assess(image_rgb)

        # 2. Conjunctiva Segmentation
        seg_res: SegmentationResult = self.segmenter.segment(image_rgb)

        # Base64 encode visual overlay and cropped ROI
        overlay_b64 = _array_to_b64_jpeg(seg_res.visual_overlay)
        roi_b64 = _array_to_b64_jpeg(seg_res.roi_crop)

        # If quality is rejected, return early with quality gate failure details
        if not quality_res.is_usable:
            return InferenceResult(
                is_usable=False,
                quality_score=quality_res.quality_score,
                rejection_reasons=quality_res.rejection_reasons,
                quality_details={
                    "focus_score": quality_res.focus_score,
                    "mean_intensity": quality_res.mean_intensity,
                    "overexposure_ratio": quality_res.overexposure_ratio,
                    "underexposure_ratio": quality_res.underexposure_ratio,
                    "specular_ratio": quality_res.specular_ratio,
                },
                segmentation_details=seg_res.quality_metrics,
                feature_summary={},
                estimated_hb_g_dl=None,
                prediction_interval=None,
                confidence_level=None,
                reliability_score=None,
                research_category="Quality Gate Failure",
                disclaimer="Image rejected due to quality heuristics (blur/exposure). Please recapture.",
                visual_overlay_b64=overlay_b64,
                roi_crop_b64=roi_b64,
            )

        # 3. Color Calibration & Normalization
        calib_res: CalibrationResult = self.calibrator.calibrate(seg_res.roi_crop)

        # 4. Feature Extraction
        feature_vec: FeatureVector = self.feature_extractor.extract(calib_res.calibrated_image, seg_res.mask)

        # 5. ML Model Prediction
        prediction: ModelPrediction = self.hb_estimator.predict(feature_vec)

        return InferenceResult(
            is_usable=True,
            quality_score=quality_res.quality_score,
            rejection_reasons=quality_res.rejection_reasons,
            quality_details={
                "focus_score": quality_res.focus_score,
                "mean_intensity": quality_res.mean_intensity,
                "overexposure_ratio": quality_res.overexposure_ratio,
                "underexposure_ratio": quality_res.underexposure_ratio,
                "specular_ratio": quality_res.specular_ratio,
            },
            segmentation_details=seg_res.quality_metrics,
            feature_summary={
                "redness_index": round(feature_vec.redness_index, 4),
                "erythema_index": round(feature_vec.erythema_index, 4),
                "a_star_redness": round(feature_vec.a_star_mean, 2),
                "b_star_yellowness": round(feature_vec.b_star_mean, 2),
                "l_star_luminance": round(feature_vec.l_star_mean, 2),
                "red_green_ratio": round(feature_vec.red_green_ratio, 3),
            },
            estimated_hb_g_dl=prediction.estimated_hb_g_dl,
            prediction_interval=prediction.prediction_interval,
            confidence_level=prediction.confidence_level,
            reliability_score=prediction.reliability_score,
            research_category=prediction.research_category,
            disclaimer=prediction.disclaimer,
            visual_overlay_b64=overlay_b64,
            roi_crop_b64=roi_b64,
        )
