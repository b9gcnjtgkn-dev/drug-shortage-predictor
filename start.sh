#!/bin/bash

# start.sh - Launch the Drug Shortage Predictor AI Product

echo "🚀 Starting Drug Shortage Predictor AI..."

# Kill any existing processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start Backend
echo "🐍 Starting FastAPI Backend on port 8000..."
source venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "💻 Starting Next.js Frontend on port 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Both servers are starting!"
echo "➡️  Frontend Dashboard: http://localhost:3000"
echo "➡️  Backend API Docs: http://localhost:8000/docs"
echo "Press Ctrl+C to stop both servers."

# Wait for user interrupt
trap "echo 'Stopping servers...'; kill -9 $BACKEND_PID; kill -9 $FRONTEND_PID; exit" SIGINT SIGTERM
wait
