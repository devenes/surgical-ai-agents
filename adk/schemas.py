"""Pydantic schemas and typed specialist contracts for the Surgical AI multi-agent system.

Matches agents/*/output-schema.json specifications and provides typed input/output
contracts for Evidence Agent and Guideline Agent.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# Evidence Agent Contracts
# =============================================================================

class EvidenceQueryInput(BaseModel):
    """Structured input contract for Evidence Agent delegation."""

    population: str = Field(description="Target surgical patient cohort (e.g. adults undergoing elective colorectal surgery)")
    intervention: str = Field(description="Specific surgical protocol, technique, or perioperative bundle (e.g. multimodal prehabilitation)")
    comparator: str = Field(default="standard care", description="Comparator or control arm (e.g. conventional care)")
    outcomes: List[str] = Field(description="Key clinical and surgical endpoints of interest (e.g. 30-day morbidity, functional recovery)")
    study_designs: List[str] = Field(
        default_factory=lambda: ["randomized controlled trial", "systematic review and meta-analysis"],
        description="Target evidence tiers to prioritize",
    )
    time_range: Optional[str] = Field(default="recent 5-10 years", description="Publication time window")


class StudyFindingModel(BaseModel):
    study_title: str
    authors_or_organization: str
    publication_year: int
    evidence_type: str
    key_findings: str
    url: str
    primary_endpoints: List[str] = Field(default_factory=list)


class EvidenceAgentOutputModel(BaseModel):
    """Structured output contract produced by Evidence Agent."""

    query_summary: str = Field(description="Normalized summary of the literature query executed")
    not_found: bool = Field(default=False, description="True if no reliable trial evidence was identified")
    not_found_reason: Optional[str] = Field(default="", description="Detailed rationale if evidence was not found")
    overall_evidence_quality: str = Field(default="moderate", description="Aggregate evidence quality assessment (high, moderate, low, very_low)")
    studies: List[StudyFindingModel] = Field(default_factory=list, description="Verified scientific publications")
    evidence_synthesis: str = Field(description="Narrative synthesis of identified studies")


# =============================================================================
# Guideline Agent Contracts
# =============================================================================

class GuidelineQueryInput(BaseModel):
    """Structured input contract for Guideline Agent delegation."""

    clinical_topic: str = Field(description="Specific surgical topic or clinical decision domain (e.g. prehabilitation in elective colorectal surgery)")
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


class GuidelineAgentOutputModel(BaseModel):
    """Structured output contract produced by Guideline Agent."""

    query_summary: str = Field(description="Summary of the guideline scope queried")
    not_found: bool = Field(default=False, description="True if no official society guidelines were verified")
    not_found_reason: Optional[str] = Field(default="", description="Detailed rationale if guidelines were not found")
    guidelines: List[GuidelineStatementModel] = Field(default_factory=list, description="Catalog of verified society guidelines")
    guideline_synthesis: str = Field(description="Narrative synthesis of institutional positions and consensus")


# =============================================================================
# Coordinator Agent Contracts & Master Evidence Brief
# =============================================================================

class ResearchScopeModel(BaseModel):
    population: str = Field(description="Target surgical patient population")
    context: str = Field(description="Clinical setting (elective, emergency, inpatient)")
    intervention_exposure: str = Field(description="Surgical protocol or intervention")
    comparator: str = Field(description="Comparator or control arm")
    outcomes: List[str] = Field(description="Target surgical and clinical endpoints")
    time_range: Optional[str] = Field(default="recent 5-10 years", description="Time window evaluated")


class NotFoundStatusModel(BaseModel):
    evidence_not_found: bool = Field(description="True if no reliable peer-reviewed evidence was identified")
    guidelines_not_found: bool = Field(description="True if no formal society guidelines were found")
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
