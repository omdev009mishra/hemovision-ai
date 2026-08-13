"""
HemoVision Participant-Grouped Cross-Validation
Implements GroupKFold cross-validation grouped by participant_id to avoid data leakage across folds.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
from sklearn.model_selection import GroupKFold

from ml.src.evaluation.regression_metrics import calculate_regression_metrics
from ml.src.models.baseline_models import BaselineModelFactory


class GroupCrossValidator:

    def __init__(self, n_splits: int = 5, random_seed: int = 42):
        self.n_splits = n_splits
        self.random_seed = random_seed

    def evaluate_model(
        self,
        model_type: str,
        X: np.ndarray,
        y: np.ndarray,
        groups: np.ndarray
    ) -> Dict[str, Any]:
        unique_groups = np.unique(groups)
        actual_splits = min(self.n_splits, len(unique_groups))

        if actual_splits < 2:
            # Not enough groups for KFold, return single fit metrics
            model = BaselineModelFactory.create_model(model_type, self.random_seed)
            model.fit(X, y)
            preds = model.predict(X)
            metrics = calculate_regression_metrics(y, preds)
            return {
                "model_type": model_type,
                "cv_folds": 1,
                "mean_mae": metrics["mae"],
                "std_mae": 0.0,
                "mean_rmse": metrics["rmse"],
                "std_rmse": 0.0,
                "mean_r2": metrics["r2"],
                "std_r2": 0.0,
            }

        gkf = GroupKFold(n_splits=actual_splits)
        fold_maes, fold_rmses, fold_r2s = [], [], []

        for train_idx, val_idx in gkf.split(X, y, groups):
            X_tr, y_tr = X[train_idx], y[train_idx]
            X_va, y_va = X[val_idx], y[val_idx]

            model = BaselineModelFactory.create_model(model_type, self.random_seed)
            model.fit(X_tr, y_tr)
            preds = model.predict(X_va)
            m = calculate_regression_metrics(y_va, preds)

            fold_maes.append(m["mae"])
            fold_rmses.append(m["rmse"])
            fold_r2s.append(m["r2"])

        return {
            "model_type": model_type,
            "cv_folds": actual_splits,
            "mean_mae": round(float(np.mean(fold_maes)), 4),
            "std_mae": round(float(np.std(fold_maes)), 4),
            "mean_rmse": round(float(np.mean(fold_rmses)), 4),
            "std_rmse": round(float(np.std(fold_rmses)), 4),
            "mean_r2": round(float(np.mean(fold_r2s)), 4),
            "std_r2": round(float(np.std(fold_r2s)), 4),
        }
