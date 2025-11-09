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

# Run the web app (landing page) and dashboard
echo "Starting landing page on http://localhost:3000..."
echo "Starting dashboard on http://localhost:3001..."
pnpm dev --filter=vibeassist --filter=dashboard
