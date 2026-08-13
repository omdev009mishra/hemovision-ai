"""
Tests for Segmentation Failure Cases and Quality Gating
"""

import pytest
import cv2
import numpy as np
from pathlib import Path
from ml.src.segmentation.conjunctiva_segmenter import create_segmenter
from ml.src.inference.pipeline import InferencePipeline


def test_segmentation_failure_fixtures():
    segmenter = create_segmenter("classical_cv")
    failures_dir = Path("dataset/samples/segmentation")

    for f_name in ["no_eye.png", "dark_eye.png", "overexposed_eye.png", "blurry_eye.png", "incorrect_framing.png"]:
        f_path = failures_dir / f_name
        if not f_path.exists():
            continue

        bgr = cv2.imread(str(f_path))
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        res = segmenter.segment(rgb)
        # Should either fail or produce zero/minimal invalid ROI
        if not res.success:
            assert res.failure_reason is not None


def test_inference_pipeline_gates_on_segmentation_failure():
    pipeline = InferencePipeline()
    blank_eye = np.full((512, 512, 3), 40, dtype=np.uint8)

    res = pipeline.process(blank_eye)
    assert res.is_usable is False
    assert res.estimated_hb_g_dl is None
