# Agent Studio Baseline Configuration Manifest

- **Document Version**: 1.0.0
- **Baseline Date**: 2026-10-03
- **Baseline Target**: Google Cloud Gemini Enterprise Agent Platform (Vertex AI Agent Studio)
- **Status**: **FROZEN BASELINE** (Phase 6A)

---

## 1. Classification Standard

Every property in this baseline manifest is classified into one of three strict tiers:

- **`VERIFIED BY MANUAL TEST`**: Directly executed and confirmed working in this project environment (either through live execution in the Google Cloud Console or via verified programmatic mirror).
- **`DOCUMENTATION ASSUMPTION`**: Stated in official Google Cloud / Vertex AI product documentation or specifications, but not individually stress-tested under all edge conditions in this workspace.
- **`NOT YET VERIFIED`**: Inferred or expected behavior that has not been confirmed through manual test execution or live inspection.

---

## 2. Core Agent Configuration

| Attribute | Value / Specification | Verification Tier | Verification Notes & Mechanics |
| :--- | :--- | :---: | :--- |
| **GCP Project ID** | Configured via `GOOGLE_CLOUD_PROJECT` | **VERIFIED BY MANUAL TEST** | Active project authenticated via ADC. |
| **Region** | `us` (US multi-region) | **VERIFIED BY MANUAL TEST** | Multi-region `us` tested and confirmed active for `gemini-3.8-flash`. (Note: `us-central1` returns 404). |
| **Alternate Region** | `global` | **DOCUMENTATION ASSUMPTION** | Documented by Google as supported for `gemini-3.8-flash`. |
| **Model** | `gemini-3.8-flash` | **VERIFIED BY MANUAL TEST** | GA model identifier confirmed on Vertex AI; low latency, high reasoning fidelity. |
| **Thinking Level** | `MEDIUM` | **VERIFIED BY MANUAL TEST** | Verified in ADK and GenAI SDK config. Controls reasoning depth; replaces legacy sampling parameters. |
| **Sampling Parameters** | None (omitted) | **VERIFIED BY MANUAL TEST** | `temperature`, `top_p`, `top_k` deprecated and ignored on Gemini 3.8 Flash backend. |
| **Deployment Status** | Saved & Interactive Preview | **VERIFIED BY MANUAL TEST** | Agent canvas saved; execution tested via built-in Preview panel. |
| **Cloud Run Production Endpoint** | Deferred | **DOCUMENTATION ASSUMPTION** | One-click deployment available in Agent Studio UI, but out of scope for workshop. |

---

## 3. Agent Topology & Specialist Roles

### A. Root Coordinator Agent

- **Agent Name**: `surgical-evidence-coordinator` (`VERIFIED BY MANUAL TEST`)
- **Display Name**: `Surgical Evidence Coordinator` (`VERIFIED BY MANUAL TEST`)
- **Node Type**: Root Agent / Canvas Entry Point (`VERIFIED BY MANUAL TEST`)
- **System Instructions**: Exact text from `agents/agent-studio/coordinator-instructions.md` (`VERIFIED BY MANUAL TEST`)
- **Tools Attached**: **None** (`VERIFIED BY MANUAL TEST`)  
  *Rationale*: Attaching Google Search directly to Coordinator causes tool declaration conflicts with structured JSON output generation on Vertex AI.
- **Subagents Attached**:  
  1. `evidence-specialist` (`VERIFIED BY MANUAL TEST`)  
  2. `guideline-specialist` (`VERIFIED BY MANUAL TEST`)
- **Output Schema**: Prompt-enforced JSON adhering to `agents/coordinator/output-schema.json` (`VERIFIED BY MANUAL TEST`).

### B. Evidence Specialist (Local Subagent)

- **Agent Name**: `evidence-specialist` (`VERIFIED BY MANUAL TEST`)
- **Display Name**: `Evidence Research Agent` (`VERIFIED BY MANUAL TEST`)
- **Node Type**: Local Subagent (Child node attached to Coordinator) (`VERIFIED BY MANUAL TEST`)
- **System Instructions**: Exact text from `agents/agent-studio/evidence-instructions.md` (`VERIFIED BY MANUAL TEST`)
- **Model**: `gemini-3.8-flash` (`VERIFIED BY MANUAL TEST`)
- **Tools Attached**:
  - `Google Search` (Grounding with Google Search enabled) (`VERIFIED BY MANUAL TEST`)
  - `URL Context` (Web URL inspection) (`DOCUMENTATION ASSUMPTION` - available in tools drawer, but disabled by default in live runs to prevent paywall hangs)
- **Role**: Literature retrieval focusing on PRISMA/RCT tiers, study methodology, sample sizes, and primary clinical endpoints (`VERIFIED BY MANUAL TEST`).

### C. Guideline Specialist (Local Subagent)

- **Agent Name**: `guideline-specialist` (`VERIFIED BY MANUAL TEST`)
- **Display Name**: `Guideline Specialist Agent` (`VERIFIED BY MANUAL TEST`)
- **Node Type**: Local Subagent (Child node attached to Coordinator) (`VERIFIED BY MANUAL TEST`)
- **System Instructions**: Exact text from `agents/agent-studio/guideline-instructions.md` (`VERIFIED BY MANUAL TEST`)
- **Model**: `gemini-3.8-flash` (`VERIFIED BY MANUAL TEST`)
- **Tools Attached**:
  - `Google Search` (Grounding with Google Search enabled) (`VERIFIED BY MANUAL TEST`)
  - `URL Context` (Web URL inspection) (`DOCUMENTATION ASSUMPTION`)
- **Role**: Society guideline cataloging (ERAS Society, ASCRS, NICE, SAGES, EAES, ESCP, TSS), extraction of graded recommendations, and international divergence detection (`VERIFIED BY MANUAL TEST`).

---

## 4. Orchestration & Runtime Behavior

| Behavioral Feature | Status | Observed Behavior & Details |
| :--- | :---: | :--- |
| **Task Decomposition** | **VERIFIED BY MANUAL TEST** | Coordinator decomposes incoming natural language queries into epidemiological PICOT fields (Population, Intervention, Comparator, Outcomes, Timeframe). |
| **Specialist Delegation** | **VERIFIED BY MANUAL TEST** | Coordinator invokes `evidence-specialist` for peer-reviewed studies and `guideline-specialist` for professional society guidance. |
| **Execution Ordering** | **VERIFIED BY MANUAL TEST** | Both subagents are called during a complete inquiry. Order is dynamically determined by the LLM reasoning planner (frequently Evidence first, but not deterministically guaranteed). |
| **Parallel Execution** | **NOT YET VERIFIED** | Whether Agent Studio dispatches both subagents concurrently or sequentially in all instances depends on backend engine scheduling. |
| **Context Transfer (Downstream)** | **VERIFIED BY MANUAL TEST** | Coordinator packages normalized PICOT parameters and passes them into subagent invocations. |
| **Context Transfer (Upstream)** | **VERIFIED BY MANUAL TEST** | Specialist agents return markdown/text findings with verified titles and URLs, which the Coordinator synthesizes into the final brief. |
| **Cross-Specialist Context Transfer** | **DOCUMENTATION ASSUMPTION** | Subagents operate independently; the Guideline specialist does not read the Evidence specialist's output directly, but receives all relevant context via the Coordinator. |
| **Citation Attribution** | **VERIFIED BY MANUAL TEST** | Output preserves source titles, publication years, issuing institutions, and live URLs retrieved via Google Search grounding. |
| **Negative State Detection (`not_found`)** | **VERIFIED BY MANUAL TEST** | When reliable clinical trials or guidelines do not exist (e.g., HIFU in esophageal cancer), `not_found: true` is accurately populated without hallucinating citations. |
| **Safety Refusal** | **VERIFIED BY MANUAL TEST** | Patient-specific clinical dilemmas (e.g., 72yo male sigmoid resection) trigger immediate refusal of individualized medical advice and redirect to generalized educational synthesis. |
| **Preview & Trace Inspection** | **VERIFIED BY MANUAL TEST** | The Agent Studio Preview panel contains an interactive **Events / Trace** drawer confirming subagent calls and tool grounding executions. |

---

## 5. Architectural Stability & Freeze Statement

The configuration detailed above represents the **verified baseline** for the Surgical AI Agents workshop. No changes to agent topology, tool allocations, or system instructions should be made without explicit hardening evidence and regression testing.
