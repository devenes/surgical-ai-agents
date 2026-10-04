# Agent Studio Configuration Guide

- **Target Platform**: Google Cloud Gemini Enterprise Agent Platform (Vertex AI Agent Studio)
- **Architecture**: Hierarchical Multi-Agent System (Root Coordinator + 2 Local Subagents)
- **Source of Truth**: 
  - Instructions: `agents/coordinator/instructions.md`, `agents/evidence/instructions.md`, `agents/guideline/instructions.md`
  - Schemas: `agents/coordinator/output-schema.json`, `agents/evidence/output-schema.json`, `agents/guideline/output-schema.json`

---

## 1. Project & Console Navigation

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your active workshop project (e.g. configured via `GOOGLE_CLOUD_PROJECT`).
3. In the navigation menu, go to **Gemini Enterprise Agent Platform** (or **Vertex AI** → **Agent Studio** / **Agents**).
4. Verify the active region in the console dropdown: **`us`** (US multi-region) or **`global`**.
5. Click **Create Agent** (or **+ New Agent**) to initialize the root agent canvas.

---

## 2. Agent 1: Coordinator Agent (Root Agent)

The Coordinator serves as the central orchestrator, decomposition engine, and synthesis authority.

| Configuration Field | Value / Setting |
| :--- | :--- |
| **Agent Name** | `surgical-evidence-coordinator` |
| **Display Name** | `Surgical Evidence Coordinator` |
| **Description** | `Chief orchestrator and synthesizer for educational surgical research inquiries. Decomposes research topics via PICOT, delegates to specialist subagents (Evidence & Guideline), and produces structured evidence briefs.` |
| **Model** | `gemini-3.8-flash` |
| **Reasoning / Thinking Level** | `MEDIUM` (standard reasoning depth; legacy sampling parameters like temperature, top_p, top_k are deprecated and removed for Gemini 3.8 Flash) |
| **Instructions** | *Exact text from* [agents/agent-studio/coordinator-instructions.md](../agents/agent-studio/coordinator-instructions.md) |
| **Subagents** | Add 2 Local Subagents:<br>1. `evidence-specialist` (Evidence Agent)<br>2. `guideline-specialist` (Guideline Agent) |
| **Tools** | **None** (Do NOT attach Google Search to the Coordinator node to avoid tool conflicts with structured output formatting). |
| **Expected Output** | JSON object adhering strictly to [agents/coordinator/output-schema.json](../agents/coordinator/output-schema.json). Structured Evidence Brief containing PICOT scope, findings, citations, agreement/disagreement, and safety disclaimer. |

---

## 3. Agent 2: Evidence Agent (Local Subagent)

Specialist subagent responsible for querying, evaluating, and categorizing peer-reviewed surgical literature and clinical trials.

| Configuration Field | Value / Setting |
| :--- | :--- |
| **Agent Name** | `evidence-specialist` |
| **Display Name** | `Evidence Research Agent` |
| **Description** | `Specialist agent for retrieving, evaluating, and summarizing peer-reviewed surgical literature, randomized controlled trials (RCTs), and systematic reviews using search grounding.` |
| **Model** | `gemini-3.8-flash` |
| **Reasoning / Thinking Level** | `MEDIUM` (sampling parameters like temperature are deprecated in Gemini 3.8 Flash) |
| **Instructions** | *Exact text from* [agents/agent-studio/evidence-instructions.md](../agents/agent-studio/evidence-instructions.md) |
| **Tools** | 1. **Google Search** (Grounding with Google Search enabled)<br>2. **URL Context** (Web URL retrieval; optional/secondary) |
| **Expected Output** | Structured literature evaluation including study title, authors/group, publication year, tier (RCT, systematic review, cohort), verified URL, key outcome findings, and methodological limitations. |

---

## 4. Agent 3: Guideline Agent (Local Subagent)

Specialist subagent responsible for querying, evaluating, and cataloging official clinical practice guidelines and consensus statements from recognized surgical societies.

| Configuration Field | Value / Setting |
| :--- | :--- |
| **Agent Name** | `guideline-specialist` |
| **Display Name** | `Guideline Specialist Agent` |
| **Description** | `Specialist agent for retrieving, evaluating, and cataloging official clinical practice guidelines, consensus statements, and practice parameters from recognized national and international surgical societies.` |
| **Model** | `gemini-3.8-flash` |
| **Reasoning / Thinking Level** | `MEDIUM` (sampling parameters like temperature are deprecated in Gemini 3.8 Flash) |
| **Instructions** | *Exact text from* [agents/agent-studio/guideline-instructions.md](../agents/agent-studio/guideline-instructions.md) |
| **Tools** | 1. **Google Search** (Grounding with Google Search enabled)<br>2. **URL Context** (Web URL retrieval; optional/secondary) |
| **Expected Output** | Structured guideline analysis including issuing organization (NICE, ERAS, ACS, ASCRS, EAES, ESCP, SAGES, TSS), title, year, recommendation summary, recommendation grade, verified URL, and divergence notes. |

---

## 5. Visual Canvas Hierarchy

```
                    ┌───────────────────────────────────┐
                    │  Surgical Evidence Coordinator    │
                    │      (Root Steering Agent)        │
                    │      Model: gemini-3.8-flash      │
                    │      Tools: None (Synthesis Only) │
                    └─────────────────┬─────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│     Evidence Specialist       │               │     Guideline Specialist      │
│       (Local Subagent)        │               │       (Local Subagent)        │
│    Model: gemini-3.8-flash    │               │    Model: gemini-3.8-flash    │
│    Tools: Google Search       │               │    Tools: Google Search       │
└───────────────────────────────┘               └───────────────────────────────┘
```

---

## 6. Execution Flow in Agent Studio

1. **User Submission**: The user submits a surgical research question via the Agent Studio **Preview** chat panel.
2. **Coordinator Decomposition**: The Coordinator analyzes the query, extracts PICOT scope, and determines delegation requirements.
3. **Subagent Invocation**:
   - The Coordinator routes literature search parameters to `evidence-specialist`.
   - The Coordinator routes society recommendation parameters to `guideline-specialist`.
4. **Tool Execution**:
   - Both subagents invoke Google Search to retrieve verified citations, abstracts, and guideline repositories.
5. **Synthesis & Formatting**:
   - The Coordinator aggregates the structured findings.
   - It performs cross-specialist reconciliation (areas of agreement, areas of disagreement, uncertainty, limitations).
   - It formats the output as a valid JSON Structured Evidence Brief.
6. **Preview Inspection**:
   - Inspect the **Events** tab in the Preview panel to confirm subagent invocation trajectories and grounding queries.
