# Environment Inspection & Phase 2 Runtime Verification Report

**Date of Inspection**: October 2026 (Phase 2 Live ADK POC)
**Scope**: Virtual environment, Google Agent Development Kit (ADK), Vertex AI model connectivity, Application Default Credentials (ADC), Search Grounding, and safety boundary enforcement.

---

## Status Classification Legend

- **VERIFIED & WORKING**: Fully tested and confirmed operating in the live POC execution.
- **VERIFIED**: Static file or toolchain element confirmed present.
- **NOT WORKING**: Feature attempted but failing (none currently).
- **NOT TESTED**: Remote features intentionally deferred to Phase 3.
- **REQUIRES MANUAL ACTION**: Actions needing human credentials or approval (none currently; ADC is active).

---

## Status Matrix

| Component | Status | Details |
| :--- | :--- | :--- |
| **Virtual Environment** | **VERIFIED & WORKING** | `.venv` created via `uv venv --python 3.12` using CPython 3.12.13 |
| **ADK Framework** | **VERIFIED & WORKING** | `google-adk 2.11.0` installed in `.venv` |
| **Google GenAI SDK** | **VERIFIED & WORKING** | `google-genai 2.28.0` installed in `.venv` |
| **Authentication (ADC)** | **VERIFIED & WORKING** | Active credentials at `~/.config/gcloud/application_default_credentials.json` |
| **GCP Project** | **VERIFIED & WORKING** | Configured via `GOOGLE_CLOUD_PROJECT` (location: `us` / `global`) |
| **Gemini Foundation Models** | **VERIFIED & WORKING** | `gemini-3.8-flash` (`publishers/google/models/gemini-3.8-flash`) verified active |
| **Google Search Grounding** | **VERIFIED & WORKING** | `google.adk.tools.google_search` tested and grounded on live PubMed / trials |
| **URL Context Tool** | **VERIFIED & WORKING** | `google.adk.tools.url_context` attached to specialist research agents |
| **Agent-as-a-Tool Delegation**| **VERIFIED & WORKING** | `AgentTool(evidence_agent)` & `AgentTool(guideline_agent)` invoked by Coordinator |
| **Structured Output Schema** | **VERIFIED & WORKING** | Conforms 100% to `agents/coordinator/output-schema.json` via JSON Schema validation |
| **Live Primary Test Run** | **VERIFIED & WORKING** | Saved to `examples/research-questions/colorectal-prehabilitation-live-example.json` |
| **Safety Boundary Refusal** | **VERIFIED & WORKING** | Refuses patient-specific clinical questions; redirects to general research |
| **Automated Unit Tests** | **VERIFIED & WORKING** | 61 offline pytest tests passing across agents, Draft-07 schemas, FastAPI routes, and rehearsal cases |
| **Multimodal Vision Studio** | **VERIFIED & WORKING** | Operative landmark observation verified in Web UI (`app/`) and standalone CLI (`multimodal-demo/`) |
| **Production Cloud Run Container** | **VERIFIED & TESTED** | Production Dockerfile (`python:3.12-slim`, non-root) and deployment guide verified in `workshop/cloud-deployment.md` |
| **Enterprise RAG / Vector Stores** | **NOT TESTED** | Phase 4A hospital-specific institutional RAG deferred by design |

---

## Verified ADK Runtime Behavior

1. **Agent Orchestration**:
   - Coordinator does NOT perform search directly.
   - Coordinator invokes `evidence_agent` and `guideline_agent` as discrete tools via `AgentTool`.
   - Specialist agents invoke Google Search grounding to retrieve peer-reviewed literature and clinical guidelines.
   - Coordinator reconciles findings into agreements, disagreements, uncertainties, and limitations.

2. **Safety Enforcement**:
   - Direct patient management prompts (`EDGE-07`) trigger an immediate conversational refusal and educational redirection without generating clinical treatment directives.
