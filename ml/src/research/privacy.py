"""Small, shared privacy controls for research metadata."""

from __future__ import annotations

from typing import Any, Iterable, List


# Direct identifiers must remain in institution-controlled systems, never in the
# research dataset or its audit trail. Pseudonymous participant/session/operator
# identifiers are explicitly allowed and do not match these exact key fragments.
DIRECT_IDENTIFIER_KEY_FRAGMENTS = {
    "full_name",
    "first_name",
    "last_name",
    "patient_name",
    "name",
    "email",
    "phone",
    "mobile",
    "address",
    "postcode",
    "zip_code",
    "aadhaar",
    "national_id",
    "government_id",
    "medical_record_number",
    "mrn",
    "hospital_identifier",
    "hospital_id",
    "imei",
    "serial_number",
    "device_serial",
    "gps",
    "latitude",
    "longitude",
}


class DirectIdentifierError(ValueError):
    """Raised when a record attempts to contain a direct identifier."""


def find_direct_identifier_keys(value: Any, prefix: str = "") -> List[str]:
    """Return paths of prohibited identifier keys in a nested metadata object."""
    found: List[str] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key).lower().replace("-", "_").replace(" ", "_")
            path = f"{prefix}.{key}" if prefix else str(key)
            if key_text in DIRECT_IDENTIFIER_KEY_FRAGMENTS:
                found.append(path)
            found.extend(find_direct_identifier_keys(nested_value, path))
    elif isinstance(value, (list, tuple)):
        for index, nested_value in enumerate(value):
            found.extend(find_direct_identifier_keys(nested_value, f"{prefix}[{index}]"))
    return found


def ensure_no_direct_identifiers(value: Any, context: str = "research metadata") -> None:
    """Fail closed if a direct identifier is present in a record."""
    paths = find_direct_identifier_keys(value)
    if paths:
        raise DirectIdentifierError(
            f"Direct identifiers are not permitted in {context}: {', '.join(paths)}"
        )


def redact_to_allowed_keys(value: dict, allowed_keys: Iterable[str]) -> dict:
    """Keep a documented allow-list after validating the source contains no PII."""
    ensure_no_direct_identifiers(value)
    allowed = set(allowed_keys)
    return {key: value[key] for key in value if key in allowed}
