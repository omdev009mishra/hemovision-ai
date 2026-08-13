"""
Unit tests for HemoVision FastAPI Backend Services & Endpoints — Phase 9
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "investigational" in data["disclaimer"].lower()


def test_demo_samples_endpoint():
    response = client.get("/api/v1/demo-samples")
    assert response.status_code == 200
    data = response.json()
    assert "presets" in data
    assert len(data["presets"]) == 4
    preset_a = data["presets"][0]
    assert "Normal" in preset_a["name"]
    assert preset_a["image_b64"] != ""


def test_analyze_endpoint_with_preset_payload():
    samples_res = client.get("/api/v1/demo-samples")
    image_b64 = samples_res.json()["presets"][0]["image_b64"]

    response = client.post("/api/v1/analyze", json={"image_b64": image_b64})
    assert response.status_code == 200
    data = response.json()

    assert data["session_id"].startswith("HV-SESS-")
    assert data["is_usable"] is True
    assert data["quality"]["quality_score"] > 0.0
    assert data["prediction"]["estimated_hb_g_dl"] is not None
    assert len(data["prediction"]["prediction_interval"]) == 2
    assert data["visual_overlay_b64"] != ""


def test_generate_markdown_report():
    samples_res = client.get("/api/v1/demo-samples")
    image_b64 = samples_res.json()["presets"][0]["image_b64"]

    response = client.post("/api/v1/reports/markdown", json={"image_b64": image_b64})
    assert response.status_code == 200
    data = response.json()

    assert "markdown" in data
    assert "# HemoVision" in data["markdown"]
    assert "Estimated Hb:" in data["markdown"]
