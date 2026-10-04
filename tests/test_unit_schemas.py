"""Offline unit tests for schemas, models, and validation."""

import json
from pathlib import Path

import jsonschema

from adk.schemas import StructuredEvidenceBriefModel

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_coordinator_output_schema_is_valid():
    schema_path = REPO_ROOT / "agents" / "coordinator" / "output-schema.json"
    assert schema_path.exists(), "Coordinator output-schema.json must exist"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["type"] == "object"
    assert "research_question" in schema["required"]
    assert "safety_disclaimer" in schema["required"]
    assert "not_found" in schema["required"]


def test_evidence_output_schema_is_valid():
    schema_path = REPO_ROOT / "agents" / "evidence" / "output-schema.json"
    assert schema_path.exists()
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["type"] == "object"
    assert "studies" in schema["required"]


def test_guideline_output_schema_is_valid():
    schema_path = REPO_ROOT / "agents" / "guideline" / "output-schema.json"
    assert schema_path.exists()
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["type"] == "object"
    assert "guidelines" in schema["required"]


def test_pydantic_brief_model_validates_and_matches_json_schema():
    brief_data = {
        "research_question": "What is the role of prehabilitation in elective colorectal surgery?",
        "research_scope": {
            "population": "Adults undergoing elective colorectal resection",
            "context": "Elective perioperative care",
            "intervention_exposure": "Multimodal prehabilitation",
            "comparator": "Standard care",
            "outcomes": ["Complications", "Functional capacity"],
            "time_range": "2018-2026",
        },
        "not_found": {
            "evidence_not_found": False,
            "guidelines_not_found": False,
            "details": "Studies and guidelines found",
        },
        "evidence_findings": {
            "summary": "RCTs demonstrate improved walking capacity.",
            "key_study_findings": [
                {
                    "study_title": "PREHAB trial",
                    "authors_or_organization": "Molenaar et al.",
                    "publication_year": 2023,
                    "evidence_type": "randomized_controlled_trial",
                    "key_findings": "Reduced medical complications in high-risk patients.",
                    "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/",
                    "primary_endpoints": ["Complications"],
                }
            ],
        },
        "guideline_findings": {
            "summary": "ERAS guidelines recommend prehabilitation in high-risk patients.",
            "guideline_statements": [
                {
                    "organization": "ERAS Society",
                    "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
                    "publication_or_update_year": 2023,
                    "recommendation_summary": "Consider prehabilitation for frail patients.",
                    "url": "https://erassociety.org/guidelines/colorectal/",
                    "strength_of_recommendation": "Conditional",
                }
            ],
        },
        "sources": [
            {
                "source_id": "SRC-01",
                "title": "PREHAB trial",
                "author_or_institution": "Molenaar et al.",
                "year": 2023,
                "source_type": "randomized_trial",
                "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/",
            }
        ],
        "areas_of_agreement": [
            {
                "domain": "Functional reserve",
                "consensus_summary": "Both agree high-risk patients benefit most.",
                "supporting_sources": ["SRC-01"],
            }
        ],
        "areas_of_disagreement": [],
        "uncertainty": [
            {
                "topic": "Optimal duration",
                "uncertainty_rationale": "Heterogeneous protocols between 2 to 6 weeks.",
            }
        ],
        "limitations": ["Limited blinding possible in exercise trials"],
        "discussion_questions": ["How to optimize 4-week window without surgical delay?"],
        "safety_disclaimer": "Educational research prototype only. Not medical advice.",
    }

    # Verify Pydantic model parses
    model = StructuredEvidenceBriefModel(**brief_data)
    assert model.research_question == brief_data["research_question"]

    # Verify JSON Schema validates
    schema_path = REPO_ROOT / "agents" / "coordinator" / "output-schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    jsonschema.validate(instance=model.model_dump(), schema=schema)
