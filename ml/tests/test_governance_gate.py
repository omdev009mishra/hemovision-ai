"""
Tests for GovernanceGate
"""

import pytest
import json
from pathlib import Path
from ml.src.data.governance_gate import GovernanceGate, GovernanceState


def test_governance_gate_synthetic_default(tmp_path):
    gate = GovernanceGate(str(tmp_path))
    res = gate.evaluate()
    assert res.state == GovernanceState.SYNTHETIC
    assert res.is_clinical_training_allowed is False


def test_governance_gate_unverified_clinical(tmp_path):
    gov_file = tmp_path / "dataset_governance.json"
    with open(gov_file, "w", encoding="utf-8") as f:
        json.dump({
            "dataset_type": "clinical",
            "governance_status": "unverified",
            "consent_verified": True,
            "ethics_approval_reference": "ETHICS_APPROVAL_REFERENCE_REQUIRED"
        }, f)

    gate = GovernanceGate(str(tmp_path))
    res = gate.evaluate()
    assert res.state == GovernanceState.UNVERIFIED_CLINICAL
    assert res.is_clinical_training_allowed is False


def test_governance_gate_governed_clinical(tmp_path):
    gov_file = tmp_path / "dataset_governance.json"
    with open(gov_file, "w", encoding="utf-8") as f:
        json.dump({
            "dataset_type": "clinical",
            "governance_status": "approved",
            "consent_verified": True,
            "ethics_approval_reference": "IRB-2026-HV-001",
            "deidentification_verified": True
        }, f)

    gate = GovernanceGate(str(tmp_path))
    res = gate.evaluate()
    assert res.state == GovernanceState.GOVERNED_CLINICAL
    assert res.is_clinical_training_allowed is True
