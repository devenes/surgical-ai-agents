"""Pydantic schemas and typed specialist contracts for the Surgical AI multi-agent system.

Matches agents/*/output-schema.json specifications and provides typed input/output
contracts for Evidence Agent and Guideline Agent.
"""

import urllib.parse
from typing import Any, List, Optional
from pydantic import BaseModel, Field, field_validator

GENERIC_TITLES = {
    "clinical study",
    "clinical guideline",
    "clinical practice guideline",
    "clinical source",
    "clinical reference",
    "clinical trial",
    "study",
    "guideline",
    "unknown",
    "n/a",
    "none",
}

GENERIC_AUTHORS = {
    "investigators",
    "authors",
    "author",
    "surgical society",
    "society",
    "organization",
    "unknown",
    "n/a",
    "none",
}

GENERIC_FINDINGS = {
    "findings reported.",
    "recommendation provided.",
    "none",
    "n/a",
    "unknown",
}

VALID_SOURCE_TYPES = {
    "systematic_review",
    "randomized_trial",
    "observational_study",
    "practice_guideline",
    "consensus_statement",
    "other",
}


def validate_title(val: Any) -> Optional[str]:
    """Validate that title is a non-empty string and not a fabricated generic placeholder."""
    if not isinstance(val, str):
        return None
    cleaned = val.strip()
    if len(cleaned) < 3 or cleaned.lower() in GENERIC_TITLES:
        return None
    return cleaned


def validate_author_or_org(val: Any) -> Optional[str]:
    """Validate that author or issuing organization is non-empty and not a placeholder."""
    if not isinstance(val, str):
        return None
    cleaned = val.strip()
    if len(cleaned) < 2 or cleaned.lower() in GENERIC_AUTHORS:
        return None
    return cleaned


def validate_year(val: Any) -> Optional[int]:
    """Validate that publication year is a valid positive integer in a plausible range."""
    if isinstance(val, bool) or val is None:
        return None
    try:
        if isinstance(val, str):
            val_str = val.strip()
            if not val_str.isdigit():
                if len(val_str) >= 4 and val_str[:4].isdigit():
                    val = int(val_str[:4])
                else:
                    return None
            else:
                val = int(val_str)
        elif isinstance(val, (int, float)):
            val = int(val)
        else:
            return None

        if 1800 <= val <= 2100:
            return val
        return None
    except (ValueError, TypeError, OverflowError):
        return None


def validate_url(val: Any) -> Optional[str]:
    """Validate that URL is an absolute HTTP/HTTPS URL and not a generic homepage/placeholder."""
    if not isinstance(val, str):
        return None
    cleaned = val.strip()
    if not cleaned or cleaned.startswith("#"):
        return None
    try:
        parsed = urllib.parse.urlparse(cleaned)
        if parsed.scheme.lower() not in ("http", "https"):
            return None
        netloc = parsed.netloc.lower()
        if not netloc or "." not in netloc:
            return None

        path = parsed.path.rstrip("/")
        # Reject generic PubMed homepage
        if netloc in ("pubmed.ncbi.nlm.nih.gov", "www.ncbi.nlm.nih.gov", "ncbi.nlm.nih.gov"):
            if path in ("", "/pubmed"):
                return None
        # Reject generic guidelines.org placeholder
        if netloc in ("guidelines.org", "www.guidelines.org"):
            if path in ("",):
                return None

        return cleaned
    except Exception:
        return None


def map_source_type(val: Any) -> str:
    """Map evidence/source type string to output-schema enum without manufacturing trial status."""
    if not isinstance(val, str) or not val.strip():
        return "other"
    low = val.lower().strip()
    if low in VALID_SOURCE_TYPES:
        return low
    if "guideline" in low or "practice" in low:
        return "practice_guideline"
    if "consensus" in low or "statement" in low or "advisory" in low:
        return "consensus_statement"
    if "meta" in low or "systematic" in low or "review" in low:
        return "systematic_review"
    if "random" in low or "trial" in low or "rct" in low:
        return "randomized_trial"
    if "cohort" in low or "observational" in low or "prospective" in low or "retrospective" in low:
        return "observational_study"
    return "other"


# =============================================================================
# Evidence Agent Contracts
# =============================================================================


class EvidenceQueryInput(BaseModel):
    """Structured input contract for Evidence Agent delegation."""

    population: str = Field(
        description="Target surgical patient cohort (e.g. adults undergoing elective colorectal surgery)"
    )
    intervention: str = Field(
        description="Specific surgical protocol, technique, or perioperative bundle (e.g. multimodal prehabilitation)"
    )
    comparator: str = Field(
        default="standard care", description="Comparator or control arm (e.g. conventional care)"
    )
    outcomes: List[str] = Field(
        description="Key clinical and surgical endpoints of interest (e.g. 30-day morbidity, functional recovery)"
    )
    study_designs: List[str] = Field(
        default_factory=lambda: [
            "randomized controlled trial",
            "systematic review and meta-analysis",
        ],
        description="Target evidence tiers to prioritize",
    )
    time_range: Optional[str] = Field(
        default="recent 5-10 years", description="Publication time window"
    )


class StudyFindingModel(BaseModel):
    study_title: str
    authors_or_organization: str
    publication_year: int
    evidence_type: str
    key_findings: str
    url: str
    primary_endpoints: List[str] = Field(default_factory=list)

    @field_validator("study_title")
    @classmethod
    def check_study_title(cls, v: str) -> str:
        res = validate_title(v)
        if not res:
            raise ValueError(f"Invalid or fabricated study title: {v!r}")
        return res

    @field_validator("authors_or_organization")
    @classmethod
    def check_authors(cls, v: str) -> str:
        res = validate_author_or_org(v)
        if not res:
            raise ValueError(f"Invalid or fabricated author/organization: {v!r}")
        return res

    @field_validator("publication_year")
    @classmethod
    def check_year(cls, v: int) -> int:
        res = validate_year(v)
        if res is None:
            raise ValueError(f"Invalid publication year: {v!r}")
        return res

    @field_validator("url")
    @classmethod
    def check_url(cls, v: str) -> str:
        res = validate_url(v)
        if not res:
            raise ValueError(f"Invalid, relative, or generic URL: {v!r}")
        return res


class EvidenceAgentOutputModel(BaseModel):
    """Structured output contract produced by Evidence Agent."""

    query_summary: str = Field(description="Normalized summary of the literature query executed")
    not_found: bool = Field(
        default=False, description="True if no reliable trial evidence was identified"
    )
    not_found_reason: Optional[str] = Field(
        default="", description="Detailed rationale if evidence was not found"
    )
    overall_evidence_quality: str = Field(
        default="moderate",
        description="Aggregate evidence quality assessment (high, moderate, low, very_low)",
    )
    studies: List[StudyFindingModel] = Field(
        default_factory=list, description="Verified scientific publications"
    )
    evidence_synthesis: str = Field(description="Narrative synthesis of identified studies")


# =============================================================================
# Guideline Agent Contracts
# =============================================================================


class GuidelineQueryInput(BaseModel):
    """Structured input contract for Guideline Agent delegation."""

    clinical_topic: str = Field(
        description="Specific surgical topic or clinical decision domain (e.g. prehabilitation in elective colorectal surgery)"
    )
    target_population: str = Field(description="Patient cohort and surgical setting addressed")
    target_societies: List[str] = Field(
        default_factory=lambda: ["ASCRS", "ERAS Society", "SAGES", "EAES", "ESCP", "NICE"],
        description="Recognized surgical professional bodies and guideline agencies to query",
    )
    specific_questions: List[str] = Field(
        default_factory=list,
        description="Specific guideline questions regarding recommendations, grades, and implementation",
    )


class GuidelineStatementModel(BaseModel):
    organization: str
    guideline_title: str
    publication_or_update_year: int
    recommendation_summary: str
    url: str
    strength_of_recommendation: Optional[str] = ""

    @field_validator("organization")
    @classmethod
    def check_org(cls, v: str) -> str:
        res = validate_author_or_org(v)
        if not res:
            raise ValueError(f"Invalid or fabricated organization: {v!r}")
        return res

    @field_validator("guideline_title")
    @classmethod
    def check_guideline_title(cls, v: str) -> str:
        res = validate_title(v)
        if not res:
            raise ValueError(f"Invalid or fabricated guideline title: {v!r}")
        return res

    @field_validator("publication_or_update_year")
    @classmethod
    def check_guideline_year(cls, v: int) -> int:
        res = validate_year(v)
        if res is None:
            raise ValueError(f"Invalid guideline year: {v!r}")
        return res

    @field_validator("url")
    @classmethod
    def check_guideline_url(cls, v: str) -> str:
        res = validate_url(v)
        if not res:
            raise ValueError(f"Invalid, relative, or generic guideline URL: {v!r}")
        return res


class GuidelineAgentOutputModel(BaseModel):
    """Structured output contract produced by Guideline Agent."""

    query_summary: str = Field(description="Summary of the guideline scope queried")
    not_found: bool = Field(
        default=False, description="True if no official society guidelines were verified"
    )
    not_found_reason: Optional[str] = Field(
        default="", description="Detailed rationale if guidelines were not found"
    )
    guidelines: List[GuidelineStatementModel] = Field(
        default_factory=list, description="Catalog of verified society guidelines"
    )
    guideline_synthesis: str = Field(
        description="Narrative synthesis of institutional positions and consensus"
    )


# =============================================================================
# Coordinator Agent Contracts & Master Evidence Brief
# =============================================================================


class ResearchScopeModel(BaseModel):
    population: str = Field(description="Target surgical patient population")
    context: str = Field(description="Clinical setting (elective, emergency, inpatient)")
    intervention_exposure: str = Field(description="Surgical protocol or intervention")
    comparator: str = Field(description="Comparator or control arm")
    outcomes: List[str] = Field(description="Target surgical and clinical endpoints")
    time_range: Optional[str] = Field(
        default="recent 5-10 years", description="Time window evaluated"
    )


class NotFoundStatusModel(BaseModel):
    evidence_not_found: bool = Field(
        description="True if no reliable peer-reviewed evidence was identified"
    )
    guidelines_not_found: bool = Field(
        description="True if no formal society guidelines were found"
    )
    details: Optional[str] = Field(default="", description="Explanation of missing data")


class EvidenceFindingsModel(BaseModel):
    summary: str
    key_study_findings: List[StudyFindingModel] = Field(default_factory=list)


class GuidelineFindingsModel(BaseModel):
    summary: str
    guideline_statements: List[GuidelineStatementModel] = Field(default_factory=list)


class SourceCitationModel(BaseModel):
    source_id: str = Field(description="e.g. SRC-01")
    title: str
    author_or_institution: str
    year: int
    source_type: str
    url: str

    @field_validator("title")
    @classmethod
    def check_source_title(cls, v: str) -> str:
        res = validate_title(v)
        if not res:
            raise ValueError(f"Invalid or fabricated citation title: {v!r}")
        return res

    @field_validator("author_or_institution")
    @classmethod
    def check_source_author(cls, v: str) -> str:
        res = validate_author_or_org(v)
        if not res:
            raise ValueError(f"Invalid or fabricated author/institution: {v!r}")
        return res

    @field_validator("year")
    @classmethod
    def check_source_year(cls, v: int) -> int:
        res = validate_year(v)
        if res is None:
            raise ValueError(f"Invalid citation year: {v!r}")
        return res

    @field_validator("url")
    @classmethod
    def check_source_url(cls, v: str) -> str:
        res = validate_url(v)
        if not res:
            raise ValueError(f"Invalid, relative, or generic citation URL: {v!r}")
        return res


class AreaOfAgreementModel(BaseModel):
    domain: str
    consensus_summary: str
    supporting_sources: List[str] = Field(default_factory=list)


class AreaOfDisagreementModel(BaseModel):
    issue: str
    divergence_description: str
    conflicting_sources: List[str] = Field(default_factory=list)


class UncertaintyModel(BaseModel):
    topic: str
    uncertainty_rationale: str


class StructuredEvidenceBriefModel(BaseModel):
    """Structured Evidence Brief conforming to agents/coordinator/output-schema.json."""

    research_question: str
    research_scope: ResearchScopeModel
    not_found: NotFoundStatusModel
    evidence_findings: EvidenceFindingsModel
    guideline_findings: GuidelineFindingsModel
    sources: List[SourceCitationModel] = Field(default_factory=list)
    areas_of_agreement: List[AreaOfAgreementModel] = Field(default_factory=list)
    areas_of_disagreement: List[AreaOfDisagreementModel] = Field(default_factory=list)
    uncertainty: List[UncertaintyModel] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    discussion_questions: List[str] = Field(default_factory=list)
    safety_disclaimer: str
