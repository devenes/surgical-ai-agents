# Google Agent Development Kit (ADK) Setup & Verification Report

## Overview

This document records the exact package names, versions, verification procedures, and API interfaces for the Google Agent Development Kit (ADK) implementation within this repository.

---

## 1. Verified Packages and Versions

All packages are installed in an isolated virtual environment (`.venv`) managed via `uv`:

| Package | Installed Version | Source | Role in System |
| :--- | :--- | :--- | :--- |
| **`google-adk`** | `2.11.0` | PyPI | Official Google Agent Development Kit: agent definitions, `sub_agents`, orchestration, `Runner`, `AgentEvaluator` |
| **`google-genai`** | `2.28.0` | PyPI | Unified Google GenAI SDK powering model calls (Vertex AI backend) |
| **`google-auth`** | `2.59.1` | PyPI | Handles Application Default Credentials (ADC) token generation |
| **`pydantic`** | `2.13.5` | PyPI | Structured data models, typing validation, and output schema generation |
| **`jsonschema`** | `4.26.0` | PyPI | Strict draft-07 JSON Schema validation against repository schemas |
| **`pyyaml`** | `6.0.3` | PyPI | Parsing test case specifications (`evaluations/test-cases.yaml`) |

---

## 2. Installation Commands

To reproduce the exact verified environment from scratch:

```bash
# 1. Create dedicated virtual environment with Python 3.12 (preferred for Google GenAI SDK compatibility)
uv venv --python 3.12

# 2. Install minimal required dependencies
uv pip install -e .
```

---

## 3. Authentication Method

- **Primary Authentication**: Google Cloud **Application Default Credentials (ADC)**.
- **Verification Status**: **VERIFIED & WORKING**.
- **Account**: Developer account authenticated via ADC (`gcloud auth application-default login`)
- **Active GCP Project**: Configured via `GOOGLE_CLOUD_PROJECT` (e.g. `your-project-id`)
- **Target Vertex AI Location**: `us` (US multi-region) / `global`
- **Model Endpoints Verified**:
  - `gemini-3.8-flash` (`publishers/google/models/gemini-3.8-flash`) — Verified available & default (`us`, `global`)
  - `gemini-2.5-flash` (`publishers/google/models/gemini-2.5-flash`) — Verified available (`us-central1`)
- **Credential Storage**: Located strictly in the user home directory (`~/.config/gcloud/application_default_credentials.json`). **No secrets or API keys are stored in this repository.**

---

## 4. Verified ADK APIs & Capabilities

### Modernized Single-Turn Specialist Subagents (`sub_agents`)
In `google-adk 2.11.0`, the recommended delegation pattern uses `mode="single_turn"` with explicit typed `input_schema`:
```python
from google.adk import Agent
from google.adk.tools import google_search
from adk.schemas import EvidenceQueryInput, GuidelineQueryInput

evidence_agent = Agent(
    name="evidence_agent",
    description="Specialist biomedical literature researcher.",
    model=gemini_model,
    instruction=evidence_instruction,
    tools=[google_search],
    mode="single_turn",
    input_schema=EvidenceQueryInput,
)

guideline_agent = Agent(
    name="guideline_agent",
    description="Specialist surgical practice guidelines researcher.",
    model=gemini_model,
    instruction=guideline_instruction,
    tools=[google_search],
    mode="single_turn",
    input_schema=GuidelineQueryInput,
)
```

### Parent Coordinator Orchestration
The parent Coordinator receives subagents via `sub_agents=[...]`. ADK automatically wraps them into typed `_SingleTurnAgentTool` tools on the parent agent:
```python
coordinator = Agent(
    name="coordinator",
    description="Master surgical evidence synthesis coordinator.",
    model=gemini_model,
    instruction=coordinator_instruction,
    sub_agents=[
        evidence_agent,
        guideline_agent,
    ],
    output_schema=StructuredEvidenceBriefModel,
)
```

### Execution Runtime (`google.adk.Runner`)
```python
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

runner = Runner(
    app_name="surgical_ai",
    agent=coordinator,
    session_service=InMemorySessionService(),
    auto_create_session=True,
)

async for event in runner.run_async(
    user_id="surgeon",
    session_id="session-1",
    new_message=types.Content(
        role="user",
        parts=[types.Part.from_text(text=research_question)],
    ),
):
    # Check official ADK validated action response
    if hasattr(event, "actions") and event.actions and event.actions.set_model_response:
        structured_brief = event.actions.set_model_response
```

---

## 5. Critical Version-Specific Behavior & Rules

1. **Vertex AI Tool Limitation (Search vs Function Calling Collision)**:
   In Vertex AI Gemini API, `google_search` cannot be mixed with function declaration tools (`set_model_response`) in the same request. If `output_schema` is placed directly on a subagent that also uses `google_search`, ADK injects `set_model_response`, causing Vertex AI to throw `400 INVALID_ARGUMENT: Multiple tools are supported only when they are all search tools`.
   *Solution*: Subagents hold `tools=[google_search]` and `input_schema=...` without `output_schema`, returning their evidence findings to the coordinator. The Coordinator (which has no direct search tools) holds `output_schema=StructuredEvidenceBriefModel` and synthesizes the final JSON brief.
2. **`app_name` Requirement in `Runner`**:
   In `google-adk 2.11.0`, `Runner` raises `ValueError: app_name is required when agent is provided without app`. An explicit application name (`app_name="surgical_ai"`) must always be passed.
3. **Structured Response Extraction via `event.actions`**:
   When using `output_schema` with subagents, ADK stores the validated Pydantic dictionary in `event.actions.set_model_response`.
4. **Native ADK Evaluation (`google.adk.evaluation`)**:
   `AgentEvaluator.evaluate_eval_set` discovers agents when the module exposes `root_agent` or `get_agent_async()`. We export `root_agent = create_coordinator_agent()` in `adk/coordinator/agent.py`.
5. **Gemini 3.8 Flash Generation Parameters**:
   For `gemini-3.8-flash`, sampling parameters (`temperature`, `top_p`, `top_k`) are deprecated and ignored by the backend. Reasoning depth is configured exclusively via `thinking_config=types.ThinkingConfig(thinking_level="MEDIUM")`. All legacy sampling parameters are omitted from `GenerateContentConfig` to ensure full API compliance.
