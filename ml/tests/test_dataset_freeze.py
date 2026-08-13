import json

import pytest

from ml.src.research.dataset_freeze import (
    DatasetFreezeAuthorizationError,
    DatasetFreezeManager,
)


CONSENT = [{
    "consent_id": "HV-CNS-TEST0001",
    "participant_id": "HV-P-TEST001",
    "consent_status": "verified_active",
    "withdrawal_status": "active",
    "operator_id": "HV-OP-1",
}]


def _record(image_id, **overrides):
    record = {
        "image_id": image_id,
        "participant_id": "HV-P-TEST001",
        "session_id": "HV-SESSION-000001",
        "quality_status": "USABLE",
        "segmentation_status": "SUCCEEDED",
        "alignment_status": "aligned",
    }
    record.update(overrides)
    return record


def test_freeze_requires_authorized_workflow(tmp_path):
    manager = DatasetFreezeManager(str(tmp_path / "freeze"))
    with pytest.raises(DatasetFreezeAuthorizationError):
        manager.freeze([_record("IMG-1")], CONSENT, authorized=False)


def test_freeze_excludes_rejected_images_and_blocks_later_modification(tmp_path):
    report_dir = tmp_path / "freeze"
    manager = DatasetFreezeManager(str(report_dir))
    report = manager.freeze(
        [_record("IMG-1"), _record("IMG-2", quality_status="REJECTED")],
        CONSENT,
        authorized=True,
        splits={"train": {"HV-P-TEST001"}, "val": set(), "test": set()},
    )
    assert report["freeze_status"] == "FROZEN"
    assert report["research_ready_image_count"] == 1
    assert report["excluded_image_count"] == 1
    assert json.loads((report_dir / "freeze_report.json").read_text())["freeze_status"] == "FROZEN"
    with pytest.raises(DatasetFreezeAuthorizationError):
        manager.assert_modifiable()


def test_freeze_excludes_withdrawn_participants(tmp_path):
    withdrawn = [dict(CONSENT[0], consent_status="withdrawn", withdrawal_status="withdrawn")]
    report = DatasetFreezeManager(str(tmp_path / "freeze")).freeze(
        [_record("IMG-1")], withdrawn, authorized=True
    )
    assert report["research_ready_image_count"] == 0
    assert report["withdrawn_participant_count"] == 1
