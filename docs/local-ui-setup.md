# Local UI Setup & User Guide (FastAPI + Streamlit)

This guide provides step-by-step instructions for running, testing, and developing the **Surgical AI Web UI** locally.

---

## 🌟 Architecture Overview

The Web UI is structured into two lightweight layers located in [`app/`](../app/):

- **Backend (FastAPI)**: REST API serving multimodal vision endpoints, multi-agent consensus pipelines, query decomposition, and OpenAPI Swagger documentation at [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).
- **Frontend (Streamlit)**: An interactive, user-friendly interface inspired by [Google Cloud Generative AI Sample Apps](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/sample-apps/gemini-streamlit-cloudrun) accessible at [`http://localhost:8501`](http://localhost:8501).
- **Unified CLI Launcher ([`app/cli.py`](../app/cli.py))**: A single command-line interface to launch the backend, frontend, or both simultaneously.

---

## 🚀 Prerequisites & Installation

### 1. Python Environment
Make sure you have Python 3.10+ installed (Python 3.12 recommended) and `uv` package manager:

> 🪟 **Windows Users**: For detailed Windows PowerShell/CMD instructions, virtualenv scripts (`.venv\Scripts\Activate.ps1`), and troubleshooting, see the dedicated [Windows Setup Guide](windows-setup-guide.md).

```bash
# Clone the repository (if not already done)
git clone https://github.com/devenes/surgical-ai-agents.git
cd surgical-ai-agents

# Create and activate virtual environment
# On macOS/Linux:
uv venv --python 3.12
source .venv/bin/activate

# On Windows (PowerShell):
# uv venv --python 3.12
# .venv\Scripts\Activate.ps1

# Install all project dependencies (including FastAPI, Streamlit, and dev tools)
uv pip install -e ".[dev]"
```

---

## 💻 Running the UI Locally

You can launch the application in three ways using the unified launcher:

### Option A: Launch Both Backend & Frontend Simultaneously (Recommended)
```bash
uv run python -m app.cli all
```
This spawns:
- **Streamlit Web UI**: [`http://127.0.0.1:8501`](http://127.0.0.1:8501)
- **FastAPI Backend**: [`http://127.0.0.1:8000`](http://127.0.0.1:8000) (Swagger Docs: [`/docs`](http://127.0.0.1:8000/docs))

Press `Ctrl+C` in the terminal to stop both services gracefully.

---

### Option B: Launch FastAPI Backend Only
Useful for headless API testing, curl requests, or OpenAPI Swagger exploration:
```bash
uv run python -m app.cli backend --backend-port 8000
```
- Interactive Swagger UI: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- Interactive ReDoc: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)
- Health Check: `curl http://127.0.0.1:8000/api/health`

---

### Option C: Launch Streamlit Frontend Only
```bash
uv run python -m app.cli frontend --frontend-port 8501
```
*Note: The Streamlit app supports dual connection modes in the sidebar: it can connect directly in-process or route requests to the running FastAPI REST backend.*

---

## ⚡ Zero-Token Offline Simulation Mode

To minimize API cost and token usage during local development, testing, and UI demonstration, the system includes a **Zero-Token Offline Mode**:

1. **Default State**: Enabled by default in the sidebar (`⚡ Zero-Token Offline Mode`).
2. **Behavior**: Provides instant, deterministic, high-fidelity multimodal and multi-agent responses without calling external Vertex AI / Gemini APIs.
3. **Switching to Live Mode**:
   - Uncheck `⚡ Zero-Token Offline Mode` in the sidebar.
   - Ensure your environment has valid Google Cloud Application Default Credentials (`gcloud auth application-default login`) or `GOOGLE_API_KEY` set in your `.env` file.

---

## 🎛️ Features & Tab Breakdown

### 1. 👁️ Multimodal Vision Studio
- **Image Input**: Upload custom images (`PNG`, `JPG`, `WEBP`) or select the bundled *Critical View of Safety (CVS)* schematic.
- **Inquiry Prompts**: Choose from quick preset prompts (anatomical landmarks, CVS criteria, robotic computer vision research) or enter a custom prompt.
- **Inspectable Results**:
  - `Observation & Analysis`: Visual narrative and detected anatomical features.
  - `Generation Parameters`: Active model, latency, temperature, top-p, and estimated tokens.
  - `Raw JSON Payload`: Complete structured API response.

### 2. 🤖 Multi-Agent Consensus Studio
- **Coordinator + 2 Sub-Agents Architecture**:
  - `Coordinator Agent`: Decomposes natural language queries into PICOT.
  - `Sub-Agent 1 (Evidence Specialist)`: Searches and synthesizes clinical trials (PubMed).
  - `Sub-Agent 2 (Guideline Specialist)`: Queries surgical societies (ASCRS, ERAS, SAGES).
  - `Coordinator Synthesis`: Compares evidence vs guidelines, produces a consensus matrix, and formats verified sources.
- **Timeline Stepper**: Visual execution progress showing latency per step.
- **Side-by-Side Cards**: Direct visual comparison of empirical findings vs society guidelines.

### 3. ⚡ PICOT Query Decomposer
- Fast conversion of surgeon clinical questions into formal:
  - **P**opulation
  - **I**ntervention
  - **C**omparator
  - **O**utcomes
  - **T**imeframe
  - Keyword search vectors

### 4. 📚 Specialist Deep-Dive
- Query Sub-Agent 1 or Sub-Agent 2 independently for focused literature or guideline checks.

### 5. ⚙️ API & Diagnostics
- Ping FastAPI backend connection.
- Verify credential configuration (`GOOGLE_API_KEY`, `GOOGLE_CLOUD_PROJECT`).
- Review token saving recommendations.

---

## 🧪 Validating Offline Unit Tests

Run the full offline test suite without consuming any tokens:

```bash
# Run app-specific tests
uv run pytest tests/test_unit_app_*.py -v

# Run entire repository test suite
uv run pytest
```

All 31 offline tests pass deterministically in under 2 seconds.
