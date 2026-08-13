import subprocess

from ml.src.research.privacy import find_direct_identifier_keys


def test_clinical_data_directory_is_gitignored():
    result = subprocess.run(
        ["git", "check-ignore", "dataset/clinical/participant-image.png"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0


def test_pii_key_scan_detects_direct_identifiers_and_allows_pseudonyms():
    assert find_direct_identifier_keys({"participant_id": "HV-P-TEST001"}) == []
    assert find_direct_identifier_keys({"nested": {"gps": "not-permitted"}}) == ["nested.gps"]
