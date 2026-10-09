# Multimodal Demonstration Assets & Licensing Registry

- **Directory Scope**: De-identified demonstration radiology images and echocardiogram video for the multimodal vision and video studios.
- **Safety Rule**: **100% Zero-PHI and Zero Patient Identification**.

---

## 1. Compliance & Ethical Standards

In strict compliance with healthcare privacy laws (HIPAA, GDPR) and ethical AI research standards:
- **Zero Protected Health Information (PHI)**: All imagery and video clips are completely de-identified, non-identifiable, open-access, and scrubbed of any patient identifiers, DICOM tags, dates, hospital names, or demographic information.
- **Permissive / Open-Access**: All assets are drawn from public educational archives and open medical repositories for teaching, algorithm benchmarking, and multimodal AI demonstration.
- **Educational / Non-Diagnostic Scope**: Assets are strictly evaluated for computer-vision and feature extraction benchmarks; no clinical diagnosis or patient-specific decisions are produced.

---

## 2. Asset Catalog

| Asset Filename | Modality / Anatomy | Description | Format |
| :--- | :--- | :--- | :--- |
| `miliary-tuberculosis-5.jpeg` | Plain Radiograph (Chest PA) | Bilateral diffuse micronodular pulmonary opacities in classic miliary pattern | JPEG |
| `anterior-shoulder-dislocation-26.jpeg` | Plain Radiograph (Shoulder) | Glenohumeral joint alignment showing anterior-inferior humeral head displacement | JPEG |
| `phalanx-fracture-hand.png` | Plain Radiograph (Hand) | Osseous cortical continuity disruption and alignment of phalanges | PNG |
| `osteochondroma-femur-7.png` | Plain Radiograph (Femur) | Metaphyseal exostosis continuous with host cortex and medullary canal | PNG |
| `pulmonary-metastatic-calcification.jpeg` | Plain Radiograph (Chest PA) | High-density confluent parenchymal opacities and calcifications | JPEG |
| `apical_4_chamber_echo.mp4` | Transthoracic Echocardiogram (TTE) | Real-time dynamic apical 4-chamber video showing ventricular/atrial wall motion | MP4 (H.264) |

---

## 3. Asset Details & Modality Descriptions

### 1. `miliary-tuberculosis-5.jpeg`
- **Projection**: Posteroanterior (PA) chest radiograph.
- **Observed Features**: Fine, uniform 1-2 mm micronodules scattered symmetrically throughout both lung fields. Preserved sharp costophrenic angles and normal cardiothoracic ratio.
- **Research Utility**: Benchmark for diffuse nodular segmentation and lung field pattern classification.

### 2. `anterior-shoulder-dislocation-26.jpeg`
- **Projection**: Anteroposterior (AP) shoulder radiograph.
- **Observed Features**: Humeral head displaced inferomedially relative to the glenoid fossa, resting beneath the coracoid process.
- **Research Utility**: Joint alignment recognition and trauma classification.

### 3. `phalanx-fracture-hand.png`
- **Projection**: Plain hand radiograph.
- **Observed Features**: Discrete cortical breach across phalangeal shaft with minimal angular deformity.
- **Research Utility**: Bone cortical boundary extraction and fracture detection models.

### 4. `osteochondroma-femur-7.png`
- **Projection**: Femur radiograph (knee joint adjacent).
- **Observed Features**: Bony outgrowth from the distal femoral metaphysis pointing away from the joint space, showing direct corticomedullary continuity.
- **Research Utility**: Musculoskeletal lesion boundary segmentation and morphometry.

### 5. `pulmonary-metastatic-calcification.jpeg`
- **Projection**: Chest radiograph.
- **Observed Features**: Confluent dense calcific parenchymal opacities predominantly affecting the upper and mid lung zones.
- **Research Utility**: High-attenuation density profiling and lung field segmentation.

### 6. `apical_4_chamber_echo.mp4`
- **Modality**: Transthoracic Echocardiogram (TTE), Apical 4-Chamber view.
- **Observed Features**: Real-time contraction and rhythmic wall motion of the Left Ventricle (LV), Right Ventricle (RV), Left Atrium (LA), and Right Atrium (RA); mitral and tricuspid valvular leaflets opening during diastole and coapting during systole; spontaneous echo contrast ("smoke") observable in the left atrium.
- **Research Utility**: Temporal video transformers, automated ejection fraction (EF) estimation, and multi-chamber segmentation across cardiac cycles.
