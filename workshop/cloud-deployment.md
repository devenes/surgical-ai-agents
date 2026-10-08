# Cloud Run & Container Deployment Guide (Additional Track)

> **Architectural Notice**:
> This deployment track is an **additional / advanced option** designed for production hosting, hospital institutional sharing, or continuous staging on Google Cloud.
> **The primary path of the 60-minute workshop remains the low-code Agent Studio visual designer and local ADK development environment.**

---

## Overview

You can deploy the complete Surgical AI Web Studio (Streamlit UI + FastAPI backend + 16 benchmark cases) to **Google Cloud Run** using either:
1. **Source-based deployment via Cloud Buildpacks** (fastest, no Dockerfile required)
2. **Custom production Dockerfile via Google Artifact Registry** (maximum security, non-root user, explicit layers)

Both deployment paths adhere strictly to the **Principle of Least Privilege** using a dedicated Custom Service Account (`surgical-agent-sa`) restricted to `roles/aiplatform.user`.

---

## Method 1: Deploy Directly from Source (Cloud Buildpacks)

Deploying directly from source is ideal for fast iterations and workshop demonstrations where attendees do not want to manage local Docker daemons.

### Step 1: Create Dedicated Service Account (Least Privilege)

```bash
# Set your active project and regions
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"      # Cloud Run compute region
export VERTEX_LOCATION="us"     # Vertex AI multi-region for gemini-3.8-flash (us-central1 returns 404)

# Create a dedicated, non-privileged service account
gcloud iam service-accounts create surgical-agent-sa \
  --description="Dedicated service account for Surgical AI ADK Agent on Cloud Run" \
  --display-name="Surgical Agent Service Account"
```

### Step 2: Grant Least-Privilege IAM Roles

Grant only the Gemini Enterprise Agent Platform user role (`roles/aiplatform.user`):

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Step 3: Deploy to Cloud Run from Source

Cloud Run automatically analyzes your repository, detects `requirements.txt`, and uses Google Cloud Buildpacks to compile a secure runtime container:

```bash
gcloud run deploy surgical-ai-studio \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --labels workshop=cerrahi-kongresi \
  --command "/cnb/lifecycle/launcher" \
  --args "sh,-c,python3 -m streamlit run app/frontend/main.py --server.port=\$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false --server.headless=true" \
  --service-account "surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --set-env-vars GOOGLE_GENAI_USE_ENTERPRISE=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$VERTEX_LOCATION
```

> **Note**: If prompted to create an Artifact Registry Docker repository to store built containers (e.g., *Do you want to continue (Y/n)?*), enter `Y`. Buildpack compilation takes approximately 3–4 minutes.

---

## Method 2: Custom Production Dockerfile & Artifact Registry

For institutional hospital compliance, air-gapped clinical intranets, or strict container vulnerability scans, use the repository's production [`Dockerfile`](../Dockerfile).

### Security Architecture of the Dockerfile
- **Base Image**: `python:3.12-slim` for minimal CVE exposure and minimal image size.
- **Least-Privilege User**: Runs as non-root `appuser` (UID 10001) in `appgroup` (GID 10001).
- **Environment Flags**: `PYTHONUNBUFFERED=1` and `PYTHONDONTWRITEBYTECODE=1`.
- **Healthcheck**: Periodically probes `http://localhost:${PORT}/_stcore/health`.
- **Flexible Entrypoint**: [`docker-entrypoint.sh`](../docker-entrypoint.sh) supports:
  - `streamlit` (default: runs Streamlit on `$PORT`)
  - `backend` (runs FastAPI via uvicorn on `$PORT`)
  - `all` (runs FastAPI on internal port 8000 and Streamlit on `$PORT`)
  - `rehearse` (executes zero-token dry-run rehearsal)

### Step 1: Build & Verify Locally

```bash
# 1. Build local container image
docker build -t surgical-ai-agents:latest .

# 2. Run automated zero-token simulation rehearsal inside container
docker run --rm surgical-ai-agents:latest rehearse

# 3. Test interactive web application locally
docker run -d --name surgical-ai-app -p 8080:8080 -e PORT=8080 surgical-ai-agents:latest

# 4. Verify health check
curl -I http://localhost:8080/_stcore/health

# 5. Clean up local test container
docker stop surgical-ai-app && docker rm surgical-ai-app
```

### Step 2: Push to Google Artifact Registry

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"      # Cloud Run compute region
export VERTEX_LOCATION="us"     # Vertex AI multi-region for gemini-3.8-flash (us-central1 returns 404)
export REPO="surgical-ai-repo"

# 1. Create Docker repository in Artifact Registry
gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION \
  --description="Docker repository for Surgical AI multi-agent workshop"

# 2. Configure Docker authentication
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

# 3. Tag and push container image
docker tag surgical-ai-agents:latest $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/surgical-ai-studio:latest
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/surgical-ai-studio:latest
```

### Step 3: Deploy Pre-Built Image to Cloud Run

```bash
gcloud run deploy surgical-ai-studio \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/surgical-ai-studio:latest \
  --region $REGION \
  --allow-unauthenticated \
  --service-account "surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --set-env-vars GOOGLE_GENAI_USE_ENTERPRISE=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$VERTEX_LOCATION
```

---

## 💬 Discussion: Deploying Containers vs. Source & IAM Security

### 1. How did Cloud Run build our app without a Dockerfile?
When using `gcloud run deploy --source .`, Cloud Run leverages **CNCF Buildpacks** under the hood. Buildpacks inspect the root directory: upon detecting `requirements.txt` and Python source files, the buildpack engine automatically selects a secure Python runtime, creates a multi-layer container, installs dependencies, and prepares the launcher.

- **Deploying from source (`--source .`)**: Ideal for rapid prototyping and classroom codelabs. Requires zero local Docker daemon setup.
- **Custom `Dockerfile`**: Essential for production compliance, custom C/system libraries, deterministic multi-stage caching, and non-root user enforcement.

### 2. Why a dedicated Service Account instead of the default Compute Engine account?
**Safety and clinical data protection first.**
- The default Compute Engine service account (`{PROJECT_NUMBER}-compute@developer.gserviceaccount.com`) is granted the broad **Editor (`roles/editor`)** role by default.
- If an application running under the default service account contains a software dependency vulnerability or prompt injection flaw, an attacker could potentially read, modify, or delete any cloud storage buckets, databases, or VM resources across your entire Google Cloud project.
- By provisioning a dedicated service account (`surgical-agent-sa`) and binding **only** `roles/aiplatform.user`, we enforce the **Principle of Least Privilege**: the container has the precise permissions needed to invoke Gemini foundational models on Vertex AI, and absolutely nothing else.

---

## 🧹 Cost Management & GCP Cleanup Protocol

To avoid incurring ongoing storage or hosting charges on Google Cloud after your workshop or testing session concludes, run the following cleanup commands:

```bash
# 1. Delete the Cloud Run service (terminates compute instances)
gcloud run services delete surgical-ai-studio \
  --region $REGION \
  --quiet

# 2. Delete the Artifact Registry repository (removes stored container images)
gcloud artifacts repositories delete $REPO \
  --location=$REGION \
  --quiet

# 3. Delete the dedicated service account
gcloud iam service-accounts delete surgical-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --quiet
```
