# daemon.py

import os
import threading
import time
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import json
from pathlib import Path

# --- 1. State Management ---
# The in-memory "Project Cortex"
# A thread lock is ESSENTIAL to prevent race conditions
state = {
    "security_score": 100,
    "active_issues": [],
    "project_charter": {"initialized": False},
    "last_analyzed_commit": None
}
state_lock = threading.Lock()

# Global project path (set on startup)
project_path = None
VIBE_ASSIST_DIR = None
STATE_FILE_PATH = None
CONTEXT_FILE_PATH = None

# --- 2. Core Logic Modules (Separate Files) ---
from . import analysis  # Contains all Gemini calls
from . import watcher   # Contains file/git watching logic
from . import screen    # Contains screenshot logic

# --- 3. FastAPI App ---
app = FastAPI(title="Vibe Assist API", version="0.1.0")

# Add CORS middleware to allow Next.js frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/state")
async def get_state():
    """Returns the current application state."""
    print("📡 API: GET /state")
    with state_lock:
        return state

@app.post("/oracle/generate_prompt")
async def generate_prompt_endpoint(goal: str = Form(...), screenshot: UploadFile = File(...)):
    """Generate an optimized prompt based on user goal and screenshot."""
    print(f"📡 API: POST /oracle/generate_prompt - Goal: {goal[:50]}...")

    # Read screenshot as bytes
    image_bytes = await screenshot.read()

    with state_lock:
        current_context = state.copy()

    prompt = analysis.generate_oracle_prompt(goal, image_bytes, current_context)
    return {"prompt": prompt}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    print("📡 API: GET /health")
    return {"status": "healthy", "gemini_initialized": analysis.client is not None}

def print_state_summary():
    """Print a summary of the current state to console."""
    with state_lock:
        print("\n" + "="*60)
        print("📊 CURRENT STATE SUMMARY")
        print("="*60)
        print(f"🔐 Security Score: {state['security_score']}/100")
        print(f"🚨 Active Issues: {len(state['active_issues'])}")

        if state['active_issues']:
            print("\nIssues:")
            for i, issue in enumerate(state['active_issues'][-5:], 1):  # Last 5 issues
                print(f"  {i}. [{issue['severity']}] {issue['type']}: {issue['description'][:60]}...")

        charter = state.get('project_charter', {})
        if charter.get('initialized'):
            commit_hash = state.get('last_analyzed_commit')
            if commit_hash:
                print(f"\n📋 Last Analyzed Commit: {commit_hash[:8]}")
        else:
            print("\n📋 Project charter not yet initialized.")

        print("="*60 + "\n")

# --- 4. Background Threads ---
def run_watcher_thread(project_path: str):
    """Thread for watching git diff and file changes."""
    watcher.start(project_path, state, state_lock, STATE_FILE_PATH, CONTEXT_FILE_PATH)

def run_screen_thread():
    """Thread for periodic screen analysis."""
    screen.start(state, state_lock)

def run_state_summary_thread():
    """Thread for periodic state summary display."""
    import time
    while True:
        time.sleep(60)  # Print summary every 60 seconds
        print_state_summary()

# --- 5. Main Execution Block ---
def main():
    """Main entry point for the daemon."""
    import sys
    import os
    global project_path, VIBE_ASSIST_DIR, STATE_FILE_PATH, CONTEXT_FILE_PATH, state

    if len(sys.argv) < 2:
        print("Usage: python -m daemon /path/to/your/project")
        print("   or: vibe-assist /path/to/your/project (if installed)")
        print("\nMake sure to set GEMINI_API_KEY environment variable:")
        print("  export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)

    project_path = sys.argv[1]

    # Verify project path exists
    if not os.path.exists(project_path):
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    print("="*60)
    print("Vibe Assist - Starting Daemon")
    print("="*60)

    # --- State and Context Initialization ---
    VIBE_ASSIST_DIR = Path(project_path) / ".vibe-assist"
    STATE_FILE_PATH = VIBE_ASSIST_DIR / "state.json"
    CONTEXT_FILE_PATH = VIBE_ASSIST_DIR / "context.vibe"

    VIBE_ASSIST_DIR.mkdir(exist_ok=True)

    if STATE_FILE_PATH.exists():
        print(f"✅ Found existing state file: {STATE_FILE_PATH}")
        with open(STATE_FILE_PATH, 'r') as f:
            loaded_state = json.load(f)
            # Update in-memory state with loaded data
            state.update(loaded_state)
    else:
        print("ℹ️  No state file found. Project will be initialized.")

    # Initialize Gemini client
    print("\nInitializing Gemini API client...")
    if not analysis.initialize_client():
        print("\nWARNING: Running without AI features.")
        print("Set GEMINI_API_KEY to enable AI analysis.")
    
    # Check if charter is initialized, if not, run the full analysis
    if not state.get("project_charter", {}).get("initialized"):
        print("\n🚀 Project charter not initialized. Performing first-time full codebase analysis...")
        analysis.initialize_project_context_full(
            project_path, state, state_lock, STATE_FILE_PATH, CONTEXT_FILE_PATH
        )
    else:
        print("\n✅ Project charter is already initialized.")


    print(f"\nMonitoring project: {project_path}")

    # Start the background threads
    print("\nStarting background threads...")
    watcher_thread = threading.Thread(
        target=run_watcher_thread,
        args=(project_path,),
        daemon=True,
        name="GitWatcher"
    )
    screen_thread = threading.Thread(
        target=run_screen_thread,
        daemon=True,
        name="ScreenAnalyzer"
    )
    summary_thread = threading.Thread(
        target=run_state_summary_thread,
        daemon=True,
        name="StateSummary"
    )

    watcher_thread.start()
    print("  ✓ Git watcher started")

    screen_thread.start()
    print("  ✓ Screen analyzer started")

    summary_thread.start()
    print("  ✓ State summary reporter started (60s interval)")

    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    # Start the FastAPI server (this will block the main thread)
    print(f"\nStarting API server on http://{host}:{port}")
    print(f"  - State endpoint: http://localhost:{port}/state")
    print(f"  - Oracle endpoint: http://localhost:{port}/oracle/generate_prompt")
    print(f"  - Health check: http://localhost:{port}/health")
    print(f"  - Docs: http://localhost:{port}/docs")
    print(f"\n📸 Screenshots saved to: /tmp/vibe-assist-screenshots")
    print("\nPress Ctrl+C to stop")
    print("="*60)

    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
