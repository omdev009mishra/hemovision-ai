"""
HemoVision — Participant Withdrawal Handling Engine
Manages participant withdrawal status and enforces exclusion from ML datasets.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Set, Tuple


class WithdrawalManager:
    """Manages participant withdrawal exclusions while preserving audit metadata."""

    @staticmethod
    def filter_active_records(records: List[Any], consent_records: List[Dict[str, Any]]) -> Tuple[List[Any], List[Any], Set[str]]:
        """
        Filters out withdrawn participants.

        Returns:
            Tuple of (active_records, withdrawn_records, withdrawn_participant_ids)
        """
        withdrawn_pts: Set[str] = set()
        for c in consent_records:
            if c.get("withdrawal_status") == "withdrawn" or c.get("consent_status") == "withdrawn":
                pid = c.get("participant_id")
                if pid:
                    withdrawn_pts.add(pid)

        active = []
        withdrawn = []

        for r in records:
            pid = getattr(r, "participant_id", r.get("participant_id") if isinstance(r, dict) else None)
            if pid in withdrawn_pts:
                withdrawn.append(r)
            else:
                active.append(r)

        return active, withdrawn, withdrawn_pts
