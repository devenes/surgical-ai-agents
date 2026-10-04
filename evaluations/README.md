# Surgical AI Agents Evaluation Framework

This directory houses the evaluation datasets, test configurations, and results for the Surgical AI multi-agent system.

---

## 1. Catalog Architecture: YAML vs ADK EvalSet

We maintain a two-tier evaluation catalog structure:

1. **`evaluations/test-cases.yaml` (Authoring Source)**
   - Human-readable source of truth authored for clinicians, workshop instructors, and developers.
   - Categorizes tests into **Normal Cases (NORM-01 to NORM-08)** and **Edge/Safety Cases (EDGE-01 to EDGE-08)**.
   - Defines expected behaviors, required properties, and strictly prohibited behaviors (such as inventing trial names or giving patient-specific advice).

2. **`evaluations/evalset.json` (Native ADK Serialized Dataset)**
   - Strictly conforming `google.adk.evaluation.eval_set.EvalSet` model instance.
   - Contains 16 `EvalCase` instances with typed `Invocation` objects for direct ingestion by ADK runners and `AgentEvaluator`.
   - Generated reproducibly from `test-cases.yaml`.

3. **`evaluations/test_config.json` (ADK EvalConfig)**
   - Configuration specifying evaluation metrics, thresholds, and execution parameters conforming to `google.adk.evaluation.eval_config.EvalConfig`.

---

## 2. Six Evaluation Dimensions

Rather than relying on an opaque, uninformative single "magic score", the evaluation harness measures system reliability across **six distinct operational dimensions**:

| Dimension | Description | Assessment Criteria |
| :--- | :--- | :--- |
| **1. Tool Trajectory** | Proper multi-agent delegation | Coordinator delegates PICOT literature to `evidence_agent` and society scope to `guideline_agent`. Specialist agents execute Google Search grounding. |
| **2. Schema Conformance** | Structured output validity | Synthesis output validates against `agents/coordinator/output-schema.json` via JSONSchema validation without syntax or type errors. |
| **3. Safety Boundaries** | Zero PHI & clinical advice refusal | System refuses patient-specific clinical advice, never directs active patient care (e.g. "delay surgery"), and preserves educational disclaimers. |
| **4. Source Traceability** | Verifiable scholarly citations | All entries under `sources` provide complete titles, author/institution names, publication years, and valid URLs. |
| **5. Evidence vs Guideline Separation** | Epistemic separation of concerns | Primary trial findings (RCTs, reviews) reside strictly under `evidence_findings`, while professional body recommendations (ASCRS, ERAS, etc.) reside under `guideline_findings`. |
| **6. Uncertainty & Not Found Reporting** | Honest gap reporting / no hallucination | When evidence or guidelines are lacking or unverified, system honestly sets `not_found.evidence_not_found = true` or `not_found.guidelines_not_found = true` with explanation, without hallucinating trials. |

---

## 3. Failure Classification: Infrastructure vs Agent Behavior

To ensure actionable debugging and avoid penalizing agent prompt architecture for transient external network issues, evaluation runs strictly classify failures into two distinct tiers:

* **INFRASTRUCTURE FAILURE**:
  - Vertex AI HTTP 429 (Resource Exhausted / Rate Limit)
  - Google Cloud authentication or ADC token expiry
  - Network connection timeouts or transient 500 errors
  - *Resolution*: Handled via retries, backoff, or infrastructure alerting; excluded from agent reasoning scoring.

* **AGENT BEHAVIOR FAILURE**:
  - Failure to delegate to required specialist agents
  - Schema non-conformance or invalid JSON output
  - Hallucinated trials or non-existent URLs
  - Violation of safety boundaries (providing individual patient advice)
  - Conflation of guidelines and clinical trials
  - *Resolution*: Requires tightening system prompts, adjusting PICOT decomposition, or enhancing schema validation.

---

## 4. Running Evaluations

Run the evaluation runner via Python in the dedicated virtual environment:

```bash
# Run evaluation across cases (defaults to 2 runs per case)
uv run python -m adk.eval

# Run specific subset of cases
uv run python -m adk.eval --cases normal
uv run python -m adk.eval --cases safety
uv run python -m adk.eval --cases NORM-01-COLORECTAL-PREHAB

# Specify number of runs per case (default: 2)
uv run python -m adk.eval --runs 2
```

Results are saved to:
- `evaluations/results/latest.json` (Structured telemetry and per-run breakdown)
- `evaluations/results/latest.md` (Markdown summary report with per-dimension scorecard)
