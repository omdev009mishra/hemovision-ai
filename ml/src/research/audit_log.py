"""Pseudonymous audit events. Direct identifiers are rejected before logging."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ml.src.research.privacy import ensure_no_direct_identifiers


class AuditLogger:
    """An in-memory audit logger suitable for an institution-controlled sink."""

    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = []
        self._counter = 0

    @property
    def events(self) -> List[Dict[str, Any]]:
        return list(self._events)

    def record(
        self,
        operator_id: str,
        event_type: str,
        action: str,
        result: str,
        participant_id: Optional[str] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ensure_no_direct_identifiers(details or {}, "audit event details")
        self._counter += 1
        event = {
            "event_id": f"HV-AUDIT-{self._counter:06d}",
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "operator_id": operator_id,
            "event_type": event_type,
            "participant_id": participant_id,
            "session_id": session_id,
            "action": action,
            "result": result,
        }
        if details:
            event["details"] = dict(details)
        self._events.append(event)
        return dict(event)
