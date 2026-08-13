import json
import pathlib
import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "dataset" / "schema"
SAMPLE_DIR = REPO_ROOT / "dataset" / "samples"

SCHEMAS = {
    "participants": {
        "filename": "participants.schema.json",
        "sample_filename": "participant.example.json",
        "expected_required": ["participant_id", "age", "sex", "pregnancy_status", "smoking_status"]
    },
    "images": {
        "filename": "images.schema.json",
        "sample_filename": "image.example.json",
        "expected_required": [
            "image_id", "participant_id", "image_path", "eye_side",
            "phone_model", "capture_timestamp", "lighting_condition",
            "image_width", "image_height", "focus_score", "exposure_info", "annotation_status"
        ]
    },
    "labels": {
        "filename": "labels.schema.json",
        "sample_filename": "label.example.json",
        "expected_required": [
            "image_id", "participant_id", "laboratory_hb_g_dl",
            "measurement_timestamp", "measurement_method", "anemia_label", "label_source"
        ]
    }
}


def load_json_file(filepath: pathlib.Path) -> dict:
    """Helper to load and parse a JSON file."""
    assert filepath.exists(), f"File does not exist: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("schema_key", ["participants", "images", "labels"])
def test_schema_validity_and_structure(schema_key):
    """Verify schema files exist, are valid JSON, and pass Draft202012Validator check_schema."""
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


@pytest.mark.parametrize("schema_key", ["participants", "images", "labels"])
def test_valid_synthetic_fixtures(schema_key):
    """Verify synthetic fixtures validate successfully against Draft202012Validator."""
    config = SCHEMAS[schema_key]
    schema = load_json_file(SCHEMA_DIR / config["filename"])
    sample = load_json_file(SAMPLE_DIR / config["sample_filename"])

    validator = Draft202012Validator(schema)
    # validate() raises ValidationError if invalid
    validator.validate(sample)


def test_negative_participant_schema_validations():
    """Verify participant schema rejects missing fields, invalid types, and invalid enums."""
    schema = load_json_file(SCHEMA_DIR / SCHEMAS["participants"]["filename"])
    valid_sample = load_json_file(SAMPLE_DIR / SCHEMAS["participants"]["sample_filename"])
    validator = Draft202012Validator(schema)

    # 1. Missing participant_id
    sample_missing_id = valid_sample.copy()
    del sample_missing_id["participant_id"]
    with pytest.raises(ValidationError):
        validator.validate(sample_missing_id)

    # 2. Invalid age type (string instead of int)
    sample_invalid_age = valid_sample.copy()
    sample_invalid_age["age"] = "twenty-eight"
    with pytest.raises(ValidationError):
        validator.validate(sample_invalid_age)

    # 3. Invalid sex enum
    sample_invalid_sex = valid_sample.copy()
    sample_invalid_sex["sex"] = "unknown_category"
    with pytest.raises(ValidationError):
        validator.validate(sample_invalid_sex)


def test_negative_image_schema_validations():
    """Verify image schema rejects missing fields, invalid patterns, and invalid enums."""
    schema = load_json_file(SCHEMA_DIR / SCHEMAS["images"]["filename"])
    valid_sample = load_json_file(SAMPLE_DIR / SCHEMAS["images"]["sample_filename"])
    validator = Draft202012Validator(schema)

    # 1. Missing image_id
    sample_missing_id = valid_sample.copy()
    del sample_missing_id["image_id"]
    with pytest.raises(ValidationError):
        validator.validate(sample_missing_id)

    # 2. Invalid lighting_condition enum
    sample_invalid_light = valid_sample.copy()
    sample_invalid_light["lighting_condition"] = "disco_lights"
    with pytest.raises(ValidationError):
        validator.validate(sample_invalid_light)

    # 3. Invalid image_width type
    sample_invalid_width = valid_sample.copy()
    sample_invalid_width["image_width"] = -10
    with pytest.raises(ValidationError):
        validator.validate(sample_invalid_width)


def test_negative_label_schema_validations():
    """Verify label schema rejects missing laboratory_hb_g_dl, non-numeric Hb, and invalid anemia enums."""
    schema = load_json_file(SCHEMA_DIR / SCHEMAS["labels"]["filename"])
    valid_sample = load_json_file(SAMPLE_DIR / SCHEMAS["labels"]["sample_filename"])
    validator = Draft202012Validator(schema)

    # 1. Missing laboratory_hb_g_dl
    sample_missing_hb = valid_sample.copy()
    del sample_missing_hb["laboratory_hb_g_dl"]
    with pytest.raises(ValidationError):
        validator.validate(sample_missing_hb)

    # 2. Non-numeric laboratory_hb_g_dl
    sample_invalid_hb = valid_sample.copy()
    sample_invalid_hb["laboratory_hb_g_dl"] = "13.5_string"
    with pytest.raises(ValidationError):
        validator.validate(sample_invalid_hb)

    # 3. Invalid anemia_label enum
    sample_invalid_label = valid_sample.copy()
    sample_invalid_label["anemia_label"] = "definitely_anemic_guaranteed"
    with pytest.raises(ValidationError):
        validator.validate(sample_invalid_label)
