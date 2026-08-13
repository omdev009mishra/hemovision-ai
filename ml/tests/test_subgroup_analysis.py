"""
Tests for Subgroup Performance Analyzer
"""

import pytest
import pandas as pd
import numpy as np
from ml.src.evaluation.subgroup_analysis import SubgroupAnalyzer


def test_subgroup_analysis():
    analyzer = SubgroupAnalyzer(is_synthetic_smoke_test=True)
    df = pd.DataFrame({
        "target": np.array([12.0, 13.0, 14.0, 15.0]),
        "pred": np.array([12.1, 13.2, 13.9, 14.8]),
        "camera_lens_direction": ["front", "front", "back", "back"],
        "phone_manufacturer": ["Google", "Google", "Samsung", "Samsung"]
    })

    res = analyzer.evaluate_subgroups(df, "target", "pred", ["camera_lens_direction", "phone_manufacturer"])
    assert len(res) == 4
    csv_p = analyzer.save_csv(res, "research/test_reports/subgroup.csv")
    assert pd.read_csv(csv_p) is not None
