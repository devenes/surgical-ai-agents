"""FastAPI REST Application for Surgical AI Web UI and Multi-Agent Services."""

import os
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.backend.schemas import (
    ComparativeAnalysisRequest,
    ComparativeAnalysisResponse,
    ModelInfo,
    MonolithicDirectRequest,
    MonolithicDirectResponse,
    MultiAgentConsensusRequest,
    MultiAgentConsensusResponse,
    MultimodalInquiryRequest,
    MultimodalInquiryResponse,
    PICOTDecomposeRequest,
    PICOTDecomposeResponse,
)
from app.backend.service import AppService

app = FastAPI(
    title="Surgical AI Multi-Agent & Vision API",
    description=(
        "Lightweight FastAPI backend powering educational multimodal vision inspection "
        "and multi-agent evidence synthesis workflows for surgical research."
    ),
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for Streamlit and external frontend consumers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = AppService()


@app.get("/", tags=["General"])
def root() -> Dict[str, str]:
    """Root status greeting with API documentation pointers."""
    return {
        "service": "Surgical AI Multi-Agent & Multimodal API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health", tags=["Diagnostics"])
def health_check() -> Dict[str, Any]:
    """Check backend operational health, configuration, and credential presence."""
    has_api_key = bool(os.environ.get("GOOGLE_API_KEY"))
    has_project = bool(
        os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )

    return {
        "status": "healthy",
        "service": "surgical-ai-api",
        "credentials_configured": has_api_key or has_project,
        "auth_mode": "api_key"
        if has_api_key
        else ("adc_vertex" if has_project else "offline_simulation_only"),
        "default_region": os.environ.get("GOOGLE_CLOUD_LOCATION")
        or os.environ.get("GOOGLE_CLOUD_REGION", "us"),
        "default_project": os.environ.get("GOOGLE_CLOUD_PROJECT", "auto-inferred"),
        "subagent_architecture": "Coordinator + Evidence Specialist (Sub-Agent 1) + Guideline Specialist (Sub-Agent 2)",
    }


@app.get("/api/models", response_model=List[ModelInfo], tags=["Catalog"])
def list_models() -> List[ModelInfo]:
    """List supported Gemini and multimodal models with feature capabilities."""
    return service.get_models()


@app.get("/api/presets", tags=["Catalog"])
def get_presets() -> Dict[str, Any]:
    """Fetch pre-configured surgical inquiries and reference schematic images."""
    inquiries, images = service.get_presets()
    return {
        "inquiries": inquiries,
        "images": images,
    }


@app.get("/api/presets/image/{image_id}", tags=["Catalog"])
def get_preset_image(image_id: str):
    """Retrieve raw bytes of a bundled schematic image."""
    img_bytes = service.get_preset_image_bytes(image_id)
    if not img_bytes:
        raise HTTPException(status_code=404, detail=f"Preset image '{image_id}' not found.")
    return Response(content=img_bytes, media_type="image/png")


@app.post("/api/multimodal", response_model=MultimodalInquiryResponse, tags=["Multimodal Vision"])
def execute_multimodal_inquiry(req: MultimodalInquiryRequest) -> MultimodalInquiryResponse:
    """Analyze an image (upload or preset) combined with an educational prompt."""
    try:
        return service.execute_multimodal(req)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multimodal inquiry failed: {str(exc)}",
        ) from exc


@app.post(
    "/api/agents/consensus",
    response_model=MultiAgentConsensusResponse,
    tags=["Multi-Agent Orchestration"],
)
def execute_multiagent_consensus(req: MultiAgentConsensusRequest) -> MultiAgentConsensusResponse:
    """Run Coordinator Agent with Evidence (Sub-Agent 1) and Guideline (Sub-Agent 2) specialists."""
    try:
        return service.execute_multiagent_consensus(req)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multi-agent consensus failed: {str(exc)}",
        ) from exc


@app.post(
    "/api/agents/decompose",
    response_model=PICOTDecomposeResponse,
    tags=["Multi-Agent Orchestration"],
)
def decompose_picot_inquiry(req: PICOTDecomposeRequest) -> PICOTDecomposeResponse:
    """Decompose raw clinical text into formal surgical PICOT research scope."""
    try:
        return service.decompose_picot(req)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decomposition failed: {str(exc)}",
        ) from exc


@app.post(
    "/api/agents/direct",
    response_model=MonolithicDirectResponse,
    tags=["Multi-Agent Orchestration"],
)
def execute_monolithic_direct(req: MonolithicDirectRequest) -> MonolithicDirectResponse:
    """Run direct zero-shot query without agents or grounding tools (monolithic baseline)."""
    try:
        return service.execute_monolithic_direct(req)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Direct monolithic execution failed: {str(exc)}",
        ) from exc


@app.post(
    "/api/agents/compare",
    response_model=ComparativeAnalysisResponse,
    tags=["Multi-Agent Orchestration"],
)
def execute_comparative_analysis(req: ComparativeAnalysisRequest) -> ComparativeAnalysisResponse:
    """Run head-to-head comparison: Monolithic Baseline vs 2-SubAgent Architecture."""
    try:
        return service.execute_comparative_analysis(req)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparative analysis failed: {str(exc)}",
        ) from exc
