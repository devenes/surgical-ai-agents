"""Pydantic schemas for the FastAPI backend and Web UI."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    """Metadata regarding an available Gemini model."""

    id: str
    display_name: str
    description: str
    supports_vision: bool = True
    supports_thinking: bool = False
    default_temperature: float = 0.4
    recommended_use_case: str = ""


class MultimodalInquiryRequest(BaseModel):
    """Request for multimodal (vision + text) inference."""

    prompt: str = Field(
        ...,
        description="Text prompt or inquiry to accompany the image",
        min_length=1,
    )
    image_base64: Optional[str] = Field(
        None,
        description="Base64-encoded image data",
    )
    image_mime_type: str = Field(
        "image/png",
        description="MIME type of the uploaded image (e.g., image/png, image/jpeg)",
    )
    preset_image_id: Optional[str] = Field(
        None,
        description="Optional ID of a bundled preset image",
    )
    video_base64: Optional[str] = Field(
        None,
        description="Base64-encoded video data",
    )
    video_mime_type: str = Field(
        "video/mp4",
        description="MIME type of the video (e.g., video/mp4)",
    )
    preset_video_id: Optional[str] = Field(
        None,
        description="Optional ID of a bundled preset video",
    )
    model: str = Field(
        "gemini-2.5-flash",
        description="Model ID to invoke",
    )
    temperature: float = Field(
        0.4,
        ge=0.0,
        le=2.0,
        description="Sampling temperature",
    )
    top_p: float = Field(
        0.95,
        ge=0.0,
        le=1.0,
        description="Top-p nucleus sampling",
    )
    max_output_tokens: int = Field(
        2048,
        ge=64,
        le=8192,
        description="Maximum tokens to generate",
    )
    thinking_budget: Optional[int] = Field(
        None,
        ge=0,
        le=24576,
        description="Thinking budget limit (tokens) for models supporting thinking",
    )
    mock_mode: bool = Field(
        False,
        description="If True, returns deterministic mock response without making live API calls (0 tokens)",
    )


class MultimodalInquiryResponse(BaseModel):
    """Response returned from multimodal visual inference."""

    text: str = Field(..., description="Generated text response from the model")
    model: str = Field(..., description="Model identifier used")
    latency_ms: float = Field(..., description="Execution latency in milliseconds")
    token_estimate: int = Field(default=0, description="Estimated total tokens used")
    visual_elements_detected: List[str] = Field(
        default_factory=list,
        description="Key anatomical/visual elements detected or discussed",
    )
    safety_disclaimer: str = Field(
        "For educational and research demonstration purposes only. Does not provide clinical diagnosis or patient management recommendations.",
        description="Standard medical/educational safety disclaimer",
    )


class SubAgentExecutionStep(BaseModel):
    """Record of an individual step in the multi-agent pipeline."""

    agent_name: str
    step_type: str  # "decomposition", "evidence_search", "guideline_search", "synthesis"
    status: str  # "pending", "running", "completed", "skipped", "error"
    duration_ms: float = 0.0
    summary: str = ""
    details: Dict[str, Any] = Field(default_factory=dict)


class MultiAgentConsensusRequest(BaseModel):
    """Request to execute the multi-agent research workflow."""

    question: str = Field(
        ...,
        description="Clinical or surgical research question",
        min_length=5,
    )
    model: str = Field(
        "gemini-2.5-flash",
        description="Model ID to invoke for agents",
    )
    enable_evidence_agent: bool = Field(
        True,
        description="Whether to run Sub-Agent 1 (Evidence Specialist)",
    )
    enable_guideline_agent: bool = Field(
        True,
        description="Whether to run Sub-Agent 2 (Guideline Specialist)",
    )
    mock_mode: bool = Field(
        False,
        description="If True, returns deterministic simulated consensus without spending tokens",
    )


class MultiAgentConsensusResponse(BaseModel):
    """Structured response representing multi-agent consensus brief."""

    research_question: str
    normalized_picot: Dict[str, Any]
    evidence_findings: Dict[str, Any]
    guideline_findings: Dict[str, Any]
    consensus_matrix: Dict[str, Any]
    sources: List[Dict[str, Any]]
    final_synthesis: str
    execution_steps: List[SubAgentExecutionStep]
    latency_ms: float
    safety_disclaimer: str


class PICOTDecomposeRequest(BaseModel):
    """Request to decompose a question into PICOT format."""

    question: str = Field(..., min_length=5)
    model: str = Field("gemini-2.5-flash")
    mock_mode: bool = Field(False)


class PICOTDecomposeResponse(BaseModel):
    """Structured PICOT decomposition of a research inquiry."""

    population: str
    intervention: str
    comparator: str
    outcomes: List[str]
    time_range: str
    search_keywords: List[str]
    raw_question: str


class PresetInquiry(BaseModel):
    """Pre-configured clinical question for educational benchmarks and demo."""

    id: str
    title: str
    question: str
    category: str
    case_type: str = "normal_synthesis"  # normal_synthesis, missing_evidence, missing_guideline, evidence_conflict, safety_refusal
    pedagogical_lesson: str = ""
    expected_without_agent_flaw: str = ""
    expected_with_agent_benefit: str = ""
    recommended_model: str = "gemini-2.5-flash"


class PresetImage(BaseModel):
    """Pre-bundled image for quick vision demonstration."""

    id: str
    title: str
    filename: str
    description: str
    suggested_prompts: List[str]


class PresetVideo(BaseModel):
    """Pre-bundled medical video for video-language multimodal demonstration."""

    id: str
    title: str
    filename: str
    description: str
    duration_sec: Optional[float] = None
    suggested_prompts: List[str]


class MonolithicDirectRequest(BaseModel):
    """Request for direct zero-shot query without agents or tools."""

    question: str = Field(..., min_length=5)
    model: str = Field("gemini-2.5-flash")
    mock_mode: bool = Field(False)


class MonolithicDirectResponse(BaseModel):
    """Result of a direct monolithic model call without multi-agent decomposition."""

    raw_response: str
    model: str
    latency_ms: float
    hallucination_risk: str  # "High", "Moderate", "Low"
    grounding_status: str  # "Unverified / Static Training Weights"
    safety_boundary_status: str  # "Violated (Direct Patient Advice)", "Speculative", "Compliant"
    citations_audited: List[str] = Field(default_factory=list)
    key_flaws_noted: List[str] = Field(default_factory=list)


class ComparativeAuditScorecard(BaseModel):
    """Side-by-side evaluation dimension in comparative analysis."""

    dimension: str
    without_agent_rating: str
    with_agent_rating: str
    explanation: str


class ComparativeAnalysisRequest(BaseModel):
    """Request to execute a head-to-head comparison: Without Agents vs With Agents."""

    question: str = Field(..., min_length=5)
    case_id: Optional[str] = None
    model: str = Field("gemini-2.5-flash")
    mock_mode: bool = Field(False)


class ComparativeAnalysisResponse(BaseModel):
    """Complete comparative result comparing monolithic vs multi-agent execution."""

    case_id: Optional[str] = None
    case_title: str
    case_type: str
    question: str
    without_agent: MonolithicDirectResponse
    with_agent: MultiAgentConsensusResponse
    scorecard: List[ComparativeAuditScorecard]
    pedagogical_takeaway: str
