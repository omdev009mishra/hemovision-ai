import json
from pathlib import Path

from jsonschema import Draft202012Validator

from ml.src.research.protocol_deviation import ProtocolDeviationLogger


def test_protocol_deviation_is_pseudonymous_and_schema_valid():
    record = ProtocolDeviationLogger().record(
        "HV-P-TEST001",
        "HV-SESSION-000001",
        "incorrect_lighting",
        "Lighting record was incomplete.",
        "HV-OP-1",
    )
    schema_path = Path("dataset/schema/protocol_deviation.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(record)
    assert record["deviation_id"] == "HV-DEV-000001"
    assert "name" not in record
