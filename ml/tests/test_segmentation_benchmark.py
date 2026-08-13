"""
Tests for Segmentation Benchmark Runner
"""

import pytest
import os
from pathlib import Path
from ml.src.segmentation.benchmark import run_benchmark


def test_segmentation_benchmark_execution():
    out_dir = "research/test_reports/segmentation_bench"
    run_benchmark("dataset/samples/segmentation", out_dir)

    assert Path(os.path.join(out_dir, "segmentation_metrics.csv")).exists()
    assert Path(os.path.join(out_dir, "benchmark_summary.json")).exists()
    assert Path(os.path.join(out_dir, "benchmark_report.md")).exists()

    with open(os.path.join(out_dir, "benchmark_report.md"), "r", encoding="utf-8") as f:
        content = f.read()
        assert "SYNTHETIC" in content
        assert "NOT PERFORMED" in content
