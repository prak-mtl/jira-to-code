#!/bin/bash

# Stop script for the Developer Productivity Dashboard demo

echo "=========================================="
echo "Stopping Demo Servers"
echo "=========================================="
echo ""

# Check if PID files exist
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo "✅ Backend stopped"
    else
        echo "⚠️  Backend process not found"
    fi
    rm .backend.pid
else
    echo "⚠️  No backend PID file found"
    # Try to find and kill any running backend
    pkill -f "simple_main.py" && echo "✅ Killed backend process" || echo "No backend process found"
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✅ Frontend stopped"
    else
        echo "⚠️  Frontend process not found"
    fi
    rm .frontend.pid
else
    echo "⚠️  No frontend PID file found"
    # Try to find and kill any running vite
    pkill -f "vite" && echo "✅ Killed frontend process" || echo "No frontend process found"
fi

echo ""
echo "=========================================="
echo "✅ Demo servers stopped"
echo "=========================================="

