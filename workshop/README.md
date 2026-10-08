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

| Document (EN) | Document (TR) | Purpose & Audience |
| :--- | :--- | :--- |
| [`presenter-runbook.md`](presenter-runbook.md) | [`presenter-runbook-TR.md`](presenter-runbook-TR.md) | **Presenter Only**: Minute-by-minute scripted flow (00–60m), exact click actions, demo prompts, talking points, and fallbacks. |
| [`participant-guide.md`](participant-guide.md) | [`participant-guide-TR.md`](participant-guide-TR.md) | **Attendees**: Simplified reference guide for attendees to turn their clinical problem into an AI project. |
| [`demo-prompts.md`](demo-prompts.md) | [`demo-prompts-TR.md`](demo-prompts-TR.md) | **Presenter & Attendees**: Curated prompt catalog with primary, secondary, edge-case, and prompt transformation examples. |
| [`storyboard.md`](storyboard.md) | [`storyboard-TR.md`](storyboard-TR.md) | **Educational Narrative**: The conceptual pedagogical journey from raw surgical dilemma to AI prototype. |
| [`troubleshooting.md`](troubleshooting.md) | [`troubleshooting-TR.md`](troubleshooting-TR.md) | **Live Ops**: Diagnostics and rapid recovery steps for common classroom, network, and UI errors. |
| [`fallback-demo.md`](fallback-demo.md) | [`fallback-demo-TR.md`](fallback-demo-TR.md) | **Contingency Plans**: 4 graded fallback workflows (A, B, C, D) if live cloud services encounter friction. |
| [`cloud-deployment.md`](cloud-deployment.md) | [`cloud-deployment-TR.md`](cloud-deployment-TR.md) | **Additional Track**: Cloud Run and production container deployment using Cloud Buildpacks or Dockerfile with least-privilege IAM service accounts. |

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

---

## 3. Session Tutorial Steps Roadmap

Follow these scripted tutorial steps during the workshop:

| Step / Segment | Time | Stage / Topic | Hands-On Actions | Primary Sub-Document Links (EN / TR) |
| :---: | :---: | :--- | :--- | :--- |
| **Step 0** | T-30m | **Podium Verification** | Run automated dry-run rehearsal command | [EN](presenter-runbook.md#🛡️-t-30-minute-pre-workshop-rehearsal-protocol-podium-verification) \| [TR](presenter-runbook-TR.md#🛡️-t-30-dakika-çalıştay-öncesi-prova-protokolü-kürsü-doğrulaması---podium-verification) |
| **Step 1** | 00–07m | **Introduction & Agentic Shift** | Frame clinical dilemma; Monolithic vs Agentic | [EN](storyboard.md) \| [TR](storyboard-TR.md) • [EN](../docs/safety.md) \| [TR](../docs/safety-TR.md) |
| **Step 2** | 07–20m | **Live Multi-Agent Demo** | Run primary Colorectal Prehab inquiry in Canvas/UI | [EN](presenter-runbook.md#segment-2-live-multi-agent-demo-0700--2000) \| [TR](presenter-runbook-TR.md#bölüm-2-canlı-multi-agent-demosu-0700--2000) • [EN](demo-prompts.md#1-primary-demo-multimodal-colorectal-prehabilitation) \| [TR](demo-prompts-TR.md#1-birincil-demo-multimodal-kolorektal-prehabilitasyon-primary-demo) |
| **Step 3** | 20–25m | **Trace & Grounding Audit** | Inspect search queries, source URLs, JSON schema | [Schema](../agents/coordinator/output-schema.json) • [EN](troubleshooting.md) \| [TR](troubleshooting-TR.md) |
| **Step 4** | 25–30m | **Multimodal Vision Demo** | Non-diagnostic observation of Strasberg CVS diagram | [EN](../multimodal-demo/prompt.md) \| [TR](../multimodal-demo/prompt-TR.md) • [EN](../multimodal-demo/safety.md) \| [TR](../multimodal-demo/safety-TR.md) |
| **Step 5** | 30–50m | **Hands-On Project Exercise** | Attendees frame PICOT & test specialist queries | [EN](participant-guide.md) \| [TR](participant-guide-TR.md) • [EN](demo-prompts.md) \| [TR](demo-prompts-TR.md) |
| **Step 6** | 50–57m | **Appraisal & Edge Cases** | Test missing evidence (`EDGE-01`) & safety (`EDGE-07`) | [Eval](../evaluations/expected-behavior.md) • [EN](fallback-demo.md) \| [TR](fallback-demo-TR.md) |
| **Step 7** | 57–60m | **Wrap-Up & Code Mirror** | Export to Python ADK; explore Cloud Run hosting | [EN](../docs/adk-setup.md) \| [TR](../docs/adk-setup-TR.md) • [EN](cloud-deployment.md) \| [TR](cloud-deployment-TR.md) |
