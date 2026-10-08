# Google Cloud Setup & Prerequisites Guide

## Overview

This guide describes the prerequisites and configuration steps required to connect the multi-agent system to Google Cloud Vertex AI and Gemini services.

---

## 1. Verified Google Cloud Project Configuration

| Configuration Item | Status | Verified Value | Guidance |
| :--- | :--- | :--- | :--- |
| **GCP Project ID** | **VERIFIED & WORKING** | Configured via `GOOGLE_CLOUD_PROJECT` | Target project with active Vertex AI access. |
| **Primary Region** | **VERIFIED & WORKING** | `us` (US multi-region) | Default location for Gemini 3.8 Flash model endpoints (`global` also verified). |
| **Authentication** | **VERIFIED & WORKING** | Application Default Credentials (ADC) | Configured via `gcloud auth application-default login`. |
| **Verified Models**| **VERIFIED & WORKING** | `gemini-3.8-flash` | Model endpoint verified accessible on Vertex AI (`us` and `global`). |
| **Search Grounding**| **VERIFIED & WORKING**| Google Search Grounding | Operates via `google.adk.tools.google_search`. |

---

## 2. Google Cloud APIs

The following APIs are active and utilized by the multi-agent system:

- **Vertex AI API** (`aiplatform.googleapis.com`): Required for Gemini model inference via `google-genai` and `google-adk`.
- **Search Grounding**: Utilized natively through Vertex AI tool execution.

To enable these APIs on a new GCP project:
```bash
gcloud services enable \
    aiplatform.googleapis.com \
    discoveryengine.googleapis.com
```

---

## 3. Identity and Access Management (IAM) Roles

Access follows the principle of least privilege:

### Local Development / Workshop Facilitators (Verified Path)
Developers authenticate with their developer account using Google Cloud Application Default Credentials (ADC):
```bash
gcloud auth application-default login
```
This stores user credentials securely in `~/.config/gcloud/application_default_credentials.json`, outside of this repository. No API keys or service account keys are stored or needed.

### Automated Service Account Execution (Optional for CI/CD)
When running in headless automated pipelines or container environments (e.g. Cloud Run):
1. Create a dedicated service account: `surgical-ai-agent-runner@[GCP-PROJECT-ID].iam.gserviceaccount.com`
2. Assign minimal roles strictly following the Principle of Least Privilege:
   - **Vertex AI User** (`roles/aiplatform.user`): Required for Gemini model inference and prediction API calls.
   - **Discovery Engine Viewer** (`roles/discoveryengine.viewer`, optional): Required if integrating enterprise Discovery Engine datastores for search grounding.
   - **Cloud Run Invoker** (`roles/run.invoker`, optional): Required if invoking containerized services deployed to Cloud Run.

> [!IMPORTANT]
> **Regional Endpoint Constraint**:
> Foundation model `gemini-3.8-flash` is available in multi-region **`us`** and **`global`**. Deploying or executing against single-region `us-central1` will return `404 NOT_FOUND` for the model publisher endpoint. Always set `GOOGLE_CLOUD_LOCATION=us` (or `global`).

---

## 4. Model & Grounding Tool Configuration

### Foundation Models
- **Coordinator Agent**: `gemini-3.8-flash` on Vertex AI (`us` multi-region).
- **Evidence Agent**: `gemini-3.8-flash` with Google Search grounding and URL context tools attached.
- **Guideline Agent**: `gemini-3.8-flash` with Google Search grounding and URL context tools attached.

### Grounding Tools
- **`google_search`**: Built-in ADK tool (`google.adk.tools.google_search`) that issues real-time grounded queries to retrieve peer-reviewed literature and clinical guidelines.
- **`url_context`**: Built-in ADK tool (`google.adk.tools.url_context`) for targeted URL inspection.

---

## 5. Environment Configuration

Copy `.env.example` to `.env` (gitignored) if overriding project or location defaults:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us
GEMINI_MODEL=gemini-3.8-flash
```
