# Workshop Storyboard: The Participant Journey

- **Document Version**: 1.0.0
- **Audience**: Workshop Designers, Faculty, and Facilitators
- **Objective**: Map the cognitive journey of an attendee through the 60-minute workshop experience.

---

## 1. The Core Narrative Arc

The workshop follows a structured pedagogical progression from clinical dilemma to functioning AI system architecture:

```
"I bring a surgical problem."
              │
              ▼
"Coordinator turns it into tasks."
              │
              ▼
"Specialist agents research."
              │
              ▼
"Sources appear."
              │
              ▼
"I understand how agents work."
              │
              ▼
"I redesign the workflow for my own problem."
              │
              ▼
"I have the first version of an AI project."
```

---

## 2. Step-by-Step Attendee Cognitive Milestones

### Beat 1: "I bring a surgical problem." (Minute 00–07)
- **Mental State**: Sarcastic or frustrated with AI chatbots that give generic answers or hallucinate citations.
- **Trigger**: The presenter articulates the real friction surgeons face: *"Why does ChatGPT tell me a study exists when the PMID is fake?"*
- **Aha! Moment**: Chatbots predict words; agents execute workflows.

### Beat 2: "Coordinator turns it into tasks." (Minute 07–15)
- **Mental State**: Curious about how AI handles complex, multi-faceted questions.
- **Visual Event**: The primary colorectal prehabilitation prompt is submitted in Agent Studio Preview.
- **Aha! Moment**: The Coordinator doesn't just guess—it decomposes the inquiry into an epidemiological PICOT framework (Population, Intervention, Comparator, Outcomes, Timeframe).

### Beat 3: "Specialist agents research." (Minute 15–20)
- **Mental State**: Engaged by the division of clinical labor.
- **Visual Event**: Trace panel shows the Coordinator delegating literature queries to the Evidence Specialist and guideline queries to the Guideline Specialist.
- **Aha! Moment**: Separating peer-reviewed trials from society guidelines mirrors real-world academic surgical appraisal.

### Beat 4: "Sources appear." (Minute 20–25)
- **Mental State**: Reassured by scientific rigor and verifiability.
- **Visual Event**: Live, clickable URLs from PubMed, *JAMA Surgery*, and the ERAS Society appear in the output. Negative states (`not_found: true`) show epistemic humility.
- **Aha! Moment**: Grounding anchors the model in reality; the system admits what it doesn't know.

### Beat 5: "I understand how agents work." (Minute 20–25)
- **Mental State**: Empowered with architectural insight.
- **Visual Event**: Presenter opens the Trace drawer, showing the prompt contracts, tool calls, and structured JSON output.
- **Aha! Moment**: An agent is just a structured loop of planning, tool calling, and synthesis.

---

## 3. Where the Supplemental Multimodal Mini-Demo Fits (Minute 25–30)

```
                       [Core Text-Based Research Storyline]
                                        │
                                        ▼ (Minute 25: Visual Dimension)
                        ┌───────────────────────────────┐
                        │   Supplemental Mini-Demo      │
                        │ "AI can also accept non-text" │
                        │  • Separate Freeform surface  │
                        │  • Neutral visual features    │
                        │  • Non-diagnostic boundary    │
                        └───────────────┬───────────────┘
                                        │
                                        ▼ (Return to Main Path)
                     [Participant Hands-on Design Exercise]
```

### The Supporting Role of Multimodal:
- **What it is**: A brief 5-minute showcase demonstrating that the underlying Gemini foundation model can process operative images and anatomical landmarks alongside text.
- **What it is NOT**: It is **not** an image-input subagent inside the Agent Designer research canvas. It does not diagnose pathology or advise intraoperative surgical steps.
- **Pedagogical Function**: Expands the surgeon's imagination for future applications (e.g. computer vision research, Critical View of Safety validation) while reinforcing strict non-diagnostic boundaries.

---

## 4. Returning to the Active Creator Path

### Beat 6: "I redesign the workflow for my own problem." (Minute 30–50)
- **Mental State**: Creative, active builder.
- **Activity**: Attendees open the Participant Guide and apply PICOT deconstruction to their own clinical specialty (hernia repair, pancreatectomy, ICG perfusion, trauma resuscitation).
- **Aha! Moment**: *"I can apply this exact multi-agent pattern to my department's research questions."*

### Beat 7: "I have the first version of an AI project." (Minute 50–60)
- **Mental State**: Accomplished; possess an actionable next step.
- **Deliverable**: A completed PICOT deconstruction, two specialist prompts, and an understanding of how to implement or publish the concept.
