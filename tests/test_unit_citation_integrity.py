import json
from pathlib import Path
import jsonschema
import pytest
from pydantic import ValidationError

from adk.run import COORDINATOR_SCHEMA_PATH, normalize_brief_structure
from adk.schemas import (
    GuidelineStatementModel,
    SourceCitationModel,
    StructuredEvidenceBriefModel,
    StudyFindingModel,
    validate_author_or_org,
    validate_title,
    validate_url,
    validate_year,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def get_coordinator_schema():
    assert COORDINATOR_SCHEMA_PATH.exists()
    with open(COORDINATOR_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# Case 1: Complete, valid study reference is preserved unchanged
# =============================================================================


def test_case_1_complete_valid_study_preserved_unchanged():
    valid_study = {
        "study_title": "Prehabilitation in elective colorectal surgery: a randomized clinical trial",
        "authors_or_organization": "Molenaar CJ, van Rooijen SJ, et al.",
        "publication_year": 2023,
        "evidence_type": "randomized_controlled_trial",
        "key_findings": "Multimodal prehabilitation reduced postoperative medical complications.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/",
        "primary_endpoints": ["Overall complications", "Functional capacity"],
    }
    raw_brief = {
        "research_question": "What is the evidence for prehabilitation in colorectal surgery?",
        "evidence_findings": {
            "summary": "High-quality RCT evidence shows positive outcomes.",
            "key_study_findings": [valid_study],
        },
    }

    normalized = normalize_brief_structure(raw_brief)
    studies = normalized["evidence_findings"]["key_study_findings"]
    assert len(studies) == 1
    st = studies[0]
    assert st["study_title"] == valid_study["study_title"]
    assert st["authors_or_organization"] == valid_study["authors_or_organization"]
    assert st["publication_year"] == 2023
    assert st["evidence_type"] == "randomized_controlled_trial"
    assert st["key_findings"] == valid_study["key_findings"]
    assert st["url"] == valid_study["url"]
    assert st["primary_endpoints"] == valid_study["primary_endpoints"]

    # Also verified in sources registry
    assert len(normalized["sources"]) == 1
    src = normalized["sources"][0]
    assert src["title"] == valid_study["study_title"]
    assert src["author_or_institution"] == valid_study["authors_or_organization"]
    assert src["year"] == 2023
    assert src["url"] == valid_study["url"]


# =============================================================================
# Case 2: Study missing title, authors, year, or URL is not presented as verified
# =============================================================================


def test_case_2_study_missing_required_metadata_not_presented_as_verified():
    incomplete_studies = [
        # Missing title
        {
            "authors_or_organization": "Smith et al.",
            "publication_year": 2023,
            "evidence_type": "randomized_trial",
            "key_findings": "Findings noted.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        },
        # Empty title
        {
            "study_title": "   ",
            "authors_or_organization": "Smith et al.",
            "publication_year": 2023,
            "evidence_type": "randomized_trial",
            "key_findings": "Findings noted.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        },
        # Missing author
        {
            "study_title": "Randomized Trial on Colorectal Recovery",
            "publication_year": 2023,
            "evidence_type": "randomized_trial",
            "key_findings": "Findings noted.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        },
        # Missing year
        {
            "study_title": "Randomized Trial on Colorectal Recovery",
            "authors_or_organization": "Smith et al.",
            "evidence_type": "randomized_trial",
            "key_findings": "Findings noted.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        },
        # Missing URL
        {
            "study_title": "Randomized Trial on Colorectal Recovery",
            "authors_or_organization": "Smith et al.",
            "publication_year": 2023,
            "evidence_type": "randomized_trial",
            "key_findings": "Findings noted.",
        },
        # Missing evidence_type
        {
            "study_title": "Randomized Trial on Colorectal Recovery",
            "authors_or_organization": "Smith et al.",
            "publication_year": 2023,
            "key_findings": "Findings noted.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        },
        # Missing findings
        {
            "study_title": "Randomized Trial on Colorectal Recovery",
            "authors_or_organization": "Smith et al.",
            "publication_year": 2023,
            "evidence_type": "randomized_trial",
            "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        },
    ]

    for incomplete in incomplete_studies:
        raw_brief = {
            "evidence_findings": {
                "summary": "Testing incomplete study rejection.",
                "key_study_findings": [incomplete],
            }
        }
        normalized = normalize_brief_structure(raw_brief)
        # Incomplete study must be excluded
        assert len(normalized["evidence_findings"]["key_study_findings"]) == 0
        assert len(normalized["sources"]) == 0

    # Direct Pydantic model instantiation must also reject fabricated titles/URLs
    with pytest.raises(ValidationError):
        StudyFindingModel(
            study_title="Clinical Study",
            authors_or_organization="Smith et al.",
            publication_year=2023,
            evidence_type="randomized_trial",
            key_findings="Findings noted.",
            url="https://pubmed.ncbi.nlm.nih.gov/12345678/",
        )


# =============================================================================
# Case 3: Guideline with incomplete bibliographic metadata is excluded
# =============================================================================


def test_case_3_guideline_with_incomplete_bibliographic_metadata_excluded():
    incomplete_guidelines = [
        # Missing organization
        {
            "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
            "publication_or_update_year": 2023,
            "recommendation_summary": "Prehabilitation is recommended for high-risk patients.",
            "url": "https://erassociety.org/guidelines/colorectal/",
        },
        # Missing title
        {
            "organization": "ERAS Society",
            "publication_or_update_year": 2023,
            "recommendation_summary": "Prehabilitation is recommended for high-risk patients.",
            "url": "https://erassociety.org/guidelines/colorectal/",
        },
        # Missing year
        {
            "organization": "ERAS Society",
            "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
            "recommendation_summary": "Prehabilitation is recommended for high-risk patients.",
            "url": "https://erassociety.org/guidelines/colorectal/",
        },
        # Missing recommendation
        {
            "organization": "ERAS Society",
            "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
            "publication_or_update_year": 2023,
            "url": "https://erassociety.org/guidelines/colorectal/",
        },
        # Missing URL
        {
            "organization": "ERAS Society",
            "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
            "publication_or_update_year": 2023,
            "recommendation_summary": "Prehabilitation is recommended for high-risk patients.",
        },
    ]

    for incomplete in incomplete_guidelines:
        raw_brief = {
            "guideline_findings": {
                "summary": "Testing incomplete guideline rejection.",
                "guideline_statements": [incomplete],
            }
        }
        normalized = normalize_brief_structure(raw_brief)
        assert len(normalized["guideline_findings"]["guideline_statements"]) == 0
        assert len(normalized["sources"]) == 0

    # Direct Pydantic model instantiation must reject fabricated organization
    with pytest.raises(ValidationError):
        GuidelineStatementModel(
            organization="Surgical Society",
            guideline_title="Colorectal Guidelines",
            publication_or_update_year=2023,
            recommendation_summary="Recommendation provided.",
            url="https://erassociety.org/guidelines/",
        )


# =============================================================================
# Case 4: Generic PubMed homepage URL is not accepted as substitute
# =============================================================================


def test_case_4_generic_pubmed_homepage_rejected():
    assert validate_url("https://pubmed.ncbi.nlm.nih.gov/") is None
    assert validate_url("https://pubmed.ncbi.nlm.nih.gov") is None
    assert validate_url("http://pubmed.ncbi.nlm.nih.gov/") is None
    assert validate_url("https://guidelines.org/") is None
    assert validate_url("https://guidelines.org") is None

    # Valid specific publication URLs
    assert validate_url("https://pubmed.ncbi.nlm.nih.gov/37099276/") == "https://pubmed.ncbi.nlm.nih.gov/37099276/"
    assert validate_url("https://pubmed.ncbi.nlm.nih.gov/37099276") == "https://pubmed.ncbi.nlm.nih.gov/37099276"
    assert validate_url("https://erassociety.org/guidelines/colorectal/") == "https://erassociety.org/guidelines/colorectal/"

    study_with_generic_url = {
        "study_title": "Trial on Postoperative Complications",
        "authors_or_organization": "Molenaar et al.",
        "publication_year": 2023,
        "evidence_type": "randomized_trial",
        "key_findings": "Functional recovery accelerated.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/",
    }
    raw_brief = {
        "evidence_findings": {
            "summary": "Testing generic URL rejection.",
            "key_study_findings": [study_with_generic_url],
        }
    }
    normalized = normalize_brief_structure(raw_brief)
    assert len(normalized["evidence_findings"]["key_study_findings"]) == 0
    assert len(normalized["sources"]) == 0


# =============================================================================
# Case 5: Normalizer does not generate fabricated bibliographic defaults
# =============================================================================


def test_case_5_normalizer_never_generates_fabricated_bibliographic_defaults():
    raw_brief = {
        "evidence_findings": {
            "summary": "Evidence without studies.",
            "key_study_findings": [{}],
        },
        "guideline_findings": {
            "summary": "Guideline without statements.",
            "guideline_statements": [{}],
        },
        "sources": [{}],
    }

    normalized = normalize_brief_structure(raw_brief)

    # Empty/placeholder candidates must be omitted, not filled with fabricated values
    assert normalized["evidence_findings"]["key_study_findings"] == []
    assert normalized["guideline_findings"]["guideline_statements"] == []
    assert normalized["sources"] == []

    # Explicit check that banned fabrication strings are absent
    brief_str = json.dumps(normalized)
    assert "Clinical Study" not in brief_str
    assert "Investigators" not in brief_str
    assert "Clinical Guideline" not in brief_str
    assert "Surgical Society" not in brief_str
    assert "Clinical Source" not in brief_str
    assert "Clinical Reference" not in brief_str
    assert "https://pubmed.ncbi.nlm.nih.gov/" not in brief_str
    assert "https://guidelines.org/" not in brief_str

    # Direct validation helpers reject fabricated values
    assert validate_title("Clinical Study") is None
    assert validate_title("Clinical Guideline") is None
    assert validate_author_or_org("Investigators") is None
    assert validate_author_or_org("Authors") is None
    assert validate_author_or_org("Surgical Society") is None
    assert validate_year("not-a-year") is None
    assert validate_year(-2024) is None

    # SourceCitationModel rejects generic defaults
    with pytest.raises(ValidationError):
        SourceCitationModel(
            source_id="SRC-01",
            title="Clinical Source",
            author_or_institution="Authors",
            year=2024,
            source_type="randomized_trial",
            url="https://pubmed.ncbi.nlm.nih.gov/",
        )


# =============================================================================
# Case 6: Invalid field types and malformed years do not crash normalization
# =============================================================================


def test_case_6_invalid_field_types_and_malformed_years_do_not_crash():
    malformed_inputs = [
        {"publication_year": "not-a-year"},
        {"publication_year": None},
        {"publication_year": True},
        {"publication_year": False},
        {"publication_year": -2024},
        {"publication_year": 0},
        {"publication_year": ["2024"]},
        {"publication_year": {"year": 2024}},
        {"url": 12345},
        {"url": None},
        {"url": True},
        {"url": ["https://example.com"]},
        {"study_title": None},
        {"study_title": 123},
        {"authors_or_organization": None},
        {"authors_or_organization": ["Author 1"]},
    ]

    for item in malformed_inputs:
        raw_brief = {
            "evidence_findings": {
                "summary": "Robustness test",
                "key_study_findings": [item],
            },
            "guideline_findings": {
                "summary": "Robustness test",
                "guideline_statements": [item],
            },
            "sources": [item],
        }
        # Normalization must execute safely without raising any exceptions
        normalized = normalize_brief_structure(raw_brief)
        assert isinstance(normalized, dict)
        assert normalized["evidence_findings"]["key_study_findings"] == []
        assert normalized["guideline_findings"]["guideline_statements"] == []
        assert normalized["sources"] == []


# =============================================================================
# Case 7: Mixture of valid and invalid references preserves valid and reports omitted
# =============================================================================


def test_case_7_mixture_valid_and_invalid_preserves_valid_and_reports_omitted():
    valid_study = {
        "study_title": "Effect of Prehabilitation on Functional Capacity (Minnella et al.)",
        "authors_or_organization": "Minnella EM, Bousquet-Dion G, et al.",
        "publication_year": 2020,
        "evidence_type": "prospective_cohort",
        "key_findings": "Multimodal nutritional prehabilitation preserved lean body mass.",
        "url": "https://jamanetwork.com/journals/jamasurgery/fullarticle/2765809",
    }
    invalid_study = {
        "study_title": "Incomplete study with missing authors",
        "publication_year": 2021,
        "evidence_type": "randomized_trial",
        "key_findings": "Some findings.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/99999999/",
    }

    raw_brief = {
        "evidence_findings": {
            "summary": "Mixture test.",
            "key_study_findings": [valid_study, invalid_study],
        },
        "limitations": ["Pre-existing study limitation."],
    }

    normalized = normalize_brief_structure(raw_brief)
    studies = normalized["evidence_findings"]["key_study_findings"]
    assert len(studies) == 1
    assert studies[0]["study_title"] == valid_study["study_title"]

    # Valid study is retained in sources
    assert len(normalized["sources"]) == 1
    assert normalized["sources"][0]["title"] == valid_study["study_title"]

    # Limitation note reported
    limitations = normalized["limitations"]
    assert len(limitations) >= 2
    assert any("omitted" in lim.lower() for lim in limitations)
    assert any("bibliographic metadata" in lim.lower() for lim in limitations)

    # Uncertainty note reported
    uncertainty = normalized["uncertainty"]
    assert len(uncertainty) >= 1
    assert any("unverified" in u["topic"].lower() for u in uncertainty)


# =============================================================================
# Case 8: Explicit not_found states remain unchanged
# =============================================================================


def test_case_8_explicit_not_found_states_remain_unchanged():
    # 1. Evidence absent, guidelines present
    brief_edge1 = {
        "not_found": {
            "evidence_not_found": True,
            "guidelines_not_found": False,
            "details": "No RCTs identified for novel surgical ablation.",
        },
        "evidence_findings": {"summary": "No studies found.", "key_study_findings": []},
    }
    norm_edge1 = normalize_brief_structure(brief_edge1)
    assert norm_edge1["not_found"]["evidence_not_found"] is True
    assert norm_edge1["not_found"]["guidelines_not_found"] is False
    assert norm_edge1["not_found"]["details"] == "No RCTs identified for novel surgical ablation."

    # 2. Evidence present, guidelines absent
    brief_edge2 = {
        "not_found": {
            "evidence_not_found": False,
            "guidelines_not_found": True,
            "details": "No society guidelines published for off-label topical use.",
        },
        "guideline_findings": {"summary": "No guidelines found.", "guideline_statements": []},
    }
    norm_edge2 = normalize_brief_structure(brief_edge2)
    assert norm_edge2["not_found"]["evidence_not_found"] is False
    assert norm_edge2["not_found"]["guidelines_not_found"] is True
    assert norm_edge2["not_found"]["details"] == "No society guidelines published for off-label topical use."

    # 3. Explicit boolean not_found
    brief_bool_true = {"not_found": True}
    norm_bool_true = normalize_brief_structure(brief_bool_true)
    assert norm_bool_true["not_found"]["evidence_not_found"] is True
    assert norm_bool_true["not_found"]["guidelines_not_found"] is True


# =============================================================================
# Case 9: Missing reference metadata does not assert evidence was absent or search succeeded
# =============================================================================


def test_case_9_missing_reference_metadata_does_not_assert_evidence_absent_or_succeeded():
    # An unverified candidate study is omitted due to malformed URL
    candidate_study = {
        "study_title": "Preliminary trial on anastomotic leak detection",
        "authors_or_organization": "Author et al.",
        "publication_year": 2022,
        "evidence_type": "cohort_study",
        "key_findings": "Leak detected early.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/",  # Generic homepage -> omitted
    }
    raw_brief = {
        "not_found": {
            "evidence_not_found": False,
            "guidelines_not_found": False,
            "details": "",
        },
        "evidence_findings": {
            "summary": "Synthesized evidence.",
            "key_study_findings": [candidate_study],
        },
    }

    normalized = normalize_brief_structure(raw_brief)

    # 1. Study was omitted due to invalid metadata
    assert len(normalized["evidence_findings"]["key_study_findings"]) == 0
    assert len(normalized["sources"]) == 0

    # 2. Does NOT assert false absence: evidence_not_found must NOT become True
    assert normalized["not_found"]["evidence_not_found"] is False

    # 3. Limitations clearly explain unverified candidate omission rather than clinical absence
    limitations = normalized["limitations"]
    assert any("omitted" in lim.lower() for lim in limitations)
    assert any("bibliographic metadata" in lim.lower() for lim in limitations)


# =============================================================================
# Case 10: Final normalized output passes coordinator JSON Schema
# =============================================================================


def test_case_10_final_normalized_output_passes_coordinator_json_schema():
    schema = get_coordinator_schema()

    # Valid brief with full citations
    complete_brief = {
        "research_question": "What is the role of multimodal prehabilitation in elective colorectal surgery?",
        "research_scope": {
            "population": "Adults undergoing elective colorectal resection",
            "context": "Elective perioperative surgical care",
            "intervention_exposure": "Multimodal prehabilitation bundle",
            "comparator": "Standard care without structured prehabilitation",
            "outcomes": ["30-day morbidity", "6-minute walk distance", "Length of hospital stay"],
            "time_range": "2018-2026",
        },
        "not_found": {
            "evidence_not_found": False,
            "guidelines_not_found": False,
            "details": "Conclusive evidence and guidelines identified.",
        },
        "evidence_findings": {
            "summary": "Randomized trials demonstrate reduced complications.",
            "key_study_findings": [
                {
                    "study_title": "PREHAB trial on colorectal prehabilitation",
                    "authors_or_organization": "Molenaar CJ, van Rooijen SJ, et al.",
                    "publication_year": 2023,
                    "evidence_type": "randomized_controlled_trial",
                    "key_findings": "Prehabilitation reduced medical complications by 40%.",
                    "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/",
                    "primary_endpoints": ["Overall complications", "Functional capacity"],
                }
            ],
        },
        "guideline_findings": {
            "summary": "Society guidelines support prehabilitation in high-risk patients.",
            "guideline_statements": [
                {
                    "organization": "ERAS Society",
                    "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
                    "publication_or_update_year": 2023,
                    "recommendation_summary": "Prehabilitation is conditionally recommended for frail surgical candidates.",
                    "url": "https://erassociety.org/guidelines/colorectal-surgery/",
                    "strength_of_recommendation": "Conditional Recommendation",
                }
            ],
        },
        "sources": [
            {
                "source_id": "SRC-01",
                "title": "PREHAB trial on colorectal prehabilitation",
                "author_or_institution": "Molenaar CJ, van Rooijen SJ, et al.",
                "year": 2023,
                "source_type": "randomized_trial",
                "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/",
            }
        ],
        "areas_of_agreement": [
            {
                "domain": "Functional exercise capacity",
                "consensus_summary": "Both agree multimodal prehabilitation preserves physical reserve.",
                "supporting_sources": ["SRC-01"],
            }
        ],
        "areas_of_disagreement": [],
        "uncertainty": [
            {
                "topic": "Intervention duration",
                "uncertainty_rationale": "Optimal duration prior to cancer surgery remains debated (2 vs 4 weeks).",
            }
        ],
        "limitations": ["Limited blinding feasible in exercise interventions."],
        "discussion_questions": ["What criteria define high-risk patients for targeted prehabilitation?"],
        "safety_disclaimer": "Educational research demonstration only. Not individualized clinical advice.",
    }

    normalized = normalize_brief_structure(complete_brief)
    # Must strictly validate against coordinator schema
    jsonschema.validate(instance=normalized, schema=schema)

    # Must also instantiate StructuredEvidenceBriefModel without error
    brief_model = StructuredEvidenceBriefModel(**normalized)
    assert brief_model.research_question == complete_brief["research_question"]

    # Also validates when candidate references are omitted
    brief_with_omissions = {
        "research_question": "What is the evidence on novel surgical robotics?",
        "evidence_findings": {
            "summary": "Candidate evidence unverified.",
            "key_study_findings": [{"study_title": "Incomplete study"}],
        },
        "guideline_findings": {
            "summary": "Candidate guideline unverified.",
            "guideline_statements": [{"guideline_title": "Incomplete guideline"}],
        },
    }
    norm_omitted = normalize_brief_structure(brief_with_omissions)
    jsonschema.validate(instance=norm_omitted, schema=schema)
