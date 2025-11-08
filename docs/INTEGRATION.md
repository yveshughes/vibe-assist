# Vibe Assist - Component Integration Guide

This document explains how all the components of Vibe Assist work together.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Vibe Assist System                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  macOS Widget    │      │   Next.js Web    │      │  Python Daemon   │
│   (Swift)        │◄────►│  (apps/web)      │◄────►│  (apps/daemon)   │
│                  │      │                  │      │                  │
│  Displays        │      │  Dashboard UI    │      │  AI Analysis     │
│  Checklist       │      │  /api/checklist  │      │  FastAPI Server  │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         │                         │                         │
         │                         │                         │
         └─────────────────────────┴─────────────────────────┘
                    Fetch /api/checklist every 15min
                    (gets security score & issues)
```

## Component Details

### 1. Python Daemon (Port 8000)

**Location:** `apps/daemon/`

**Purpose:** AI-powered backend that monitors code and provides analysis.

**Configuration:** `apps/daemon/.env`
```bash
GEMINI_API_KEY=your-key-here
HOST=0.0.0.0
PORT=8000
GIT_WATCH_INTERVAL=2
SCREEN_WATCH_INTERVAL=10
STATE_SUMMARY_INTERVAL=60
```

**Endpoints:**
- `GET /health` - Health check
- `GET /state` - Current security score and issues
- `POST /oracle/generate_prompt` - AI prompt generation
- `GET /docs` - Interactive API documentation

**Start:**
```bash
cd apps/daemon
source venv/bin/activate
python -m src.daemon /path/to/monitored/project
```

### 2. Next.js Web App (Port 3000)

**Location:** `apps/web/`

**Purpose:** Web dashboard and API bridge for the widget.

**Configuration:** `apps/web/.env.local`
```bash
DAEMON_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:3000
```

**Key Route:** `/api/checklist`
- Fetches data from daemon's `/state` endpoint
- Transforms it into widget-friendly format
- Provides fallback data if daemon is offline

**Start:**
```bash
cd apps/web
pnpm dev
```

### 3. macOS Widget

**Location:** `apps/widget/ChecklistWidget.swift`

**Purpose:** Native macOS widget displaying security status.

**Configuration:** Line 48 in `ChecklistWidget.swift`
```swift
guard let url = URL(string: "http://localhost:3000/api/checklist") else {
```

**Refresh Interval:** 15 minutes (line 39)

**Setup:**
1. Open Xcode
2. Create new Widget Extension
3. Copy `ChecklistWidget.swift` code
4. Build and run
5. Add widget to Notification Center

## Data Flow

### Normal Operation

1. **Python Daemon** monitors your project:
   - Watches git changes (every 2s)
   - Analyzes screen (every 10s)
   - Updates internal state with findings

2. **Next.js API** (`/api/checklist`):
   - Fetches daemon state every request
   - Converts to checklist format:
     ```json
     {
       "items": [
         {"id": "security", "title": "Security Score: 90/100", "completed": false},
         {"id": "issue-0", "title": "[Critical] SQL Injection detected", "completed": false}
       ],
       "lastUpdated": "2025-01-08T12:00:00Z"
     }
     ```

3. **macOS Widget**:
   - Fetches from Next.js API every 15 minutes
   - Displays checklist items
   - Shows completed items in green with checkmark
   - Shows incomplete items in gray with circle

### When Daemon is Offline

1. Next.js API catches fetch error
2. Returns fallback checklist:
   ```json
   {
     "items": [
       {"id": "1", "title": "⚠️ Daemon not running", "completed": false},
       {"id": "2", "title": "Start daemon: cd apps/daemon...", "completed": false}
     ]
   }
   ```
3. Widget displays these fallback items

## Environment Variables Summary

### Python Daemon (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Google Gemini API key |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `GIT_WATCH_INTERVAL` | `2` | Git check frequency (seconds) |
| `SCREEN_WATCH_INTERVAL` | `10` | Screen capture frequency (seconds) |
| `STATE_SUMMARY_INTERVAL` | `60` | Console summary frequency (seconds) |

### Next.js Web (`.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DAEMON_URL` | `http://localhost:8000` | Python daemon API URL |
| `NEXT_PUBLIC_API_URL` | `http://localhost:3000` | Next.js public URL |

## Testing the Integration

### 1. Start All Services

**Terminal 1 - Python Daemon:**
```bash
cd apps/daemon
source venv/bin/activate
python -m src.daemon ~/your-project
```

Expected output:
```
============================================================
Vibe Assist - Starting Daemon
============================================================
...
Starting API server on http://0.0.0.0:8000
```

**Terminal 2 - Next.js:**
```bash
cd apps/web
pnpm dev
```

Expected output:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### 2. Test Daemon API

```bash
# Health check
curl http://localhost:8000/health

# Get state
curl http://localhost:8000/state
```

Expected response:
```json
{
  "security_score": 100,
  "active_issues": [],
  "project_charter": {}
}
```

### 3. Test Next.js API

```bash
curl http://localhost:3000/api/checklist
```

Expected response:
```json
{
  "items": [
    {
      "id": "security",
      "title": "Security Score: 100/100",
      "completed": true
    },
    {
      "id": "all-clear",
      "title": "✅ No security issues detected",
      "completed": true
    }
  ],
  "lastUpdated": "2025-01-08T12:00:00.000Z"
}
```

### 4. Test Widget

1. Open **System Settings** → **Desktop & Dock** → **Widgets**
2. Add **ChecklistWidget** to your desktop or Notification Center
3. Widget should display security score and issues
4. Widget updates every 15 minutes

### 5. Trigger a Security Issue

In your monitored project, create a file with SQL injection:

```python
# test_bad.py
query = f"SELECT * FROM users WHERE id = {user_input}"
```

Save the file (don't commit). Within 2 seconds, you should see:

**Daemon Console:**
```
============================================================
🔍 FAST PATH ANALYSIS - Security Check
============================================================
⚠️  SECURITY ISSUE DETECTED!
```

**Next.js API** (after refresh):
```json
{
  "items": [
    {
      "id": "security",
      "title": "Security Score: 90/100",
      "completed": false
    },
    {
      "id": "issue-0",
      "title": "[Critical] Security: Potential SQL injection...",
      "completed": false
    }
  ]
}
```

**Widget** (after 15 minutes or manual refresh):
- Shows "Security Score: 90/100" with gray circle
- Shows security issue with gray circle

## CORS Configuration

The daemon allows requests from Next.js:

```python
# apps/daemon/src/daemon.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
)
```

## Troubleshooting

### Widget shows "Daemon not running"

1. Check daemon is running: `curl http://localhost:8000/health`
2. Check Next.js is running: `curl http://localhost:3000/api/checklist`
3. Check widget URL is correct in `ChecklistWidget.swift`

### Next.js API returns fallback data

1. Verify daemon is running on port 8000
2. Check `DAEMON_URL` in `apps/web/.env.local`
3. Check CORS is configured correctly

### Widget doesn't update

1. Widget refresh interval is 15 minutes
2. Force refresh: Remove and re-add widget
3. Check Next.js dev server logs for API requests

### CORS errors in browser

1. Verify daemon CORS middleware includes your Next.js URL
2. Restart daemon after CORS changes
3. Clear browser cache

## Production Deployment

### Python Daemon

Deploy with:
- Gunicorn + Uvicorn workers
- Systemd service for auto-restart
- Nginx reverse proxy
- HTTPS/TLS certificates

### Next.js

Deploy to:
- Vercel (recommended)
- Netlify
- Self-hosted with PM2

Update environment variables:
```bash
DAEMON_URL=https://your-daemon-domain.com
```

### macOS Widget

Update API URL in Swift code:
```swift
guard let url = URL(string: "https://your-nextjs-domain.com/api/checklist") else {
```

Rebuild and distribute via:
- Mac App Store
- Direct download (.app bundle)
- TestFlight (during development)

## Summary

✅ **Daemon** runs on port 8000, monitors code, provides AI analysis
✅ **Next.js** runs on port 3000, bridges daemon data to widget
✅ **Widget** fetches from Next.js every 15 minutes, displays status
✅ All components communicate via REST APIs
✅ Graceful fallbacks when components are offline

For more details, see:
- [Setup Guide](./SETUP.md)
- [Daemon README](../apps/daemon/README.md)
- [Widget README](../apps/widget/README.md)
