# Historical Exploratory Prototypes (Archive)

This directory contains early exploratory prototypes and experimental multi-agent workflow drafts exported during initial architecture design:

| File | Exploration Topic | Architecture & Pipeline | Description |
| :--- | :--- | :--- | :--- |
| [`1.py`](1.py) | 3-Agent Hierarchical Evidence Synthesis | `surgical_evidence_coordinator` → `evidence_specialist` → `guideline_specialist` | Hierarchical delegation pipeline synthesizing peer-reviewed surgical trials and clinical guidelines into a structured JSON evidence brief with PICOT scoping. |
| [`2.py`](2.py) | 6-Agent Sequential Research & Verification | `Surgical_Research_Coordinator` → `evidence_finder` → `guideline_finder` → `recent_evidence_finder` → `study_critic` → `source_checker` → `final_writer` | Multi-step sequential chaining pipeline with dedicated evidence search, guideline lookup, recent literature updates, methodological critique, rigorous URL verification/recovery, and calibrated synthesis. |
| [`3.py`](3.py) | Postoperative Sentinel & Deterioration Monitoring | `Clinical_Deterioration_Analyzer` → `postoperative_evidence__guideline_specialist` → `final_postoperative_sentinel` | Clinical decision-support pipeline evaluating postoperative recovery trajectories, vital sign and biomarker trends, complication pattern recognition (e.g., anastomotic leak, collection, bleeding), and safety alerts. |
| [`4.py`](4.py) | Multidisciplinary Tumor Board (MDT) Oncology Brief | `Surgical_MDT_Case_Board` → `clinical_case_analyst_2` → `evidence_guideline_specialist` → `final_mdt_synthesis_agent_2` | Surgical oncology case board workflow structuring patient cases, retrieving clinical guidelines and clinical trials, and synthesizing consensus points, evidence gaps, and treatment options for MDT discussion. |

> **Note**: These files are preserved for historical reference and exploration ideas. The active production ADK implementation is maintained in [`adk/`](../adk/) and the active workshop configuration in [`agents/agent-studio/`](../agents/agent-studio/).
