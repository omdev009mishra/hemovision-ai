import pytest

from ml.src.research.session_manager import SessionCreationBlockedError, SessionManager
from ml.src.research.study_status import StudyStatus


DEVICE = {
    "study_device_id": "HV-DEVICE-001",
    "manufacturer": "TestPhone",
    "model": "SyntheticModel",
    "camera_direction": "rear",
}


def test_session_is_blocked_before_collection_approval():
    with pytest.raises(SessionCreationBlockedError):
        SessionManager().create_session(
            "HV-P-TEST001", "verified_active", "HV-OP-1", DEVICE, "clinical_room"
        )


def test_sessions_are_unique_and_linked_to_pseudonymous_participant():
    manager = SessionManager()
    first = manager.create_session(
        "HV-P-TEST001",
        "verified_active",
        "HV-OP-1",
        DEVICE,
        {"setting": "clinical_room", "ambient_lux": 250},
        "2026-01-01T00:00:00+00:00",
        study_status=StudyStatus.APPROVED_FOR_COLLECTION,
    )
    second = manager.create_session(
        "HV-P-TEST001",
        "verified_active",
        "HV-OP-1",
        DEVICE,
        "clinical_room",
        study_status=StudyStatus.APPROVED_FOR_COLLECTION,
    )
    assert first["session_id"] == "HV-SESSION-000001"
    assert second["session_id"] == "HV-SESSION-000002"
    assert first["participant_id"] == "HV-P-TEST001"
    assert "serial_number" not in first["device_metadata"]
