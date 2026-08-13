from types import SimpleNamespace

import numpy as np

from ml.src.research.research_workflow import (
    CaptureQualityStatus,
    ResearchCollectionReviewer,
    ResearchLabLinker,
    RejectionReason,
)


class PassingQualityAssessor:
    def assess(self, _image):
        return SimpleNamespace(
            quality_score=1.0,
            focus_score=300.0,
            mean_intensity=128.0,
            overexposure_ratio=0.0,
            underexposure_ratio=0.0,
            specular_ratio=0.0,
            rejection_reasons=(),
        )


class FailingSegmenter:
    def segment(self, _image):
        return SimpleNamespace(success=False, failure_reason="synthetic failure")


class PassingSegmenter:
    def segment(self, _image):
        return SimpleNamespace(success=True)


def test_segmentation_failure_requires_review_and_never_predicts():
    review = ResearchCollectionReviewer(PassingQualityAssessor(), FailingSegmenter()).review_image(
        np.zeros((8, 8, 3), dtype=np.uint8)
    )
    assert review.quality_status is CaptureQualityStatus.REVIEW_REQUIRED
    assert review.rejection_reason == RejectionReason.SEGMENTATION_FAILED.value
    assert review.prediction_performed is False


def test_capture_observation_rejects_image_before_segmentation():
    review = ResearchCollectionReviewer(PassingQualityAssessor(), PassingSegmenter()).review_image(
        np.zeros((8, 8, 3), dtype=np.uint8), {"motion_detected": True}
    )
    assert review.quality_status is CaptureQualityStatus.REJECTED
    assert review.rejection_reason == RejectionReason.MOTION.value
    assert review.segmentation_status == "NOT_RUN"


def test_lab_linker_uses_explicit_protocol_window():
    linkage = ResearchLabLinker(30.0).link(
        "2026-01-01T12:00:00Z",
        [{
            "lab_measurement_id": "LAB-001",
            "measurement_timestamp": "2026-01-01T12:10:00Z",
            "laboratory_hb_g_dl": 13.5,
        }],
    )
    assert linkage["selected_lab_measurement_id"] == "LAB-001"
    assert linkage["time_delta_minutes"] == 10.0
    assert linkage["alignment_status"] == "aligned"
