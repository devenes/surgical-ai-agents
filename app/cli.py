"""Command line interface to launch the Surgical AI Web UI and FastAPI backend."""

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_backend(port: int = 8000, host: str = "127.0.0.1", reload: bool = True) -> None:
    """Launch the FastAPI backend server using uvicorn."""
    import uvicorn

    print(
        f"🚀 Starting FastAPI backend at http://{host}:{port} (docs at http://{host}:{port}/docs)..."
    )
    uvicorn.run("app.backend.api:app", host=host, port=port, reload=reload)


def _stop_process(proc: subprocess.Popen) -> None:
    """Safely terminate a child process across Windows, macOS, and Linux."""
    if proc is None or proc.poll() is not None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=2.0)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def run_frontend(port: int = 8501, host: str = "127.0.0.1") -> None:
    """Launch the Streamlit frontend application."""
    frontend_path = REPO_ROOT / "app" / "frontend" / "main.py"
    print(f"🩺 Starting Streamlit UI at http://{host}:{port}...")
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(frontend_path),
        "--server.port",
        str(port),
        "--server.address",
        host,
        "--server.headless",
        "true",
    ]
    subprocess.run(cmd, check=True)


def run_all(backend_port: int = 8000, frontend_port: int = 8501) -> None:
    """Launch both FastAPI backend and Streamlit frontend concurrently."""
    frontend_path = REPO_ROOT / "app" / "frontend" / "main.py"
    print("=" * 60)
    print("SURGICAL AI MULTIMODAL & MULTI-AGENT WORKSPACE")
    print("=" * 60)
    print(f"Backend API:  http://127.0.0.1:{backend_port} (/docs for Swagger)")
    print(f"Streamlit UI: http://127.0.0.1:{frontend_port}")
    print("Press Ctrl+C to stop both services gracefully.")
    print("-" * 60)

    # Spawn backend as subprocess
    backend_proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.backend.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(backend_port),
        ]
    )

    time.sleep(1.2)
    frontend_proc = None

    try:
        frontend_proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(frontend_path),
                "--server.port",
                str(frontend_port),
                "--server.address",
                "127.0.0.1",
                "--server.headless",
                "true",
            ]
        )
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        _stop_process(backend_proc)
        _stop_process(frontend_proc)
        print("Services stopped successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Surgical AI Web UI Launcher")
    parser.add_argument(
        "service",
        choices=["backend", "frontend", "all"],
        default="all",
        nargs="?",
        help="Service to launch: 'backend' (FastAPI), 'frontend' (Streamlit), or 'all' (both).",
    )
    parser.add_argument(
        "--backend-port", type=int, default=8000, help="FastAPI port (default: 8000)"
    )
    parser.add_argument(
        "--frontend-port", type=int, default=8501, help="Streamlit port (default: 8501)"
    )
    args = parser.parse_args()

    if args.service == "backend":
        run_backend(port=args.backend_port)
    elif args.service == "frontend":
        run_frontend(port=args.frontend_port)
    elif args.service == "all":
        run_all(backend_port=args.backend_port, frontend_port=args.frontend_port)


if __name__ == "__main__":
    main()
