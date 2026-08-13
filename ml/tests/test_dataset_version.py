"""
Tests for DatasetVersionManager
"""

import pytest
import os
import json
from ml.src.data.dataset_version import DatasetVersionManager


def test_dataset_version_manifest_generation(tmp_path):
    mgr = DatasetVersionManager(version="1.1.0", dataset_type="synthetic")
    out_p = tmp_path / "dataset_manifest.json"

    manifest = mgr.create_manifest(
        governance_status="synthetic",
        total_participants=5,
        total_sessions=5,
        total_images=10,
        usable_images=8,
        excluded_images=2,
        withdrawn_participants=0,
        train_count=6,
        val_count=2,
        test_count=2,
        output_path=str(out_p)
    )

    assert manifest["dataset_version"] == "v1.1.0"
    assert manifest["counts"]["participant_count"] == 5
    assert manifest["governance"]["clinical_training_allowed"] is False
    assert out_p.exists()
