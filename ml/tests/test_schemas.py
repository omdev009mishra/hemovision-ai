import json
import pathlib
import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError
from ml.src.data.validate_dataset import DatasetValidator, DatasetValidationError

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "dataset" / "schema"
SAMPLE_DIR = REPO_ROOT / "dataset" / "samples"

SCHEMAS = {
    "participant": {
        "filename": "participants.schema.json",
        "sample_filename": "participant.example.json",
        "expected_required": ["participant_id", "age_years", "sex", "pregnancy_status", "smoking_status"]
    },
    "session": {
        "filename": "sessions.schema.json",
        "sample_filename": "session.example.json",
        "expected_required": [
            "session_id", "participant_id", "session_timestamp", "operator_id",
            "capture_environment", "lighting_condition", "device_id", "consent_status"
        ]
    },
    "image": {
        "filename": "images.schema.json",
        "sample_filename": "image.example.json",
        "expected_required": [
            "image_id", "session_id", "participant_id", "eye_side", "frame_index",
            "image_path", "capture_timestamp", "phone_manufacturer", "phone_model",
            "camera_lens_type", "image_width", "image_height", "focus_score",
            "exposure_info", "image_quality_status", "annotation_status"
        ]
    },
    "lab": {
        "filename": "lab_measurements.schema.json",
        "sample_filename": "lab_measurement.example.json",
        "expected_required": [
            "lab_measurement_id", "participant_id", "measurement_timestamp",
            "laboratory_hb_g_dl", "measurement_method", "instrument_manufacturer",
            "instrument_model", "lab_quality_status"
        ]
    },
    "annotation": {
        "filename": "annotations.schema.json",
        "sample_filename": "annotation.example.json",
        "expected_required": [
            "annotation_id", "image_id", "annotator_id", "annotation_version",
            "conjunctiva_mask_path", "quality_label", "occlusion_label",
            "annotation_status", "review_status"
        ]
    }
}


def load_json_file(filepath: pathlib.Path) -> dict:
    """Helper to load and parse a JSON file."""
    assert filepath.exists(), f"File does not exist: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("schema_key", list(SCHEMAS.keys()))
def test_schema_validity_and_structure(schema_key):
    """Verify all 5 schema files exist, are valid JSON, and pass Draft202012Validator check_schema."""
    config = SCHEMAS[schema_key]
    schema_path = SCHEMA_DIR / config["filename"]
    schema = load_json_file(schema_path)

    # 1. Draft 2020-12 Schema Check
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as e:
        pytest.fail(f"Schema {config['filename']} is not a valid Draft 2020-12 schema: {e}")

    # 2. Structural Requirements
    assert "$schema" in schema, f"Missing '$schema' in {config['filename']}"
    assert "title" in schema, f"Missing 'title' in {config['filename']}"
    assert schema.get("type") == "object", f"Root type in {config['filename']} must be 'object'"
    assert "properties" in schema, f"Missing 'properties' in {config['filename']}"
    assert "required" in schema, f"Missing 'required' in {config['filename']}"

    # 3. Check expected required fields
    properties = schema["properties"]
    required = schema["required"]
    for expected_field in config["expected_required"]:
        assert expected_field in required, f"Field '{expected_field}' missing from required list in {config['filename']}"
        assert expected_field in properties, f"Required field '{expected_field}' not defined in properties of {config['filename']}"


@pytest.mark.parametrize("schema_key", list(SCHEMAS.keys()))
def test_valid_synthetic_fixtures(schema_key):
    """Verify synthetic fixtures validate successfully against Draft202012Validator."""
    config = SCHEMAS[schema_key]
    schema = load_json_file(SCHEMA_DIR / config["filename"])
    sample = load_json_file(SAMPLE_DIR / config["sample_filename"])

    validator = Draft202012Validator(schema)
    validator.validate(sample)


def test_referential_consistency_of_synthetic_samples():
    """Verify referential integrity and linkage across all synthetic samples."""
    validator = DatasetValidator(SCHEMA_DIR)

    participant = load_json_file(SAMPLE_DIR / SCHEMAS["participant"]["sample_filename"])
    session = load_json_file(SAMPLE_DIR / SCHEMAS["session"]["sample_filename"])
    image = load_json_file(SAMPLE_DIR / SCHEMAS["image"]["sample_filename"])
    lab = load_json_file(SAMPLE_DIR / SCHEMAS["lab"]["sample_filename"])
    annotation = load_json_file(SAMPLE_DIR / SCHEMAS["annotation"]["sample_filename"])

    # Document-level referential linkage checks
    assert session["participant_id"] == participant["participant_id"]
    assert image["participant_id"] == participant["participant_id"]
    assert image["session_id"] == session["session_id"]
    assert lab["participant_id"] == participant["participant_id"]
    assert annotation["image_id"] == image["image_id"]

    # Execute full DatasetValidator referential integrity check
    assert validator.validate_referential_integrity(
        participants=[participant],
        sessions=[session],
        images=[image],
        labs=[lab],
        annotations=[annotation]
    )


def test_participant_leakage_detection():
    """Verify DatasetValidator detects participant data leakage across splits."""
    validator = DatasetValidator(SCHEMA_DIR)

    train_pids = {"SYNTHETIC-P001", "SYNTHETIC-P002"}
    val_pids = {"SYNTHETIC-P003"}
    test_pids = {"SYNTHETIC-P004"}

    # Valid split -> No leakage
    assert validator.validate_participant_split_leakage(train_pids, val_pids, test_pids)

    # Invalid split -> Leakage between TRAIN and TEST
    leaky_test_pids = {"SYNTHETIC-P001", "SYNTHETIC-P004"}
    with pytest.raises(DatasetValidationError):
        validator.validate_participant_split_leakage(train_pids, val_pids, leaky_test_pids)
