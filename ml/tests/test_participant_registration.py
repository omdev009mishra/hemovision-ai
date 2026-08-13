import pytest

from ml.src.research.participant_registration import ParticipantRegistrar
from ml.src.research.privacy import DirectIdentifierError
from ml.src.research.study_status import StudyStatus


def test_registration_is_blocked_while_approval_is_pending():
    result = ParticipantRegistrar().register("verified_active", {"age_band": "adult"})
    assert result.registration_for_real_collection == "BLOCKED"
    assert result.participant_record is None


def test_registration_is_blocked_when_consent_is_missing():
    result = ParticipantRegistrar().register(
        "pending", {"age_band": "adult"}, StudyStatus.APPROVED_FOR_COLLECTION
    )
    assert result.registration_for_real_collection == "BLOCKED"


def test_registration_creates_pseudonymous_id_without_direct_identifiers():
    result = ParticipantRegistrar().register(
        "verified_active", {"age_band": "adult"}, StudyStatus.APPROVED_FOR_COLLECTION
    )
    assert result.registration_for_real_collection == "CREATED"
    assert result.participant_record["participant_id"].startswith("HV-P-")
    assert "name" not in result.participant_record


def test_registration_rejects_direct_identifier_fields():
    with pytest.raises(DirectIdentifierError):
        ParticipantRegistrar().register(
            "verified_active",
            {"name": "Synthetic Test Name"},
            StudyStatus.APPROVED_FOR_COLLECTION,
        )
