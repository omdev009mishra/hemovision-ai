"""
Tests for ImageIngestor
"""

import pytest
from pathlib import Path
from ml.src.data.image_ingestion import ImageIngestor


def test_image_ingestion_synthetic_sample():
    ingestor = ImageIngestor()
    fixture_path = Path("dataset/samples/synthetic_eye_001.png")
    assert fixture_path.exists()

    rec = ingestor.ingest_image(
        source_path=str(fixture_path),
        session_id="HV-SESS-001",
        participant_id="HV-P-000001",
        raw_exif={"Make": "SyntheticCorp", "GPSLatitude": "12.34 N"}
    )

    assert rec.success is True
    assert rec.image_id.startswith("HV-IMG-")
    assert len(rec.sha256_hash) == 64
    assert "GPSLatitude" not in rec.sanitized_metadata
    assert rec.width == 512
    assert rec.height == 512
