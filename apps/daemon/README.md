# Vibe Assist Daemon

Python backend service that provides AI-powered code analysis, security monitoring, and proactive development assistance.

## Quick Start

```bash
# From the daemon directory
cd apps/daemon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY='your-api-key-here'

# Run the daemon
python -m src.daemon /path/to/your/project
```

## Features

- **🔍 Fast Path Analysis** - Real-time security vulnerability detection
- **🧠 Deep Path Analysis** - AI-powered commit review against project charter
- **👁️ Screen Analysis** - Proactive coding suggestions from screen capture
- **🔮 Oracle** - AI prompt engineering for optimal developer assistance

## API Endpoints

The daemon runs a FastAPI server on port 8000:

- `GET /health` - Health check and status
- `GET /state` - Current security score and active issues
- `POST /oracle/generate_prompt` - Generate optimized AI prompts

## Configuration

Environment variables (optional, see `.env.example`):

```bash
GEMINI_API_KEY=your-key-here  # Required
HOST=0.0.0.0                   # Default: 0.0.0.0
PORT=8000                      # Default: 8000
GIT_WATCH_INTERVAL=2           # Default: 2 seconds
SCREEN_WATCH_INTERVAL=10       # Default: 10 seconds
STATE_SUMMARY_INTERVAL=60      # Default: 60 seconds
```

## Development

### Project Structure

```
apps/daemon/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── daemon.py         # Main FastAPI server & orchestrator
│   ├── analysis.py       # Gemini AI integration
│   ├── watcher.py        # Git file monitoring
│   └── screen.py         # Screen capture & analysis
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup
├── .env.example         # Environment variable template
└── README.md            # This file
```

### Install in Development Mode

```bash
pip install -e .
```

This allows you to run:

```bash
vibe-assist /path/to/your/project
```

## Documentation

Full documentation is available in the `/docs` directory:

- [Setup Guide](../../docs/SETUP.md)
- [Gemini API Documentation](../../docs/genai_api.md)
- [Implementation Plan](../../docs/implementation_plan.md)

## Requirements

- Python 3.8+
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Git repository to monitor

## License

MIT
