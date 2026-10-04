# Presenter Script: 5-Minute Multimodal Demonstration

- **Segment**: Workshop Segment 4 (Minutes 25:00 – 30:00)
- **Presenter Goal**: Demonstrate foundational vision-language capabilities in Gemini 3.8 Flash while maintaining strict non-diagnostic boundaries.
- **Surface**: Agent Studio Chat / Freeform (or Vertex AI Studio Multimodal Prompt)

---

## Scripted Sequence

### Minute 25:00 – 26:00: Contextual Setup
- **Presenter Actions**:
  1. Leave the Agent Studio Agent Designer canvas open in Browser Tab 1.
  2. Switch to Browser Tab 2: **Agent Studio Chat / Freeform**.
  3. Ensure Model selector is set to **`gemini-3.8-flash`**.
- **Presenter Dialogue**:
  > *"So far today, our multi-agent research coordinator has operated purely in text. That was an intentional architectural choice: text and structured JSON give us deterministic, auditable evidence briefs.*
  > 
  > *However, surgery is fundamentally a visual discipline. We read laparoscopic video, fluoroscopy, and CT scans. What happens when we present surgical imagery to modern multimodal foundation models like Gemini 3.8 Flash?*
  > 
  > *Let's see. In this separate Freeform window, I am going to upload a schematic representation of a laparoscopic operative field."*

---

### Minute 26:00 – 27:30: Stage 1 — Neutral Visual Observation
- **Presenter Actions**:
  1. Click the **Attach Image** icon (+ or paperclip).
  2. Select `multimodal-demo/assets/laparoscopic_cvs_schematic.png`.
  3. Paste Prompt 1 from `multimodal-demo/prompt.md`:
     ```text
     Describe only the observable visual features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
     ```
  4. Click **Run** / Send.
- **Presenter Dialogue**:
  > *"Notice the guardrail in my prompt: I explicitly forbid diagnosis or clinical decision-making. We are asking the model only for neutral visual inventory.*
  > 
  > *Look at the response: Gemini identifies the key visual entities—the organ contour, the tubular duct-like structures, the instrument grasper, and the dissected anatomical plane. It describes them objectively without jumping to conclusions about whether the gallbladder is infected or whether it is safe to cut."*

---

### Minute 27:30 – 29:00: Stage 2 — Academic Informatics Follow-Up
- **Presenter Actions**:
  1. In the same chat turn, paste Prompt 2 from `multimodal-demo/prompt.md`:
     ```text
     Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
     ```
  2. Click **Run** / Send.
- **Presenter Dialogue**:
  > *"Now we turn this visual observation into an academic research question. Notice how Gemini maps these visual features directly to real surgical data science challenges:*
  > *1. Semantic segmentation: training algorithms to outline anatomical boundaries.*
  > *2. Critical View of Safety (CVS) criteria verification in laparoscopic cholecystectomy.*
  > *3. Tool tracking and phase detection.*
  > 
  > *Notice that Gemini also reminds us that these computer vision systems require validation under standards like DECIDE-AI before they can ever be considered in an operating room."*

---

### Minute 29:00 – 30:00: Transition to Participant Exercise
- **Presenter Actions**:
  1. Switch back to Browser Tab 1 or show the **Participant Guide** on the main projector.
- **Presenter Dialogue**:
  > *"This multimodal preview shows where surgical AI is headed. But for our workshop today, we return to the core skill every surgeon needs right now: how to take a clinical problem, deconstruct it, and build an agentic research architecture.*
  > 
  > *Please open your Participant Guides. Let's start our 20-minute design exercise."*
