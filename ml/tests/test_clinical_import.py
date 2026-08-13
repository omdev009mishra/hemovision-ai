"""
Tests for Clinical & Synthetic Dataset Importer (run_import_dataset)
"""

import pytest
from ml.src.data.import_dataset import run_import_dataset


def test_import_dataset_synthetic_dry_run(tmp_path):
    out_dir = tmp_path / "clinical"
    run_import_dataset("dataset/samples", str(out_dir), dry_run=True)
    # Dry-run must NOT write dataset_manifest.json or files to output destination
    assert not (out_dir / "dataset_manifest.json").exists()
