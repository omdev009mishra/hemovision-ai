"""
Tests for LabAligner
"""

import pytest
from ml.src.data.lab_alignment import LabAligner


def test_lab_aligner_within_window():
    aligner = LabAligner(maximum_delta_minutes=60.0)
    capture_ts = "2026-01-01T12:00:00Z"
    labs = [
        {"lab_measurement_id": "LAB-001", "measurement_timestamp": "2026-01-01T12:20:00Z", "laboratory_hb_g_dl": 13.5},
        {"lab_measurement_id": "LAB-002", "measurement_timestamp": "2026-01-01T15:00:00Z", "laboratory_hb_g_dl": 14.0},
    ]

    res = aligner.align(capture_ts, labs)
    assert res.is_aligned is True
    assert res.selected_lab_measurement_id == "LAB-001"
    assert res.time_delta_minutes == 20.0
    assert res.laboratory_hb_g_dl == 13.5


def test_lab_aligner_outside_window():
    aligner = LabAligner(maximum_delta_minutes=30.0)
    capture_ts = "2026-01-01T12:00:00Z"
    labs = [
        {"lab_measurement_id": "LAB-001", "measurement_timestamp": "2026-01-01T14:00:00Z", "laboratory_hb_g_dl": 13.5},
    ]

    res = aligner.align(capture_ts, labs)
    assert res.is_aligned is False
    assert res.alignment_status == "outside_protocol"
