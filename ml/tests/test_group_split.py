"""
Tests for Participant-Level Grouped Splitting & GroupKFold
"""

import pytest
import numpy as np
from ml.src.data.split_dataset import DatasetSplitter
from ml.src.training.cross_validation import GroupCrossValidator


def test_participant_split_zero_leakage():
    pts = [f"P{i:03d}" for i in range(20)]
    splitter = DatasetSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, random_seed=42)
    splits = splitter.split_participants(pts)

    train_pts = splits["train"]
    val_pts = splits["val"]
    test_pts = splits["test"]

    assert len(train_pts.intersection(val_pts)) == 0
    assert len(train_pts.intersection(test_pts)) == 0
    assert len(val_pts.intersection(test_pts)) == 0
    assert len(train_pts) + len(val_pts) + len(test_pts) == len(pts)


def test_group_cross_validator():
    cv = GroupCrossValidator(n_splits=3, random_seed=42)
    X = np.random.randn(30, 10)
    y = np.random.randn(30)
    groups = np.array([f"P{i // 5:02d}" for i in range(30)])

    res = cv.evaluate_model("ridge", X, y, groups)
    assert res["model_type"] == "ridge"
    assert "mean_mae" in res
    assert "mean_rmse" in res
    assert "mean_r2" in res
