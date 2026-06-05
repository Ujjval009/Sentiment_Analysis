#!/bin/bash
set -e

echo "========================================"
echo "   EmotionSense - Startup"
echo "========================================"

# Check venv
if [ ! -f "venv/bin/activate" ]; then
  echo "[ERROR] Virtual environment not found at venv/"
  echo "        Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# Check backend files
if [ ! -f "backend/model.pkl" ] || [ ! -f "backend/vectorizer.pkl" ]; then
  echo "[ERROR] Model files missing in backend/"
  echo "        Open ModelForge_AI.ipynb, run the last cell (save cell),"
  echo "        then re-run this script."
  exit 1
fi

echo ""
echo "[1/3] Activating Python environment..."
source venv/bin/activate

echo "[2/3] Starting backend API on port 8000..."
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..
sleep 2

# Verify backend started
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
  echo "  ✓ Backend is running at http://localhost:8000"
  echo "    API docs: http://localhost:8000/docs"
else
  echo "  ✗ Backend failed to start. Check logs above."
  kill $BACKEND_PID 2>/dev/null
  exit 1
fi

echo "[3/3] Starting frontend dev server on port 5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "   Both servers are running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped.'; exit" INT TERM
wait
