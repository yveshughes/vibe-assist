# analysis.py

import os
import io
import PIL.Image
from google import genai
from google.genai import types

# Initialize Gemini client
# Make sure to set your GEMINI_API_KEY environment variable
client = None

def initialize_client():
    """Initialize the Gemini client with API key from environment."""
    global client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not set. AI features will be disabled.")
        return False
    try:
        client = genai.Client(api_key=api_key)
        print("Gemini client initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return False

def analyze_fast_path(diff, state, lock):
    """
    Analyzes the git diff for immediate, high-priority issues.
    Uses gemini-2.5-flash for speed.
    """
    print("\n" + "="*60)
    print("🔍 FAST PATH ANALYSIS - Security Check")
    print("="*60)

    if not client:
        print("⚠️  Gemini client not initialized, skipping analysis")
        return

    print(f"📝 Analyzing {len(diff)} characters of code changes...")

    prompt = f"""
    Analyze the following code diff for critical security vulnerabilities like SQL injection, XSS, or exposed secrets.
    If a critical vulnerability is found, respond with a JSON object describing the issue with fields: type, description, severity.
    If not, respond with "None".

    Diff:
    {diff}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,  # Deterministic for security checks
                max_output_tokens=500,
            ),
        )

        result = response.text.strip() if response.text else None

        if result and result.lower() != "none":
            print("⚠️  SECURITY ISSUE DETECTED!")
            print("-" * 60)
            print(result)
            print("-" * 60)

            with lock:
                state["security_score"] -= 10
                state["active_issues"].append({
                    "type": "Security",
                    "description": result,
                    "severity": "Critical"
                })
                print(f"📊 Security Score: {state['security_score']}/100")
                print(f"🚨 Total Active Issues: {len(state['active_issues'])}")
        else:
            print("✅ No security issues detected")

        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error in fast path analysis: {e}")
        print("="*60 + "\n")

def analyze_deep_path(commit, state, lock):
    """
    Performs a deep analysis of a commit to update project context.
    Uses gemini-2.5-pro for deeper reasoning.
    """
    print("\n" + "="*60)
    print("🧠 DEEP PATH ANALYSIS - Commit Review")
    print("="*60)

    if not client:
        print("⚠️  Gemini client not initialized, skipping analysis")
        return

    print(f"📦 Commit: {commit.hexsha[:8]}")
    print(f"👤 Author: {commit.author.name}")
    print(f"📅 Date: {commit.authored_datetime}")
    print(f"💬 Message: {commit.message.strip()}")
    print("-" * 60)

    with lock:
        charter = state.get("project_charter", {})

    # Get commit diff
    commit_diff = commit.diff(commit.parents[0]) if commit.parents else []
    diff_text = "\n".join([d.diff.decode('utf-8', 'ignore') if d.diff else '' for d in commit_diff])

    print(f"📝 Analyzing {len(diff_text)} characters of commit changes...")

    prompt = f"""
    Given the project charter:
    {charter}

    And the following commit diff:
    {diff_text[:2000]}  # Limit to avoid token limits

    Does this commit align with the project charter? Update the status of the charter items.
    Respond with a JSON object representing the updated charter.
    If the charter is empty, analyze the commit and suggest what charter items it addresses.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1000,
                response_mime_type='application/json',
            ),
        )

        print("✅ Commit analysis complete")
        if response.text:
            print("📋 Charter Update:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)

        with lock:
            state['project_charter']['last_analyzed_commit'] = commit.hexsha
            # Could parse and update charter from response.parsed if needed

        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error in deep path analysis: {e}")
        print("="*60 + "\n")

def analyze_screen_proactively(image_bytes, state, lock):
    """
    Analyzes the screen for proactive assistance opportunities.
    Uses gemini-2.5-flash for fast multimodal analysis.
    """
    print("\n" + "="*60)
    print("👁️  SCREEN ANALYSIS - Proactive Assistance")
    print("="*60)

    if not client:
        print("⚠️  Gemini client not initialized, skipping analysis")
        return

    print(f"🖼️  Analyzing screenshot ({len(image_bytes)} bytes)...")

    try:
        # Get current state context
        with lock:
            issues_summary = f"{len(state.get('active_issues', []))} active issues"
            security_score = state.get('security_score', 100)

        prompt = f"""Analyze this developer's screen image and identify if there are any clear coding opportunities.

Current project status: Security Score {security_score}/100, {issues_summary}

Look for:
- Visible errors or warnings in code editor or terminal
- Code patterns that could be improved
- Potential bugs in visible code
- Opportunities for refactoring visible code

Only respond if you see something specific and actionable on screen.
If nothing notable, respond with: None

Keep response under 50 words and be specific to what you see on screen."""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            ],
            config=types.GenerateContentConfig(
                temperature=1,
                max_output_tokens=500,
            ),
        )

        # Log the raw response for debugging
        if response.text:
            print(f"📝 Response received ({len(response.text)} chars)")
        else:
            print("⚠️  Empty response from API (possible safety filter or rate limit)")
            print("="*60 + "\n")
            return

        result = response.text.strip()

        if result and result.lower() != "none":
            print("💡 SUGGESTION FOUND!")
            print("-" * 60)
            print(result)
            print("-" * 60)

            with lock:
                state["active_issues"].append({
                    "type": "Proactive Suggestion",
                    "description": result,
                    "severity": "Medium"
                })
                print(f"🚨 Total Active Issues: {len(state['active_issues'])}")
        else:
            print("✅ No suggestions at this time")

        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error in screen analysis: {e}")
        import traceback
        print(traceback.format_exc())
        print("="*60 + "\n")

def generate_oracle_prompt(goal, image_bytes, context):
    """
    Generates a detailed prompt for the Oracle function.
    Uses gemini-2.5-pro for advanced prompt engineering.
    """
    print("\n" + "="*60)
    print("🔮 ORACLE - Prompt Engineering")
    print("="*60)
    print(f"🎯 Goal: {goal}")
    print(f"🖼️  Screenshot: {len(image_bytes)} bytes")
    print("-" * 60)

    if not client:
        print("❌ Gemini client not initialized. Please set GEMINI_API_KEY.")
        print("="*60 + "\n")
        return "Error: Gemini client not initialized. Please set GEMINI_API_KEY."

    try:
        prompt_engineering_prompt = f"""
        As an expert prompt engineer, your task is to create a new, detailed prompt for another AI model.

        User's Goal: {goal}
        Project Context: {context}

        The user has provided a screenshot of their current work.
        Based on all this information, generate the most effective prompt to help the user achieve their goal.
        Make the prompt specific, actionable, and optimized for an AI assistant.
        """

        print("🤖 Generating optimized prompt...")

        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[
                prompt_engineering_prompt,
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            ],
            config=types.GenerateContentConfig(
                temperature=0.7,  # More creative for prompt engineering
                max_output_tokens=1000,
            ),
        )

        print("✅ Oracle prompt generated!")
        print("-" * 60)
        print(response.text)
        print("="*60 + "\n")

        return response.text
    except Exception as e:
        error_msg = f"Error generating prompt: {str(e)}"
        print(f"❌ {error_msg}")
        print("="*60 + "\n")
        return error_msg

def initialize_project_context(project_path, state, lock):
    """
    Initialize project context by analyzing the codebase structure.
    Creates a context.md file and updates the project charter.
    """
    print("\n" + "="*60)
    print("📋 INITIALIZING PROJECT CONTEXT")
    print("="*60)

    if not client:
        print("⚠️  Gemini client not initialized, skipping initialization")
        return {"error": "Gemini client not initialized"}

    print(f"📂 Analyzing project: {project_path}")

    try:
        import subprocess
        import json
        from pathlib import Path

        # Get git info
        try:
            git_info = subprocess.run(
                ['git', '-C', project_path, 'log', '-1', '--pretty=format:%H|%an|%ae|%s'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if git_info.returncode == 0:
                commit_hash, author, email, message = git_info.stdout.split('|')
                git_context = f"Latest commit: {commit_hash[:8]} by {author} - {message}"
            else:
                git_context = "No git repository found"
        except Exception as e:
            git_context = f"Could not read git info: {e}"

        # Get file structure (limited to avoid token limits)
        try:
            tree_output = subprocess.run(
                ['find', project_path, '-type', 'f', '-not', '-path', '*/node_modules/*',
                 '-not', '-path', '*/.git/*', '-not', '-path', '*/venv/*'],
                capture_output=True,
                text=True,
                timeout=5
            )
            files = tree_output.stdout.split('\n')[:100]  # Limit to first 100 files
            file_structure = '\n'.join(files)
        except Exception as e:
            file_structure = f"Could not read file structure: {e}"

        # Read package.json or requirements.txt if they exist
        tech_stack = []
        package_json_path = Path(project_path) / 'package.json'
        requirements_path = Path(project_path) / 'requirements.txt'

        if package_json_path.exists():
            try:
                with open(package_json_path) as f:
                    pkg = json.load(f)
                    tech_stack.append(f"JavaScript/Node.js project: {pkg.get('name', 'unknown')}")
                    if 'dependencies' in pkg:
                        tech_stack.append(f"Dependencies: {', '.join(list(pkg['dependencies'].keys())[:10])}")
            except:
                pass

        if requirements_path.exists():
            try:
                with open(requirements_path) as f:
                    reqs = f.read().split('\n')[:10]
                    tech_stack.append(f"Python project with packages: {', '.join(reqs)}")
            except:
                pass

        tech_info = '\n'.join(tech_stack) if tech_stack else "Could not determine tech stack"

        # Generate analysis with Gemini
        analysis_prompt = f"""Analyze this project and create a structured project context document.

Git Context:
{git_context}

Technology Stack:
{tech_info}

File Structure (sample):
{file_structure[:1000]}

Create a JSON response with:
1. "project_name": The likely project name
2. "description": A brief description of what this project does
3. "tech_stack": List of technologies used
4. "key_directories": Important directories and their purposes
5. "charter": List of project goals/objectives you can infer

Be concise and focus on what's actually visible in the codebase."""

        print("🤖 Analyzing project structure with AI...")

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=analysis_prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=5000,
                response_mime_type='application/json',
            ),
        )

        if not response.text:
            print("⚠️  Empty response from API")
            return {"error": "Empty response from API"}

        context_data = json.loads(response.text)

        # Create context.md file
        context_md_path = Path(project_path) / '.vibe-assist' / 'context.md'
        context_md_path.parent.mkdir(exist_ok=True)

        md_content = f"""# Project Context

Generated: {git_context}

## Overview
{context_data.get('description', 'No description available')}

## Technology Stack
{chr(10).join('- ' + tech for tech in context_data.get('tech_stack', []))}

## Key Directories
{chr(10).join('- **' + k + '**: ' + v for k, v in context_data.get('key_directories', {}).items())}

## Project Charter
{chr(10).join('- ' + item for item in context_data.get('charter', []))}

---
*This file is automatically maintained by Vibe Assist*
"""

        with open(context_md_path, 'w') as f:
            f.write(md_content)

        print(f"✅ Created context file: {context_md_path}")

        # Update state
        with lock:
            state['project_charter'] = {
                'initialized': True,
                'project_name': context_data.get('project_name', 'Unknown'),
                'description': context_data.get('description', ''),
                'charter_items': context_data.get('charter', []),
                'context_file': str(context_md_path)
            }

        print("✅ Project context initialized successfully")
        print("="*60 + "\n")

        return {
            "success": True,
            "context_file": str(context_md_path),
            "data": context_data
        }

    except Exception as e:
        print(f"❌ Error initializing project context: {e}")
        import traceback
        print(traceback.format_exc())
        print("="*60 + "\n")
        return {"error": str(e)}

