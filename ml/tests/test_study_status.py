from ml.src.research.study_status import (
    DEFAULT_STUDY_STATUS,
    StudyStatus,
    collection_gate,
)


def test_default_study_status_is_approval_pending():
    assert DEFAULT_STUDY_STATUS is StudyStatus.APPROVAL_PENDING
    assert collection_gate(DEFAULT_STUDY_STATUS).registration_for_real_collection == "BLOCKED"


def test_collection_requires_explicit_approval_for_collection_state():
    assert collection_gate(StudyStatus.PROTOCOL_READY).registration_for_real_collection == "BLOCKED"
    assert collection_gate(StudyStatus.APPROVED_FOR_COLLECTION).registration_for_real_collection == "ALLOWED"


def test_unknown_study_status_fails_closed():
    assert collection_gate("APPROVED_SOMEHOW").registration_for_real_collection == "BLOCKED"
