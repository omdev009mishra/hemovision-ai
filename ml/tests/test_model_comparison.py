"""
Tests for Baseline Models, Model Comparison, and Correlation Metrics
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


def test_regression_metrics_constant_y_true():
    y_true = np.array([12.5, 12.5, 12.5])
    y_pred = np.array([12.0, 13.0, 14.0])
    m = calculate_regression_metrics(y_true, y_pred)
    assert m["pearson_r"] is None
    assert m["spearman_rho"] is None


def test_regression_metrics_constant_y_pred():
    y_true = np.array([11.0, 13.0, 15.0])
    y_pred = np.array([13.0, 13.0, 13.0])
    m = calculate_regression_metrics(y_true, y_pred)
    assert m["pearson_r"] is None
    assert m["spearman_rho"] is None


def test_regression_metrics_one_sample_input():
    y_true = np.array([13.5])
    y_pred = np.array([13.2])
    m = calculate_regression_metrics(y_true, y_pred)
    assert m["mae"] == 0.3
    assert m["pearson_r"] is None
    assert m["spearman_rho"] is None


def test_regression_metrics_normal_non_constant():
    y_true = np.array([10.0, 12.0, 14.0, 16.0])
    y_pred = np.array([10.1, 12.1, 13.9, 16.0])
    m = calculate_regression_metrics(y_true, y_pred)
    assert m["pearson_r"] is not None
    assert m["spearman_rho"] is not None
    assert m["pearson_r"] > 0.95
