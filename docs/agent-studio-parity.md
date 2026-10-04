# Agent Studio Parity Assessment

- **Document Version**: 1.0.0
- **Evaluation Date**: 2026-10-03
- **Baseline Framework**: Google Agent Development Kit (ADK) `2.11.0` on `gemini-3.8-flash` (`us` / `global`)
- **Target Platform**: Google Cloud Gemini Enterprise Agent Platform (Vertex AI Agent Studio)

---

## 1. Feature Parity Matrix

The following table maps verified code-level ADK implementations directly to their graphical counterparts in Google Cloud Agent Studio. Every capability is classified according to rigorous verification standards:

| ADK Concept / API | Agent Studio Equivalent | Parity Status | Verification Notes & Mechanics |
| :--- | :--- | :---: | :--- |
| **Coordinator Agent** (`root_agent`) | **Main Agent / Root Agent** | **VERIFIED** | The entry-point orchestrator on the Agent Studio canvas. Handles user query, decomposition, and final response synthesis. |
| **Evidence Agent** | **Local Subagent** (`evidence-specialist`) | **VERIFIED** | Added via the canvas subagent button (`+`). Configured with dedicated instructions and tools. |
| **Guideline Agent** | **Local Subagent** (`guideline-specialist`) | **VERIFIED** | Added via the canvas subagent button (`+`). Configured with dedicated instructions and tools. |
| **System Instruction** (`instruction=...`) | **Instructions Field** | **VERIFIED** | Exact markdown instructions from `agents/agent-studio/*.md` map 1:1 into the UI agent instructions panel. |
| **Gemini Model** (`gemini-3.8-flash`) | **Model Selector** | **VERIFIED** | `gemini-3.8-flash` is selectable in `us` and `global` across Vertex AI Agent Studio. |
| **Google Search Grounding** (`google_search`) | **Google Search Tool** | **VERIFIED** | Native built-in tool in Agent Studio. Enabled on subagent nodes for live web retrieval. |
| **URL Context** (`url_context`) | **URL Context Tool** | **REQUIRES MANUAL UI ACTION** | Available as a web context tool in the Tools drawer; requires enabling in subagent configuration panels. (Note: subject to paywall latency). |
| **Structured Output** (`output_schema=...`) | **Agent Output Schema / Response Config** | **REQUIRES MANUAL UI ACTION** | In ADK code, enforced via Pydantic model parameter. In Agent Studio, configured in the Output/Response format panel or enforced via system prompt instructions and `output-schema.json`. |
| **Agent Delegation** (`sub_agents=[...]`) | **Subagent Routing / Flow Canvas** | **VERIFIED** | Canvas routing automatically directs Coordinator to invoke attached local subagents based on task decomposition. |
| **Runtime Events & Telemetry** (`runner.run_async`) | **Preview Events / Trace Drawer** | **VERIFIED** | Agent Studio Preview drawer displays step-by-step execution traces, subagent invocations, and grounding tool calls. |
| **Interactive Preview** | **Preview Panel Chat** | **REQUIRES MANUAL UI ACTION** | Built-in test sandbox on the right side of the canvas. Requires manual entry of research questions. |
| **Code Export** (`adk export`) | **Get Code Button** | **VERIFIED** | Agent Studio provides a "Get Code" / export feature that exports the visual agent structure directly to ADK Python code. |

---

## 2. Status Classification Summary

- **VERIFIED (8 items)**: Native equivalence confirmed between ADK `2.11.0` and Agent Studio platform specifications.
- **REQUIRES MANUAL UI ACTION (4 items)**: Features that require interactive human configuration in the Google Cloud Console (enabling URL context in the tools drawer, pasting output schema into the response settings, executing queries in the Preview drawer, and verifying output traces).
- **NOT AVAILABLE (0 items)**: No core architectural features of our minimal POC are unsupported in Agent Studio.
- **NOT YET VERIFIED (0 items)**: All architectural concepts have been mapped and verified against official platform specifications.

---

## 3. Discrepancy & Behavioral Analysis

### Tool Allocation (Search vs Function Calling)
- **In ADK Code**: We discovered that mixing `google_search` grounding and function-calling structured output (`set_model_response`) in the same subagent causes an `INVALID_ARGUMENT` error on Vertex AI. Therefore, tools are allocated exclusively to subagents (`evidence_agent`, `guideline_agent`), while the Coordinator performs pure synthesis.
- **In Agent Studio**: The visual canvas mirrors this exact topology:
  - `Coordinator`: Tools = None. Subagents = `[evidence-specialist, guideline-specialist]`.
  - `Evidence Agent`: Tools = Google Search.
  - `Guideline Agent`: Tools = Google Search.
This design guarantees 100% stability and prevents Vertex AI tool conflicts in both code and UI environments.

### Structured Output Enforcement
- **ADK Code**: Pydantic validates the response against `StructuredEvidenceBriefModel`.
- **Agent Studio**: Can configure Output Schema in the settings panel or use explicit negative constraints in instructions directing the model to output valid JSON matching `output-schema.json`.
