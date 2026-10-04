# Walkthrough Example: Colorectal Prehabilitation

This example demonstrates how a real-world surgical research topic is decomposed and synthesized by the multi-agent system.

---

## 1. Input Clinical Research Inquiry
> *"For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?"*

---

## 2. Coordinator PICOT Decomposition

- **Population**: Adults undergoing elective colorectal surgery (colon or rectal resection for benign or malignant indications).
- **Context**: Elective perioperative surgical care pathway within an Enhanced Recovery After Surgery (ERAS) framework.
- **Intervention**: Multimodal prehabilitation (structured physical exercise, nutritional screening and optimization, psychological stress-reduction/coaching) initiated 2–6 weeks prior to surgery.
- **Comparator**: Standard preoperative care, unassisted preoperative counseling, or single-modality prehabilitation (e.g. exercise alone).
- **Outcomes**:
  - Primary: Functional walking capacity (e.g., 6-Minute Walk Test [6MWT]), postoperative complication rate (Clavien-Dindo Classification Grade ≥2), hospital length of stay (LOS).
  - Secondary: 30-day and 90-day readmissions, mortality, compliance/adherence to prehab programs, health-related quality of life.
- **Time Range**: 2018–present.

---

## 3. Specialist Sub-Agent Delegation

### A. Query Delegated to Evidence Agent
- **Target**: Peer-reviewed systematic reviews, meta-analyses, and multicenter RCTs.
- **Search Scope**: `("colorectal surgery" OR "colectomy" OR "proctectomy") AND ("prehabilitation" OR "multimodal prehabilitation" OR "preoperative exercise") AND ("randomized controlled trial" OR "systematic review" OR "meta-analysis")`.
- **Key Evidence Extracted**:
  - *Minnella et al. (Annals of Surgery)*: Multimodal prehabilitation improved preoperative and postoperative functional walking capacity (6MWD), but observed mixed effects on overall Clavien-Dindo complications.
  - *Molenaar et al. (JAMA Surgery - PREHAB trial)*: Multicenter RCT showing multimodal prehabilitation reduced medical complications in high-risk patients undergoing colorectal cancer resection.
  - *Cochrane Systematic Review / Meta-analyses*: Identified significant heterogeneity in prehabilitation protocols, intervention durations, and adherence reporting.

### B. Query Delegated to Guideline Agent
- **Target**: Official guidelines from ASCRS, ERAS Society, and NICE.
- **Search Scope**: `("prehabilitation" OR "preoperative preparation") AND ("ERAS Society" OR "ASCRS" OR "NICE") AND "colorectal"`.
- **Key Recommendations Extracted**:
  - *ERAS Society Guidelines for Colorectal Surgery (2018/2023 update)*: Recommends preoperative exercise and nutritional optimization, especially in frail, elderly, or malnourished patients (Conditional/Moderate recommendation). Notes that while functional capacity consistently improves, reduction in surgical complications requires further high-quality trials.
  - *ASCRS Clinical Practice Guidelines for Enhanced Recovery (2023)*: Acknowledges prehabilitation as an evolving component; supports targeted preoperative optimization for high-risk patients.
  - *NICE Guidelines*: Endorses routine preoperative assessment and optimization of nutrition and physical activity prior to major elective cancer surgery.

---

## 4. Synthesized Evidence Brief (Representative Output)

```json
{
  "research_question": "For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?",
  "research_scope": {
    "population": "Adults undergoing elective colorectal resection",
    "context": "Elective inpatient surgical pathway / ERAS setting",
    "intervention_exposure": "Multimodal prehabilitation (exercise, nutrition, psychological support)",
    "comparator": "Standard preoperative care or single-modality prehabilitation",
    "outcomes": [
      "Functional walking capacity (6-Minute Walk Test)",
      "Postoperative complication rate (Clavien-Dindo)",
      "Hospital length of stay",
      "Comprehensive Complication Index"
    ],
    "time_range": "2018-2026"
  },
  "not_found": {
    "evidence_not_found": false,
    "guidelines_not_found": false,
    "details": "High-level randomized trial evidence and official society guidelines are both available."
  },
  "evidence_findings": {
    "summary": "Recent multicenter RCTs and meta-analyses consistently demonstrate that multimodal prehabilitation significantly preserves or improves perioperative functional walking capacity (6MWT). Evidence regarding reductions in 30-day postoperative complications is more nuanced: while significant reductions in medical complications are documented in frail or high-risk cohorts (e.g. PREHAB trial), universal reduction in surgical complications (e.g., anastomotic leak) remains unproven.",
    "key_study_findings": [
      {
        "study_title": "Effect of Multimodal Prehabilitation on Complications in High-Risk Patients Undergoing Colorectal Cancer Resection (PREHAB)",
        "authors_or_organization": "Molenaar et al.",
        "publication_year": 2023,
        "evidence_type": "randomized_controlled_trial",
        "primary_endpoints": [
          "Postoperative complications (Comprehensive Complication Index)",
          "Functional walking capacity"
        ],
        "key_findings": "Multimodal prehabilitation significantly reduced severe medical complications in high-risk patients compared to standard care.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/"
      }
    ]
  },
  "guideline_findings": {
    "summary": "Major surgical societies (ERAS Society, ASCRS) endorse the principles of prehabilitation, specifically highlighting targeted preoperative optimization (exercise and nutrition) in vulnerable, frail, or malnourished patients.",
    "guideline_statements": [
      {
        "organization": "ERAS Society",
        "guideline_title": "Guidelines for Perioperative Care in Elective Colorectal Surgery: Enhanced Recovery After Surgery (ERAS) Society Recommendations",
        "publication_or_update_year": 2023,
        "recommendation_summary": "Multimodal prehabilitation should be considered, particularly in patients with baseline frailty, low physical reserve, or high risk of postoperative morbidity.",
        "strength_of_recommendation": "Conditional recommendation, moderate-quality evidence",
        "url": "https://erassociety.org/guidelines/colorectal/"
      }
    ]
  },
  "sources": [
    {
      "source_id": "SRC-01",
      "title": "Effect of Multimodal Prehabilitation on Complications in High-Risk Patients Undergoing Colorectal Cancer Resection (PREHAB)",
      "author_or_institution": "Molenaar et al.",
      "year": 2023,
      "source_type": "randomized_trial",
      "url": "https://pubmed.ncbi.nlm.nih.gov/37099276/"
    },
    {
      "source_id": "SRC-02",
      "title": "Guidelines for Perioperative Care in Elective Colorectal Surgery",
      "author_or_institution": "ERAS Society",
      "year": 2023,
      "source_type": "practice_guideline",
      "url": "https://erassociety.org/guidelines/colorectal/"
    }
  ],
  "areas_of_agreement": [
    {
      "domain": "Functional Capacity and High-Risk Cohorts",
      "consensus_summary": "Both clinical trials and guidelines agree that prehabilitation improves baseline physiologic functional capacity and yields the greatest clinical return in frail, high-risk patients.",
      "supporting_sources": ["SRC-01", "SRC-02"]
    }
  ],
  "areas_of_disagreement": [
    {
      "issue": "Universal Application vs. Targeted Application",
      "divergence_description": "Some trial advocates propose universal prehabilitation for all elective colorectal patients, whereas guidelines currently recommend selective targeting of frail patients due to cost, logistics, and resource constraints.",
      "conflicting_sources": ["SRC-01", "SRC-02"]
    }
  ],
  "uncertainty": [
    {
      "topic": "Optimal Duration and Adherence",
      "uncertainty_rationale": "High heterogeneity exists in literature regarding optimal program length (2 weeks vs 4 weeks vs 8 weeks) and patient adherence rates in real-world settings."
    }
  ],
  "limitations": [
    "Most randomized trials have modest sample sizes and lack blinding due to the nature of exercise interventions.",
    "Variability in oncology treatment pathways (e.g. neoadjuvant chemotherapy timing) complicates standardized prehabilitation windows."
  ],
  "discussion_questions": [
    "How can surgical departments realistically operationalize a 4-week prehabilitation program without delaying cancer resection beyond recommended surgical waiting times?",
    "Which objective functional screening test (e.g., cardiopulmonary exercise testing vs 6MWT vs handgrip strength) is best suited for identifying candidates who benefit most?"
  ],
  "safety_disclaimer": "This evidence brief was generated by an educational AI research prototype for instructional purposes only. It does not constitute medical advice, patient diagnosis, or clinical decision support."
}
```
