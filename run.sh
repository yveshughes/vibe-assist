#!/bin/bash

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

# Check if daemon is already running
if ! lsof -i :8000 &> /dev/null; then
    echo "Starting daemon on http://localhost:8000..."

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
    cd apps/daemon
    source venv/bin/activate
    nohup python -m src.daemon /Users/andriikonovalenko/vibe-assist > ../../daemon.log 2>&1 &
    echo "Daemon started (logs: daemon.log)"
    cd ../..

    # Wait a moment for daemon to start
    sleep 2
else
    echo "Daemon already running on http://localhost:8000"
fi

# Run the web app
echo "Starting web app on http://localhost:3000..."
pnpm dev --filter=web
