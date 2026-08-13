"""
Tests for EXIFSanitizer
"""

import pytest
from ml.src.data.exif_sanitizer import EXIFSanitizer


def test_exif_sanitizer_removes_gps_and_serials():
    raw_meta = {
        "Make": "Motorola",
        "Model": "edge 70",
        "GPSLatitude": "12.9716 N",
        "GPSLongitude": "77.5946 E",
        "DeviceSerialNumber": "SN-99887766",
        "ExposureTime": "0.01"
    }

    sanitized, had_forbidden = EXIFSanitizer.sanitize_metadata(raw_meta)
    assert had_forbidden is True
    assert "GPSLatitude" not in sanitized
    assert "DeviceSerialNumber" not in sanitized
    assert sanitized["Make"] == "Motorola"
    assert sanitized["Model"] == "edge 70"
