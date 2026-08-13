"""
Tests for Baseline Models & Model Comparison
"""

import pytest
import numpy as np
from ml.src.models.baseline_models import BaselineModelFactory
from ml.src.evaluation.regression_metrics import calculate_regression_metrics


def test_baseline_model_factory():
    for m_type in ["mean", "linear", "ridge", "rf", "gb"]:
        model = BaselineModelFactory.create_model(m_type, random_seed=42)
        X = np.random.randn(20, 5)
        y = 12.0 + np.random.randn(20)
        model.fit(X, y)
        preds = model.predict(X)
        assert len(preds) == 20

        metrics = calculate_regression_metrics(y, preds)
        assert "mae" in metrics
        assert "rmse" in metrics
        assert "r2" in metrics
