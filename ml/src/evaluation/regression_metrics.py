"""
HemoVision Regression Metrics Evaluator
Calculates MAE, RMSE, R², Pearson r, and Spearman rho correlation metrics.
"""

from typing import Dict
import numpy as np
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    if len(y_true) == 0:
        return {
            "mae": 0.0,
            "rmse": 0.0,
            "r2": 0.0,
            "pearson_r": 0.0,
            "spearman_rho": 0.0,
        }

    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    
    if len(y_true) > 1 and np.var(y_true) > 1e-8:
        r2 = float(r2_score(y_true, y_pred))
        pearson_r, _ = stats.pearsonr(y_true, y_pred)
        spearman_rho, _ = stats.spearmanr(y_true, y_pred)
    else:
        r2 = 0.0
        pearson_r = 0.0
        spearman_rho = 0.0

    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(float(r2), 4),
        "pearson_r": round(float(pearson_r) if not np.isnan(pearson_r) else 0.0, 4),
        "spearman_rho": round(float(spearman_rho) if not np.isnan(spearman_rho) else 0.0, 4),
    }
