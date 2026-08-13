"""
HemoVision Baseline Regression Models
Implements Mean Predictor, Linear Regression, Ridge, Random Forest, and Gradient Boosting regressors.
"""

import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


class BaselineModelFactory:

    @staticmethod
    def create_model(model_type: str, random_seed: int = 42):
        name = model_type.lower()

        if name in ["mean", "dummy", "mean_predictor"]:
            return DummyRegressor(strategy="mean")
        elif name in ["linear", "linear_regression"]:
            return LinearRegression()
        elif name in ["ridge", "ridge_regression"]:
            return Ridge(alpha=1.0, random_state=random_seed)
        elif name in ["rf", "random_forest"]:
            return RandomForestRegressor(n_estimators=50, random_state=random_seed)
        elif name in ["gb", "gradient_boosting"]:
            return GradientBoostingRegressor(n_estimators=50, random_state=random_seed)
        else:
            raise ValueError(f"Unknown baseline model type: {model_type}")
