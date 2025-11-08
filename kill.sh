#!/bin/bash

echo "Stopping all running processes..."

# Kill processes on ports 8000, 3000, 3001
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:3001 | xargs kill -9 2>/dev/null || true

echo "All processes stopped."
