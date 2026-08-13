"""
Tests for HemoVision Training Pipeline & Config
"""

import pytest
from pathlib import Path
from ml.src.training.train_config import TrainingConfig
from ml.src.training.train_pipeline import run_pipeline
from ml.src.data.dataset_loader import DatasetLoader
from ml.src.data.dataset_validator import DatasetValidator
from ml.src.data.dataset_manifest import DatasetManifestGenerator


def test_train_config_loading():
    config = TrainingConfig.load_from_yaml("ml/configs/hb_training.yaml")
    assert config.dataset_root == "dataset"
    assert config.train_ratio == 0.70
    assert config.target_name == "laboratory_hb_g_dl"
    assert "ridge" in config.enabled_models


def test_dataset_loader_reads_samples():
    loader = DatasetLoader("dataset")
    records = loader.load_records()
    assert len(records) > 0
    first = records[0]
    assert first.participant_id is not None
    assert first.camera_lens_direction in ["front", "back", "unknown"]


def test_dataset_validator_runs():
    validator = DatasetValidator("dataset")
    issues, summary = validator.validate()
    assert "total_records" in summary
    json_p, md_p = validator.generate_reports("research/reports")
    assert Path(json_p).exists()
    assert Path(md_p).exists()


def test_dataset_manifest_generator():
    loader = DatasetLoader("dataset")
    records = loader.load_records()
    gen = DatasetManifestGenerator(dataset_type="synthetic", seed=42)
    manifest = gen.generate_manifest(records, "research/test_manifest.json")
    assert manifest["dataset_type"] == "synthetic"
    assert manifest["governance"]["clinical_training_allowed"] is False


def test_train_pipeline_smoke_test():
    # Execute pipeline on synthetic dataset (must not raise error)
    run_pipeline("ml/configs/hb_training.yaml")
