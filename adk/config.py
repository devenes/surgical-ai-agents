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
DEFAULT_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_instruction_file(relative_path: str) -> str:
    """Load system instructions from markdown file in repository."""
    full_path = REPO_ROOT / relative_path
    if not full_path.exists():
        raise FileNotFoundError(f"Instruction file not found at {full_path}")
    return full_path.read_text(encoding="utf-8")


def get_default_generate_content_config(
    model_name: Optional[str] = None,
    thinking_level: Optional[str] = "MEDIUM",
    thinking_budget: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
):
    """Return GenerateContentConfig configured safely for the target model architecture.

    Note:
        - Gemini 3.8+ models: Reasoning depth is controlled exclusively via
          thinking_config(thinking_level='MEDIUM'|'LOW'|'HIGH'|'MINIMAL'). Legacy sampling
          parameters (temperature, top_p) are omitted as they are ignored/deprecated.
        - Gemini 2.5 models: Reasoning depth is controlled via thinking_budget (tokens).
          CRITICAL: Gemini 2.5 does NOT support thinking_level and returns 400 INVALID_ARGUMENT
          if thinking_level is passed. Any thinking_level is mapped to a token budget and
          never passed directly as thinking_level.
    """
    from google.genai import types

    chosen_model = (model_name or DEFAULT_MODEL).lower()

    # Gemini 3.x series (e.g. gemini-3.8-flash)
    if "gemini-3." in chosen_model:
        eff_level = thinking_level or "MEDIUM"
        if isinstance(eff_level, str) and eff_level.upper() in ("OFF", "NONE", "DISABLED"):
            thinking_config = None
        else:
            thinking_config = types.ThinkingConfig(thinking_level=eff_level.upper())
        return types.GenerateContentConfig(thinking_config=thinking_config)

    # Gemini 2.5 series (e.g. gemini-2.5-flash, gemini-2.5-pro)
    if "gemini-2.5" in chosen_model:
        eff_budget = thinking_budget
        if eff_budget is None and thinking_level and str(thinking_level).upper() not in ("OFF", "NONE", "DISABLED"):
            level_budget_map = {"MINIMAL": 512, "LOW": 1024, "MEDIUM": 2048, "HIGH": 4096}
            eff_budget = level_budget_map.get(str(thinking_level).upper(), 2048)

        thinking_config = types.ThinkingConfig(thinking_budget=eff_budget) if eff_budget is not None else None

        config_kwargs = {}
        if thinking_config is not None:
            config_kwargs["thinking_config"] = thinking_config
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        if top_p is not None:
            config_kwargs["top_p"] = top_p
        if max_output_tokens is not None:
            config_kwargs["max_output_tokens"] = max_output_tokens

        return types.GenerateContentConfig(**config_kwargs)

    # Other models (e.g. gemini-2.0-flash)
    config_kwargs = {}
    if temperature is not None:
        config_kwargs["temperature"] = temperature
    if top_p is not None:
        config_kwargs["top_p"] = top_p
    if max_output_tokens is not None:
        config_kwargs["max_output_tokens"] = max_output_tokens

    return types.GenerateContentConfig(**config_kwargs)


def get_gemini_model(
    model_name: Optional[str] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> Gemini:
    """Instantiate a configured Gemini model connecting to Vertex AI via ADC."""
    chosen_model = model_name or DEFAULT_MODEL
    chosen_project = project or DEFAULT_PROJECT
    chosen_location = location or DEFAULT_LOCATION

    # Map location appropriately: Gemini 2.x models are hosted in us-central1; Gemini 3.x models in us
    if chosen_location == "us" and ("gemini-2." in chosen_model or "gemini-1." in chosen_model):
        chosen_location = "us-central1"
    elif chosen_location == "us-central1" and "gemini-3." in chosen_model:
        chosen_location = "us"

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
