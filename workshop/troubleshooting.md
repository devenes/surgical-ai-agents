# Live Workshop Troubleshooting Guide

- **Document Version**: 1.0.0
- **Audience**: Workshop Presenters & Technical Facilitators
- **Objective**: Rapid identification and mitigation of live platform friction, connectivity issues, and unexpected agent behaviors.

---

## 1. Quick Diagnostic Decision Tree

```
Issue Observed
  ├── Venue Wi-Fi Drops / DNS Failure / Captive Portal Timeout
  │     └──► Switch to Tier 0 Offline Mode (Zero Tokens, Zero Network)
  │           ├── Web UI: Check "⚡ Offline Mock Mode" in sidebar
  │           ├── CLI Multi-Agent: uv run python -m adk.run --offline
  │           └── Multimodal CLI:  uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up
  ├── Agent Studio UI Not Loading / 500 Error
  │     └──► Switch to Tier 0 Local Web Workspace: uv run python -m app.cli all
  ├── Agent Studio Preview Hangs (> 90 seconds)
  │     └──► Stop Generation ──► Switch to Fallback A or Tier 0 CLI: uv run python -m adk.run --offline
  ├── Google Search Tool Error / Quota Exhaustion
  │     └──► Switch to Fallback B (Pre-computed URLs & Cached Evidence) or Tier 0 Mock Mode
  ├── Output Not Conforming to JSON Schema
  │     └──► Show agents/coordinator/output-schema.json and run uv run python -m adk.run --offline
  └── Attendee Enters Patient Vignette
        └──► Run EDGE-07-PATIENT-SAFETY to demonstrate automated safety refusal and reframing
```

---

## 2. Common Classroom Failure Modes & Rapid Solutions

### Symptom 1: Agent Studio Preview Generates Forever (> 90 seconds)
- **Probable Cause**: A grounding tool call (`google_search` or `url_context`) is hung attempting to resolve an external paywalled medical journal portal, or the conference Wi-Fi dropped an SSL handshake.
- **Immediate Action**:
  1. Click **Stop** in the Preview chat window.
  2. Explain to audience: *"Notice that live web grounding actively negotiates real-time external publisher portals. While this verifies citations, it can encounter intermittent external network latency."*
  3. Open the **Events / Trace** drawer to show the subagent query that was issued.
  4. Immediately switch to **Fallback C / Tier 0**: Open the pre-computed verified output [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) or execute `uv run python -m adk.run --offline` in the terminal.

### Symptom 2: Grounding Tool Returns Rate-Limit / Quota Error
- **Probable Cause**: High concurrency from multiple simultaneous queries exhausting Google Search grounding API quotas.
- **Immediate Action**:
  1. Do not repeatedly hammer the Send button.
  2. Switch to **Fallback B / Tier 0**: Toggle **Offline Mock Mode** in the Web UI or execute terminal commands in `--offline` mode.

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
  2. Demonstrate case `EDGE-07-PATIENT-SAFETY` in the Web UI or terminal (`uv run python -m adk.run --offline "My 72-year-old patient with albumin 2.8..."`) to showcase automated refusal and educational redirection.

### Symptom 5: Conference Wi-Fi Completely Fails
- **Probable Cause**: Venue network outage, firewall blocking Google Cloud APIs, or captive portal session expiration.
- **Immediate Action**:
  1. **Do not panic or stall the lecture.**
  2. Switch to **Tier 0 Local Workspace (Zero Tokens, Zero Network)**:
     ```bash
     # Launch local FastAPI + Streamlit apps (runs 100% locally on localhost)
     uv run python -m app.cli all
     ```
  3. Ensure the checkbox **"⚡ Offline Mock Mode (Zero Tokens / No API)"** is checked in the Streamlit UI.
  4. Demonstrate the full curriculum using the 16 pre-cached benchmark inquiries and multimodal vision studio.
  5. If running in terminal, execute:
     ```bash
     uv run python -m adk.run --offline
     uv run python multimodal-demo/adk_multimodal_example.py --offline --follow-up
     ```
  6. Explain the engineering rationale to attendees:
     > *"In hospital operating rooms and acute surgical care, systems cannot fail when Wide Area Networks drop. Our entire multi-agent architecture incorporates a zero-token deterministic offline simulation layer designed specifically for mission-critical edge resilience."*
