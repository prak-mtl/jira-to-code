#!/bin/bash

# Quick start script for the Developer Productivity Dashboard demo
# This script starts both backend and frontend servers

set -e

echo "=========================================="
echo "Developer Productivity Dashboard"
echo "Quick Start Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the demo-app directory"
    echo "Usage: cd demo-app && ./start-demo.sh"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Install backend dependencies if needed
echo "📦 Checking backend dependencies..."
if [ ! -f "backend/requirements.txt" ]; then
    echo "⚠️  Warning: requirements.txt not found, using default dependencies"
fi

# Install frontend dependencies if needed
echo "📦 Checking frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
cd ..

echo ""
echo "🚀 Starting servers..."
echo ""

# Start backend in background
echo "Starting backend on http://localhost:8000..."
cd backend
nohup python3 simple_main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend may not be ready yet, waiting..."
    sleep 2
fi

# Start frontend in background
echo "Starting frontend on http://localhost:3000..."
cd frontend
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
cd ..

# Wait for frontend to start
sleep 5

echo ""
echo "=========================================="
echo "✅ Demo is ready!"
echo "=========================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend/backend.log"
echo "   Frontend: tail -f frontend/frontend.log"
echo ""
echo "🛑 To stop the demo:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   or run: ./stop-demo.sh"
echo ""
echo "=========================================="
echo ""

# Save PIDs for stop script
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

# Open browser (optional, comment out if not desired)
if command -v open &> /dev/null; then
    echo "Opening browser..."
    sleep 2
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    echo "Opening browser..."
    sleep 2
    xdg-open http://localhost:3000
fi

echo "Press Ctrl+C to view logs, or close this terminal to keep servers running"
echo ""

# Follow logs
tail -f backend/backend.log frontend/frontend.log

