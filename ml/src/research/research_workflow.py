"""Quality, segmentation, and ROI-review orchestration for research images."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

import numpy as np

from ml.src.quality.quality_assessment import ResearchQualityAssessor
from ml.src.data.lab_alignment import LabAligner
from ml.src.segmentation.conjunctiva_segmenter import ClassicalCVSegmenter


class CaptureQualityStatus(str, Enum):
    USABLE = "USABLE"
    REJECTED = "REJECTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class RejectionReason(str, Enum):
    BLUR = "BLUR"
    MOTION = "MOTION"
    OVEREXPOSURE = "OVEREXPOSURE"
    UNDEREXPOSURE = "UNDEREXPOSURE"
    REFLECTION = "REFLECTION"
    OCCLUSION = "OCCLUSION"
    BAD_FRAMING = "BAD_FRAMING"
    CONJUNCTIVA_NOT_VISIBLE = "CONJUNCTIVA_NOT_VISIBLE"
    SEGMENTATION_FAILED = "SEGMENTATION_FAILED"


@dataclass(frozen=True)
class ResearchImageReview:
    quality_status: CaptureQualityStatus
    rejection_reason: Optional[str]
    quality_metrics: Dict[str, Any]
    segmentation_status: str
    segmentation_result: Optional[Any]
    prediction_performed: bool = False


class ResearchCollectionReviewer:
    """Runs only quality and ClassicalCV segmentation—never Hb prediction."""

    def __init__(
        self,
        quality_assessor: Optional[ResearchQualityAssessor] = None,
        segmenter: Optional[ClassicalCVSegmenter] = None,
    ):
        self.quality_assessor = quality_assessor or ResearchQualityAssessor()
        self.segmenter = segmenter or ClassicalCVSegmenter()

    def review_image(
        self,
        image_rgb: np.ndarray,
        capture_observations: Optional[Dict[str, bool]] = None,
    ) -> ResearchImageReview:
        """Evaluate capture suitability then segment the ROI if suitable."""
        observations = capture_observations or {}
        quality = self.quality_assessor.assess(image_rgb)
        reasons = self._quality_reasons(quality.rejection_reasons, observations)
        metrics = {
            "quality_score": quality.quality_score,
            "focus_score": quality.focus_score,
            "mean_intensity": quality.mean_intensity,
            "overexposure_ratio": quality.overexposure_ratio,
            "underexposure_ratio": quality.underexposure_ratio,
            "specular_ratio": quality.specular_ratio,
        }
        if reasons:
            return ResearchImageReview(
                CaptureQualityStatus.REJECTED,
                reasons[0],
                metrics,
                "NOT_RUN",
                None,
            )

        result = self.segmenter.segment(image_rgb)
        if not result.success:
            return ResearchImageReview(
                CaptureQualityStatus.REVIEW_REQUIRED,
                RejectionReason.SEGMENTATION_FAILED.value,
                metrics,
                "FAILED",
                result,
            )
        return ResearchImageReview(
            CaptureQualityStatus.USABLE,
            None,
            metrics,
            "SUCCEEDED",
            result,
        )

    @staticmethod
    def _quality_reasons(quality_reasons: Any, observations: Dict[str, bool]) -> list[str]:
        mapping = {
            "rejected_blur": RejectionReason.BLUR.value,
            "rejected_overexposure": RejectionReason.OVEREXPOSURE.value,
            "rejected_underexposure": RejectionReason.UNDEREXPOSURE.value,
            "rejected_specularity": RejectionReason.REFLECTION.value,
        }
        reasons = [mapping.get(str(reason), str(reason).upper()) for reason in quality_reasons]
        observation_reasons = (
            ("motion_detected", RejectionReason.MOTION.value),
            ("reflection_detected", RejectionReason.REFLECTION.value),
            ("occlusion_detected", RejectionReason.OCCLUSION.value),
            ("bad_framing", RejectionReason.BAD_FRAMING.value),
            ("conjunctiva_not_visible", RejectionReason.CONJUNCTIVA_NOT_VISIBLE.value),
        )
        for flag, reason in observation_reasons:
            if observations.get(flag):
                reasons.append(reason)
        return list(dict.fromkeys(reasons))


class ResearchLabLinker:
    """Protocol-windowed laboratory linkage using the Phase 8 ``LabAligner``."""

    def __init__(self, alignment_window_minutes: Optional[float]):
        if alignment_window_minutes is None or alignment_window_minutes < 0:
            raise ValueError("An approved non-negative laboratory alignment window is required.")
        self.aligner = LabAligner(maximum_delta_minutes=alignment_window_minutes)

    def link(self, image_timestamp: str, lab_measurements: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Return recorded temporal linkage metadata; never estimates Hb from images."""
        result = self.aligner.align(image_timestamp, lab_measurements)
        selected = next(
            (
                record for record in lab_measurements
                if record.get("lab_measurement_id") == result.selected_lab_measurement_id
            ),
            {},
        )
        return {
            "image_timestamp": image_timestamp,
            "lab_timestamp": selected.get("measurement_timestamp"),
            "time_delta_minutes": result.time_delta_minutes,
            "selected_lab_measurement_id": result.selected_lab_measurement_id,
            "alignment_status": result.alignment_status,
        }
