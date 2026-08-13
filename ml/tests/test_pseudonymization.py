"""
Tests for Pseudonymizer and PII Scanner
"""

import pytest
from ml.src.data.pseudonymization import Pseudonymizer


def test_pseudonymizer_id_generation():
    pid = Pseudonymizer.generate_participant_id(1)
    assert pid == "HV-P-000001"

    hashed_id = Pseudonymizer.hash_identifier("MRN-998877")
    assert hashed_id.startswith("HV-P-")


def test_pii_scanner_detects_forbidden_fields():
    data_clean = {"participant_id": "HV-P-000001", "age_years": 45}
    assert len(Pseudonymizer.scan_for_pii(data_clean)) == 0

    data_pii = {
        "participant_id": "HV-P-000001",
        "name": "John Doe",
        "email": "patient@hospital.com",
        "phone": "9876543210"
    }
    issues = Pseudonymizer.scan_for_pii(data_pii)
    assert len(issues) >= 3
