# Vibe Assist - Quick Start Guide

Get all components running in 5 minutes!

## Prerequisites

- ✅ Python 3.8+
- ✅ Node.js 18+ and pnpm
- ✅ Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- ✅ Git repository to monitor
- ✅ Xcode (for macOS widget)

## Step 1: Install Dependencies

```bash
# Clone and navigate
cd vibe-assist

# Install JavaScript/TypeScript dependencies
pnpm install

# Install Python dependencies
cd apps/daemon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../..
```

## Step 2: Configure Environment Variables

### Python Daemon

The `.env` file already exists in `apps/daemon/.env`:

```bash
# apps/daemon/.env (already configured!)
GEMINI_API_KEY=AIzaSyALYH8vW1DVK-jfQ_HZFSBNYVzQiTM4Feo
HOST=0.0.0.0
PORT=8000
GIT_WATCH_INTERVAL=2
SCREEN_WATCH_INTERVAL=10
STATE_SUMMARY_INTERVAL=60
```

> ⚠️ **Note:** The API key is already set in your .env file!

### Next.js Web App (Optional)

Create `apps/web/.env.local` (if needed):

```bash
# apps/web/.env.local
DAEMON_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Step 3: Start the Services

### Terminal 1 - Python Daemon (Required)

```bash
cd apps/daemon
source venv/bin/activate
python -m src.daemon /path/to/your/project

# Example:
python -m src.daemon ~/my-coding-project
```

**Expected Output:**
```
============================================================
Vibe Assist - Starting Daemon
============================================================

Initializing Gemini API client...
Gemini client initialized successfully

Monitoring project: /Users/you/my-coding-project

Starting background threads...
  ✓ Git watcher started
  ✓ Screen analyzer started
  ✓ State summary reporter started (60s interval)

Starting API server on http://0.0.0.0:8000
  - State endpoint: http://localhost:8000/state
  - Oracle endpoint: http://localhost:8000/oracle/generate_prompt
  - Health check: http://localhost:8000/health
  - Docs: http://localhost:8000/docs

Press Ctrl+C to stop
============================================================
```

### Terminal 2 - Next.js Web (Optional, for widget)

```bash
cd apps/web
pnpm dev
```

**Expected Output:**
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000

 ✓ Ready in 2.3s
```

## Step 4: Verify Everything Works

### Test Python Daemon

```bash
# Health check
curl http://localhost:8000/health

# Expected: {"status":"healthy","gemini_initialized":true}

# Get current state
curl http://localhost:8000/state

# Expected: {"security_score":100,"active_issues":[],"project_charter":{}}
```

### Test Next.js API (if running)

```bash
curl http://localhost:3000/api/checklist
```

Expected response:
```json
{
  "items": [
    {"id":"security","title":"Security Score: 100/100","completed":true},
    {"id":"all-clear","title":"✅ No security issues detected","completed":true}
  ],
  "lastUpdated":"2025-01-08T12:00:00.000Z"
}
```

### Test the System

1. In your monitored project, create a file with a security issue:

```python
# test_bad.py
query = f"SELECT * FROM users WHERE id = {user_input}"
```

2. Save the file (don't commit)

3. Within 2 seconds, check the daemon console:

```
============================================================
🔍 FAST PATH ANALYSIS - Security Check
============================================================
📝 Analyzing 78 characters of code changes...
⚠️  SECURITY ISSUE DETECTED!
------------------------------------------------------------
Potential SQL injection vulnerability detected...
------------------------------------------------------------
📊 Security Score: 90/100
🚨 Total Active Issues: 1
============================================================
```

4. Check the API again:

```bash
curl http://localhost:8000/state
```

You should see `"security_score": 90` and active issues!

## Step 5: Setup macOS Widget (Optional)

1. Open Xcode
2. Create new project: **Widget Extension** under macOS
3. Name it "ChecklistWidget"
4. Replace code with `apps/widget/ChecklistWidget.swift`
5. Build and run (⌘R)
6. Add widget to Notification Center

The widget will automatically fetch from Next.js and display your security status!

## What Each Component Does

| Component | Port | Purpose |
|-----------|------|---------|
| **Python Daemon** | 8000 | AI analysis, monitors git & screen |
| **Next.js Web** | 3000 | Dashboard UI + API bridge |
| **macOS Widget** | - | Native widget display |

## Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  macOS       │      │  Next.js     │      │  Python      │
│  Widget      │─────▶│  /api/       │─────▶│  Daemon      │
│  (Swift)     │      │  checklist   │      │  :8000       │
└──────────────┘      └──────────────┘      └──────────────┘
                           :3000                  │
                                                  │
                                            ┌─────▼──────┐
                                            │  Gemini    │
                                            │  AI API    │
                                            └────────────┘
```

## Configuration Summary

### Python Daemon (apps/daemon/.env)

```bash
GEMINI_API_KEY=your-key-here          # ✅ Already set!
HOST=0.0.0.0                          # Server host
PORT=8000                             # Server port
GIT_WATCH_INTERVAL=2                  # Git check frequency
SCREEN_WATCH_INTERVAL=10              # Screen check frequency
STATE_SUMMARY_INTERVAL=60             # Console summary frequency
```

### Next.js (apps/web/.env.local)

```bash
DAEMON_URL=http://localhost:8000      # Python daemon URL
NEXT_PUBLIC_API_URL=http://localhost:3000  # Next.js public URL
```

### Widget (ChecklistWidget.swift line 48)

```swift
guard let url = URL(string: "http://localhost:3000/api/checklist") else {
```

## Common Issues

### "GEMINI_API_KEY not set"
Your key is already in `apps/daemon/.env`! Just make sure you activated the venv:
```bash
cd apps/daemon
source venv/bin/activate
```

### "Module not found"
Install dependencies:
```bash
pip install -r requirements.txt
```

### Widget shows "Daemon not running"
1. Start daemon first
2. Then start Next.js
3. Check both are running with curl commands above

## Next Steps

- 📖 Read [Integration Guide](docs/INTEGRATION.md) for detailed architecture
- 📖 Read [Setup Guide](docs/SETUP.md) for advanced configuration
- 🔧 Customize analysis intervals in `.env`
- 🎨 Build your own dashboard in `apps/web`

## Support

- **Documentation:** See `/docs` directory
- **Daemon README:** `apps/daemon/README.md`
- **Widget README:** `apps/widget/README.md`

---

🎉 **You're all set!** The daemon will now monitor your code and provide AI-powered suggestions in real-time!
