# Workshop Dry-Run Execution Checklist

- **Document Version**: 1.0.0
- **Dry-Run Target**: Full Rehearsal of 60-Minute Surgical AI Agent Workshop
- **Rule**: Every item begins with `status: NOT TESTED`. Verification is only marked after live manual rehearsal.

---

## 1. Pre-Workshop Verification Checklist (Before Workshop)

| Check ID | Verification Item | Target Standard & Requirement | Status | Notes & Verification Date |
| :---: | :--- | :--- | :---: | :--- |
| **PRE-01** | **Browser Environment** | Chrome/Edge updated to latest stable version; clean profile with no disruptive ad blockers. | `status: NOT TESTED` | |
| **PRE-02** | **Google Cloud Account** | Authenticated to designated Google Cloud project via Google Cloud Console with valid project permissions. | `status: NOT TESTED` | |
| **PRE-03** | **Agent Studio Access** | Vertex AI Agent Studio / Gemini Enterprise Agent Platform accessible in region `us` or `global`. | `status: NOT TESTED` | |
| **PRE-04** | **Agent Canvas Exists** | Root agent `surgical-evidence-coordinator` and two subagents (`evidence-specialist`, `guideline-specialist`) configured. | `status: NOT TESTED` | |
| **PRE-05** | **Agent Canvas Saves** | Canvas modifications persist successfully without console error upon clicking **Save**. | `status: NOT TESTED` | |
| **PRE-06** | **Preview Panel Works** | Interactive Preview chat drawer opens and initializes chat session cleanly. | `status: NOT TESTED` | |
| **PRE-07** | **Deployment Works** | Agent is operational in Preview test environment. | `status: NOT TESTED` | |
| **PRE-08** | **Primary Prompt Execution** | Colorectal prehabilitation query runs within 90s, delegates to both subagents, and returns JSON brief. | `status: NOT TESTED` | |
| **PRE-09** | **Safety Prompt Execution** | 72yo sigmoid resection query triggers immediate non-clinical refusal and educational reframing. | `status: NOT TESTED` | |
| **PRE-10** | **Citations & URLs Work** | Retrieved citations contain live, clickable, non-hallucinated URLs from PubMed / surgical societies. | `status: NOT TESTED` | |
| **PRE-11** | **Trace / Events Drawer** | Trace drawer displays Coordinator PICOT decomposition, subagent calls, and search tool queries. | `status: NOT TESTED` | |
| **PRE-12** | **Fallbacks Ready** | Single-agent prompt, pre-computed JSON briefs, and terminal ADK CLI ready in background tabs. | `status: NOT TESTED` | |
| **PRE-13** | **Multimodal Surface Ready** | Agent Studio Freeform / Chat open in separate tab; non-clinical operative image asset staged. | `status: NOT TESTED` | |

---

## 2. Live Workshop Execution Checklist (During Workshop)

| Check ID | Rehearsal Item | Target Standard & Requirement | Status | Notes & Rehearsal Observations |
| :---: | :--- | :--- | :---: | :--- |
| **DUR-01** | **Segment 1 Timing (00–07m)** | Introduction and agentic framing completed within 7 minutes; no dead air. | `status: NOT TESTED` | |
| **DUR-02** | **Segment 2 Timing (07–20m)** | Live prehab demo prompt submitted, running commentary provided during generation, brief reviewed. | `status: NOT TESTED` | |
| **DUR-03** | **Prompt Copy / Paste** | Demo prompt from `workshop/demo-prompts.md` pastes cleanly into Preview panel without formatting artifacts. | `status: NOT TESTED` | |
| **DUR-04** | **Trace Inspection (20–25m)** | Trace drawer opened; tool execution and subagent delegation clearly demonstrated to audience. | `status: NOT TESTED` | |
| **DUR-05** | **Multimodal Demo (25–30m)** | Operative image loaded in Freeform tab; non-diagnostic visual description generated within 5 minutes. | `status: NOT TESTED` | |
| **DUR-06** | **Participant Exercise (30–50m)**| Attendees receive Participant Guide; exercise instructions and zero-PHI rules clearly communicated. | `status: NOT TESTED` | |
| **DUR-07** | **Expected Output Fidelity** | Synthesized briefs conform to structured schema without conversational hallucinations. | `status: NOT TESTED` | |
| **DUR-08** | **Troubleshooting Readiness**| Presenter smoothly navigates potential network latency or tool hiccups using `troubleshooting.md`. | `status: NOT TESTED` | |
| **DUR-09** | **Discussion & Wrap-Up (50–60m)**| Attendee questions appraised; safety disclaimer reinforced; session concludes on time at 60:00. | `status: NOT TESTED` | |

---

## 3. Post-Workshop Debrief Checklist (After Workshop)

| Debrief Dimension | Key Debrief Question | Status | Post-Rehearsal Findings |
| :--- | :--- | :---: | :--- |
| **What Worked Well** | Which parts of the demonstration resonated most with the surgical audience? | `status: NOT TESTED` | |
| **What Failed / Stalled**| Did any tool calls, subagents, or network connections time out or throw errors? | `status: NOT TESTED` | |
| **What Was Confusing** | Did attendees struggle with PICOT concepts, agent vs chatbot definitions, or safety rules? | `status: NOT TESTED` | |
| **Timing Deviations** | Did any segment overrun its allotted window (e.g. demo latency eating exercise time)? | `status: NOT TESTED` | |
| **UI Inconsistencies** | Did Agent Studio console labels, drawers, or button locations differ from the runbook? | `status: NOT TESTED` | |
