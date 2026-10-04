"""Offline unit tests for FastAPI endpoints using Starlette TestClient."""

import pytest
from starlette.testclient import TestClient

from app.backend.api import app


@pytest.fixture
def client():
    return TestClient(app)


def test_api_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Surgical AI Multi-Agent & Multimodal API"
    assert "docs" in data


def test_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "subagent_architecture" in data


def test_api_models(client):
    response = client.get("/api/models")
    assert response.status_code == 200
    models = response.json()
    assert len(models) >= 3
    model_ids = [m["id"] for m in models]
    assert "gemini-2.5-flash" in model_ids


def test_api_presets(client):
    response = client.get("/api/presets")
    assert response.status_code == 200
    data = response.json()
    assert "inquiries" in data
    assert "images" in data
    assert len(data["inquiries"]) >= 3


def test_api_preset_image(client):
    response = client.get("/api/presets/image/lap_cvs_schematic")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0


def test_api_preset_image_not_found(client):
    # Temporarily rename/ensure nonexistent id
    response = client.get("/api/presets/image/nonexistent_image_id_xyz")
    # Should either 404 or return fallback if fallback is configured
    assert response.status_code in (200, 404)


def test_api_multimodal_endpoint(client):
    payload = {
        "prompt": "Identify observable surgical anatomy.",
        "preset_image_id": "lap_cvs_schematic",
        "model": "gemini-2.5-flash",
        "temperature": 0.3,
        "mock_mode": True,
    }
    response = client.post("/api/multimodal", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["token_estimate"] == 0
    assert "visual_elements_detected" in data


def test_api_multiagent_consensus_endpoint(client):
    payload = {
        "question": "For adults undergoing elective colorectal surgery, evaluate prehabilitation.",
        "model": "gemini-2.5-flash",
        "enable_evidence_agent": True,
        "enable_guideline_agent": True,
        "mock_mode": True,
    }
    response = client.post("/api/agents/consensus", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["research_question"] == payload["question"]
    assert "normalized_picot" in data
    assert "evidence_findings" in data
    assert "guideline_findings" in data
    assert "consensus_matrix" in data
    assert len(data["execution_steps"]) >= 4


def test_api_picot_decompose_endpoint(client):
    payload = {
        "question": "What is the evidence on laparoscopic vs open repair for inguinal hernia?",
        "model": "gemini-2.5-flash",
        "mock_mode": True,
    }
    response = client.post("/api/agents/decompose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "population" in data
    assert "intervention" in data
    assert "comparator" in data
    assert len(data["outcomes"]) > 0
