"""Guideline Agent real ADK implementation.

Retrieves and analyzes clinical practice guidelines and society consensus statements.
"""

from typing import Optional

from google.adk import Agent
from google.adk.tools import google_search, url_context

from adk.config import (
    get_default_generate_content_config,
    get_gemini_model,
    load_instruction_file,
)
from adk.schemas import GuidelineQueryInput


def create_guideline_agent(
    model_name: Optional[str] = None,
    use_url_context: bool = False,
    thinking_level: Optional[str] = None,
    thinking_budget: Optional[int] = None,
) -> Agent:
    """Create a fully grounded Guideline Agent instance."""
    tools = [google_search]
    if use_url_context:
        tools.append(url_context)

    instruction = load_instruction_file("agents/guideline/instructions.md")

    return Agent(
        name="guideline_agent",
        description=(
            "Specialist surgical practice guidelines researcher. Searches official recommendations, "
            "consensus statements, and clinical practice parameters issued by recognized national "
            "and international surgical societies (e.g. ASCRS, ERAS Society, SAGES, EAES, NICE). "
            "Extracts organization names, guideline titles, publication years, graded recommendations, "
            "and verified URLs. Reports not_found when formal guidelines do not exist."
        ),
        model=get_gemini_model(model_name),
        instruction=instruction,
        tools=tools,
        generate_content_config=get_default_generate_content_config(
            model_name=model_name,
            thinking_level=thinking_level,
            thinking_budget=thinking_budget,
        ),
        mode="single_turn",
        input_schema=GuidelineQueryInput,
    )
