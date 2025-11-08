# Vibe Assist

Vibe Assist is a powerful tool that combines a macOS widget with a monitoring core to help you keep track of your system's key metrics. This repository contains the source code for the macOS widget, the public-facing website, and the core monitoring engine.

## Components

This project is a monorepo that includes the following components:

### 1. macOS Widget

A native macOS widget that displays a checklist of tasks or system statuses, fetched from a Next.js API endpoint.

**Features:**

-   Displays a list of items with their completion status.
-   Fetches data from a live API endpoint.
-   Customizable refresh rate.
-   Supports small, medium, and large widget sizes.

**Location:** `apps/widget/`

### 2. Website

The public-facing website, built with Next.js, that explains what Vibe Assist does, how it works, and how to install it. The `apps/web` directory contains the source code for the website.

**Features:**

-   Dashboard for viewing security metrics
-   API endpoint (`/api/checklist`) that bridges the monitoring core to the widget
-   Responsive design

**Location:** `apps/web/`

### 3. Monitoring Core (Daemon)

The core of the application, responsible for monitoring your codebase and providing AI-powered security analysis and development assistance.

**Features:**

-   Real-time security vulnerability detection (SQL injection, XSS, exposed secrets)
-   AI-powered commit analysis using Google Gemini
-   Proactive screen analysis for bug detection and refactoring suggestions
-   REST API for dashboard and widget integration

**Location:** `apps/daemon/`

**Tech Stack:** Python, FastAPI, Google Gemini AI

## Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  macOS       │      │  Next.js     │      │  Python      │
│  Widget      │─────▶│  Website     │─────▶│  Daemon      │
│              │      │  /api/       │      │  (Core)      │
└──────────────┘      └──────────────┘      └──────────────┘
                                                   │
                                             ┌─────▼──────┐
                                             │  Gemini    │
                                             │  AI API    │
                                             └────────────┘
```

## Getting Started

To get started with development, you'll need to have [pnpm](https://pnpm.io/installation), [Node.js](https://nodejs.org/), and [Python 3.8+](https://www.python.org/) installed.

### 1. Clone the repository

```sh
git clone https://github.com/yveshughes/vibe-assist.git
cd vibe-assist
```

### 2. Install dependencies

**JavaScript/TypeScript dependencies:**
```sh
pnpm install
```

**Python dependencies (for monitoring core):**
```sh
cd apps/daemon
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../..
```

### 3. Configure environment

**Set up Gemini API key** (for monitoring core):
```sh
# Get your API key from https://aistudio.google.com/app/apikey
export GEMINI_API_KEY='your-api-key-here'
```

The daemon configuration is in `apps/daemon/.env`

### 4. Start the development servers

**Option A: Start Everything**

Terminal 1 - Monitoring Core (Python Daemon):
```sh
cd apps/daemon
source venv/bin/activate
python -m src.daemon /path/to/your/project
```

Terminal 2 - Website & API:
```sh
pnpm dev
```

**Option B: Start Individual Components**

```sh
# Website only
pnpm dev --filter=web

# Docs site
pnpm dev --filter=docs

# Python daemon
cd apps/daemon && python -m src.daemon /path/to/project
```

## Quick Links

- 🚀 **[Quick Start Guide](QUICK_START.md)** - Get running in 5 minutes
- 📖 **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- 🔗 **[Integration Guide](docs/INTEGRATION.md)** - How all components connect
- 🤖 **[Gemini API Docs](docs/genai_api.md)** - AI integration reference

## Project Structure

```
vibe-assist/
├── apps/
│   ├── daemon/           # Python monitoring core (FastAPI + Gemini AI)
│   ├── web/              # Next.js website & API
│   ├── docs/             # Documentation site
│   └── widget/           # macOS Swift widget
├── packages/
│   ├── ui/               # Shared React components
│   ├── eslint-config/    # Shared ESLint config
│   └── typescript-config/# Shared TypeScript config
├── docs/                 # Project documentation
└── README.md             # This file
```

## Development Workflow

### For Widget Development

The widget fetches data from the Next.js API endpoint at `/api/checklist`. This endpoint automatically pulls data from the monitoring core (daemon).

See `apps/widget/README.md` for widget-specific setup.

### For Monitoring Core Development

The daemon provides a REST API on port 8000 that the website consumes. All AI analysis happens here.

See `apps/daemon/README.md` for daemon-specific development.

### For Website Development

The website serves as both the public-facing site and the API bridge between the widget and the monitoring core.

Standard Next.js development workflow applies.

## API Endpoints

The monitoring core exposes these endpoints:

- `GET /health` - Health check and status
- `GET /state` - Current security score and active issues
- `POST /oracle/generate_prompt` - AI prompt engineering
- `GET /docs` - Interactive API documentation

The Next.js website exposes:

- `GET /api/checklist` - Widget-friendly data format

## Tech Stack

- **Frontend:** Next.js 16, React 19, TypeScript
- **Backend:** Python 3.8+, FastAPI, Uvicorn
- **AI:** Google Gemini 2.5 Flash & Pro
- **Widget:** Swift, WidgetKit
- **Monorepo:** Turborepo, pnpm

## Contributing

This is a monorepo managed by Turborepo. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes in the appropriate app or package
4. Test thoroughly
5. Submit a pull request

## Useful Links

-   [Turborepo Documentation](https://turborepo.org/docs)
-   [Next.js Documentation](https://nextjs.org/docs)
-   [SwiftUI Documentation](https://developer.apple.com/xcode/swiftui/)
-   [FastAPI Documentation](https://fastapi.tiangolo.com/)
-   [Gemini API Documentation](https://ai.google.dev/docs)

## License

MIT

---

Built with ❤️ by the Vibe Assist team
