# Workshop Readiness & Repository Audit

- **Document Version**: 1.0.0
- **Audit Date**: 2026-10-03
- **Audit Target**: Surgical AI Agents Workshop Proof-of-Concept (POC)
- **Status**: Complete Repository Audit (Phase 6A)

---

## 1. Executive Summary

This audit assesses the readiness of the repository for a 60-minute interactive educational workshop for academic surgeons, surgical residents, and clinical fellows.

The primary workshop presentation environment is **Google Cloud Agent Studio (Agent Designer)**. The programmatic implementation in **Google Agent Development Kit (ADK)** serves as the developer/reference baseline and evaluation mirror.

The architecture is strictly defined as:
```
Coordinator Agent
    ├── Evidence Specialist (Local Subagent)
    └── Guideline Specialist (Local Subagent)
```

Multimodal image understanding is treated as a **separate, supplemental mini-demo** executed in Agent Studio Chat / Freeform, and is **not** integrated into the multi-agent canvas.

---

## 2. Repository Artifact Classification

An inventory of repository artifacts was conducted to separate truth from historical artifacts and clarify component ownership:

| Artifact / Path | Role / Category | Current Classification | Description & Authority |
| :--- | :--- | :---: | :--- |
| `agents/coordinator/instructions.md` | Core Agent Prompt | **Source of Truth** | Canonical PICOT decomposition and synthesis logic for Coordinator. |
| `agents/evidence/instructions.md` | Core Agent Prompt | **Source of Truth** | Canonical biomedical literature retrieval logic for Evidence Agent. |
| `agents/guideline/instructions.md` | Core Agent Prompt | **Source of Truth** | Canonical clinical guideline cataloging logic for Guideline Agent. |
| `agents/*/output-schema.json` | JSON Schema Draft-07 | **Source of Truth** | Rigid contract for coordinator and specialist outputs. |
| `agents/agent-studio/*.md` | UI Prompts & Setup | **Source of Truth (Agent Studio)** | System prompts, workflow topology, and setup checklist for visual canvas. |
| `adk/` (`config.py`, `schemas.py`, etc.) | Programmatic Code | **Source of Truth (ADK Reference)** | Python reference implementation using `google-adk 2.11.0` and `google-genai 2.28.0`. |
| `evaluations/evalset.json`, `test-cases.yaml` | Evaluation Catalogs | **Source of Truth (Evaluation)** | Standardized 16-case benchmark (8 normal, 8 edge cases). |
| `evaluations/results/gemini-3-8-migration.*` | Live Evaluation Logs | **Verified Historical Evidence** | 100% pass verification across 6 live tests on `gemini-3.8-flash`. |
| `docs/adk-baseline.md` | Documentation | **Historical Baseline** | Reflects Phase 3 freeze; references `gemini-2.5-flash` in early table sections prior to 3.8 Flash migration. |
| `docs/model-baseline.md` | Documentation | **Current Model Baseline** | Official verification of `gemini-3.8-flash` in multi-region `us` and `global`. |
| `docs/agent-studio-parity.md` | Documentation | **Historical Assessment** | Maps ADK constructs to Agent Studio; classifies manual UI actions. |
| `docs/architecture.md` | System Architecture | **Verified Architecture** | Describes 4 operational surfaces (Web UI, Agent Studio, Multimodal, ADK Reference). |
| `README.md` | Project Overview | **Verified Project Overview** | Comprehensive documentation with 4 surfaces, workshop agenda, and quick starts. |
| `app/README.md` | Web UI Documentation | **Source of Truth (Web UI)** | Operational FastAPI + Streamlit web dashboard with 16 benchmark cases and offline zero-token rehearsal. |

---

## 3. Current Verified Capabilities

### A. Programmatic ADK Baseline (Developer Reference)
- **Orchestration**: The `Coordinator` agent creates a hierarchical delegation tree with `sub_agents=[evidence_agent, guideline_agent]`.
- **Tool Allocation**: Search grounding (`google.adk.tools.google_search`) is attached strictly to specialist subagents (`evidence_agent`, `guideline_agent`). No tools are directly attached to `coordinator`, preventing Vertex AI tool collisions with structured JSON response generation.
- **Model Baseline**: Verified on `gemini-3.8-flash` using Vertex AI multi-region `us` (`https://us-aiplatform.googleapis.com`) and `global`.
- **Thinking Configuration**: Verified with `thinking_level="MEDIUM"`; legacy sampling parameters (`temperature`, `top_p`, `top_k`) are omitted as required by Gemini 3.8.
- **Offline Validation**: 61/61 offline unit tests passing (100% schema compliance, agent construction, FastAPI routes, and rehearsal checks).
- **Live Integration**: 6/6 live integration test cases passing on Vertex AI, including primary colorectal prehabilitation, ICG fluorescence, HIFU missing evidence, topical TXA missing guideline, bowel prep conflicting evidence, and patient-specific safety refusal.
- **Evaluation Framework**: Native ADK evaluation runner (`adk/eval.py`) scores 100% across all 6 surgical informatics dimensions.

### B. Agent Studio Manual Verification
- **Visual Canvas Topology**: Root Coordinator connected to two local subagents (`evidence-specialist`, `guideline-specialist`).
- **Tool Assignment**: Native Google Search tool attached to subagents; Coordinator operates purely as reasoning and synthesis orchestrator.
- **Decomposition**: Coordinator successfully normalizes natural language queries into PICOT dimensions.
- **Source Citations**: Subagents retrieve live, clickable URLs from PubMed and surgical societies.
- **Preview & Trace**: Agent Studio Preview drawer displays step-by-step execution traces, subagent invocations, and search grounding tool calls.

---

## 4. Current Agent Studio Behavior vs. ADK Baseline

| Dimension | Programmatic ADK Baseline | Agent Studio UI Implementation |
| :--- | :--- | :--- |
| **Model** | `gemini-3.8-flash` via Vertex AI client | `gemini-3.8-flash` selected in Model dropdown |
| **Location / Region** | `us` multi-region (specified in `adk/config.py`) | `us` or `global` console selector |
| **Agent Hierarchy** | `root_agent` with `sub_agents=[ev, gd]` | Visual root node with 2 local subagents (`+` button) |
| **Tool Execution** | `google_search` tool call event | Grounding with Google Search toggle enabled on subagents |
| **Structured Output** | Enforced strictly via `output_schema=StructuredEvidenceBriefModel` | Prompt-level JSON schema enforcement via system instructions |
| **Trace Inspection** | Telemetry dictionary / log parsing (`adk.run`) | Interactive **Preview Events / Trace** drawer in console |
| **Execution Order** | Autonomous dynamic invocation by Gemini | Autonomous dynamic invocation by Gemini (Preview trace) |
| **Safety Handling** | Refusal detection & educational reframing | Refusal detection & educational reframing via instructions |

---

## 5. Known Differences Between ADK and Agent Studio

1. **Schema Enforcement Mechanism**:
   - In ADK, schema validation is enforced programmatically at the model level (`response_schema` / `output_schema` parameter).
   - In Agent Studio, while Google documents Output Schema configurations in certain platform versions, the most reliable and verified mechanism in the visual canvas is **prompt-level schema specification** with negative formatting constraints.
2. **Execution Telemetry Visibility**:
   - In ADK, events are captured as structured Python objects and scored programmatically.
   - In Agent Studio, execution steps appear visually in the collapsible **Trace / Events** drawer on the right side of the canvas.
3. **Execution Latency**:
   - In both environments, live search grounding and multi-agent synthesis take **45 to 120 seconds** per query. Presenters must actively engage the audience while waiting for generation.

---

## 6. Unverified Assumptions

1. **Deterministic Execution Order**: It cannot be assumed that `evidence-specialist` will always run before `guideline-specialist`. Depending on prompt phrasing, Gemini may invoke them sequentially in either order or request both simultaneously if the platform supports concurrent tool dispatch.
2. **Zero-Latency Search**: Web grounding depends on live Google Search indexing. Intermittent network latency or rate limiting could impact response speed.
3. **Identical Visual Canvas Across Projects**: UI controls in Google Cloud Agent Studio evolve periodically. Label names ("Events" vs "Trace", "Tools" vs "Extensions") may vary slightly across console rollouts.

---

## 7. Workshop Risks & Failure Modes

| Risk ID | Risk Description | Severity | Likelihood | Mitigation Strategy |
| :--- | :--- | :---: | :---: | :--- |
| **RSK-01** | Live query generation latency (60–120s) leaves presenter with dead air. | Medium | High | Presenter scripted talking points, architecture walkthrough, and PICOT explanation during active generation. |
| **RSK-02** | Agent Studio canvas unavailable or slow due to cloud connectivity issues. | High | Low | Prepared fallback screenshots, pre-computed JSON briefs, and local ADK CLI terminal fallback. |
| **RSK-03** | Google Search grounding returns paywalled links or empty snippets. | Medium | Medium | Subagents instructed to prioritize open-access PubMed abstracts and society guideline portals; fallback slides with pre-verified citations. |
| **RSK-04** | Attendee submits real patient clinical vignette expecting a diagnostic plan. | High | Medium | Strict safety guardrails refuse individualized advice; presenter reinforces educational boundaries upfront. |
| **RSK-05** | Output JSON formatting deviates slightly in Agent Studio Preview. | Low | Low | Instructions include explicit negative constraints and few-shot JSON schema structure. |

---

## 8. Recommended Fixes & Hardening Roadmap (Phase 6A)

1. **Freeze Agent Studio Baseline**: Create `docs/agent-studio-baseline.md` documenting verified configuration and distinguishing manual test from documentation assumptions.
2. **Safety Policy Documentation**: Formalize `agents/agent-studio/safety-policy.md` codifying non-diagnostic, non-prescriptive, zero-PHI boundaries.
3. **Hardening Test Matrix**: Document expectations for H1–H6 tests in `evaluations/agent-studio-hardening.md`.
4. **Structured Output & Routing Deep Dives**: Create `evaluations/agent-studio-structured-output.md`, `evaluations/agent-studio-routing.md`, and `evaluations/agent-studio-context-transfer.md`.
5. **Workshop Package**: Author complete workshop package (`workshop/presenter-runbook.md`, `participant-guide.md`, `demo-prompts.md`, `troubleshooting.md`, `fallback-demo.md`, `storyboard.md`).
6. **Separate Multimodal Demo**: Create isolated `multimodal-demo/` directory with non-clinical surgical visual prompt, synthetic/open asset documentation, safety boundaries, and runnable standalone ADK fallback script.
7. **Document Product Boundaries**: Update `README.md` and `docs/architecture.md` to define the 3 operational boundaries clearly.
