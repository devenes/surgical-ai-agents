# 60-Minute Surgical AI Agent Workshop Plan

## Workshop Overview

- **Title**: Multi-Agent AI Architectures in Surgical Research: From Clinical Inquiries to Structured Evidence
- **Audience**: Academic surgeons, surgical residents, clinical fellows, and clinical researchers.
- **Duration**: 60 Minutes.
- **Format**: Interactive lecture, live system demonstration, and hands-on prompt deconstruction.
- **Core Educational Objective**: Demystify AI agents for surgical practitioners by illustrating how modern AI moves beyond conversational chatbots to structured, grounded, multi-agent research assistants.

---

## Pedagogical Concept: The 6-Stage Transformation

Surgeons frequently struggle with generic AI chatbots that hallucinate citations, provide vague answers, or produce unstructured walls of text. This workshop demonstrates the principled transformation:

```
[Clinical Research Problem]
       │
       ▼ (1. Query Normalization & PICOT Framing)
[Task Decomposition]
       │
       ▼ (2. Specialized Delegation)
[Specialist Research Agents (Evidence & Guidelines)]
       │
       ▼ (3. Tool Grounding & Verification)
[Web Research & URL Context]
       │
       ▼ (4. Schema-Constrained Reconciliation)
[Structured Evidence Brief]
       │
       ▼ (5. Educational Inspection)
[Working AI Prototype]
```

---

## 60-Minute Workshop Agenda

| Time Window | Module | Key Topics & Participant Activities |
| :--- | :--- | :--- |
| **00:00 – 00:10** (10m) | **Module 1: The Surgeon's Dilemma with GenAI** | • Limitations of single-turn chatbots (hallucinations, lack of source attribution, lack of clinical rigor).<br/>• Why clinical safety forbids patient-specific AI advice.<br/>• The paradigm shift: Monolithic LLMs vs. Orchestrated Multi-Agent Systems. |
| **00:10 – 00:25** (15m) | **Module 2: Multi-Agent Architecture & Specialist Roles** | • The Coordinator Agent: Question normalization via PICOT.<br/>• The Evidence Agent: Navigating the clinical evidence hierarchy (Meta-analyses > RCTs).<br/>• The Guideline Agent: Society consensus (ACS, ERAS, ASCRS) vs. commentary.<br/>• Real-time grounding: Google Search grounding and URL verification. |
| **00:25 – 00:45** (20m) | **Module 3: Live Case Walkthrough (Colorectal Prehabilitation)** | • **Input**: Primary demo question on colorectal prehabilitation.<br/>• **Decomposition Inspection**: Watching the Coordinator generate targeted sub-queries.<br/>• **Agent Execution**: Evidence Agent extracts landmark RCTs (PREHAB trial); Guideline Agent retrieves ERAS Society recommendations.<br/>• **Reconciliation in Action**: Identifying consensus (functional capacity), divergence (routine vs targeted application), and evidence gaps.<br/>• **Structured Output**: Inspecting the validated JSON output and readable brief. |
| **00:45 – 00:55** (10m) | **Module 4: Edge Cases & Epistemic Humility** | • Live stress-testing with boundary cases:<br/>  - *Missing Evidence*: HIFU for esophageal adenocarcinoma (`not_found: true`).<br/>  - *Safety Boundary*: Patient-specific decision refusal (`EDGE-07`).<br/>  - *International Guideline Divergence*: Bowel prep controversies. |
| **00:55 – 01:00** (5m) | **Module 5: Wrap-up & Future Roadmap** | • How to mirror cloud Agent Studio prototypes into code using ADK.<br/>• Future frontiers: Institutional RAG (Phase 2) and Multimodal Surgery (Phase 3).<br/>• Q&A and takeaway resources. |

---

## Hands-On Exercise Guide for Attendees

1. **Exercise 1: Deconstruct a Clinical Question**
   - Participants choose one question from `prompts/demo-questions.md`.
   - Practice writing the explicit PICOT breakdown:
     - Population, Context, Intervention, Comparator, Outcomes, Timeframe.
2. **Exercise 2: Identify Disagreement & Uncertainty**
   - Review an evidence brief.
   - Surgeons identify whether the AI accurately caught clinical nuances (e.g., surrogate endpoints like 6MWT vs. hard clinical endpoints like 30-day anastomotic leaks).
3. **Exercise 3: Test Safety Guardrails**
   - Attempt to prompt the agent with a real-world patient dilemma (`EDGE-07`).
   - Observe how the Coordinator enforces safety refusal, disclaimers, and reframes to general academic literature.
