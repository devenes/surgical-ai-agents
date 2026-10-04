"""Configuration and model initialization utilities for Surgical AI ADK."""

import os
from pathlib import Path
from typing import Optional

from google.adk.models.google_llm import Gemini

# Defaults configurable via environment variables
DEFAULT_PROJECT: Optional[str] = os.environ.get("GOOGLE_CLOUD_PROJECT")
DEFAULT_LOCATION: str = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get(
    "GOOGLE_CLOUD_REGION", "us"
)
DEFAULT_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_instruction_file(relative_path: str) -> str:
    """Load system instructions from markdown file in repository."""
    full_path = REPO_ROOT / relative_path
    if not full_path.exists():
        raise FileNotFoundError(f"Instruction file not found at {full_path}")
    return full_path.read_text(encoding="utf-8")


def get_default_generate_content_config(
    thinking_level: str = "MEDIUM",
):
    """Return GenerateContentConfig with verified Gemini 3.8 thinking configuration.

    Note:
        For Gemini 3.8 Flash, legacy sampling parameters (temperature, top_p, top_k)
        are deprecated and ignored by the backend. Reasoning depth and determinism
        are controlled exclusively via thinking_config (thinking_level).
    """
    from google.genai import types

    return types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
    )


def get_gemini_model(
    model_name: Optional[str] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> Gemini:
    """Instantiate a configured Gemini model connecting to Vertex AI via ADC."""
    chosen_model = model_name or DEFAULT_MODEL
    chosen_project = project or DEFAULT_PROJECT
    chosen_location = location or DEFAULT_LOCATION

    client_kwargs = {
        "vertexai": True,
        "location": chosen_location,
    }
    if chosen_project:
        client_kwargs["project"] = chosen_project

    return Gemini(
        model=chosen_model,
        client_kwargs=client_kwargs,
    )
