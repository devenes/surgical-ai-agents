# Workshop Fallback & Contingency Plans

- **Document Version**: 1.0.0
- **Purpose**: Operational contingency procedures to guarantee a seamless 60-minute workshop regardless of cloud platform, Wi-Fi, or API issues.
- **Rule**: Never fabricate real-time results; always explain the fallback mechanism transparently to attendees.

---

## Contingency Matrix

| Fallback Tier | Trigger Condition | Contingency Workflow | Fallback Asset / Command |
| :---: | :--- | :--- | :--- |
| **Fallback A** | Multi-agent orchestration fails or subagent loops | Switch to a single-agent grounded query in Agent Studio | Single-agent prompt with Google Search grounding tool |
| **Fallback B** | Google Search grounding quota exhausted or failing | Present pre-verified public literature sources and society links | Pre-computed citation cache in `examples/research-questions/` |
| **Fallback C** | Agent Studio UI is unresponsive, slow, or 500 error | Execute programmatic ADK CLI baseline or show verified JSON | Terminal: `.venv/bin/python -m adk.run` or pre-computed JSON |
| **Fallback D** | Attendee exercise friction or venue network down | Presenter-led interactive chalkboard / slide exercise | Project Transformation Worksheet (Participant Guide) |

---

## Fallback A: Single-Agent Grounded Demo

### When to Use
If the Coordinator fails to invoke subagents, enters a tool recursion error, or if multi-agent delegation stalls in the Agent Studio Preview.

### Presenter Action & Narrative
1. Transition smoothly without panic:
   > *"In multi-agent systems, orchestration involves multiple distributed reasoning steps. If we want to inspect grounding directly without multi-turn delegation, we can query a single grounded research agent directly."*
2. In Agent Studio, open a single grounded agent (or in Preview, select the `evidence-specialist` node directly).
3. Paste the following unified prompt:
   ```text
   For adults undergoing elective colorectal surgery, summarize what recent randomized trials and ERAS Society guidelines report regarding multimodal prehabilitation. Ground your answer using Google Search and cite verified titles and URLs. Conclude with a safety disclaimer.
   ```
4. Observe the direct search tool call and grounded synthesis in a single turn.

---

## Fallback B: Pre-Computed Verified Citations

### When to Use
If Google Search grounding encounters rate-limiting (HTTP 429), network timeout, or returns empty snippets during live demonstration.

### Presenter Action & Narrative
1. Explain the grounding dependency honestly:
   > *"Real-time search grounding relies on live queries against web indices. In high-traffic environments, search APIs can experience throttling. Let's inspect our pre-verified citation registry for this exact inquiry."*
2. Open the verified citation registry in [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) or [`examples/research-questions/colorectal-prehabilitation.md`](../examples/research-questions/colorectal-prehabilitation.md).
3. Walk attendees through the verified citations:
   - **PREHAB Trial**: Molenaar et al., *JAMA Surgery* 2023. [https://jamanetwork.com/journals/jamasurgery/fullarticle/2804564](https://jamanetwork.com/journals/jamasurgery/fullarticle/2804564)
   - **BJS Meta-analysis**: Waterland et al., *BJS* 2021. [https://academic.oup.com/bjs/article/108/8/900/6298514](https://academic.oup.com/bjs/article/108/8/900/6298514)
   - **ERAS Society Guidelines**: Gustafsson et al., *World J Surg* / ERAS Society 2023. [https://erassociety.org/guidelines/colorectal/](https://erassociety.org/guidelines/colorectal/)
   - **ASCRS Practice Parameters**: You et al., *Dis Colon Rectum* 2023. [https://fascrs.org/healthcare-providers/practice-parameters](https://fascrs.org/healthcare-providers/practice-parameters)

---

## Fallback C: Programmatic ADK CLI Reference

### When to Use
If the Google Cloud Console web application is inaccessible, slow, or experiencing regional UI downtime.

### Presenter Action & Narrative
1. Switch to terminal:
   > *"One of the greatest strengths of this architecture is that everything built visually in Agent Studio has an exact 1:1 code mirror in the Google Agent Development Kit (ADK). If the web console is ever unavailable, we can run the entire multi-agent system directly from our terminal."*
2. Open terminal in the repository root and execute:
   ```bash
   .venv/bin/python -m adk.run
   ```
3. Show the live console output streaming the PICOT extraction, subagent delegation, and resulting JSON output.
4. Alternatively, view the formatted JSON file directly:
   ```bash
   cat examples/research-questions/colorectal-prehabilitation-gemini-3-8.json
   ```

---

## Fallback D: Presenter-Led Collaborative Canvas Exercise

### When to Use
If venue Wi-Fi fails completely, preventing attendees from browsing or using online tools during the hands-on exercise segment (Minutes 30–50).

### Presenter Action & Narrative
1. Transition to an interactive masterclass format:
   > *"No internet connection needed to think like an AI System Architect. Let's do this together on the whiteboard. Who has a surgical dilemma from their clinical work this week?"*
2. Invite a participant to propose a clinical dilemma (e.g. *"Early vs. interval cholecystectomy in acute pancreatitis"*).
3. On the whiteboard or projector screen, collaboratively build the 5-part PICOT framework:
   - **P**: Adult patients with first episode of mild acute biliary pancreatitis.
   - **I**: Index admission laparoscopic cholecystectomy within 72h.
   - **C**: Delayed elective cholecystectomy at 4–6 weeks post-discharge.
   - **O**: Recurrent biliary events, readmission, conversion rate, total hospital stay.
   - **T**: Recent 5 years.
4. Outline the exact subagent query instructions for the Evidence Specialist (IAP/APA trials, PONCHO trial) and Guideline Specialist (WSES, Tokyo Guidelines, IAP/APA).
5. Walk attendees through predicting the synthesis: consensus on index surgery reducing readmissions; divergence on technical difficulty in inflamed gallbladders.
