"""Offline unit tests for agent construction and configuration."""

from pathlib import Path
from adk.config import load_instruction_file
from adk.coordinator.agent import create_coordinator_agent
from adk.evidence.agent import create_evidence_agent
from adk.guideline.agent import create_guideline_agent
from google.adk.tools import AgentTool

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_instruction_files_load_properly():
    coord_inst = load_instruction_file("agents/coordinator/instructions.md")
    evid_inst = load_instruction_file("agents/evidence/instructions.md")
    guide_inst = load_instruction_file("agents/guideline/instructions.md")

    assert "Coordinator Agent" in coord_inst
    assert "PICOT" in coord_inst
    assert "Evidence Agent" in evid_inst
    assert "Hierarchy" in evid_inst
    assert "Guideline Agent" in guide_inst
    assert "ASCRS" in guide_inst


def test_evidence_agent_construction():
    agent = create_evidence_agent()
    assert agent.name == "evidence_agent"
    assert any("google_search" in str(t).lower() for t in agent.tools)
    assert agent.input_schema is not None


def test_guideline_agent_construction():
    agent = create_guideline_agent()
    assert agent.name == "guideline_agent"
    assert any("google_search" in str(t).lower() for t in agent.tools)
    assert agent.input_schema is not None


def test_coordinator_agent_construction():
    agent = create_coordinator_agent()
    assert agent.name == "coordinator"
    # Coordinator must NOT hold direct google_search tool
    for tool in agent.tools:
        assert "google_search" not in getattr(tool, "name", str(tool)).lower()
    # Coordinator must hold subagents
    assert len(agent.sub_agents) == 2
    subagent_names = [sa.name for sa in agent.sub_agents]
    assert "evidence_agent" in subagent_names
    assert "guideline_agent" in subagent_names
    # Subagents are automatically exposed as SingleTurnAgentTool in tools
    assert any(isinstance(t, AgentTool) for t in agent.tools)
    assert agent.output_schema is not None
