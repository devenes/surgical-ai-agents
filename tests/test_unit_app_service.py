"""Offline unit tests for AppService (zero token calls)."""

import pytest

from app.backend.schemas import (
    MultiAgentConsensusRequest,
    MultimodalInquiryRequest,
    PICOTDecomposeRequest,
)
from app.backend.service import AppService


@pytest.fixture
def service():
    return AppService(force_mock=True)


def test_service_models_list(service):
    models = service.get_models()
    assert len(models) >= 3
    model_ids = [m.id for m in models]
    assert "gemini-2.5-flash" in model_ids
    assert "gemini-2.5-pro" in model_ids


def test_service_presets(service):
    inquiries, images = service.get_presets()
    assert len(inquiries) >= 3
    assert len(images) >= 1
    assert any("prehab" in q.id for q in inquiries)
    assert any("cvs" in img.id for img in images)


def test_service_preset_image_bytes(service):
    img_bytes = service.get_preset_image_bytes("lap_cvs_schematic")
    assert img_bytes is not None
    assert len(img_bytes) > 0

    assert service.get_preset_image_bytes("nonexistent_unknown_id") is None


def test_service_multimodal_mock(service):
    req = MultimodalInquiryRequest(
        prompt="Describe anatomy in schematic",
        preset_image_id="lap_cvs_schematic",
        model="gemini-2.5-flash",
        mock_mode=True,
    )
    resp = service.execute_multimodal(req)
    assert resp.text != ""
    assert "Hepatocystic Triangle" in resp.text or "Critical View of Safety" in resp.text
    assert resp.token_estimate == 0
    assert len(resp.visual_elements_detected) > 0


def test_service_multiagent_consensus_mock(service):
    req = MultiAgentConsensusRequest(
        question="For adults undergoing elective colorectal surgery, evaluate prehabilitation.",
        model="gemini-2.5-flash",
        enable_evidence_agent=True,
        enable_guideline_agent=True,
        mock_mode=True,
    )
    resp = service.execute_multiagent_consensus(req)

    assert resp.research_question == req.question
    assert "population" in resp.normalized_picot
    assert "colorectal" in resp.normalized_picot["population"].lower()

    # Sub-agent findings
    assert "key_study_findings" in resp.evidence_findings
    assert len(resp.evidence_findings["key_study_findings"]) > 0

    assert "guideline_statements" in resp.guideline_findings
    assert len(resp.guideline_findings["guideline_statements"]) > 0

    # Consensus matrix
    assert len(resp.consensus_matrix["areas_of_agreement"]) > 0
    assert len(resp.consensus_matrix["areas_of_disagreement"]) > 0

    # Execution steps
    assert len(resp.execution_steps) >= 4
    agent_names = [s.agent_name for s in resp.execution_steps]
    assert "Coordinator Agent" in agent_names
    assert "Evidence Specialist (Sub-Agent 1)" in agent_names
    assert "Guideline Specialist (Sub-Agent 2)" in agent_names


def test_service_multiagent_disable_one_subagent(service):
    req = MultiAgentConsensusRequest(
        question="For adults undergoing elective colorectal surgery, evaluate prehabilitation.",
        enable_evidence_agent=True,
        enable_guideline_agent=False,
        mock_mode=True,
    )
    resp = service.execute_multiagent_consensus(req)

    # Guideline agent step should be skipped
    guide_step = next(s for s in resp.execution_steps if "Guideline" in s.agent_name)
    assert guide_step.status == "skipped"


def test_service_picot_decomposition(service):
    req = PICOTDecomposeRequest(
        question="What are outcomes of CVS in laparoscopic cholecystectomy for bile duct injury?",
        mock_mode=True,
    )
    resp = service.decompose_picot(req)

    assert "cholecystectomy" in resp.population.lower() or "cholecystectomy" in resp.intervention.lower()
    assert len(resp.outcomes) > 0
    assert len(resp.search_keywords) > 0
