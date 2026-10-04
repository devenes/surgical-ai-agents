# Presenter Runbook: 60-Minute Surgical AI Agent Workshop

- **Session Title**: Multi-Agent AI Architectures in Surgical Research: From Clinical Inquiries to Structured Evidence
- **Presenter Role**: Lead Surgical AI Faculty / Workshop Instructor
- **Primary Live Surface**: Google Cloud Agent Studio (Agent Designer Canvas)
- **Supplemental Live Surface**: Agent Studio Chat / Freeform (Multimodal Mini-Demo)
- **Backup Surface**: ADK CLI Terminal & Pre-computed Evidence Briefs
- **Target Duration**: Exactly 60 Minutes

---

## Timeline Overview

| Time Window | Segment | Focus | Surface |
| :---: | :--- | :--- | :--- |
| **00:00 – 07:00** (7m) | Segment 1 | Introduction & The Agentic Paradigm Shift | Slide Deck / Screen Share |
| **07:00 – 20:00** (13m) | Segment 2 | Live Multi-Agent Demo (Colorectal Prehabilitation) | Agent Studio Canvas + Preview |
| **20:00 – 25:00** (5m) | Segment 3 | Architectural Deconstruction & Trace Inspection | Agent Studio Trace Drawer |
| **25:00 – 30:00** (5m) | Segment 4 | Supplemental Multimodal Mini-Demo | Agent Studio Chat / Freeform |
| **30:00 – 50:00** (20m) | Segment 5 | Participant Hands-on Project Exercise | Participant Guide & Worksheets |
| **50:00 – 57:00** (7m) | Segment 6 | Group Discussion & Output Appraisal | Shared Screen / Discussion |
| **57:00 – 60:00** (3m) | Segment 7 | Wrap-Up, Clinical Safety, & Next Steps | Concluding Slides |

---

## Segment 1: Introduction & The Agentic Shift (00:00 – 07:00)

- **Objective**: Establish why academic surgeons need multi-agent architectures instead of monolithic chatbots; introduce PICOT task decomposition and epistemic humility.
- **What Presenter Says**:
  > *"Welcome everyone. As surgeons, we've all experimented with commercial AI chatbots like ChatGPT or Gemini. And we've all hit the same clinical wall: they hallucinate fake study citations, they write vague conversational prose, they conflate clinical trials with society guidelines, and they can be dangerously willing to offer medical advice for individual patients.*
  > 
  > *Today, we are moving beyond the chatbot. We are going to explore AI agents. An agent doesn't just predict the next word—it plans, uses tools like live Google Search, delegates specialized tasks to subagents, and outputs deterministic, structured evidence briefs. Over the next 60 minutes, you will see how we turn high-stakes surgical inquiries into structured, verifiable AI systems."*
- **What Presenter Clicks**:
  - Slide 1: Title & Surgical Informatics Dilemma.
  - Slide 2: Chatbot vs. Agent Architecture comparison table.
  - Switch display to Google Cloud Console showing Agent Studio canvas.
- **Exact Demo Prompt**: None (Lecture and framing).
- **Expected Visual State**: Presentation slides; transition to browser displaying the `surgical-evidence-coordinator` canvas.
- **Expected Output**: Audience understands the session goal: structured research synthesis, not clinical diagnosis.
- **Fallback**: If projector/screen fails, speak from physical printed agenda notes.

---

## Segment 2: Live Multi-Agent Demo (07:00 – 20:00)

- **Objective**: Execute the primary live colorectal prehabilitation inquiry in Agent Studio Preview; demonstrate autonomous decomposition, subagent delegation, real-time web grounding, and structured JSON synthesis.
- **What Presenter Says**:
  > *"Let's see this in action. On my screen is Google Cloud Agent Studio. We have built a three-agent system: a central Coordinator and two local subagents—an Evidence Specialist that searches medical literature, and a Guideline Specialist that queries surgical societies.*
  > 
  > *I am going to submit a real clinical research question regarding elective colorectal prehabilitation. Watch what happens in the Preview panel."*
- **What Presenter Clicks**:
  1. Click **Preview** on the top-right of the Agent Studio canvas.
  2. Paste the primary demo prompt into the input box.
  3. Click **Send** (or press Enter).
  4. While the agent runs (approx. 45–90 seconds), highlight the canvas topology and explain the PICOT decomposition occurring behind the scenes.
- **Exact Demo Prompt**:
  ```text
  For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?
  ```
- **Expected Visual State**:
  - Progress indicators appear in the Preview panel.
  - Step events show Coordinator invoking `evidence-specialist` and `guideline-specialist`.
  - Final response renders as a clean, structured JSON evidence brief.
- **Expected Output**:
  - `research_scope`: PICOT breakdown populated (Adults, Elective colorectal, Multimodal prehab, Standard care, 6MWD/complications).
  - `evidence_findings`: PREHAB trial (Molenaar 2023), BJS meta-analyses with live URLs.
  - `guideline_findings`: ERAS Society (2023) and ASCRS recommendations with URLs.
  - `areas_of_agreement`: Consensus on functional capacity improvement.
  - `areas_of_disagreement`: Mixed findings on hard surgical complication reduction in unselected cohorts.
  - `safety_disclaimer`: Mandatory non-clinical disclaimer present.
- **Fallback**:
  - *If generation takes > 90 seconds or times out*: Click into `workshop/fallback-demo.md` or display pre-computed file [`examples/research-questions/colorectal-prehabilitation-gemini-3-8.json`](../examples/research-questions/colorectal-prehabilitation-gemini-3-8.json) in the browser or terminal (`.venv/bin/python -m adk.run`).

---

## Segment 3: Explain Architecture & Preview/Trace (20:00 – 25:00)

- **Objective**: Demystify the "black box" by opening the Trace / Events drawer to show attendees the exact mechanics of tool calls, search queries, and prompt contracts.
- **What Presenter Says**:
  > *"Why should a surgeon trust this output? Because we can inspect every step of the agent's reasoning. Look at this Trace drawer on the right.*
  > 
  > *Here is the exact PICOT query the Coordinator sent to the Evidence Specialist. Here is the Google Search query executed in real-time. Notice the source URLs returned from PubMed and the ERAS Society. And notice that the Coordinator agent itself has NO direct search tool—it is purely a reasoning and synthesis engine. This separation prevents tool collisions and ensures strict scientific accountability."*
- **What Presenter Clicks**:
  1. Click the **Events** (or **Trace**) tab in the Preview drawer.
  2. Expand the Coordinator delegation event.
  3. Expand the `evidence-specialist` subagent event to show the `google_search` query string.
  4. Expand the `guideline-specialist` subagent event to show the retrieved society links.
  5. Highlight the final JSON output formatting step.
- **Exact Demo Prompt**: None (Inspection of previously executed run).
- **Expected Visual State**: Collapsible trace hierarchy displaying Coordinator -> Subagent -> Tool Call -> Synthesis.
- **Expected Output**: Attendees see that agent execution is deterministic, grounded, and inspectable, not magic.
- **Fallback**: If the trace drawer fails to expand in the browser, show the equivalent trace structure in [`docs/agent-studio-baseline.md`](../docs/agent-studio-baseline.md) or terminal telemetry from `adk.run`.

---

## Segment 4: Separate Multimodal Mini-Demo (25:00 – 30:00)

- **Objective**: Demonstrate that modern AI models can process visual surgical information (laparoscopic views, operative fields) while strictly enforcing non-diagnostic, non-prescriptive safety boundaries.
- **What Presenter Says**:
  > *"Before we begin our hands-on exercise, I want to show you one supplemental capability. Surgery is an inherently visual discipline. Can AI understand surgical imagery?*
  > 
  > *Important note: Our multi-agent research canvas is intentionally text-based. But Gemini also supports multimodal reasoning in a separate surface. Let's switch to the Agent Studio Chat / Freeform window and upload an operative illustration.*
  > 
  > *Notice our strict prompt: we ask the model to describe only observable visual features, explicitly forbidding any individual patient diagnosis or surgical go/no-go decisions."*
- **What Presenter Clicks**:
  1. Open a new browser tab with **Agent Studio Chat / Freeform** (or Vertex AI Studio Multimodal Prompt).
  2. Click the **Attach Image** button.
  3. Upload the prepared demonstration image from `multimodal-demo/assets/`.
  4. Paste Prompt 1 from `multimodal-demo/prompt.md`.
  5. Click **Run**.
- **Exact Demo Prompt**:
  ```text
  Describe only the observable visual anatomical and operative features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
  ```
- **Follow-Up Prompt (if time allows)**:
  ```text
  Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
  ```
- **Expected Visual State**:
  - Image thumbnail displayed alongside prompt text.
  - Generated output describes observable anatomy (e.g. gallbladder infundibulum, cystic duct region, anatomical landmarks) neutrally.
  - Zero diagnostic claims; zero treatment recommendations.
- **Expected Output**: Objective anatomical description; educational discussion of computer vision validation (e.g. Critical View of Safety).
- **Fallback**:
  - *If Freeform tab is slow*: Execute the standalone script `python multimodal-demo/adk_multimodal_example.py` in the terminal, or show pre-recorded output from `multimodal-demo/fallback.md`.

---

## Segment 5: Participant Hands-On Exercise (30:00 – 50:00)

- **Objective**: Guide attendees through turning their own real-world surgical dilemma into an agentic research project using the PICOT framework and specialist delegation design.
- **What Presenter Says**:
  > *"Now it is your turn. Turn to your Participant Guide. Every attendee here has a clinical question they encountered in the operating room or clinic this week.*
  > 
  > *Your task over the next 20 minutes is not to write code. It is to act as the AI System Architect. You will:*
  > *1. Take your surgical dilemma.*
  > *2. Deconstruct it into the PICOT framework.*
  > *3. Define what the Evidence Specialist should search for.*
  > *4. Define what the Guideline Specialist should query.*
  > *5. Anticipate where trials and guidelines might disagree.*
  > 
  > *Crucial safety reminder: Do NOT use real patient data. Do NOT enter medical record numbers, dates, or identifiable details. All queries must be framed as generalized surgical research."*
- **What Presenter Clicks**:
  - Project Slide showing the **Exercise Worksheet Template** (from `workshop/participant-guide.md`).
  - Circulate around the room assisting attendees with framing.
- **Exact Demo Prompt**: Attendees use templates in [`workshop/participant-guide.md`](participant-guide.md).
- **Expected Visual State**: Attendees working individually or in pairs on laptops or printed worksheets.
- **Expected Output**: Attendees produce a completed 5-point PICOT decomposition and 2 specialist delegation prompts.
- **Fallback**: If an attendee is stuck or lacks an idea, point them to the pre-curated topics in `workshop/demo-prompts.md` (e.g. ICG leak prevention, index cholecystectomy in mild gallstone pancreatitis, prophylactic mesh in stoma formation).

---

## Segment 6: Share Results & Output Appraisal (50:00 – 57:00)

- **Objective**: Have 2–3 attendees share their decomposed clinical questions; test one attendee query live in the Agent Studio Preview if time permits; evaluate output quality and epistemic humility.
- **What Presenter Says**:
  > *"Let's hear from two volunteers. Who has a question they decomposed?*
  > 
  > *[Volunteer 1 shares topic, e.g., prophylactic mesh in end colostomy creation].*
  > 
  > *Notice how cleanly Dr. [Name] separated the literature task (RCTs on parastomal hernia incidence) from the guideline task (European Hernia Society vs ASCRS position). Let's look at how the agent synthesizes this: look at the 'areas_of_disagreement'—that is where true clinical nuance lives."*
- **What Presenter Clicks**:
  - Optionally paste one selected attendee question into Agent Studio Preview.
  - Alternatively, showcase the pre-computed output for **ICG fluorescence** or **Mechanical bowel preparation** from `workshop/demo-prompts.md`.
- **Exact Demo Prompt**: Volunteer prompt or Demo Question 3 (ICG Fluorescence) from `workshop/demo-prompts.md`.
- **Expected Visual State**: Live or prepared evidence brief displayed on the main projector.
- **Expected Output**: Interactive critique of evidence quality, citation validity, and agreement/disagreement analysis.
- **Fallback**: Use prepared Demo Question 5 (timing of cholecystectomy for acute pancreatitis) from `prompts/demo-questions.md`.

---

## Segment 7: Wrap-Up, Safety, & Next Steps (57:00 – 60:00)

- **Objective**: Reiterate safety guardrails (no CDSS, no patient advice); explain the bridge between low-code Agent Studio and high-code ADK; provide take-home resources.
- **What Presenter Says**:
  > *"To wrap up our session today, remember these three core principles:*
  > *First: Agents are not chatbots. By decomposing tasks via PICOT and delegating to specialist subagents, we eliminate citation hallucinations and gain structured, verifiable research briefs.*
  > *Second: Epistemic humility. A good AI system must know when evidence is missing and report 'not found' rather than invent plausible answers.*
  > *Third: Safety is non-negotiable. These tools are educational research assistants, never clinical decision support systems for individual patients.*
  > 
  > *Everything you saw today—the prompts, schemas, and the developer ADK codebase—is available in our open repository. Thank you for your time!"*
- **What Presenter Clicks**:
  - Concluding slide with QR code / URL to repository.
  - Final Q&A.
- **Expected Visual State**: Concluding slide.
- **Expected Output**: Session finishes exactly at 60:00.
