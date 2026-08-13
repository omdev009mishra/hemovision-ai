import json
import pathlib
import pytest

SCHEMA_DIR = pathlib.Path(__file__).resolve().parents[2] / "dataset" / "schema"

@pytest.mark.parametrize("schema_filename", [
    "participants.schema.json",
    "images.schema.json",
    "labels.schema.json"
])
def test_json_schemas_exist_and_are_valid_json(schema_filename):
    schema_path = SCHEMA_DIR / schema_filename
    assert schema_path.exists(), f"Schema file {schema_filename} does not exist at {schema_path}"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "$schema" in data, f"Schema {schema_filename} missing '$schema' key"
    assert "title" in data, f"Schema {schema_filename} missing 'title' key"
    assert data["type"] == "object", f"Schema {schema_filename} root type must be object"
    assert "properties" in data, f"Schema {schema_filename} missing 'properties'"


def test_participant_schema_fields():
    schema_path = SCHEMA_DIR / "participants.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    props = data["properties"]
    required_fields = ["participant_id", "age", "sex", "pregnancy_status", "smoking_status"]
    for field in required_fields:
        assert field in props, f"Missing field '{field}' in participant schema"
        assert field in data["required"], f"Field '{field}' must be in 'required' list"


def test_images_schema_fields():
    schema_path = SCHEMA_DIR / "images.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    props = data["properties"]
    required_fields = [
        "image_id", "participant_id", "image_path", "eye_side",
        "phone_model", "capture_timestamp", "lighting_condition",
        "image_width", "image_height", "focus_score", "exposure_info", "annotation_status"
    ]
    for field in required_fields:
        assert field in props, f"Missing field '{field}' in images schema"
        assert field in data["required"], f"Field '{field}' must be in 'required' list"


def test_labels_schema_fields():
    schema_path = SCHEMA_DIR / "labels.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    props = data["properties"]
    required_fields = [
        "image_id", "participant_id", "laboratory_hb_g_dl",
        "measurement_timestamp", "measurement_method", "anemia_label", "label_source"
    ]
    for field in required_fields:
        assert field in props, f"Missing field '{field}' in labels schema"
        assert field in data["required"], f"Field '{field}' must be in 'required' list"
