"""Coordinator Agent real ADK implementation.

Orchestrates multi-agent research workflow, delegates to Evidence and Guideline
agents via ADK single-turn sub_agents, and synthesizes structured evidence briefs.
"""

from typing import Optional

from google.adk import Agent

from adk.config import (
    get_default_generate_content_config,
    get_gemini_model,
    load_instruction_file,
)

from adk.evidence.agent import create_evidence_agent
from adk.guideline.agent import create_guideline_agent
from adk.schemas import StructuredEvidenceBriefModel


def create_coordinator_agent(
    model_name: Optional[str] = None,
    evidence_agent: Optional[Agent] = None,
    guideline_agent: Optional[Agent] = None,
) -> Agent:
    """Create the orchestrating Coordinator Agent.

    Architecture:
        - Coordinator Agent holds NO direct Search tools.
        - Coordinator delegates scholarly research to Evidence Agent via single-turn subagent.
        - Coordinator delegates guideline research to Guideline Agent via single-turn subagent.
        - Output is strictly constrained to StructuredEvidenceBriefModel (JSON Schema).
    """
    ev_agent = evidence_agent or create_evidence_agent()
    gd_agent = guideline_agent or create_guideline_agent()

    instruction = load_instruction_file("agents/coordinator/instructions.md")

    return Agent(
        name="coordinator",
        description=(
            "Master surgical evidence synthesis coordinator. Normalizes user inquiries into "
            "PICOT scope, delegates to specialist Evidence and Guideline agents, reconciles "
            "consensus and discrepancies, and generates a structured Evidence Brief conforming "
            "to output-schema.json."
        ),
        model=get_gemini_model(model_name),
        instruction=instruction,
        sub_agents=[
            ev_agent,
            gd_agent,
        ],
        generate_content_config=get_default_generate_content_config(),
        output_schema=StructuredEvidenceBriefModel,
    )

def get_root_agent() -> Agent:
    """Return a Coordinator Agent instance."""
    return create_coordinator_agent()


# Expose root_agent instance for native ADK AgentEvaluator discovery
root_agent = create_coordinator_agent()
