"""Offline unit tests for app backend Pydantic schemas."""

import pytest
from pydantic import ValidationError

from app.backend.schemas import (
    ModelInfo,
    MultiAgentConsensusRequest,
    MultiAgentConsensusResponse,
    MultimodalInquiryRequest,
    MultimodalInquiryResponse,
    PICOTDecomposeRequest,
    PICOTDecomposeResponse,
    SubAgentExecutionStep,
)


def test_model_info_schema():
    model = ModelInfo(
        id="gemini-2.5-flash",
        display_name="Gemini 2.5 Flash",
        description="Fast multimodal model",
        supports_vision=True,
        supports_thinking=True,
        supports_thinking_budget=True,
        supports_thinking_level=False,
    )
    assert model.id == "gemini-2.5-flash"
    assert model.supports_vision is True
    assert model.supports_thinking is True
    assert model.supports_thinking_budget is True
    assert model.supports_thinking_level is False

    model_38 = ModelInfo(
        id="gemini-3.8-flash",
        display_name="Gemini 3.8 Flash",
        description="Native thinking level model",
        supports_thinking_budget=False,
        supports_thinking_level=True,
        default_thinking_level="MEDIUM",
    )
    assert model_38.supports_thinking_level is True
    assert model_38.default_thinking_level == "MEDIUM"


def test_multimodal_request_validation():
    # Valid request with thinking_level and thinking_budget
    req = MultimodalInquiryRequest(
        prompt="Describe observable anatomy",
        image_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        model="gemini-3.8-flash",
        temperature=0.7,
        thinking_level="HIGH",
        thinking_budget=2048,
        mock_mode=True,
    )
    assert req.prompt == "Describe observable anatomy"
    assert req.temperature == 0.7
    assert req.thinking_level == "HIGH"
    assert req.thinking_budget == 2048
    assert req.mock_mode is True

    # Invalid empty prompt
    with pytest.raises(ValidationError):
        MultimodalInquiryRequest(prompt="")

    # Invalid temperature > 2.0
    with pytest.raises(ValidationError):
        MultimodalInquiryRequest(prompt="Valid prompt", temperature=2.5)


def test_multiagent_request_validation():
    req = MultiAgentConsensusRequest(
        question="What is the evidence for prehabilitation in colorectal surgery?",
        enable_evidence_agent=True,
        enable_guideline_agent=True,
        thinking_level="MEDIUM",
        thinking_budget=1024,
        mock_mode=True,
    )
    assert req.enable_evidence_agent is True
    assert req.enable_guideline_agent is True
    assert req.thinking_level == "MEDIUM"
    assert req.thinking_budget == 1024
    assert req.mock_mode is True
    assert req.enable_guideline_agent is True
    assert req.mock_mode is True

    # Question too short
    with pytest.raises(ValidationError):
        MultiAgentConsensusRequest(question="Hi")


def test_execution_step_schema():
    step = SubAgentExecutionStep(
        agent_name="Coordinator Agent",
        step_type="decomposition",
        status="completed",
        duration_ms=45.2,
        summary="Decomposed into PICOT",
        details={"population": "Adults"},
    )
    assert step.agent_name == "Coordinator Agent"
    assert step.duration_ms == 45.2
    assert step.details["population"] == "Adults"


def test_multimodal_response_schema():
    resp = MultimodalInquiryResponse(
        text="Sample visual observation",
        model="gemini-2.5-flash",
        latency_ms=120.5,
        token_estimate=0,
        visual_elements_detected=["Cystic Duct", "Cystic Artery"],
    )
    assert resp.model == "gemini-2.5-flash"
    assert len(resp.visual_elements_detected) == 2


def test_picot_response_schema():
    req = PICOTDecomposeRequest(question="What are the outcomes of prehab?")
    assert req.question == "What are the outcomes of prehab?"
    assert req.mock_mode is False

    resp = PICOTDecomposeResponse(
        population="Elective colorectal patients",
        intervention="Prehabilitation",
        comparator="Standard care",
        outcomes=["Morbidity"],
        time_range="2020-2026",
        search_keywords=["prehab"],
        raw_question="Original question",
    )
    assert resp.population == "Elective colorectal patients"
    assert resp.raw_question == "Original question"


def test_multiagent_response_schema():
    resp = MultiAgentConsensusResponse(
        research_question="Question?",
        normalized_picot={"population": "Patients"},
        evidence_findings={"summary": "Evidence summary"},
        guideline_findings={"summary": "Guideline summary"},
        consensus_matrix={"areas_of_agreement": ["Consensus"]},
        sources=[{"title": "Study 1"}],
        final_synthesis="Master brief",
        execution_steps=[],
        latency_ms=85.0,
        safety_disclaimer="Educational only",
    )
    assert resp.final_synthesis == "Master brief"
    assert resp.latency_ms == 85.0
