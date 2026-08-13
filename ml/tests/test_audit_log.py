import pytest

from ml.src.research.audit_log import AuditLogger
from ml.src.research.privacy import DirectIdentifierError


def test_audit_event_contains_only_pseudonymous_linkage_fields():
    event = AuditLogger().record(
        operator_id="HV-OP-1",
        event_type="SESSION_CREATED",
        action="create_session",
        result="SUCCESS",
        participant_id="HV-P-TEST001",
        session_id="HV-SESSION-000001",
    )
    assert event["event_id"] == "HV-AUDIT-000001"
    assert event["participant_id"] == "HV-P-TEST001"
    assert "email" not in event


def test_audit_log_rejects_pii_in_details():
    with pytest.raises(DirectIdentifierError):
        AuditLogger().record(
            "HV-OP-1", "TEST", "test", "SUCCESS", details={"email": "synthetic@example.invalid"}
        )
