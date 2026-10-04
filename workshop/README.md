# Surgical AI Agents Workshop Package

- **Session Title**: Multi-Agent AI Architectures in Surgical Research: From Clinical Inquiries to Structured Evidence
- **Target Audience**: Academic surgeons, surgical residents, clinical fellows, and health informatics researchers
- **Session Duration**: 60 Minutes
- **Primary Presentation Platform**: Google Cloud Agent Studio (Agent Designer)
- **Supplemental Platform**: Agent Studio Chat / Freeform (Multimodal Mini-Demo)
- **Developer Reference Baseline**: Google Agent Development Kit (ADK `2.11.0` on `gemini-3.8-flash`)

---

## 1. Package Contents

This folder contains the complete operational material for running the 60-minute interactive workshop:

| Document | Purpose & Audience |
| :--- | :--- |
| [`presenter-runbook.md`](presenter-runbook.md) | **Presenter Only**: Minute-by-minute scripted flow (00–60m), exact click actions, demo prompts, talking points, and fallbacks. |
| [`participant-guide.md`](participant-guide.md) | **Attendees**: Simplified reference guide for attendees to turn their clinical problem into an AI project. |
| [`demo-prompts.md`](demo-prompts.md) | **Presenter & Attendees**: Curated prompt catalog with primary, secondary, edge-case, and prompt transformation examples. |
| [`storyboard.md`](storyboard.md) | **Educational Narrative**: The conceptual pedagogical journey from raw surgical dilemma to AI prototype. |
| [`troubleshooting.md`](troubleshooting.md) | **Live Ops**: Diagnostics and rapid recovery steps for common classroom, network, and UI errors. |
| [`fallback-demo.md`](fallback-demo.md) | **Contingency Plans**: 4 graded fallback workflows (A, B, C, D) if live cloud services encounter friction. |
| [`cloud-deployment.md`](cloud-deployment.md) | **Additional Track**: Cloud Run and production container deployment using Cloud Buildpacks or Dockerfile with least-privilege IAM service accounts. |

---

## 2. Core Educational Value Proposition

Modern surgeons frequently experience frustration with generic conversational chatbots:
1. **Hallucinated Citations**: Fabricated PMIDs, non-existent trials, and plausible-sounding medical falsehoods.
2. **Unstructured Prose**: Conversational paragraphs unsuitable for rigorous scientific appraisal.
3. **Evidence Conflation**: Failure to distinguish randomized controlled trials from formal society guidelines.
4. **Safety Risks**: Inappropriate attempts to answer individualized patient dilemmas.

This workshop demonstrates the **agentic solution**:
```
Clinical Research Inquiry ──► PICOT Normalization ──► Specialist Delegation ──► Grounded Search ──► Structured JSON Evidence Brief
```
