"""Pseudonymous protocol-deviation records for controlled research operations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Set

from ml.src.research.privacy import ensure_no_direct_identifiers


class ProtocolDeviationLogger:
    def __init__(self, existing_deviation_ids: Optional[Set[str]] = None):
        self._ids = set(existing_deviation_ids or set())
        self._counter = 0

    def record(
        self,
        participant_id: str,
        session_id: str,
        deviation_type: str,
        description: str,
        operator_id: str,
        resolution: str = "OPEN",
        impact: str = "UNDER_REVIEW",
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        ensure_no_direct_identifiers(
            {"description": description, "resolution": resolution, "impact": impact},
            "protocol deviation",
        )
        deviation_id = self._new_id()
        return {
            "deviation_id": deviation_id,
            "participant_id": participant_id,
            "session_id": session_id,
            "deviation_type": deviation_type,
            "description": description,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "operator_id": operator_id,
            "resolution": resolution,
            "impact": impact,
        }

    def _new_id(self) -> str:
        while True:
            self._counter += 1
            candidate = f"HV-DEV-{self._counter:06d}"
            if candidate not in self._ids:
                self._ids.add(candidate)
                return candidate
