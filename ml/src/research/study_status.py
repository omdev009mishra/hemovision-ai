"""Explicit study-state model. Approval is never inferred by software."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union


class StudyStatus(str, Enum):
    DRAFT = "DRAFT"
    PROTOCOL_READY = "PROTOCOL_READY"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    APPROVED_FOR_COLLECTION = "APPROVED_FOR_COLLECTION"
    PILOT_COLLECTION = "PILOT_COLLECTION"
    DATA_COLLECTION = "DATA_COLLECTION"
    DATA_FREEZE = "DATA_FREEZE"
    CLOSED = "CLOSED"


# Fresh checkouts are intentionally non-collecting. This value must only be
# changed by an authorized, institution-controlled study configuration process.
DEFAULT_STUDY_STATUS = StudyStatus.APPROVAL_PENDING


@dataclass(frozen=True)
class CollectionGateResult:
    registration_for_real_collection: str
    reason: str


def normalise_study_status(value: Union[StudyStatus, str]) -> StudyStatus:
    """Parse an explicit state without supplying a permissive fallback."""
    if isinstance(value, StudyStatus):
        return value
    return StudyStatus(str(value))


def collection_gate(value: Union[StudyStatus, str]) -> CollectionGateResult:
    """Allow real registration only in the explicit collection-ready state."""
    try:
        status = normalise_study_status(value)
    except ValueError:
        return CollectionGateResult("BLOCKED", "Unknown study status; collection is blocked.")

    if status is StudyStatus.APPROVED_FOR_COLLECTION:
        return CollectionGateResult("ALLOWED", "Explicit approval-for-collection state recorded.")
    return CollectionGateResult(
        "BLOCKED",
        f"Study status is {status.value}; real collection requires APPROVED_FOR_COLLECTION.",
    )


def can_collect_real_data(value: Union[StudyStatus, str]) -> bool:
    """Convenience predicate used by participant and session workflows."""
    return collection_gate(value).registration_for_real_collection == "ALLOWED"
