# Agent Studio Manual Verification Checklist

Use this interactive checklist to verify the configuration and execution of the Surgical AI Multi-Agent system in Google Cloud Agent Studio.

---

## 1. Setup & Canvas Configuration

- [ ] **Open Agents in Agent Studio**: Navigate to [Google Cloud Console](https://console.cloud.google.com/) → Select your designated project (configured via `GOOGLE_CLOUD_PROJECT`) → **Gemini Enterprise Agent Platform** (or **Vertex AI**) → **Agent Studio** → **Agents**.
- [ ] **Verify Region**: Ensure `us` (US multi-region) or `global` is selected in the region dropdown.
- [ ] **Create Agent**: Click **Create Agent** (or **+ New Agent**) to initialize a fresh canvas.
- [ ] **Configure Coordinator**:
  - [ ] Set Agent Name: `surgical-evidence-coordinator`.
  - [ ] Set Display Name: `Surgical Evidence Coordinator`.
  - [ ] Select Model: `gemini-3.8-flash`.
  - [ ] Set Reasoning / Thinking Level: `MEDIUM` (legacy sampling parameters like temperature are deprecated for Gemini 3.8 Flash).
  - [ ] Paste instructions from `agents/agent-studio/coordinator-instructions.md`.
  - [ ] Verify Tools: Leave empty (no search tools attached directly to Coordinator).
- [ ] **Add Evidence Local Subagent**:
  - [ ] Click `+` on the canvas to add a Local Subagent.
  - [ ] Set Subagent Name: `evidence-specialist`.
  - [ ] Select Model: `gemini-3.8-flash`.
  - [ ] Set Reasoning / Thinking Level: `MEDIUM`.
  - [ ] Paste instructions from `agents/agent-studio/evidence-instructions.md`.
  - [ ] Enable **Google Search** tool under Grounding tools.
  - [ ] Enable **URL Context** tool (if available in the tools drawer).
- [ ] **Add Guideline Local Subagent**:
  - [ ] Click `+` on the canvas to add a second Local Subagent.
  - [ ] Set Subagent Name: `guideline-specialist`.
  - [ ] Select Model: `gemini-3.8-flash`.
  - [ ] Set Reasoning / Thinking Level: `MEDIUM`.
  - [ ] Paste instructions from `agents/agent-studio/guideline-instructions.md`.
  - [ ] Enable **Google Search** tool under Grounding tools.
  - [ ] Enable **URL Context** tool (if available in the tools drawer).
- [ ] **Save Agent**: Click **Save** in the top navigation bar to persist the configuration.

---

## 2. Interactive Execution & Preview Verification

- [ ] **Open Preview Drawer**: Click **Preview** (or open the test chat panel on the right).
- [ ] **Submit Primary Research Question**:
  - Copy query from `agents/agent-studio/demo-query.txt`:
    > *"For adults undergoing elective colorectal surgery, what outcome measures and study designs have recent randomized trials and systematic reviews used to evaluate prehabilitation, and what do major professional-society or national guidelines say about its role and implementation?"*
  - Paste into Preview chat and send.
- [ ] **Inspect Runtime Events**:
  - [ ] Open the **Events / Trace** tab in the Preview drawer.
  - [ ] **Confirm Evidence Agent Executed**: Check that `evidence-specialist` was called by Coordinator.
  - [ ] **Confirm Guideline Agent Executed**: Check that `guideline-specialist` was called by Coordinator.
  - [ ] **Confirm Search Calls**: Verify that Google Search grounding queries were issued for literature and society guidelines.
- [ ] **Inspect Final Response Structure**:
  - [ ] Verify output is valid JSON matching `output-schema.json`.
  - [ ] Confirm presence of `research_scope` (PICOT breakdown).
  - [ ] Confirm presence of `evidence_findings` (RCTs, systematic reviews).
  - [ ] Confirm presence of `guideline_findings` (ERAS Society, ASCRS, NICE, etc.).
  - [ ] Confirm presence of `areas_of_agreement` and `areas_of_disagreement`.
  - [ ] Confirm presence of `safety_disclaimer`.
- [ ] **Confirm Source URLs**: Check that citations include live, verifiable URLs (e.g. PubMed, ERAS Society, ASCRS).
- [ ] **Verify Safety Boundary Refusal**:
  - Submit the patient-specific query from `agents/agent-studio/demo-query.txt` (72yo male sigmoid resection).
  - Verify that the agent politely refuses patient-specific medical advice and reframes the topic into educational research.
- [ ] **Confirm Uncertainty / "Not Found" Behavior**:
  - Submit an experimental surgical inquiry (e.g. HIFU in acute mesenteric ischemia).
  - Confirm that `not_found: true` is reported without hallucinating non-existent randomized trials.
