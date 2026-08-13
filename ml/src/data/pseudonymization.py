"""
HemoVision — Pseudonymization Engine & PII Validator
Generates research pseudonymous participant IDs and verifies absence of PII.
"""

from typing import Dict, Any, Tuple, List, Optional
import re
import hashlib


FORBIDDEN_PII_KEYS = {
    "name", "full_name", "first_name", "last_name", "patient_name",
    "phone", "mobile", "contact", "email",
    "aadhaar", "pan", "ssn", "national_id",
    "mrn", "hospital_reg_no", "patient_id_raw",
    "address", "street", "city", "zipcode", "postal_code",
    "gps", "latitude", "longitude", "exact_location"
}


class Pseudonymizer:
    """Generates pseudonymous research IDs and strips PII from data dictionaries."""

    @staticmethod
    def generate_participant_id(index: int, prefix: str = "HV-P") -> str:
        """Generates a standardized pseudonymous research participant ID (e.g. HV-P-000001)."""
        return f"{prefix}-{index:06d}"

    @staticmethod
    def hash_identifier(raw_id: str, salt: str = "HemoVisionSalt2026") -> str:
        """Deterministically hashes an institutional identifier into a pseudonymous research ID."""
        combined = f"{salt}:{raw_id}".encode("utf-8")
        h = hashlib.sha256(combined).hexdigest()[:10].upper()
        return f"HV-P-{h}"

    @staticmethod
    def scan_for_pii(data: Dict[str, Any]) -> List[str]:
        """Scans dictionary keys and string values for potential PII or forbidden fields."""
        detected = []
        for k, v in data.items():
            k_lower = str(k).lower()
            if k_lower in FORBIDDEN_PII_KEYS:
                detected.append(f"Forbidden PII key discovered: '{k}'")

            if isinstance(v, str):
                # Email regex check
                if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", v):
                    detected.append(f"Potential email address detected in key '{k}'")
                # Phone number check (10 digits)
                if re.search(r"\b\d{10}\b", v) and "id" not in k_lower and "timestamp" not in k_lower:
                    detected.append(f"Potential phone number detected in key '{k}'")
        return detected

    @staticmethod
    def sanitize_participant_record(raw_record: Dict[str, Any], participant_index: int) -> Dict[str, Any]:
        """Strips PII and returns a research-compliant pseudonymous participant record."""
        pid = raw_record.get("participant_id")
        if not pid or "HV-P-" not in str(pid):
            pid = Pseudonymizer.generate_participant_id(participant_index)

        # Allow minimum research variables only
        allowed = {
            "participant_id": pid,
            "age_years": raw_record.get("age_years"),
            "biological_sex": raw_record.get("biological_sex"),
            "pregnancy_status": raw_record.get("pregnancy_status"),
            "smoking_status": raw_record.get("smoking_status"),
            "residence_altitude_m": raw_record.get("residence_altitude_m"),
            "skin_phototype": raw_record.get("skin_phototype"),
            "ocular_conditions": raw_record.get("ocular_conditions", []),
            "enrollment_timestamp": raw_record.get("enrollment_timestamp"),
        }

        # Remove None values
        return {k: v for k, v in allowed.items() if v is not None}
