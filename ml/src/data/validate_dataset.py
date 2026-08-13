"""HemoVision Dataset Validation Module.

Provides deterministic data quality, schema compliance, referential integrity,
and participant-level leakage checks for HemoVision dataset records.
"""

import datetime
import json
import pathlib
from typing import Dict, List, Set, Tuple, Any
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


class DatasetValidationError(Exception):
    """Raised when a dataset validation check fails."""
    pass


class DatasetValidator:
    """Validator for HemoVision dataset entities and data split contracts."""

    def __init__(self, schema_dir: pathlib.Path = None):
        if schema_dir is None:
            schema_dir = pathlib.Path(__file__).resolve().parents[3] / "dataset" / "schema"
        self.schema_dir = schema_dir
        self.schemas: Dict[str, dict] = {}
        self.validators: Dict[str, Draft202012Validator] = {}
        self._load_schemas()

    def _load_schemas(self):
        """Loads and compiles JSON Schemas."""
        schema_files = {
            "participant": "participants.schema.json",
            "session": "sessions.schema.json",
            "image": "images.schema.json",
            "lab": "lab_measurements.schema.json",
            "annotation": "annotations.schema.json",
            "label": "labels.schema.json"
        }
        for entity_name, filename in schema_files.items():
            path = self.schema_dir / filename
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    schema = json.load(f)
                    self.schemas[entity_name] = schema
                    self.validators[entity_name] = Draft202012Validator(schema)

    def validate_entity(self, entity_name: str, record: dict) -> bool:
        """Validates a single entity record against its JSON Schema."""
        if entity_name not in self.validators:
            raise DatasetValidationError(f"Unknown entity type: '{entity_name}'")
        try:
            self.validators[entity_name].validate(record)
            return True
        except ValidationError as e:
            raise DatasetValidationError(f"Schema validation failed for {entity_name}: {e.message}")

    def validate_timestamp_format(self, timestamp_str: str) -> bool:
        """Validates that a string is a valid ISO 8601 formatted timestamp."""
        try:
            if timestamp_str.endswith("Z"):
                timestamp_str = timestamp_str[:-1] + "+00:00"
            datetime.datetime.fromisoformat(timestamp_str)
            return True
        except Exception as e:
            raise DatasetValidationError(f"Invalid ISO 8601 timestamp string '{timestamp_str}': {e}")

    def validate_referential_integrity(
        self,
        participants: List[dict],
        sessions: List[dict],
        images: List[dict],
        labs: List[dict],
        annotations: List[dict]
    ) -> bool:
        """Verifies referential integrity across dataset entities."""
        # 1. Check duplicate participant IDs
        participant_ids: Set[str] = set()
        for p in participants:
            pid = p.get("participant_id")
            if not pid:
                raise DatasetValidationError("Participant record missing 'participant_id'")
            if pid in participant_ids:
                raise DatasetValidationError(f"Duplicate participant_id detected: '{pid}'")
            participant_ids.add(pid)

        # 2. Check sessions reference valid participant IDs
        session_ids: Set[str] = set()
        for s in sessions:
            sid = s.get("session_id")
            pid = s.get("participant_id")
            if sid in session_ids:
                raise DatasetValidationError(f"Duplicate session_id detected: '{sid}'")
            session_ids.add(sid)
            if pid not in participant_ids:
                raise DatasetValidationError(f"Session '{sid}' references unknown participant_id '{pid}'")

        # 3. Check images reference valid session_id and participant_id
        image_ids: Set[str] = set()
        for img in images:
            iid = img.get("image_id")
            sid = img.get("session_id")
            pid = img.get("participant_id")
            if iid in image_ids:
                raise DatasetValidationError(f"Duplicate image_id detected: '{iid}'")
            image_ids.add(iid)
            if sid not in session_ids:
                raise DatasetValidationError(f"Image '{iid}' references unknown session_id '{sid}'")
            if pid not in participant_ids:
                raise DatasetValidationError(f"Image '{iid}' references unknown participant_id '{pid}'")

        # 4. Check labs reference valid participant IDs
        for lab in labs:
            lid = lab.get("lab_measurement_id") or lab.get("image_id")
            pid = lab.get("participant_id")
            if pid not in participant_ids:
                raise DatasetValidationError(f"Lab measurement '{lid}' references unknown participant_id '{pid}'")

        # 5. Check annotations reference valid image IDs
        for ann in annotations:
            aid = ann.get("annotation_id")
            iid = ann.get("image_id")
            if iid not in image_ids:
                raise DatasetValidationError(f"Annotation '{aid}' references unknown image_id '{iid}'")

        return True

    def validate_participant_split_leakage(
        self,
        train_participant_ids: Set[str],
        val_participant_ids: Set[str],
        test_participant_ids: Set[str]
    ) -> bool:
        """Enforces zero participant overlap across TRAIN, VALIDATION, and TEST sets."""
        train_val_overlap = train_participant_ids.intersection(val_participant_ids)
        if train_val_overlap:
            raise DatasetValidationError(
                f"Participant data leakage detected between TRAIN and VALIDATION splits: {train_val_overlap}"
            )

        train_test_overlap = train_participant_ids.intersection(test_participant_ids)
        if train_test_overlap:
            raise DatasetValidationError(
                f"Participant data leakage detected between TRAIN and TEST splits: {train_test_overlap}"
            )

        val_test_overlap = val_participant_ids.intersection(test_participant_ids)
        if val_test_overlap:
            raise DatasetValidationError(
                f"Participant data leakage detected between VALIDATION and TEST splits: {val_test_overlap}"
            )

        return True
