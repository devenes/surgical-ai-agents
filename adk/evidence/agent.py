"""Evidence Agent real ADK implementation.

Researches peer-reviewed surgical literature with Google Search grounding.
"""

from typing import Optional

from google.adk import Agent
from google.adk.tools import google_search, url_context

from adk.config import (
    get_default_generate_content_config,
    get_gemini_model,
    load_instruction_file,
)
from adk.schemas import EvidenceQueryInput


def create_evidence_agent(
    model_name: Optional[str] = None,
    use_url_context: bool = False,
) -> Agent:

    """Create a fully grounded Evidence Agent instance."""
    tools = [google_search]
    if use_url_context:
        tools.append(url_context)

    instruction = load_instruction_file("agents/evidence/instructions.md")

    return Agent(
        name="evidence_agent",
        description=(
            "Specialist biomedical literature researcher. Searches peer-reviewed studies, "
            "randomized controlled trials, and systematic reviews via Google Search. "
            "Extracts verified study titles, authors, years, URLs, endpoints, and limitations. "
            "Reports not_found when reliable high-level trial evidence is absent."
        ),
        model=get_gemini_model(model_name),
        instruction=instruction,
        tools=tools,
        generate_content_config=get_default_generate_content_config(),
        mode="single_turn",
        input_schema=EvidenceQueryInput,
    )


