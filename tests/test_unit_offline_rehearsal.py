"""Comprehensive unit tests for the Zero-Token Offline Simulation Rehearsal workflow.

Ensures that the entire workshop package, 16 benchmark cases, multimodal studio,
and CLI terminal tools run deterministically offline with zero tokens and zero network access.
"""

import json
import pytest
import jsonschema

from adk.run import (
    COORDINATOR_SCHEMA_PATH,
    execute_inquiry_offline,
    normalize_brief_structure,
)
from app.backend.schemas import (
    ComparativeAnalysisRequest,
    MultiAgentConsensusRequest,
    MultimodalInquiryRequest,
)
from app.backend.service import (
    AppService,
    DEMO_ASSET_DIR,
    PRESET_IMAGES,
    PRESET_INQUIRIES,
)
from app.cli import run_rehearsal


@pytest.fixture
def service():
    return AppService(force_mock=True)


@pytest.fixture
def coordinator_schema():
    assert COORDINATOR_SCHEMA_PATH.exists()
    with open(COORDINATOR_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_preset_catalog_completeness():
    """Verify that all 16 evaluation benchmark inquiries and multimodal assets exist."""
    assert len(PRESET_INQUIRIES) == 16
    norm_cases = [p for p in PRESET_INQUIRIES if p.id.startswith("NORM-")]
    edge_cases = [p for p in PRESET_INQUIRIES if p.id.startswith("EDGE-")]
    assert len(norm_cases) == 8
    assert len(edge_cases) == 8

    assert len(PRESET_IMAGES) >= 1
    sample_img = DEMO_ASSET_DIR / "laparoscopic_cvs_schematic.png"
    assert sample_img.exists()
    assert sample_img.stat().st_size > 0


@pytest.mark.parametrize("preset", PRESET_INQUIRIES, ids=lambda p: p.id)
def test_preset_inquiry_consensus_offline(service, coordinator_schema, preset):
    """Test multi-agent consensus and schema compliance for each benchmark scenario offline."""
    req = MultiAgentConsensusRequest(
        question=preset.question,
        enable_evidence_agent=True,
        enable_guideline_agent=True,
        mock_mode=True,
    )
    resp = service.execute_multiagent_consensus(req)

    # Core integrity
    assert resp.research_question == preset.question
    assert "population" in resp.normalized_picot
    assert len(resp.sources) > 0
    assert resp.latency_ms >= 0

    # Epistemic Humility triggers
    if preset.id in [
        "EDGE-01-NO-EVIDENCE",
        "EDGE-05-INACCESSIBLE-SOURCE",
        "EDGE-08-FUTURE-INFORMATION",
    ]:
        assert resp.evidence_findings.get("not_found") is True
    elif preset.id == "EDGE-02-NO-GUIDELINE":
        assert resp.guideline_findings.get("not_found") is True
    elif preset.id in [
        "EDGE-03-CONFLICTING-STUDIES",
        "EDGE-04-CONFLICTING-GUIDELINES",
        "NORM-06-PROPHYLACTIC-STOMA-MESH",
    ]:
        assert len(resp.consensus_matrix.get("areas_of_disagreement", [])) > 0
    elif preset.id == "EDGE-07-PATIENT-SAFETY":
        assert (
            "SAFETY BOUNDARY" in resp.final_synthesis
            or "educational" in resp.final_synthesis.lower()
        )

    # Coordinator Schema Validation
    raw_brief = {
        "research_question": resp.research_question,
        "research_scope": resp.normalized_picot,
        "not_found": {
            "evidence_not_found": resp.evidence_findings.get("not_found", False),
            "guidelines_not_found": resp.guideline_findings.get("not_found", False),
            "details": resp.evidence_findings.get("details", "")
            or resp.guideline_findings.get("details", ""),
        },
        "evidence_findings": resp.evidence_findings,
        "guideline_findings": resp.guideline_findings,
        "sources": resp.sources,
        "areas_of_agreement": resp.consensus_matrix.get("areas_of_agreement", []),
        "areas_of_disagreement": resp.consensus_matrix.get("areas_of_disagreement", []),
        "uncertainty": resp.consensus_matrix.get("uncertainty_and_limitations", []),
        "limitations": ["Simulation brief generated offline without active token consumption."],
        "discussion_questions": ["What criteria determine implementation barriers?"],
        "safety_disclaimer": resp.safety_disclaimer,
    }
    normalized = normalize_brief_structure(raw_brief, question=preset.question)
    jsonschema.validate(instance=normalized, schema=coordinator_schema)


@pytest.mark.parametrize(
    "case_id",
    [
        "NORM-01-COLORECTAL-PREHAB",
        "EDGE-01-NO-EVIDENCE",
        "EDGE-07-PATIENT-SAFETY",
    ],
)
def test_comparative_analysis_scorecard_offline(service, case_id):
    """Test 5-dimension comparative scorecard generation offline."""
    preset = next(p for p in PRESET_INQUIRIES if p.id == case_id)
    req = ComparativeAnalysisRequest(
        case_id=case_id,
        question=preset.question,
        mock_mode=True,
    )
    resp = service.execute_comparative_analysis(req)

    assert resp.case_id == case_id
    assert resp.case_title == preset.title
    assert len(resp.scorecard) == 5

    dimensions = [item.dimension for item in resp.scorecard]
    assert any("Grounding" in d for d in dimensions)
    assert any("Citation" in d for d in dimensions)
    assert any("Evidence vs. Guideline" in d for d in dimensions)
    assert any("Epistemic Humility" in d for d in dimensions)
    assert any("Clinical Safety" in d for d in dimensions)

    # Monolithic vs Agent contrast
    assert resp.without_agent.raw_response != ""
    assert resp.with_agent.final_synthesis != ""


def test_multimodal_vision_offline(service):
    """Test multimodal vision studio offline execution."""
    req = MultimodalInquiryRequest(
        prompt="Describe observable anatomical features of the Critical View of Safety.",
        preset_image_id="lap_cvs_schematic",
        mock_mode=True,
    )
    resp = service.execute_multimodal(req)

    assert resp.text != ""
    assert (
        "Calot" in resp.text
        or "Critical View of Safety" in resp.text
        or "cystic" in resp.text.lower()
    )
    assert (
        "educational" in resp.safety_disclaimer.lower()
        or "not designed" in resp.safety_disclaimer.lower()
    )
    assert resp.token_estimate == 0


def test_terminal_runner_offline_normal():
    """Test terminal runner adk.run in offline mode for standard inquiries."""
    question = PRESET_INQUIRIES[0].question
    result, telemetry = execute_inquiry_offline(question, verbose=False)

    assert result is not None
    assert telemetry["offline_simulation"] is True
    assert telemetry["coordinator_executed"] is True
    assert telemetry["evidence_agent_executed"] is True
    assert telemetry["guideline_agent_executed"] is True
    assert telemetry["schema_valid"] is True
    assert telemetry["safety_refusal_triggered"] is False


def test_terminal_runner_offline_safety_refusal():
    """Test terminal runner adk.run in offline mode for patient-specific safety queries."""
    safety_preset = next(p for p in PRESET_INQUIRIES if p.id == "EDGE-07-PATIENT-SAFETY")
    result, telemetry = execute_inquiry_offline(safety_preset.question, verbose=False)

    # CLI should intercept patient advice and return None result
    assert result is None
    assert telemetry["safety_refusal_triggered"] is True
    assert len(telemetry["refusal_message"]) > 0


def test_full_rehearsal_command():
    """Verify that the automated dry-run rehearsal runs cleanly without exception."""
    run_rehearsal()


@pytest.mark.asyncio
async def test_evaluation_suite_offline():
    """Verify that adk.eval runs cleanly in offline mode for smoke test case."""
    from adk.eval import run_evaluation_suite

    report = await run_evaluation_suite(cases_filter="NORM-01", num_runs=1, offline=True)
    assert report["num_cases"] == 1
    assert report["failures"]["infrastructure_failures"] == 0
    assert report["failures"]["agent_behavior_failures"] == 0
    assert report["dimensional_breakdown"]["schema_conformance"] == 1.0
    assert report["dimensional_breakdown"]["safety"] == 1.0
