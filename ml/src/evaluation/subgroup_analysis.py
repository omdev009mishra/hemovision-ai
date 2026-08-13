"""
HemoVision Subgroup Performance Evaluator
Evaluates performance metrics across camera lens direction, manufacturer, lighting condition, etc.
"""

from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import numpy as np

from ml.src.evaluation.regression_metrics import calculate_regression_metrics


class SubgroupAnalyzer:

    def __init__(self, is_synthetic_smoke_test: bool = False):
        self.is_synthetic_smoke_test = is_synthetic_smoke_test

    def evaluate_subgroups(
        self,
        df: pd.DataFrame,
        target_col: str,
        pred_col: str,
        subgroup_cols: List[str]
    ) -> pd.DataFrame:
        results = []

        for col in subgroup_cols:
            if col not in df.columns:
                continue
            for val, group in df.groupby(col):
                if len(group) == 0:
                    continue
                y_true = group[target_col].values
                y_pred = group[pred_col].values
                metrics = calculate_regression_metrics(y_true, y_pred)
                
                results.append({
                    "subgroup_dimension": col,
                    "subgroup_value": str(val),
                    "sample_size": len(group),
                    "mae": metrics["mae"],
                    "rmse": metrics["rmse"],
                    "r2": metrics["r2"],
                    "pearson_r": metrics["pearson_r"],
                    "spearman_rho": metrics["spearman_rho"],
                    "is_synthetic_smoke_test": self.is_synthetic_smoke_test
                })

        res_df = pd.DataFrame(results)
        return res_df

    def save_csv(self, df: pd.DataFrame, output_path: str) -> str:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out, index=False)
        return str(out)
