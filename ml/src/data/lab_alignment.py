"""
HemoVision — Image to Laboratory Ground Truth Alignment Module
Aligns image capture timestamps with reference lab Hb measurements within configurable protocol windows.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class AlignmentResult:
    is_aligned: bool
    selected_lab_measurement_id: Optional[str]
    time_delta_minutes: Optional[float]
    alignment_status: str  # "aligned", "outside_protocol", "no_lab_measurement"
    laboratory_hb_g_dl: Optional[float]


class LabAligner:
    """Aligns image capture timestamps with laboratory Hb reference measurements."""

    def __init__(self, maximum_delta_minutes: Optional[float] = 120.0):
        self.maximum_delta_minutes = maximum_delta_minutes

    def align(self, capture_timestamp_iso: str, lab_measurements: List[Dict[str, Any]]) -> AlignmentResult:
        if not lab_measurements:
            return AlignmentResult(
                is_aligned=False,
                selected_lab_measurement_id=None,
                time_delta_minutes=None,
                alignment_status="no_lab_measurement",
                laboratory_hb_g_dl=None
            )

        try:
            capture_dt = datetime.fromisoformat(capture_timestamp_iso.replace("Z", "+00:00"))
        except Exception:
            return AlignmentResult(
                is_aligned=False,
                selected_lab_measurement_id=None,
                time_delta_minutes=None,
                alignment_status="invalid_capture_timestamp",
                laboratory_hb_g_dl=None
            )

        candidates = []
        for lab in lab_measurements:
            ts_str = lab.get("measurement_timestamp")
            if not ts_str:
                continue
            try:
                lab_dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                delta_mins = abs((capture_dt - lab_dt).total_seconds()) / 60.0
                hb_val = lab.get("hemoglobin_g_dl") or lab.get("laboratory_hb_g_dl")
                if hb_val is not None:
                    candidates.append((delta_mins, lab.get("lab_measurement_id", "UNKNOWN"), float(hb_val)))
            except Exception:
                continue

        if not candidates:
            return AlignmentResult(
                is_aligned=False,
                selected_lab_measurement_id=None,
                time_delta_minutes=None,
                alignment_status="no_valid_lab_timestamp",
                laboratory_hb_g_dl=None
            )

        # Select candidate with minimum time delta
        candidates.sort(key=lambda x: x[0])
        best_delta, best_lab_id, best_hb = candidates[0]

        if self.maximum_delta_minutes is not None and best_delta > self.maximum_delta_minutes:
            return AlignmentResult(
                is_aligned=False,
                selected_lab_measurement_id=best_lab_id,
                time_delta_minutes=round(best_delta, 2),
                alignment_status="outside_protocol",
                laboratory_hb_g_dl=best_hb
            )

        return AlignmentResult(
            is_aligned=True,
            selected_lab_measurement_id=best_lab_id,
            time_delta_minutes=round(best_delta, 2),
            alignment_status="aligned",
            laboratory_hb_g_dl=best_hb
        )
