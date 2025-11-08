#!/usr/bin/env python3
"""
View Gemini API logs to demonstrate SGR (Structured Generation Reasoning) in action.

Usage:
    python view_gemini_logs.py [path/to/project]
    python view_gemini_logs.py --latest [path/to/project]  # Show only the latest call
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def view_logs(log_file_path: Path, latest_only: bool = False):
    """Display Gemini API logs in a readable format."""

    if not log_file_path.exists():
        print(f"❌ No log file found at: {log_file_path}")
        print("Make sure the daemon has been run at least once.")
        return

    logs = []
    with open(log_file_path, 'r') as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line))

    if not logs:
        print("📝 No Gemini API calls logged yet.")
        return

    if latest_only:
        logs = [logs[-1]]

    print("="*80)
    print("🧠 GEMINI API CALL LOGS - Structured Generation Reasoning (SGR)")
    print("="*80)
    print(f"\nTotal API calls: {len(logs)}")
    print()

    for i, log in enumerate(logs, 1):
        timestamp = datetime.fromisoformat(log['timestamp']).strftime("%Y-%m-%d %H:%M:%S")

        print(f"{'='*80}")
        print(f"📞 Call #{i}: {log['function']}")
        print(f"{'='*80}")
        print(f"🕒 Timestamp: {timestamp}")
        print(f"🤖 Model: {log['model']}")
        print(f"📋 Schema: {log.get('schema', 'None')}")
        print(f"📏 Prompt length: {log['prompt_length']} chars")
        print(f"📏 Response length: {log['response_length']} chars")
        print()
        print(f"📝 PROMPT (truncated):")
        print("-"*80)
        print(log['prompt'])
        print()
        print(f"💬 RESPONSE (truncated):")
        print("-"*80)
        print(log['response'])
        print()

if __name__ == "__main__":
    latest_only = "--latest" in sys.args

    if len(sys.argv) > 1:
        project_path = sys.argv[-1]  # Last argument is always the path
    else:
        # Try to find .vibe-assist in current directory
        project_path = "."

    log_file = Path(project_path) / ".vibe-assist" / "gemini-logs.jsonl"
    view_logs(log_file, latest_only)
