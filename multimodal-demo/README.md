# Supplemental Multimodal Surgical AI Demonstration

- **Demonstration Scope**: Supplemental 5-Minute Visual Demonstration (Segment 4, Minutes 25–30)
- **Primary Live Surface**: Google Cloud Agent Studio Chat / Freeform (or Vertex AI Studio Multimodal Interface)
- **Developer Reference**: Standalone Python script (`adk_multimodal_example.py`)
- **Core Principle**: Completely separated from the primary text-based Agent Designer research canvas.

---

## 1. Architectural Boundary Notice

> [!IMPORTANT]
> **Strict Canvas Separation**:
> - The primary workshop multi-agent system (`surgical-evidence-coordinator`) is **100% text-based**.
> - Do **NOT** attempt to add an image-input subagent or multimodal perception tool to the Agent Designer canvas.
> - Multimodal reasoning is showcased as a **supplemental mini-demo** in the separate **Agent Studio Chat / Freeform** interface to illustrate foundational model vision capabilities without complicating the multi-agent orchestration architecture.

---

## 2. Package Contents

| Document / Asset | Purpose |
| :--- | :--- |
| [`prompt.md`](prompt.md) | Standardized two-stage demonstration prompts (Neutral Observation + Research Follow-Up). |
| [`safety.md`](safety.md) | Non-diagnostic, non-prescriptive multimodal safety guardrails and prohibitions. |
| [`test-cases.md`](test-cases.md) | Pre-defined multimodal test cases and evaluation criteria. |
| [`presenter-script.md`](presenter-script.md) | Scripted talking points, click steps, and timing for the 5-minute demo. |
| [`fallback.md`](fallback.md) | Contingency procedures and pre-computed visual descriptions if the live UI is slow. |
| [`assets/README.md`](assets/README.md) | Documentation of test images, copyright/license verification, and zero-PHI compliance. |
| [`adk_multimodal_example.py`](adk_multimodal_example.py) | Standalone, runnable Python reference script utilizing the official Google GenAI SDK. |

---

## 3. Workflow Overview

```
Operative Image Asset (Synthetic / Open Diagram)
                    │
                    ▼
          [Stage 1: Observation Prompt]
"Describe only observable visual anatomical features..."
                    │
                    ▼
       Gemini Multimodal Understanding
          (`gemini-3.8-flash`)
                    │
                    ▼
     Neutral Anatomical Observation
   (Landmarks, instruments, spatial orientation)
                    │
                    ▼
         [Stage 2: Educational Follow-Up]
"Explain what computer-vision research tasks use this..."
                    │
                    ▼
  Academic Informatics Discussion
(Critical View of Safety, tool segmentation, DECIDE-AI)
```
