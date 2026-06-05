#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "   EmotionSense - Production Startup"
echo "========================================"

if [ ! -f "backend/model.pkl" ] || [ ! -f "backend/vectorizer.pkl" ]; then
  echo "[ERROR] Model files missing in backend/"
  echo "        Open ModelForge_AI.ipynb, run the last cell (save cell),"
  echo "        then re-run this script."
  exit 1
fi

if [ -d "venv" ]; then
  echo "[INFO] Activating virtual environment..."
  source venv/bin/activate
fi

PORT="${PORT:-8000}"
echo ""
echo "[1/1] Starting server on 0.0.0.0:${PORT}..."
exec python3 -m uvicorn backend.app:app --host 0.0.0.0 --port "${PORT}"
