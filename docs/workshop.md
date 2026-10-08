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

## 60-Minute Workshop Agenda & Session Modules

The session follows a scripted 7-segment operational runbook detailed in [`workshop/presenter-runbook.md`](../workshop/presenter-runbook.md):

| Time Window | Segment | Focus & Participant Activities | Primary Surface & Tools | Sub-Document Reference (EN / TR) |
| :---: | :--- | :--- | :--- | :--- |
| **T-30m** | **Pre-Flight** | **Podium Verification**: Automated zero-token dry-run rehearsal (`uv run python -m app.cli rehearse`) across all 16 benchmark cases. | Terminal / Web UI | [EN](../workshop/presenter-runbook.md#🛡️-t-30-minute-pre-workshop-rehearsal-protocol-podium-verification) \| [TR](../workshop/presenter-runbook-TR.md#🛡️-t-30-dakika-çalıştay-öncesi-prova-protokolü-kürsü-doğrulaması---podium-verification) |
| **00:00 – 07:00** (7m) | **Segment 1** | **Introduction & The Agentic Shift**: Limitations of monolithic chatbots in surgery; PICOT normalization; clinical safety guardrails. | Slide Deck / Screen Share | [EN](../workshop/storyboard.md) \| [TR](../workshop/storyboard-TR.md)<br>[EN](safety.md) \| [TR](safety-TR.md) |
| **07:00 – 20:00** (13m) | **Segment 2** | **Live Multi-Agent Demo**: Primary Colorectal Prehabilitation inquiry; Coordinator decomposition; parallel Evidence & Guideline specialist search grounding. | Agent Studio Canvas / Web UI | [EN](../workshop/presenter-runbook.md#segment-2-live-multi-agent-demo-0700--2000) \| [TR](../workshop/presenter-runbook-TR.md#bölüm-2-canlı-multi-agent-demosu-0700--2000)<br>[EN](../workshop/demo-prompts.md#1-primary-demo-multimodal-colorectal-prehabilitation) \| [TR](../workshop/demo-prompts-TR.md#1-birincil-demo-multimodal-kolorektal-prehabilitasyon-primary-demo) |
| **20:00 – 25:00** (5m) | **Segment 3** | **Trace Inspection & Deconstruction**: Auditing tool calls, Google Search queries, verified source URLs, and schema validation contracts. | Agent Studio Trace / Swagger | [Schema](../agents/coordinator/output-schema.json)<br>[EN](model-baseline.md) \| [TR](model-baseline-TR.md) |
| **25:00 – 30:00** (5m) | **Segment 4** | **Supplemental Multimodal Mini-Demo**: Operative anatomical landmark observation (Critical View of Safety schematic); non-diagnostic boundary enforcement. | Vision Studio / Script | [EN](../multimodal-demo/README.md) \| [TR](../multimodal-demo/README-TR.md)<br>[EN](../multimodal-demo/prompt.md) \| [TR](../multimodal-demo/prompt-TR.md) |
| **30:00 – 50:00** (20m) | **Segment 5** | **Hands-On Participant Exercise**: Attendees deconstruct their own clinical dilemmas into PICOT and run them in Web UI or Agent Studio. | Participant Guide / Web UI | [EN](../workshop/participant-guide.md) \| [TR](../workshop/participant-guide-TR.md)<br>[EN](../workshop/demo-prompts.md) \| [TR](../workshop/demo-prompts-TR.md) |
| **50:00 – 57:00** (7m) | **Segment 6** | **Group Discussion & Output Appraisal**: Critical review of evidence briefs; evaluating agreement/disagreement and epistemic humility (`not_found: true`). | Shared Screen / Discussion | [Eval](../evaluations/expected-behavior.md)<br>[Prompts](../prompts/edge-cases.md) |
| **57:00 – 60:00** (3m) | **Segment 7** | **Wrap-Up, Code Mirror & Next Steps**: Exporting Agent Studio to Python ADK code; PRISMA review pipelines; institutional RAG roadmap. | Presentation / Terminal | [EN](adk-setup.md) \| [TR](adk-setup-TR.md)<br>[EN](../workshop/cloud-deployment.md) \| [TR](../workshop/cloud-deployment-TR.md) |

---

## Hands-On Exercise Guide for Attendees

Attendees follow the step-by-step worksheet in [`workshop/participant-guide.md`](../workshop/participant-guide.md):

1. **Exercise 1: Deconstruct a Clinical Question**
   - Participants choose one question from [`workshop/demo-prompts.md`](../workshop/demo-prompts.md) or formulate their own clinical dilemma.
   - Practice writing the explicit PICOT breakdown:
     - **Population**: Specific patient cohort (e.g. adults undergoing elective colorectal resection).
     - **Context**: Setting (elective vs emergency).
     - **Intervention**: Surgical procedure, protocol, or device.
     - **Comparator**: Standard of care / conventional therapy.
     - **Outcomes**: Primary & secondary surgical endpoints (e.g. 30-day morbidity, leak rate, length of stay).
     - **Timeframe**: Evaluated literature window (e.g. recent 5–10 years).
2. **Exercise 2: Identify Disagreement & Epistemic Humility**
   - Review an evidence brief generated by the multi-agent system.
   - Evaluate whether the AI correctly distinguished trial evidence from society clinical practice guidelines.
   - Verify negative state detection (`not_found: true`) when evidence is absent (e.g., HIFU in esophageal cancer, `EDGE-01`).
3. **Exercise 3: Test Clinical Safety Guardrails**
   - Submit a real-world patient dilemma vignette (`EDGE-07`).
   - Observe how the Coordinator enforces safety refusal, emits educational disclaimers, and reframes to general academic literature.

---

## Workshop Operational Package Links

- **Presenter Instructions**: [EN](../workshop/presenter-runbook.md) | [TR](../workshop/presenter-runbook-TR.md)
- **Participant Worksheet**: [EN](../workshop/participant-guide.md) | [TR](../workshop/participant-guide-TR.md)
- **Curated Prompt Catalog (16 Cases)**: [EN](../workshop/demo-prompts.md) | [TR](../workshop/demo-prompts-TR.md)
- **Live Ops Troubleshooting**: [EN](../workshop/troubleshooting.md) | [TR](../workshop/troubleshooting-TR.md)
- **4-Tier Contingency Plans**: [EN](../workshop/fallback-demo.md) | [TR](../workshop/fallback-demo-TR.md)
- **Cloud Run Deployment**: [EN](../workshop/cloud-deployment.md) | [TR](../workshop/cloud-deployment-TR.md)
- **Interactive Web UI Guide**: [EN](local-ui-setup.md) | [TR](local-ui-setup-TR.md)
- **Windows Setup Guide**: [EN](windows-setup-guide.md) | [TR](windows-setup-guide-TR.md)
