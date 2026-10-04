# Live Workshop Troubleshooting Guide

- **Document Version**: 1.0.0
- **Audience**: Workshop Presenters & Technical Facilitators
- **Objective**: Rapid identification and mitigation of live platform friction, connectivity issues, and unexpected agent behaviors.

---

## 1. Quick Diagnostic Decision Tree

```
Issue Observed
  ├── Agent Studio UI Not Loading / 500 Error
  │     └──► Check GCP Console Status ──► Switch to Fallback C (Local ADK CLI / Static JSON)
  ├── Agent Studio Preview Hangs (> 90 seconds)
  │     └──► Stop Generation ──► Check Search Grounding ──► Switch to Fallback A or C
  ├── Google Search Tool Error / Quota Exhaustion
  │     └──► Switch to Fallback B (Pre-computed URLs & Cached Evidence)
  ├── Output Not Conforming to JSON Schema
  │     └──► Re-prompt with explicit JSON prefix, or present ADK Pydantic Model
  └── Attendee Enters Patient Vignette
        └──► Reiterate Safety Policy ──► Use Participant Transformation Pattern
```

---

## 2. Common Classroom Failure Modes & Rapid Solutions

### Symptom 1: Agent Studio Preview Generates Forever (> 90 seconds)
- **Probable Cause**: A grounding tool call (`google_search` or `url_context`) is hung attempting to resolve an external paywalled medical journal portal, or the conference Wi-Fi dropped an SSL handshake.
- **Immediate Action**:
  1. Click **Stop** in the Preview chat window.
  2. Explain to audience: *"Notice that live web grounding actively negotiates real-time external publisher portals. While this verifies citations, it can encounter intermittent external network latency."*
  3. Open the **Events / Trace** drawer to show the subagent query that was issued.
  4. Immediately switch to **Fallback C**: Open the pre-computed verified output [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) or execute `.venv/bin/python -m adk.run` in the terminal.

### Symptom 2: Grounding Tool Returns Rate-Limit / Quota Error
- **Probable Cause**: High concurrency from multiple simultaneous queries exhausting Google Search grounding API quotas.
- **Immediate Action**:
  1. Do not repeatedly hammer the Send button.
  2. Switch to **Fallback B**: Present the cached evidence brief and walk through the pre-verified source citations and PMIDs.

### Symptom 3: Coordinator Emits Markdown Text Instead of Pure JSON
- **Probable Cause**: Absence of strict schema enforcement toggle in Agent Studio canvas allowed the LLM to wrap the response in conversational preamble (e.g., *"Here is your evidence brief:"*).
- **Immediate Action**:
  1. Highlight this to the audience as a teaching moment:
     > *"This illustrates the difference between prompt-based formatting in a low-code UI and strict programmatic schema validation in a developer framework like ADK."*
  2. Show `adk/schemas.py` and explain how `output_schema=StructuredEvidenceBriefModel` guarantees 100% rigid JSON token emission at the API level.

### Symptom 4: Attendee Asks an Unsafe Clinical Decision Question
- **Probable Cause**: Attendee asks *"Can I use this for my clinic patient tomorrow?"* or inputs a real clinical vignette with patient parameters.
- **Immediate Action**:
  1. Praise the clinical relevance of the question, but immediately enforce the safety boundary:
     > *"That is an important clinical question, but this highlights our core safety guardrail: this system is an academic research assistant, not a clinical decision support system. We must never use real patient data or ask an AI to decide whether surgery should proceed."*
  2. Demonstrate how to transform that clinical dilemma into an epidemiological PICOT research question using the pattern in `workshop/demo-prompts.md`.

### Symptom 5: Conference Wi-Fi Completely Fails
- **Probable Cause**: Venue network outage.
- **Immediate Action**:
  1. Switch laptop connection to cellular personal hotspot.
  2. If all cloud connectivity is unavailable, launch **Fallback D**: Present the slides and lead a collaborative whiteboard exercise decomposing a volunteer's surgical problem into PICOT and subagent roles.
