# Vibe Assist - Backend Setup Guide

Complete setup instructions for getting the Vibe Assist backend running.

## What is Vibe Assist?

Vibe Assist is a proactive AI assistant that monitors your codebase and provides real-time security analysis, commit reviews, and proactive coding suggestions. All output is displayed in the console for easy monitoring.

## Prerequisites

- Python 3.8+
- Git repository (for the project you want to monitor)
- Gemini API key from Google AI Studio

## Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 2: Set Up Environment

### Navigate to Daemon Directory

```bash
cd /Users/andriikonovalenko/vibe-assist/apps/daemon
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set API Key

```bash
# On macOS/Linux
export GEMINI_API_KEY='your-api-key-here'

# On Windows
set GEMINI_API_KEY=your-api-key-here

# To make it permanent, add to your ~/.bashrc or ~/.zshrc:
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Step 3: Run Vibe Assist

### Start the Daemon

The daemon monitors your project and outputs all analysis to the console.

```bash
# Make sure you're in the apps/daemon directory with venv activated
cd /Users/andriikonovalenko/vibe-assist/apps/daemon
source venv/bin/activate
python -m src.daemon /path/to/your/project

# Example:
python -m src.daemon /Users/andriikonovalenko/my-project
```

### Expected Console Output

You should see something like:

```
============================================================
Vibe Assist - Starting Daemon
============================================================

Initializing Gemini API client...
Gemini client initialized successfully

Monitoring project: /Users/andriikonovalenko/my-project

Starting background threads...
  ✓ Git watcher started
  ✓ Screen analyzer started
  ✓ State summary reporter started (60s interval)

Starting API server on http://0.0.0.0:8000
  - State endpoint: http://localhost:8000/state
  - Oracle endpoint: http://localhost:8000/oracle/generate_prompt
  - Health check: http://localhost:8000/health

Press Ctrl+C to stop
============================================================
```

## How It Works

### 1. Git Watcher (Fast Path)
Monitors uncommitted file changes every 2 seconds and performs security analysis.

**Console Output Example:**
```
============================================================
🔍 FAST PATH ANALYSIS - Security Check
============================================================
📝 Analyzing 523 characters of code changes...
⚠️  SECURITY ISSUE DETECTED!
------------------------------------------------------------
Potential SQL injection vulnerability detected:
  query = f"SELECT * FROM users WHERE id = {user_input}"
------------------------------------------------------------
📊 Security Score: 90/100
🚨 Total Active Issues: 1
============================================================
```

### 2. Git Watcher (Deep Path)
Monitors new commits and analyzes them against your project charter.

**Console Output Example:**
```
============================================================
🧠 DEEP PATH ANALYSIS - Commit Review
============================================================
📦 Commit: abc12345
👤 Author: John Doe
📅 Date: 2025-01-08 14:23:45
💬 Message: Add user authentication
------------------------------------------------------------
📝 Analyzing 1234 characters of commit changes...
✅ Commit analysis complete
📋 Charter Update:
{"authentication": "completed", "security": "in-progress"}
============================================================
```

### 3. Screen Analyzer
Captures your screen every 10 seconds and provides proactive suggestions.

**Console Output Example:**
```
============================================================
👁️  SCREEN ANALYSIS - Proactive Assistance
============================================================
🖼️  Analyzing screenshot (142352 bytes)...
💡 SUGGESTION FOUND!
------------------------------------------------------------
I notice you have an unclosed <div> tag on line 45.
This could cause layout issues.
------------------------------------------------------------
🚨 Total Active Issues: 2
============================================================
```

### 4. State Summary
Prints a summary of the current state every 60 seconds.

**Console Output Example:**
```
============================================================
📊 CURRENT STATE SUMMARY
============================================================
🔐 Security Score: 90/100
🚨 Active Issues: 2

Issues:
  1. [Critical] Security: Potential SQL injection vulnerability...
  2. [Medium] Proactive Suggestion: Unclosed <div> tag on line 45...

📋 Last Analyzed Commit: abc12345
============================================================
```

## API Endpoints

The daemon runs a FastAPI server that your frontend can connect to.

### Check Health
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "gemini_initialized": true
}
```

### Get Current State
```bash
curl http://localhost:8000/state
```

Response:
```json
{
  "security_score": 90,
  "active_issues": [
    {
      "type": "Security",
      "description": "Potential SQL injection...",
      "severity": "Critical"
    }
  ],
  "project_charter": {
    "last_analyzed_commit": "abc12345"
  }
}
```

### Generate Oracle Prompt
```bash
curl -X POST http://localhost:8000/oracle/generate_prompt \
  -F "goal=Fix authentication bug" \
  -F "screenshot=@/path/to/screenshot.png"
```

**Console Output:**
```
============================================================
🔮 ORACLE - Prompt Engineering
============================================================
🎯 Goal: Fix authentication bug
🖼️  Screenshot: 142352 bytes
------------------------------------------------------------
🤖 Generating optimized prompt...
✅ Oracle prompt generated!
------------------------------------------------------------
Based on the screenshot showing your login component...
[Generated prompt here]
============================================================
```

## Configuration

### Adjust Analysis Frequency

**Fast Path (Git Watcher)** - Edit `watcher.py` line 64:
```python
time.sleep(2)  # Change to 5 or 10 seconds
```

**Screen Analysis** - Edit `screen.py` line 34:
```python
time.sleep(10)  # Change to 30 or 60 seconds
```

**State Summary** - Edit `daemon.py` line 83:
```python
time.sleep(60)  # Change to 120 or 300 seconds
```

### Disable Screen Analysis

Comment out in `daemon.py` lines 138-142:
```python
# screen_thread.start()
# print("  ✓ Screen analyzer started")
```

### Change AI Models

In `analysis.py`, you can switch models:
- `gemini-2.5-flash` - Fast, cheaper (default for security checks)
- `gemini-2.5-pro` - More powerful, accurate (default for deep analysis)

## Troubleshooting

### "GEMINI_API_KEY not set"

Verify the environment variable is set:
```bash
echo $GEMINI_API_KEY  # Should print your key
```

If empty, export it again:
```bash
export GEMINI_API_KEY='your-api-key'
```

### "Not a valid git repository"

The path must be a git repository:
```bash
cd /path/to/your/project
git status  # Should work without errors
```

### Screen capture permissions (macOS)

Grant screen recording permissions:
1. System Preferences → Security & Privacy → Screen Recording
2. Add Terminal to the allowed applications

### Rate Limiting

The free Gemini API has limits. If you hit them:
- Increase sleep intervals in `watcher.py` and `screen.py`
- Disable screen analysis (comment out `screen_thread.start()`)
- Upgrade to a paid Gemini API plan

### No Console Output

Make sure you're running with:
```bash
cd apps/daemon
python -m src.daemon /path/to/project
```

Not as a background service. The console output is the main UI for now.

## Testing the System

### Test 1: Security Detection

1. In your monitored project, create a file with SQL injection:
   ```python
   # bad_code.py
   query = f"SELECT * FROM users WHERE id = {user_input}"
   ```

2. Save the file (don't commit)

3. Watch the console - you should see:
   ```
   🔍 FAST PATH ANALYSIS - Security Check
   ⚠️  SECURITY ISSUE DETECTED!
   ```

### Test 2: Commit Analysis

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add user query"
   ```

2. Watch the console - you should see:
   ```
   🧠 DEEP PATH ANALYSIS - Commit Review
   ```

### Test 3: Oracle API

```bash
# Create a test screenshot
screencapture -x test.png

# Call the Oracle endpoint
curl -X POST http://localhost:8000/oracle/generate_prompt \
  -F "goal=Refactor my code" \
  -F "screenshot=@test.png"
```

Watch the console for the Oracle output.

## Frontend Development

The UI is being built separately in Next.js by your cofounder. The backend provides these endpoints:

- `GET /health` - Check if daemon is running
- `GET /state` - Get current security score and issues
- `POST /oracle/generate_prompt` - Generate AI prompts

Frontend code will be in `apps/web/`.

## File Structure

```
vibe-assist/
├── apps/
│   └── daemon/              # Python backend service
│       ├── src/
│       │   ├── daemon.py    # Main FastAPI server + orchestrator
│       │   ├── analysis.py  # All Gemini API calls
│       │   ├── watcher.py   # Git file monitoring
│       │   └── screen.py    # Screen capture + analysis
│       ├── requirements.txt # Python dependencies
│       ├── setup.py         # Package setup
│       └── README.md        # Daemon documentation
├── docs/                    # Project documentation
│   ├── SETUP.md            # This file
│   ├── genai_api.md        # Gemini API documentation
│   └── implementation_plan.md
└── README.md               # Project overview
```

## Next Steps

1. ✅ **Start the daemon** - `cd apps/daemon && python -m src.daemon /path/to/project`
2. ✅ **Make code changes** - Edit files in your project
3. ✅ **Watch the console** - See real-time AI analysis
4. ✅ **Test the API** - Use curl to test endpoints
5. 🚀 **Connect frontend** - Your cofounder can build the UI in `apps/web/`

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is set correctly
3. Ensure all dependencies are installed
4. Check the troubleshooting section above

## Documentation

- **Gemini API Guide**: See `genai_api.md` for detailed API documentation
- **Implementation Plan**: See `implementation_plan.md` for architecture details

Enjoy using Vibe Assist! 🤖✨
