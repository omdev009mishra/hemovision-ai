"""Capture-session creation with consent, status, and privacy safeguards."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Set, Union

from ml.src.research.participant_registration import ACTIVE_CONSENT_STATUSES
from ml.src.research.privacy import ensure_no_direct_identifiers
from ml.src.research.study_status import DEFAULT_STUDY_STATUS, StudyStatus, collection_gate


class SessionCreationBlockedError(PermissionError):
    """Raised if a session would start without explicit collection authorization."""


class SessionManager:
    """Issues non-reusable ``HV-SESSION-######`` identifiers within a registry."""

    def __init__(self, existing_session_ids: Optional[Set[str]] = None):
        self._session_ids: Set[str] = set(existing_session_ids or set())
        self._counter = self._initial_counter()

    def _initial_counter(self) -> int:
        serials = []
        for session_id in self._session_ids:
            if session_id.startswith("HV-SESSION-"):
                try:
                    serials.append(int(session_id.rsplit("-", 1)[1]))
                except ValueError:
                    continue
        return max(serials, default=0)

    def generate_session_id(self) -> str:
        while True:
            self._counter += 1
            candidate = f"HV-SESSION-{self._counter:06d}"
            if candidate not in self._session_ids:
                self._session_ids.add(candidate)
                return candidate

    def create_session(
        self,
        participant_id: str,
        consent_status: str,
        operator_id: str,
        device_metadata: Dict[str, Any],
        capture_environment: Union[str, Dict[str, Any]],
        timestamp: Optional[str] = None,
        *,
        study_status: Union[StudyStatus, str] = DEFAULT_STUDY_STATUS,
        synthetic: bool = False,
    ) -> Dict[str, Any]:
        """Create a metadata-only capture session; images are never stored here."""
        if str(consent_status).lower() not in ACTIVE_CONSENT_STATUSES:
            raise SessionCreationBlockedError("Active verified consent is required before session creation.")
        if not synthetic:
            gate = collection_gate(study_status)
            if gate.registration_for_real_collection != "ALLOWED":
                raise SessionCreationBlockedError(gate.reason)

        ensure_no_direct_identifiers(device_metadata, "device metadata")
        if isinstance(capture_environment, dict):
            ensure_no_direct_identifiers(capture_environment, "capture environment")
            environment_name = str(capture_environment.get("setting", "unknown"))
            environment_metadata = dict(capture_environment)
        else:
            environment_name = str(capture_environment)
            environment_metadata = {"setting": environment_name}

        session_timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        research_device_id = str(device_metadata.get("study_device_id", "HV-DEVICE-UNASSIGNED"))
        safe_device_metadata = {
            key: value
            for key, value in device_metadata.items()
            if key in {
                "study_device_id", "manufacturer", "model", "operating_system",
                "app_version", "camera_direction", "camera_lens_type", "image_width",
                "image_height", "flash_policy", "exposure_policy",
            }
        }
        return {
            "session_id": self.generate_session_id(),
            "participant_id": participant_id,
            "session_timestamp": session_timestamp,
            "operator_id": operator_id,
            "capture_environment": environment_name,
            "capture_environment_metadata": environment_metadata,
            "lighting_condition": str(environment_metadata.get("lighting_condition", "unknown")),
            "ambient_lux": environment_metadata.get("ambient_lux"),
            "device_id": research_device_id,
            "device_metadata": safe_device_metadata,
            "consent_status": "verified_active",
        }
