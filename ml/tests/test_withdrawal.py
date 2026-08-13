"""
Tests for WithdrawalManager
"""

import pytest
from ml.src.data.withdrawal import WithdrawalManager


def test_withdrawal_filtering():
    records = [
        {"participant_id": "HV-P-000001", "image_id": "IMG-01"},
        {"participant_id": "HV-P-000002", "image_id": "IMG-02"},
    ]
    consents = [
        {"participant_id": "HV-P-000001", "consent_status": "given", "withdrawal_status": "active"},
        {"participant_id": "HV-P-000002", "consent_status": "withdrawn", "withdrawal_status": "withdrawn"},
    ]

    active, withdrawn, withdrawn_ids = WithdrawalManager.filter_active_records(records, consents)
    assert len(active) == 1
    assert len(withdrawn) == 1
    assert "HV-P-000002" in withdrawn_ids
