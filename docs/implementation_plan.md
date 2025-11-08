# Vibe Assist: Detailed Implementation Plan

This document outlines a pragmatic, step-by-step plan to build the Vibe Assist prototype. The architecture is centered around a single Python daemon for simplicity and rapid development.

## Core Architecture

-   **Single Process, Multi-threaded Daemon (`daemon.py`):** A single Python script orchestrates all backend tasks using threads for concurrency (watching files, analyzing screen). This avoids complex inter-process communication.
-   **In-Memory State:** A global dictionary (`state`) protected by a `threading.Lock` will serve as the single source of truth ("Project Cortex").
-   **FastAPI Server:** The daemon exposes a simple REST API using FastAPI to communicate with the UI.
-   **Modular Logic:** Core functionalities are separated into dedicated modules: `watcher.py`, `screen.py`, and `analysis.py`.
-   **Streamlit UI (`ui.py`):** A simple, separate Python script for the user interface that polls the FastAPI backend.

## File Structure

```
/
├── daemon.py               # Main application, FastAPI server, thread orchestrator
├── watcher.py              # File and Git watcher logic
├── screen.py               # Screen capture and analysis logic
├── analysis.py             # All AI (Gemini) interactions
├── ui.py                   # Streamlit user interface
├── requirements.txt        # Python dependencies
└── implementation_plan.md  # This file
```

## Dependencies (`requirements.txt`)

```
fastapi
uvicorn[standard]
python-multipart
GitPython
mss
google-genai
streamlit
requests
pillow
```

## Module Implementation Details

### 1. `daemon.py` - The Orchestrator

This script is the entry point. It initializes the state, starts background threads, and runs the FastAPI server.

```python
# daemon.py

import threading
import time
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import io
from PIL import Image

# 1. State Management
state = {"security_score": 100, "active_issues": [], "project_charter": {}}
state_lock = threading.Lock()

# 2. Core Logic Modules
import analysis
import watcher
import screen

# 3. FastAPI App
app = FastAPI()

class AppState(BaseModel):
    security_score: int
    active_issues: list
    project_charter: dict

@app.get("/state", response_model=AppState)
async def get_state():
    """Endpoint to get the current application state."""
    with state_lock:
        return state

@app.post("/oracle/generate_prompt")
async def generate_prompt(goal: str = Form(...), screenshot: UploadFile = File(...)):
    """Endpoint for the 'Oracle' feature to generate a prompt."""
    image_bytes = await screenshot.read()
    image = Image.open(io.BytesIO(image_bytes))
    # The analysis function will handle the Gemini call
    generated_prompt = analysis.generate_oracle_prompt(goal, image, state)
    return {"prompt": generated_prompt}

# 4. Background Threads
def run_watcher_thread(project_path: str):
    """Thread for watching git diff and file changes."""
    watcher.start(project_path, state, state_lock)

def run_screen_thread():
    """Thread for periodic screen analysis."""
    screen.start(state, state_lock)

# 5. Main Execution Block
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python daemon.py /path/to/your/project")
        sys.exit(1)
    
    project_path = sys.argv[1]

    # Start the background threads
    watcher_thread = threading.Thread(target=run_watcher_thread, args=(project_path,), daemon=True)
    screen_thread = threading.Thread(target=run_screen_thread, daemon=True)
    
    watcher_thread.start()
    screen_thread.start()

    # Start the FastAPI server
    print("Starting Vibe Assist daemon...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. `analysis.py` - The AI Brain

This is the most critical module, handling all communication with the Gemini API. It will use the `google-genai` library.

**Gemini API Usage Pattern:**

The user provided a streaming example. We will adapt it for our request-response needs. For multimodal inputs (image + text), we will construct the `contents` list accordingly.

```python
# analysis.py

import os
import google.genai as genai
from google.genai.types import Content, Part
from PIL import Image

# Configure the Gemini client
# IMPORTANT: Set the GEMINI_API_KEY environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision') # For multimodal tasks
text_model = genai.GenerativeModel('gemini-pro') # For text-only tasks

def analyze_fast_path(diff: str, state: dict, lock):
    """Analyzes uncommitted changes for immediate threats (Fast Path)."""
    # For the demo, we can have a hardcoded check.
    if "sql injection" in diff.lower(): # Simplified for demo
        with lock:
            state["security_score"] -= 20
            state["active_issues"].append({
                "type": "Security Vulnerability",
                "description": "Potential SQL Injection detected in uncommitted changes.",
                "severity": "Critical"
            })
    # A more advanced implementation would use Gemini here.
    pass

def analyze_deep_path(commit_diff: str, charter: dict, state: dict, lock):
    """Analyzes a new commit against the project charter (Deep Path)."""
    prompt = f"""
    Project Charter:
    {charter}

    Commit Diff:
    {commit_diff}

    Analyze the commit diff. Does it align with the project charter? 
    Identify which charter items are addressed or progressed by this commit.
    Respond in a structured format, e.g., JSON.
    """
    response = text_model.generate_content(prompt)
    # Process response and update state
    with lock:
        # ... logic to parse response and update state["project_charter"] ...
        pass

def analyze_screen_proactively(image: Image.Image, state: dict, lock):
    """Periodically analyzes the screen to offer proactive help."""
    prompt = "You are a proactive AI assistant. This is the user's screen. This is the project context: {state}. Is there anything on screen you can help with, like a potential bug or a chance to refactor? Be very brief. If not, respond with 'None'."
    
    response = model.generate_content([prompt, image])
    
    if response.text.strip().lower() != 'none':
        with lock:
            state["active_issues"].append({
                "type": "Proactive Suggestion",
                "description": response.text,
                "severity": "Low"
            })

def generate_oracle_prompt(goal: str, image: Image.Image, context: dict) -> str:
    """Generates a high-quality prompt for the user based on a goal and screenshot."""
    prompt = f"""
    User Goal: "{goal}"
    Project Context: {context}

    Based on the user's goal, the project context, and the provided screenshot, engineer a detailed, effective prompt to be sent to an advanced AI model to achieve the user's goal.
    """
    
    response = model.generate_content([prompt, image])
    return response.text
```

### 3. `watcher.py` - The Observer

Uses `GitPython` to monitor the project directory for changes.

```python
# watcher.py

import time
from git import Repo, exc
import analysis

def start(project_path: str, state: dict, lock):
    """Starts the file and git watcher loop."""
    print(f"Starting watcher for project: {project_path}")
    try:
        repo = Repo(project_path)
    except exc.InvalidGitRepositoryError:
        print(f"Error: {project_path} is not a valid Git repository.")
        return

    last_commit_hash = repo.head.commit.hexsha
    
    while True:
        # 1. Check for new commits
        current_commit_hash = repo.head.commit.hexsha
        if current_commit_hash != last_commit_hash:
            print(f"New commit detected: {current_commit_hash}")
            commit_diff = repo.git.diff(f'{last_commit_hash}..{current_commit_hash}')
            analysis.analyze_deep_path(commit_diff, state.get("project_charter", {}), state, lock)
            last_commit_hash = current_commit_hash

        # 2. Check for uncommitted changes
        diff_output = repo.index.diff(None)
        if diff_output:
            diff_str = "\n".join([d.diff.decode('utf-8', 'ignore') for d in diff_output if d.diff])
            if diff_str:
                # This could be noisy, so maybe trigger only if diff changes
                analysis.analyze_fast_path(diff_str, state, lock)

        time.sleep(5) # Check every 5 seconds
```

### 4. `screen.py` - The Proactive Assistant

Uses `mss` to take screenshots and sends them for analysis.

```python
# screen.py

import time
import mss
from PIL import Image
import analysis

def start(state: dict, lock):
    """Starts the screen analysis loop."""
    print("Starting screen analyzer...")
    sct = mss.mss()
    
    while True:
        # Take screenshot
        sct_img = sct.grab(sct.monitors[1]) # Grab the primary monitor
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Analyze screenshot
        analysis.analyze_screen_proactively(img, state, lock)
        
        time.sleep(10) # Analyze screen every 10 seconds
```

### 5. `ui.py` - The User Interface

A simple Streamlit app to visualize the state from the daemon.

```python
# ui.py

import streamlit as st
import requests
import time

st.set_page_config(layout="wide")

st.title("Vibe Assist Dashboard")

# Placeholder for the main content
main_container = st.empty()

def fetch_state():
    """Fetches the latest state from the daemon."""
    try:
        response = requests.get("http://localhost:8000/state")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

while True:
    state = fetch_state()
    
    with main_container.container():
        if "error" in state:
            st.error(f"Could not connect to the Vibe Assist daemon: {state['error']}")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Security Score", state.get("security_score", "N/A"))
                
                st.subheader("Project Charter Alignment")
                charter = state.get("project_charter", {})
                if charter:
                    for item, status in charter.items():
                        st.checkbox(item, value=status)
                else:
                    st.write("No charter defined.")

            with col2:
                st.subheader("Active Issues")
                issues = state.get("active_issues", [])
                if issues:
                    for issue in issues:
                        st.warning(f"**{issue.get('type', 'Issue')} ({issue.get('severity', 'Unknown')})**")
                        st.write(issue.get('description'))
                else:
                    st.success("No active issues.")

    time.sleep(2) # Refresh every 2 seconds
```

## Development and Execution Plan

1.  **Setup (`15 mins`):**
    *   Create the file structure.
    *   Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`.
    *   Install dependencies: `pip install -r requirements.txt`.
    *   Set the `GEMINI_API_KEY` environment variable.

2.  **Module Implementation (`2.5 hours`):**
    *   Implement `daemon.py` with the FastAPI structure.
    *   Implement `analysis.py`, focusing on `generate_oracle_prompt` and `analyze_screen_proactively` first. Use placeholder logic for `analyze_deep_path` and `analyze_fast_path` if time is short.
    *   Implement `watcher.py`. Test it by making commits and changes in a sample git repository.
    *   Implement `screen.py`. Test that it correctly captures the screen.

3.  **UI Implementation (`1 hour`):**
    *   Implement `ui.py` using Streamlit.
    *   Run the daemon (`python daemon.py /path/to/project`).
    *   Run the UI (`streamlit run ui.py`) and verify it displays data correctly.

4.  **Integration & Polish (`30 mins`):**
    *   Test the end-to-end flow.
    *   Use the "Oracle" feature from the UI (this part is not in the `ui.py` yet, can be added).
    *   Refine prompts in `analysis.py` for better results.
    *   Ensure threads close gracefully.

This detailed plan provides a clear roadmap for building the prototype within a tight timeframe, prioritizing a functional end-to-end loop.
