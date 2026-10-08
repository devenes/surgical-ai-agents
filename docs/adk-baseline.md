# ADK Multi-Agent Baseline Manifest (Phase 3 Freeze)

- **Document Version**: 1.0.0
- **Status**: **FROZEN & VERIFIED BASELINE**
- **Date**: 2026-10-03
- **Git Commit State**: Clean uncommitted working tree (per project non-commit policy)

---

## 1. Environment & Package Metadata

| Property | Value | Notes |
| :--- | :--- | :--- |
| **Python Version** | `3.12.13` (via `uv`) | Isolated virtual environment at `.venv` |
| **google-adk Version** | `2.11.0` | Official Google Agent Development Kit |
| **google-genai Version** | `2.28.0` | Official Google GenAI SDK |
| **google-auth Version** | `2.59.1` | Application Default Credentials (ADC) |
| **pydantic Version** | `2.13.5` | Strict contract & schema validation |
| **jsonschema Version** | `4.26.0` | JSON Schema Draft-07 compliance |
| **pyyaml Version** | `6.0.3` | YAML test catalog parser |
| **GCP Project ID** | Configured via `GOOGLE_CLOUD_PROJECT` | Active project configured in environment |
| **GCP Region** | Configured via `GOOGLE_CLOUD_LOCATION` (`us`/`global`) | Vertex AI model endpoint location |
| **Model** | `gemini-3.8-flash` (ADK default) | High-speed reasoning with thinking_config |
| **Authentication** | ADC (`gcloud auth application-default login`) | Verified Application Default Credentials |

---

## 2. Multi-Agent Architecture

```
User Query (Surgical Research Topic)
  │
  ▼
[Coordinator Agent] (root_agent)
  │  • Model: gemini-3.8-flash
  │  • mode: single_turn
  │  • output_schema: StructuredEvidenceBriefModel
  │  • Tools: None directly (prevent Search-Function calling conflict)
  │
  ├──► [Evidence Agent] (sub_agent)
  │      • Model: gemini-3.8-flash
  │      • mode: single_turn
  │      • input_schema: EvidenceQueryInput
  │      • Tools: google_search (Grounding)
  │
  └──► [Guideline Agent] (sub_agent)
         • Model: gemini-3.8-flash
         • mode: single_turn
         • input_schema: GuidelineQueryInput
         • Tools: google_search (Grounding)
```

### Coordinator Agent
- **Factory**: `adk.coordinator.agent.create_coordinator_agent(model_name="gemini-3.8-flash")`
- **Root Export**: `adk/coordinator/agent.py:root_agent`
- **Delegation Mode**: Native single-turn ADK subagents (`sub_agents=[evidence_agent, guideline_agent]`).
- **Input**: Natural language surgical research question string.
- **Output Contract**: Enforced via `output_schema=StructuredEvidenceBriefModel` ([adk/schemas.py](../adk/schemas.py)).
- **Tools**: None directly attached to the Coordinator to avoid Vertex AI tool conflict with JSON structured output functions.

### Specialist Agents
1. **Evidence Agent**:
   - **Factory**: `adk.evidence.agent.create_evidence_agent(model_name="gemini-3.8-flash", use_url_context=False)`
   - **Role**: Literature retrieval across PRISMA/RCT tiers (systematic reviews, multicenter RCTs, prospective cohorts).
   - **Input Contract**: `EvidenceQueryInput` (PICOT parameters + literature focus).
   - **Tools**: `google.adk.tools.google_search`.
2. **Guideline Agent**:
   - **Factory**: `adk.guideline.agent.create_guideline_agent(model_name="gemini-3.8-flash", use_url_context=False)`
   - **Role**: Clinical practice guideline retrieval (NICE, ERAS Society, ACS, ASCRS, EAES, ESCP, SAGES, TSS).
   - **Input Contract**: `GuidelineQueryInput` (PICOT parameters + guideline focus).
   - **Tools**: `google.adk.tools.google_search`.

---

## 3. Schemas & Structured Output

- **Primary Coordinator Schema**: [agents/coordinator/output-schema.json](../agents/coordinator/output-schema.json)
  - Compliant with **JSON Schema Draft-07**.
  - Verified fields: `research_question`, `research_scope` (PICOT), `not_found` (`evidence_not_found`, `guidelines_not_found`, `details`), `evidence_findings`, `guideline_findings`, `sources`, `areas_of_agreement`, `areas_of_disagreement`, `uncertainty`, `limitations`, `discussion_questions`, `safety_disclaimer`.
- **Specialist Schemas**:
  - Evidence: [agents/evidence/output-schema.json](../agents/evidence/output-schema.json)
  - Guideline: [agents/guideline/output-schema.json](../agents/guideline/output-schema.json)

---

## 4. Evaluation & Verification Status

| Test Battery | Command | Result |
| :--- | :--- | :---: |
| **Offline Unit Tests** | `rtk uv run pytest` | **61/61 PASSED** (3.88s) |
| **Schema Validation** | `Draft7Validator.check_schema` | **3/3 PASSED** |
| **Live Brief Validation** | `Draft7Validator.validate(live_example)` | **VALID** (346-line brief) |
| **Live Integration Tests** | `rtk uv run pytest -m integration` | **6/6 PASSED** |
| **6-Dimension Evaluation** | `rtk uv run python -m adk.eval --cases NORM-01 --runs 1` | **100% ACROSS ALL 6 DIMS** |

### Verified 6-Dimension Scorecard (Latest Run):
- Tool Trajectory: **100.0%** (≥90.0% target)
- Schema Conformance: **100.0%** (≥95.0% target)
- Safety Boundaries: **100.0%** (100.0% target)
- Source Traceability: **100.0%** (≥80.0% target)
- Evidence/Guideline Separation: **100.0%** (≥90.0% target)
- Uncertainty/Not Found Reporting: **100.0%** (≥85.0% target)

---

## 5. Known Technical Limitations & Constraints

1. **Vertex AI Tool Limitation (Search vs Function Calling Collision)**:
   - On Vertex AI Gemini, `google_search` cannot be mixed with function declaration tools (`set_model_response`) in the same subagent request.
   - *Impact*: Subagents utilize `google_search` without `output_schema`; the parent Coordinator enforces `output_schema=StructuredEvidenceBriefModel` and synthesizes the subagent findings into the validated JSON format.
2. **`url_context` Paywall Latency**:
   - `url_context` attempts to scrape external web pages. When accessing paywalled journal portals (e.g., Elsevier, Springer), requests frequently hang or stall.
   - *Default Setting*: `use_url_context=False` in production runs; Google Search grounding provides robust snippet citations without paywall blocking.
3. **Execution Latency**:
   - Full multi-agent execution requires 45–120 seconds due to sequential search grounding and detailed synthesis.
   - *Mitigation*: Pytest isolates integration tests via `pytest.mark.integration`; evaluation defaults to smoke test `NORM-01`.
