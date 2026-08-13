"""Pseudonymous participant registration for approved research collection."""

from __future__ import annotations

from dataclasses import dataclass
import secrets
from typing import Any, Dict, Optional, Set, Union

from ml.src.research.privacy import ensure_no_direct_identifiers
from ml.src.research.study_status import (
    DEFAULT_STUDY_STATUS,
    StudyStatus,
    collection_gate,
)


ACTIVE_CONSENT_STATUSES = {"given", "verified_active"}


class RegistrationBlockedError(PermissionError):
    """Raised when a real registration is not authorized by the explicit gate."""


@dataclass(frozen=True)
class ParticipantRegistrationResult:
    registration_for_real_collection: str
    participant_record: Optional[Dict[str, Any]]
    reason: str


class ParticipantRegistrar:
    """Creates local pseudonymous records and never accepts direct identifiers."""

    def __init__(self, existing_participant_ids: Optional[Set[str]] = None):
        self._participant_ids: Set[str] = set(existing_participant_ids or set())

    def generate_participant_id(self, synthetic: bool = False) -> str:
        prefix = "SYNTHETIC-P" if synthetic else "HV-P-"
        while True:
            candidate = f"{prefix}{secrets.token_hex(6).upper()}"
            if candidate not in self._participant_ids:
                self._participant_ids.add(candidate)
                return candidate

    def register(
        self,
        consent_status: str,
        approved_variables: Optional[Dict[str, Any]] = None,
        study_status: Union[StudyStatus, str] = DEFAULT_STUDY_STATUS,
        *,
        synthetic: bool = False,
    ) -> ParticipantRegistrationResult:
        """Verify the gate and consent before creating a pseudonymous record.

        ``approved_variables`` must be an approved protocol allow-list chosen by
        the caller. Direct identifiers are rejected rather than redacted so an
        operator can correct the source workflow.
        """
        variables = dict(approved_variables or {})
        ensure_no_direct_identifiers(variables, "participant registration")

        if str(consent_status).lower() not in ACTIVE_CONSENT_STATUSES:
            return ParticipantRegistrationResult(
                "BLOCKED", None, "Consent is absent, pending, or withdrawn; registration is blocked."
            )

        gate = collection_gate(study_status)
        if not synthetic and gate.registration_for_real_collection != "ALLOWED":
            return ParticipantRegistrationResult("BLOCKED", None, gate.reason)

        participant_id = self.generate_participant_id(synthetic=synthetic)
        record: Dict[str, Any] = {
            "participant_id": participant_id,
            "consent_status": "verified_active",
            "record_type": "synthetic_test" if synthetic else "research_participant",
        }
        record.update(variables)
        return ParticipantRegistrationResult("CREATED", record, "Pseudonymous participant record created.")

    def register_or_raise(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Return a record or raise a clear error for imperative callers."""
        result = self.register(*args, **kwargs)
        if result.registration_for_real_collection != "CREATED" or result.participant_record is None:
            raise RegistrationBlockedError(result.reason)
        return result.participant_record
