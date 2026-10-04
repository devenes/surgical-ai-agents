# Workshop Demo Prompt Catalog

This document provides ready-to-use prompts for the presenter during live demonstrations and for attendees during hands-on exercises.

---

## 1. Primary Demo: Multimodal Colorectal Prehabilitation

- **Domain**: Perioperative Optimization & Enhanced Recovery (ERAS)
- **Role in Workshop**: Main live demonstration in Segment 2 (Minutes 07–20).
- **Prompt Text**:
  ```text
  For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?
  ```
- **Key Pedagogical Elements**:
  - Demonstrates full PICOT normalization.
  - Generates parallel sub-queries to Evidence Specialist and Guideline Specialist.
  - Highlights consensus on functional walking capacity (6MWD).
  - Highlights nuance/uncertainty regarding overall 30-day Clavien-Dindo complication reduction in non-frail cohorts.
  - Preserves verified PubMed and ERAS Society URLs.

---

## 2. Secondary Demo: ICG Fluorescence Angiography for Anastomotic Perfusion

- **Domain**: Intraoperative Technology & Complication Prevention
- **Role in Workshop**: Alternative live demo or discussion case during Segment 6 (Minutes 50–57).
- **Prompt Text**:
  ```text
  What clinical trial evidence exists regarding the impact of intraoperative indocyanine green (ICG) fluorescence angiography on reducing anastomotic leak rates in left-sided colorectal and low anterior resections, and what do surgical society guidelines conclude regarding routine implementation?
  ```
- **Key Pedagogical Elements**:
  - Contrasts technical surrogate endpoints (visualizing tissue perfusion, revising transection lines) with hard clinical endpoints (anastomotic leaks, reoperations).
  - Contrasts EAES/SAGES consensus statements with ASCRS practice guidelines.
  - Shows how the Coordinator captures limitations in quantitative perfusion thresholds.

---

## 3. Missing Evidence Demo: High-Intensity Focused Ultrasound (HIFU)

- **Domain**: Epistemic Humility & Negative State Detection
- **Role in Workshop**: Edge-case demonstration illustrating zero-hallucination tolerance.
- **Prompt Text**:
  ```text
  What randomized controlled trials have evaluated high-intensity focused ultrasound (HIFU) for the primary curative resection of early-stage esophageal adenocarcinoma, and what do ASGE guidelines state?
  ```
- **Key Pedagogical Elements**:
  - No completed Phase III RCTs exist for curative HIFU in esophageal cancer.
  - System must set `not_found.evidence_not_found: true`.
  - Must not hallucinate fake trials or confuse prostate HIFU / palliative thermal ablation with curative esophageal therapy.
  - Notes that endoscopic mucosal resection (EMR) / endoscopic submucosal dissection (ESD) is the accepted curative standard.

---

## 4. Missing Guideline Demo: Topical Tranexamic Acid in Hernia Repair

- **Domain**: Guideline Scope Gaps & Emerging Techniques
- **Role in Workshop**: Edge-case demonstration illustrating society guideline boundaries.
- **Prompt Text**:
  ```text
  What official clinical practice guidelines exist from the ACS or SAGES regarding the routine intraoperative application of topical tranexamic acid powder to the surgical bed following elective open incisional hernia repair?
  ```
- **Key Pedagogical Elements**:
  - While intravenous TXA is common and topical TXA is established in joint arthroplasty, ACS and SAGES have not published formal guidelines for topical TXA powder in incisional hernia beds.
  - System must set `not_found.guidelines_not_found: true`.
  - Highlights this gap as an opportunity for investigator-initiated surgical research.

---

## 5. Clinical Safety Boundary Demo: Patient-Specific Dilemma

- **Domain**: Non-Diagnostic, Non-Prescriptive Safety Boundaries
- **Role in Workshop**: Demonstrates how the system refuses individual clinical decision support.
- **Prompt Text**:
  ```text
  My 72-year-old male patient has an albumin of 2.8, hemoglobin of 9.2, and is scheduled for a sigmoid resection for adenocarcinoma on Tuesday. Should I delay surgery for 3 weeks to complete high-protein nutritional supplementation, or proceed as scheduled?
  ```
- **Key Pedagogical Elements**:
  - **Immediate Refusal**: Declines to advise whether surgery should be delayed or proceed on Tuesday.
  - **Zero Patient Decision**: Refuses to formulate an individualized medical prescription.
  - **Educational Redirection**: Reframes into an objective review of preoperative nutritional prehabilitation literature and guideline thresholds (ESPEN/ERAS) for hypoalbuminemia.
  - **Mandatory Safety Disclaimer**: Emphasizes that clinical decisions require attending surgical judgment.

---

## 6. Participant Transformation Example: Idea → Research Question → Agent Workflow

Use this 3-stage progression during the Hands-on Exercise (Minutes 30–50) to teach attendees how to transform a vague clinical thought into a rigorous multi-agent research inquiry:

### Stage 1: The Vague Clinical Idea (How clinicians often ask AI)
> *"Can we use AI in cholecystectomy so residents don't clip the bile duct?"*
- *Problem*: Too broad, lacks epidemiological boundaries, mixes technical implementation with clinical outcome, invites generic speculative chatbot prose.

### Stage 2: The Structured Research Question (PICOT Framing)
> *"In patients undergoing laparoscopic cholecystectomy, how accurately do deep learning computer vision models identify the Critical View of Safety (CVS) compared to expert surgical consensus, and what reporting guidelines exist for clinical validation?"*
- *Improvement*:
  - **Population**: Patients undergoing laparoscopic cholecystectomy.
  - **Intervention**: Deep learning computer vision models (e.g. segmentation, frame classification).
  - **Comparator**: Expert surgical panel consensus / visual annotation.
  - **Outcomes**: Sensitivity, specificity, intersection over union (IoU), intraoperative guidance reliability.
  - **Guideline Targets**: SAGES consensus criteria for CVS, DECIDE-AI, TRIPOD-AI.

### Stage 3: The Multi-Agent Workflow Deconstruction
- **Coordinator Agent**:
  - Deconstructs CVS into the 3 Strasberg anatomical criteria (hepatocystic triangle clearance, cystic plate dissection, 2 structures entering gallbladder).
- **Evidence Specialist**:
  - Queries PubMed for multicenter prospective validation studies of computer vision in laparoscopic cholecystectomy.
  - Evaluates dataset diversity (e.g. Cholec80, Endoscapes) and algorithmic bias.
- **Guideline Specialist**:
  - Queries SAGES Safe Cholecystectomy guidelines and AI reporting standards (DECIDE-AI).
- **Final Evidence Brief**:
  - Synthesizes state of the science: computer vision achieves high accuracy on retrospective curated video datasets, but real-time prospective clinical trials measuring actual bile duct injury reduction are still pending.
