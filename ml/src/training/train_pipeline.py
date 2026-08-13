"""
HemoVision Training Pipeline CLI
Entrypoint: python -m ml.src.training.train_pipeline --config ml/configs/hb_training.yaml
"""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd

from ml.src.training.train_config import TrainingConfig
from ml.src.data.dataset_loader import DatasetLoader
from ml.src.data.dataset_validator import DatasetValidator
from ml.src.data.dataset_manifest import DatasetManifestGenerator
from ml.src.data.split_dataset import DatasetSplitter
from ml.src.models.baseline_models import BaselineModelFactory
from ml.src.models.model_registry import ModelRegistry, ModelMetadata
from ml.src.training.cross_validation import GroupCrossValidator
from ml.src.evaluation.regression_metrics import calculate_regression_metrics
from ml.src.evaluation.subgroup_analysis import SubgroupAnalyzer
from ml.src.models.feature_extractor import FeatureExtractor
from ml.src.segmentation.conjunctiva_segmenter import ConjunctivaSegmenter


def run_pipeline(config_path: str):
    print(f"[HemoVision] Loading training configuration from: {config_path}")
    config = TrainingConfig.load_from_yaml(config_path)

    # 1. Discover & Validate Dataset
    validator = DatasetValidator(config.dataset_root)
    issues, summary = validator.validate()
    reports_dir = Path("research/reports")
    json_rep, md_rep = validator.generate_reports(str(reports_dir))
    print(f"[HemoVision] Dataset Validation Report generated at: {md_rep}")

    # 2. Check Clinical Data Governance
    loader = DatasetLoader(config.dataset_root)
    records = loader.load_records()

    manifest_gen = DatasetManifestGenerator(
        dataset_version=config.dataset_version,
        dataset_type="synthetic",  # Currently synthetic fixtures in repo
        seed=config.random_seed
    )
    manifest = manifest_gen.generate_manifest(records, "dataset/dataset_manifest.json")

    has_clinical_data = manifest["governance"]["has_governed_clinical_declaration"]

    exp_id = f"EXP-{datetime.now(timezone.utc).strftime('%Y%m%m-%H%M%S')}"
    exp_dir = Path(f"research/experiments/{exp_id}")
    exp_dir.mkdir(parents=True, exist_ok=True)

    if not has_clinical_data:
        print("\n" + "=" * 60)
        print("Clinical training dataset unavailable — clinical model training not performed.")
        print("=" * 60)
        print("[HemoVision] Running synthetic smoke test for software code verification ONLY...\n")

        # Create synthetic smoke test data for pipeline verification
        rng = np.random.RandomState(config.random_seed)
        n_samples = 40
        X_smoke = rng.randn(n_samples, 28)
        y_smoke = 13.5 + 1.5 * rng.randn(n_samples)
        groups_smoke = np.array([f"P{i // 4:03d}" for i in range(n_samples)])

        # Split synthetic data
        splitter = DatasetSplitter(config.train_ratio, config.val_ratio, config.test_ratio, config.random_seed)
        unique_pts = list(set(groups_smoke))
        pts_split = splitter.split_participants(unique_pts)

        train_mask = np.isin(groups_smoke, list(pts_split["train"]))
        val_mask = np.isin(groups_smoke, list(pts_split["val"]))
        test_mask = np.isin(groups_smoke, list(pts_split["test"]))

        X_tr, y_tr, g_tr = X_smoke[train_mask], y_smoke[train_mask], groups_smoke[train_mask]
        X_va, y_va = X_smoke[val_mask], y_smoke[val_mask]
        X_te, y_te = X_smoke[test_mask], y_smoke[test_mask]

        cv = GroupCrossValidator(n_splits=config.cv_folds, random_seed=config.random_seed)
        model_results = []

        for m_name in config.enabled_models:
            # Fit model
            model = BaselineModelFactory.create_model(m_name, config.random_seed)
            model.fit(X_tr, y_tr)

            # Cross validation
            cv_res = cv.evaluate_model(m_name, X_tr, y_tr, g_tr)

            # Val & Test evaluation
            val_preds = model.predict(X_va)
            test_preds = model.predict(X_te)
            val_m = calculate_regression_metrics(y_va, val_preds)
            test_m = calculate_regression_metrics(y_te, test_preds)

            model_results.append({
                "model": m_name,
                "cv_mean_mae": cv_res["mean_mae"],
                "validation_mae": val_m["mae"],
                "validation_rmse": val_m["rmse"],
                "validation_r2": val_m["r2"],
                "test_mae": test_m["mae"],
                "test_rmse": test_m["rmse"],
                "test_r2": test_m["r2"],
                "note": "SYNTHETIC SMOKE TEST ONLY"
            })

        # Save model_comparison.csv
        comp_df = pd.DataFrame(model_results)
        comp_path = exp_dir / "model_comparison.csv"
        comp_df.to_csv(comp_path, index=False)
        print(f"[HemoVision] Synthetic smoke test completed. Results written to: {comp_path}")

        # Save subgroup analysis
        df_sub = pd.DataFrame({
            "laboratory_hb_g_dl": y_smoke,
            "pred_hb": y_smoke + rng.randn(n_samples) * 0.5,
            "camera_lens_direction": ["front", "back"] * (n_samples // 2),
            "phone_manufacturer": ["Google", "Motorola", "Samsung", "Apple"] * (n_samples // 4)
        })
        analyzer = SubgroupAnalyzer(is_synthetic_smoke_test=True)
        sub_df = analyzer.evaluate_subgroups(df_sub, "laboratory_hb_g_dl", "pred_hb", ["camera_lens_direction", "phone_manufacturer"])
        analyzer.save_csv(sub_df, str(exp_dir / "subgroup_results.csv"))

        # Save experiment log & readme
        with open(exp_dir / "README.md", "w", encoding="utf-8") as f:
            f.write("# Experiment Log: " + exp_id + "\n\n")
            f.write("**Status**: SYNTHETIC SMOKE TEST ONLY\n")
            f.write("**Notice**: Clinical model training dataset unavailable — clinical model training not performed.\n")

        # Save temporary smoke test model artifact (never clinical model artifact)
        registry = ModelRegistry("ml/models")
        meta = ModelMetadata(
            model_version="smoke-test-v0.1.0",
            model_type="Ridge",
            dataset_version=config.dataset_version,
            feature_version="1.0.0",
            preprocessing_version="1.0.0",
            training_timestamp=datetime.now(timezone.utc).isoformat(),
            random_seed=config.random_seed,
            training_participants=len(pts_split["train"]),
            validation_participants=len(pts_split["val"]),
            test_participants=len(pts_split["test"]),
            validation_metrics={"mae": 0.0, "rmse": 0.0, "r2": 0.0},
            test_metrics={"mae": 0.0, "rmse": 0.0, "r2": 0.0},
            is_clinical_model=False,
            limitations=["SYNTHETIC TEST ARTIFACT — NOT FOR CLINICAL USE"]
        )
        dummy_model = BaselineModelFactory.create_model("ridge", config.random_seed)
        dummy_model.fit(X_tr, y_tr)
        registry.save_model(dummy_model, meta, filename="smoke_test_model.joblib")

        print("[HemoVision] Training pipeline ready — clinical training pending governed dataset.")
        return

    # If clinical dataset IS available (future clinical dataset release)
    print("[HemoVision] Governed clinical dataset detected. Initializing clinical training...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HemoVision Research ML Training Pipeline")
    parser.add_argument("--config", type=str, default="ml/configs/hb_training.yaml", help="Path to training config YAML")
    args = parser.parse_args()

    run_pipeline(args.config)
