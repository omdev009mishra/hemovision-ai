"""
HemoVision Regression Metrics Evaluator
Calculates MAE, RMSE, R², Pearson r, and Spearman rho correlation metrics.
Returns None (JSON null) for correlation when sample size is insufficient or variance is constant.
"""

from typing import Dict, Optional, Any
import numpy as np
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    if len(y_true) == 0:
        return {
            "mae": 0.0,
            "rmse": 0.0,
            "r2": 0.0,
            "pearson_r": None,
            "spearman_rho": None,
        }

    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))

    # Check if correlations are valid (N >= 2, non-constant y_true, non-constant y_pred)
    is_valid_corr = (
        len(y_true) >= 2
        and float(np.var(y_true)) > 1e-8
        and float(np.var(y_pred)) > 1e-8
    )

    if is_valid_corr:
        r2 = float(r2_score(y_true, y_pred))
        pr, _ = stats.pearsonr(y_true, y_pred)
        sr, _ = stats.spearmanr(y_true, y_pred)
        pearson_r = round(float(pr), 4) if not np.isnan(pr) else None
        spearman_rho = round(float(sr), 4) if not np.isnan(sr) else None
    else:
        r2 = 0.0
        pearson_r = None
        spearman_rho = None

    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
        "pearson_r": pearson_r,
        "spearman_rho": spearman_rho,
    }
