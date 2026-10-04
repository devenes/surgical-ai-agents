#!/bin/bash
set -e

PORT="${PORT:-8080}"
BACKEND_PORT="${BACKEND_PORT:-8000}"

if [ "$1" = "backend" ]; then
    echo "🩺 Starting FastAPI backend on port $PORT..."
    exec uvicorn app.backend.api:app --host 0.0.0.0 --port "$PORT"
elif [ "$1" = "all" ]; then
    echo "🚀 Starting FastAPI backend on internal port $BACKEND_PORT..."
    uvicorn app.backend.api:app --host 127.0.0.1 --port "$BACKEND_PORT" &
    BACKEND_PID=$!

    echo "🩺 Starting Streamlit UI on public port $PORT..."
    python3 -m streamlit run app/frontend/main.py \
        --server.port "$PORT" \
        --server.address 0.0.0.0 \
        --server.enableCORS false \
        --server.enableXsrfProtection false \
        --server.headless true &
    STREAMLIT_PID=$!

    trap "kill $BACKEND_PID $STREAMLIT_PID 2>/dev/null" EXIT INT TERM
    wait -n $BACKEND_PID $STREAMLIT_PID
elif [ "$1" = "rehearse" ]; then
    echo "🛡️ Running zero-token offline simulation rehearsal..."
    exec python3 -m app.cli rehearse
elif [ "$1" = "streamlit" ] || [ -z "$1" ]; then
    echo "🩺 Starting Streamlit application on port $PORT..."
    exec python3 -m streamlit run app/frontend/main.py \
        --server.port "$PORT" \
        --server.address 0.0.0.0 \
        --server.enableCORS false \
        --server.enableXsrfProtection false \
        --server.headless true
else
    exec "$@"
fi
