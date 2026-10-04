# Multimodal Safety Guardrails & Prohibitions

- **Scope**: Supplemental Multimodal Demo (Agent Studio Chat / Freeform & Standalone Python Script)
- **Status**: **STRICT NON-NEGOTIABLE POLICY**

---

## 1. Hard Prohibitions

When processing surgical or anatomical imagery, the system and presenter must strictly adhere to the following safety boundaries:

### 1. No Medical or Surgical Diagnosis
- The system must **never** diagnose pathological conditions from an image (e.g., classifying a lesion as malignant, diagnosing acute cholecystitis, identifying appendicitis).
- It must not output pathology grading or radiological staging for clinical decision-making.

### 2. No Patient-Specific Treatment Recommendations
- The system must **never** advise what medical therapy, drug, or operative procedure should be performed based on visual findings.

### 3. No Intraoperative Surgical Decisions (Go / No-Go)
- The system must **never** advise an intraoperative surgical action (e.g. *"Clip this structure"*, *"Transect here"*, *"Convert to open surgery"*, *"It is safe to divide this artery"*).
- The system must not serve as an intraoperative guidance device.

### 4. No Clinical Risk Stratification
- The system must **never** assign patient-specific complication probabilities, mortality scores, or risk tiers based on image analysis.

### 5. Zero Real Patient Data & Zero PHI
- Real patient hospital images, identifiable surgical video clips, PACS exports containing DICOM patient headers, or MRNs are strictly barred.
- All demonstration imagery must be 100% synthetic diagrams, open-access medical educational illustrations, or non-identifiable benchmark datasets with explicit permissive licenses.

---

## 2. Permitted Educational Behaviors

The system is permitted to perform strictly **neutral visual and informatics analysis**:
- **Describing Observable Visual Features**: Identifying geometric shapes, color variations, visible surgical instruments (graspers, clip appliers), anatomical planes, and spatial landmarks.
- **Educational Informatics Discussion**: Explaining how computer vision models (bounding box detection, semantic segmentation, optical flow) are evaluated in academic literature (e.g. IoU, DICE scores, DECIDE-AI guidelines).
- **Highlighting Limitations**: Explicitly noting limitations of 2D camera views, lighting artifacts, smoke occlusion, and camera motion.
