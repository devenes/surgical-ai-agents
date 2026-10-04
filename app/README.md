# Surgical AI Web UI (FastAPI + Streamlit)

Lightweight interactive web dashboard providing multimodal vision inspection and multi-agent consensus research for surgeons, medical educators, and AI researchers.

Inspired by [Google Cloud Generative AI Sample Apps](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/sample-apps/gemini-streamlit-cloudrun).

---

## 🌟 Key Features

1. **Multimodal Vision Studio**:
   - Supports image uploads (PNG, JPG, WEBP) and bundled surgical schematics (e.g. Critical View of Safety in laparoscopic cholecystectomy).
   - Structured visual feature extraction, operative landmark observation, and research application ideation.
   - Configurable parameters: model selection, thinking budget, temperature, top-p, max tokens.
   - Three output inspection tabs: *Observation & Analysis*, *Generation Parameters*, and *Raw JSON Payload*.

2. **2-Subagent Architecture (Coordinator + Evidence & Guideline Specialists)**:
   - **Coordinator Agent**: Decomposes natural language clinical questions into structured PICOT scope.
   - **Sub-Agent 1 (Evidence Specialist)**: Investigates randomized trials and systematic reviews (PubMed).
   - **Sub-Agent 2 (Guideline Specialist)**: Analyzes official recommendations from recognized surgical bodies (ASCRS, ERAS Society, SAGES, EAES).
   - **Cross-Specialist Synthesis**: Side-by-side comparative views and consensus/divergence matrix.
   - **Execution Pipeline Timeline**: Visual progress stepper showing each agent's execution latency and step details.

3. **Specialized Use-Case Tabs**:
   - `👁️ Multimodal Vision Studio`: Interactive image + prompt visual inspection.
   - `🤖 Multi-Agent Consensus Studio`: Full 2-subagent research orchestration with side-by-side findings.
   - `⚡ PICOT Query Decomposer`: Standalone utility to convert clinical queries into formal PICOT search parameters.
   - `📚 Specialist Deep-Dive`: Direct targeted query to either Evidence Specialist or Guideline Specialist.
   - `⚙️ API & Diagnostics`: Live FastAPI health check, ADC/API key status, and token saving recommendations.

4. **Zero-Token Offline Simulation Mode**:
   - Toggle in sidebar enables high-fidelity deterministic responses with **0 API tokens** used.
   - Comprehensive offline test suite validating all schemas, API routes, and service logic without external dependencies.

---

## 📂 Architecture

```
app/
├── __init__.py
├── cli.py                  # Unified CLI launcher
├── backend/
│   ├── __init__.py
│   ├── api.py              # FastAPI REST application & OpenAPI docs (/docs)
│   ├── schemas.py          # Pydantic request/response schemas
│   └── service.py          # AppService coordinating GenAI SDK & offline simulation
└── frontend/
    ├── __init__.py
    ├── main.py             # Streamlit dashboard entrypoint
    └── components.py       # Reusable UI widgets (sidebar, timeline, consensus matrix)
```

---

## 🚀 Quickstart

> 🪟 **Windows Users**: For dedicated PowerShell/CMD setup instructions, see the [Windows Setup Guide](../docs/windows-setup-guide.md).

### 1. Launch Both Backend & Frontend
```bash
uv run python -m app.cli all
```
- **Streamlit Web UI**: http://127.0.0.1:8501
- **FastAPI OpenAPI Swagger**: http://127.0.0.1:8000/docs

### 2. Launch FastAPI Backend Only
```bash
uv run python -m app.cli backend --backend-port 8000
```

### 3. Launch Streamlit UI Only
```bash
uv run python -m app.cli frontend --frontend-port 8501
```

---

## 🧪 Offline Testing

Run full offline test validation (0 tokens consumed):
```bash
uv run pytest tests/test_unit_app_*.py -v
```
