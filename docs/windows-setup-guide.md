# Windows Setup & Execution Guide

This guide provides step-by-step instructions for installing, configuring, and running **Surgical AI Agents** and the **FastAPI + Streamlit Web UI** on Windows 10 and Windows 11.

---

## 📋 Table of Contents
1. [Prerequisites on Windows](#1-prerequisites-on-windows)
2. [Step-by-Step Installation (PowerShell / CMD)](#2-step-by-step-installation-powershell--cmd)
3. [Virtual Environment Activation on Windows](#3-virtual-environment-activation-on-windows)
4. [Running the Web UI on Windows](#4-running-the-web-ui-on-windows)
5. [Configuring Google Cloud Credentials on Windows](#5-configuring-google-cloud-credentials-on-windows)
6. [Offline Zero-Token Testing on Windows](#6-offline-zero-token-testing-on-windows)
7. [Windows Troubleshooting & FAQ](#7-windows-troubleshooting--faq)

---

## 1. Prerequisites on Windows

Before getting started, make sure you have:

### A. Python 3.10+ (Python 3.12 Recommended)
- Download from [python.org/downloads/windows](https://www.python.org/downloads/windows/).
- ⚠️ **Important during installation**: Check the box **"Add python.exe to PATH"** at the bottom of the installer!
- **Disable App Execution Aliases** (if typing `python` opens the Microsoft Store):
  1. Open Windows **Settings** (`Win + I`).
  2. Go to **Apps** > **Advanced app settings** > **App execution aliases**.
  3. Turn **OFF** both toggles for `python.exe` and `python3.exe` (App Installer).

### B. Git for Windows
- Download and install [Git for Windows](https://git-scm.com/download/win) (enables Git Bash and PowerShell `git` commands).

### C. Recommended: `uv` (Ultra-Fast Package Manager)
In PowerShell, run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Or via Winget:
```cmd
winget install --id=astral-sh.uv -e
```
*Restart your terminal after installing `uv` so the path is refreshed.*

---

## 2. Step-by-Step Installation (PowerShell / CMD)

Open **PowerShell** or **Command Prompt (CMD)**:

```powershell
# 1. Clone the repository
git clone https://github.com/devenes/surgical-ai-agents.git
cd surgical-ai-agents

# 2. Create virtual environment
# Using uv (Recommended):
uv venv --python 3.12

# OR using standard Python venv:
python -m venv .venv
```

---

## 3. Virtual Environment Activation on Windows

The activation scripts on Windows are located in `.venv\Scripts\` (instead of `.venv/bin/` on Linux/macOS):

### In PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

> [!TIP]
> **If you see `execution of scripts is disabled on this system`**:
> Open PowerShell and run this one-time command to allow local scripts:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Then run `.venv\Scripts\Activate.ps1` again.

### In Command Prompt (CMD):
```cmd
.venv\Scripts\activate.bat
```

### In Git Bash:
```bash
source .venv/Scripts/activate
```

---

## 4. Install Dependencies

Once your virtual environment is active (or using `uv`):

```powershell
# Using uv (fastest, automatically manages virtualenv):
uv pip install -e ".[dev]"

# OR using standard pip:
pip install -e ".[dev]"
```

---

## 5. Running the Web UI on Windows

The Web UI comes with a unified launcher (`app/cli.py`) that coordinates both the **FastAPI REST backend** and the **Streamlit interactive frontend**.

### Option A: Launch Both Services Simultaneously (Recommended)

```powershell
# Using uv:
uv run python -m app.cli all

# OR with active virtual environment:
python -m app.cli all
```

Once launched:
- **Streamlit Web UI**: [http://127.0.0.1:8501](http://127.0.0.1:8501)
- **FastAPI OpenAPI Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

To stop both services: press `Ctrl + C` in your terminal window.

---

### Option B: Launch FastAPI Backend Only

```powershell
uv run python -m app.cli backend --backend-port 8000
```
- Access interactive Swagger docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- Test health endpoint:
  ```powershell
  curl http://127.0.0.1:8000/api/health
  ```

---

### Option C: Launch Streamlit Frontend Only

```powershell
uv run python -m app.cli frontend --frontend-port 8501
```

---

## 6. Configuring Google Cloud Credentials on Windows

### Zero-Token Offline Mode (No Google Cloud Account Required)
By default, the Web UI runs with **Zero-Token Offline Mode** enabled in the sidebar. You can inspect all multimodal vision features, 2-subagent consensus pipelines, and PICOT query decomposition with **0 tokens consumed** and **zero cloud credentials required**!

### Live Mode (Vertex AI / Gemini API)

If you wish to run live queries against Vertex AI on Google Cloud:

1. Install Google Cloud SDK for Windows from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install).
2. Authenticate Application Default Credentials (ADC):
   ```powershell
   gcloud auth application-default login
   ```
   *This saves your credentials to `%APPDATA%\gcloud\application_default_credentials.json`.*

3. Configure your `.env` file:
   ```powershell
   Copy-Item .env.example .env
   ```
   Edit `.env` using Notepad or VS Code:
   ```env
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   GOOGLE_CLOUD_LOCATION=us
   GEMINI_MODEL=gemini-3.8-flash
   ```

4. Or set temporary environment variables in PowerShell:
   ```powershell
   $env:GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   $env:GOOGLE_CLOUD_LOCATION="us"
   ```

---

## 7. Offline Zero-Token Testing on Windows

To run the offline unit test suite on Windows without consuming any API tokens:

```powershell
# Run the entire offline test suite (31 tests)
uv run pytest

# Run only the Web UI unit tests
uv run pytest tests/test_unit_app_*.py -v
```

All 31 offline tests pass deterministically in under 2 seconds.

---

## 8. Windows Troubleshooting & FAQ

### Q1: `Set-ExecutionPolicy` error when activating virtualenv in PowerShell
**Symptom**: `cannot be loaded because running scripts is disabled on this system.`  
**Fix**: Run:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### Q2: `Address already in use` error (Port 8000 or 8501)
**Symptom**: `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`  
**Fix**: Another application or a previous terminal process is using the port.
1. Check what is using port 8000:
   ```cmd
   netstat -ano | findstr :8000
   ```
2. Or simply run on a different port:
   ```powershell
   uv run python -m app.cli all --backend-port 8080 --frontend-port 8502
   ```

---

### Q3: Windows Defender Firewall prompt
**Symptom**: Windows Firewall popup asks: *"Windows Defender Firewall has blocked some features of this app"*.  
**Fix**: Check the box for **"Private networks"** and click **"Allow access"**. The app only communicates on `127.0.0.1` (local machine).

---

### Q4: Terminal encoding / Turkish characters or emoji display
**Symptom**: Odd symbols or `UnicodeEncodeError` in Windows Command Prompt.  
**Fix**: Ensure your Windows console is configured for UTF-8:
- In CMD:
  ```cmd
  chcp 65001
  ```
- In PowerShell:
  ```powershell
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  ```
- Use the modern [Windows Terminal](https://aka.ms/terminal) (built-in on Windows 11) for full emoji and UTF-8 support.

---

### Q5: Windows MAX_PATH Limitation (260 characters)
**Symptom**: Errors installing packages in deeply nested paths.  
**Fix**: Enable long paths in PowerShell (Run as Administrator):
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
