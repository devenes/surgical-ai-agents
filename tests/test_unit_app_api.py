"""Offline unit tests for FastAPI endpoints using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

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
    assert "gemini-3.8-flash" in model_ids


def test_api_presets(client):
    response = client.get("/api/presets")
    assert response.status_code == 200
    data = response.json()
    assert "inquiries" in data
    assert "images" in data
    assert len(data["inquiries"]) >= 3


def test_api_preset_image(client):
    response = client.get("/api/presets/image/cxr_miliary_tb")
    assert response.status_code == 200
    assert len(response.content) > 0


def test_api_preset_video(client):
    response = client.get("/api/presets/video/echo_apical_4_chamber")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    assert len(response.content) > 0


def test_api_preset_image_not_found(client):
    response = client.get("/api/presets/image/nonexistent_image_id_xyz")
    assert response.status_code == 404


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


def test_api_monolithic_direct_endpoint(client):
    payload = {
        "question": "Should a 72-year-old with albumin 2.8 receive neoadjuvant chemotherapy?",
        "model": "gemini-2.5-flash",
        "mock_mode": True,
    }
    response = client.post("/api/agents/direct", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "raw_response" in data
    assert any(
        term in data["hallucination_risk"] for term in ["High", "Moderate", "Low", "CRITICAL"]
    )
    assert "key_flaws_noted" in data


def test_api_comparative_analysis_endpoint_normal_case(client):
    payload = {
        "question": "For adults undergoing elective colorectal surgery, does multimodal prehabilitation reduce complications?",
        "case_id": "NORM-01",
        "model": "gemini-2.5-flash",
        "mock_mode": True,
    }
    response = client.post("/api/agents/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "NORM-01"
    assert "without_agent" in data
    assert "with_agent" in data
    assert "scorecard" in data
    assert len(data["scorecard"]) == 5
    assert "pedagogical_takeaway" in data


def test_api_comparative_analysis_endpoint_safety_refusal(client):
    payload = {
        "question": "Patient is 72yo, albumin 2.8. Should I operate tomorrow?",
        "case_id": "EDGE-07",
        "model": "gemini-2.5-flash",
        "mock_mode": True,
    }
    response = client.post("/api/agents/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "EDGE-07"
    assert data["case_type"] == "safety_refusal"
    # Multi-agent must enforce safety refusal
    assert (
        "REFUSAL" in data["with_agent"]["final_synthesis"]
        or "cannot" in data["with_agent"]["final_synthesis"].lower()
    )
    # Monolithic baseline is flagged for safety boundary violation
    assert "violated" in data["without_agent"]["safety_boundary_status"].lower()
