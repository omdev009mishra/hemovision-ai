"""
Security Tests: Verify Git Privacy, No Clinical Image Tracking, and No PII Exposure
"""

import pytest
import subprocess
from pathlib import Path


def test_git_privacy_no_raw_clinical_images_tracked():
    """Verify that git tracked files contain no binary image files outside dataset/samples/."""
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd="d:/hemovision")
    assert result.returncode == 0, "git ls-files failed"

    tracked_files = result.stdout.splitlines()
    forbidden_images = []

    for f in tracked_files:
        f_lower = f.lower()
        if f_lower.endswith((".jpg", ".jpeg", ".png", ".dicom", ".dcm", ".svs")):
            if not (f.startswith("dataset/samples/") or f.startswith("mobile/hemovision_capture/") or f.startswith("research/results/")):
                forbidden_images.append(f)

    assert len(forbidden_images) == 0, f"Discovered untracked clinical images in Git: {forbidden_images}"


def test_git_privacy_no_credentials_or_pii_files_tracked():
    """Verify that git tracked files contain no credentials, .env files, or private keys."""
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd="d:/hemovision")
    assert result.returncode == 0

    tracked_files = result.stdout.splitlines()
    forbidden_patterns = [".env", "credentials.json", "secrets.yaml", ".pem", ".key", "dataset/clinical/"]

    violations = []
    for f in tracked_files:
        for p in forbidden_patterns:
            if p in f and not f.endswith(".gitkeep"):
                violations.append(f)

    assert len(violations) == 0, f"Discovered sensitive/clinical files in Git: {violations}"
