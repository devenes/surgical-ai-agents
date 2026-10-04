# Multimodal Demonstration Prompts

These prompts are designed for use with Gemini 3.8 Flash in the **Agent Studio Chat / Freeform** interface (or Vertex AI Studio Multimodal Prompt). They enforce neutral observation and prevent unauthorized clinical decision-making.

---

## 1. Primary Observation Prompt (Stage 1)

Upload the image from `multimodal-demo/assets/` and submit the following prompt:

```text
Describe only the observable visual features in this image. Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision.
```

### Expected Output Characteristics:
- **Objective Visual Inventory**: Identifies anatomical structures, surgical instruments, tissue contours, and spatial orientations visible in the image.
- **Epistemic Modesty**: Uses descriptive language (e.g. *"A tubular structure is visible traversing the field"*, *"Grasping instrument positioned in the upper right quadrant"*).
- **Prohibited Content**: Zero diagnostic statements (e.g. does NOT say *"This patient has acute gangrenous cholecystitis"*); zero treatment suggestions; zero go/no-go surgical advice.

---

## 2. Educational & Research Follow-Up Prompt (Stage 2)

Immediately following the model's response to Stage 1, submit this follow-up query in the same chat turn:

```text
Based on those observable features, explain what kinds of surgical research or computer-vision tasks might use similar visual information. Keep the answer educational and non-clinical.
```

### Expected Output Characteristics:
- **Computer Vision Tasks**: Semantic segmentation of anatomical planes, surgical tool detection/tracking, operative phase recognition, and Critical View of Safety (CVS) criteria verification.
- **Informatics Standards**: Mentions reporting guidelines for clinical AI (such as DECIDE-AI and TRIPOD-AI).
- **Zero Patient Decision**: Emphasizes that automated computer vision models are investigative tools requiring rigorous prospective trial validation before any clinical implementation.
