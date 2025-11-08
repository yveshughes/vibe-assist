#!/bin/bash

# Kill existing processes on ports 8000, 3000, 3001
echo "Stopping any running processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:3001 | xargs kill -9 2>/dev/null || true
sleep 1

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "pnpm not found. Installing pnpm..."
    npm install -g pnpm
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    pnpm install
fi

# Setup Python virtual environment if it doesn't exist
if [ ! -d "apps/daemon/venv" ]; then
    echo "Creating Python virtual environment..."
    cd apps/daemon
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ../..
fi

# Start daemon in background
echo "Starting daemon on http://localhost:8000..."
cd apps/daemon
source venv/bin/activate
nohup python -m src.daemon /Users/andriikonovalenko/vibe-assist > ../../daemon.log 2>&1 &
echo "Daemon started (logs: daemon.log)"
cd ../..

# Wait a moment for daemon to start
sleep 2

# Run the web app (landing page) and dashboard
echo "Starting landing page on http://localhost:3000..."
echo "Starting dashboard on http://localhost:3001..."
pnpm dev --filter=vibeassist --filter=dashboard
