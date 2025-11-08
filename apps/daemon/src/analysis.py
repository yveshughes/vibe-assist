# analysis.py

import os
import json
import fnmatch
from pathlib import Path
from typing import List, Dict, Set
from pydantic import BaseModel
from google import genai
from google.genai import types
from git import Repo, exc

# Initialize Gemini client
# Make sure to set your GEMINI_API_KEY environment variable
client = None

# Pydantic models for JSON schema validation
class APIEndpoint(BaseModel):
    """Schema for API endpoint documentation."""
    path: str
    method: str
    purpose: str

class KeyFunction(BaseModel):
    """Schema for important functions/classes."""
    name: str
    location: str  # file:line
    purpose: str

class ComponentInteraction(BaseModel):
    """Schema for how components interact."""
    from_component: str
    to_component: str
    interaction_type: str  # e.g., "API call", "file read", "event"
    description: str

class CharterItem(BaseModel):
    """Schema for a single charter goal/item."""
    goal: str
    completed: bool = False
    completed_by_commit: str = ""  # Commit hash that completed this goal

class ProjectCharter(BaseModel):
    """Schema for comprehensive project charter data returned by AI."""
    project_name: str
    description: str
    tech_stack: List[str]
    key_directories: Dict[str, str]
    charter_items: List[CharterItem]

    # Enhanced fields for better AI assistant context
    architecture_overview: str  # How components fit together
    api_endpoints: List[APIEndpoint]  # Key API routes
    key_functions: List[KeyFunction]  # Important code entities
    component_interactions: List[ComponentInteraction]  # Data flow
    coding_patterns: List[str]  # Common patterns (e.g., "Pydantic for validation")
    development_setup: str  # How to run/develop

class SecurityIssue(BaseModel):
    """Schema for security issue detection."""
    type: str
    description: str
    severity: str

class ProactiveSuggestion(BaseModel):
    """Schema for proactive screen analysis suggestions."""
    has_suggestion: bool
    suggestion_type: str = ""  # e.g., "error", "security", "bug", "architecture"
    description: str = ""
    severity: str = "High"  # Only "High" or "Critical" should be reported

class OraclePrompt(BaseModel):
    """Schema for Oracle-generated prompts."""
    optimized_prompt: str
    key_context_points: List[str]
    suggested_approach: str

class CharterAlignmentCheck(BaseModel):
    """Schema for checking if a commit aligns with charter goals."""
    completed_goals: List[int]  # Indices of charter items that this commit completes
    reasoning: str  # Brief explanation of why these goals are completed

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

def _load_ignore_patterns(project_path: str) -> Set[str]:
    """
    Load ignore patterns from .vibe-assist.ignore file.

    Returns a set of patterns to ignore during file scanning.
    Supports:
    - Comments (lines starting with #)
    - Glob patterns (*.log, test_*)
    - Directory patterns (node_modules/, .git/)
    - Exact file paths
    """
    ignore_patterns = set()
    ignore_file = Path(project_path) / ".vibe-assist.ignore"

    if not ignore_file.exists():
        print(f"ℹ️  No .vibe-assist.ignore file found at {ignore_file}")
        return ignore_patterns

    try:
        with open(ignore_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                ignore_patterns.add(line)

        if ignore_patterns:
            print(f"✓ Loaded {len(ignore_patterns)} ignore pattern(s) from .vibe-assist.ignore")
            for pattern in sorted(ignore_patterns):
                print(f"  - {pattern}")

        return ignore_patterns
    except Exception as e:
        print(f"⚠️  Error reading .vibe-assist.ignore: {e}")
        return ignore_patterns

def _should_ignore_path(path: Path, project_path: Path, ignore_patterns: Set[str]) -> bool:
    """
    Check if a path should be ignored based on ignore patterns.

    Args:
        path: The absolute path to check
        project_path: The project root path
        ignore_patterns: Set of patterns from .vibe-assist.ignore

    Returns:
        True if the path should be ignored, False otherwise
    """
    if not ignore_patterns:
        return False

    try:
        # Get relative path from project root
        rel_path = path.relative_to(project_path)
        rel_path_str = str(rel_path)

        # Check against each pattern
        for pattern in ignore_patterns:
            # Directory pattern (ends with /)
            if pattern.endswith('/'):
                dir_pattern = pattern.rstrip('/')
                # Check if any part of the path matches
                if any(part == dir_pattern for part in rel_path.parts):
                    return True
                # Check if path starts with this directory
                if rel_path_str.startswith(dir_pattern + '/') or rel_path_str == dir_pattern:
                    return True
            # Glob pattern
            elif '*' in pattern or '?' in pattern:
                # Match against full relative path
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
                # Match against just the filename
                if fnmatch.fnmatch(path.name, pattern):
                    return True
            # Exact match
            else:
                if rel_path_str == pattern or path.name == pattern:
                    return True

        return False
    except ValueError:
        # Path is not relative to project_path
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
    If a critical vulnerability is found, respond with a JSON object with: type (string), description (string), severity (string: "Critical", "High", "Medium", or "Low").
    If no critical vulnerability is found, respond with an empty JSON object: {{}}.

    Diff:
    {diff}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'max_output_tokens': 500,
                'response_mime_type': 'application/json',
                'response_json_schema': SecurityIssue.model_json_schema(),
            },
        )

        # Parse response using Pydantic
        if response.text:
            try:
                issue = SecurityIssue.model_validate_json(response.text)
            except Exception:
                # If parsing fails, no valid issue found
                print("✅ No security issues detected")
                print("="*60 + "\n")
                return
            print("⚠️  SECURITY ISSUE DETECTED!")
            print("-" * 60)
            print(f"Type: {issue.type}")
            print(f"Severity: {issue.severity}")
            print(f"Description: {issue.description}")
            print("-" * 60)

            with lock:
                state["security_score"] -= 10
                state["active_issues"].append({
                    "type": issue.type,
                    "description": issue.description,
                    "severity": issue.severity
                })
                print(f"📊 Security Score: {state['security_score']}/100")
                print(f"🚨 Total Active Issues: {len(state['active_issues'])}")
        else:
            print("✅ No security issues detected")

        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error in fast path analysis: {e}")
        print("="*60 + "\n")

def _save_state_and_charter_files(state, lock, state_file_path, charter_file_path):
    """
    Saves the current state to state.json and writes the charter to context.vibe.
    """
    if not state_file_path or not charter_file_path:
        print("❌ Cannot save state or charter: file paths not provided.")
        return

    with lock:
        # 1. Save the full state to state.json
        try:
            with open(state_file_path, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"✅ State saved successfully to {state_file_path}")
        except Exception as e:
            print(f"❌ Error saving state to {state_file_path}: {e}")

        # 2. Write the human-readable charter to context.vibe
        charter_data = state.get("project_charter", {})
        try:
            # Build API endpoints section
            api_endpoints_md = ""
            if charter_data.get('api_endpoints'):
                api_endpoints_md = "\n## API Endpoints\n"
                for ep in charter_data.get('api_endpoints', []):
                    api_endpoints_md += f"- **{ep.get('method', 'GET')} {ep.get('path', '')}**: {ep.get('purpose', '')}\n"

            # Build key functions section
            key_functions_md = ""
            if charter_data.get('key_functions'):
                key_functions_md = "\n## Key Functions & Classes\n"
                for func in charter_data.get('key_functions', []):
                    key_functions_md += f"- **{func.get('name', '')}** (`{func.get('location', '')}`): {func.get('purpose', '')}\n"

            # Build component interactions section
            interactions_md = ""
            if charter_data.get('component_interactions'):
                interactions_md = "\n## Component Interactions\n"
                for interaction in charter_data.get('component_interactions', []):
                    interactions_md += f"- **{interaction.get('from_component', '')}** → **{interaction.get('to_component', '')}** ({interaction.get('interaction_type', '')}): {interaction.get('description', '')}\n"

            # Build coding patterns section
            patterns_md = ""
            if charter_data.get('coding_patterns'):
                patterns_md = "\n## Coding Patterns & Conventions\n"
                for pattern in charter_data.get('coding_patterns', []):
                    patterns_md += f"- {pattern}\n"

            # Build charter goals section with completion status
            charter_goals_md = "\n## Project Goals\n"
            for item in charter_data.get('charter_items', []):
                if isinstance(item, dict):
                    goal_text = item.get('goal', str(item))
                    completed = item.get('completed', False)
                    completed_by = item.get('completed_by_commit', '')

                    if completed:
                        status_icon = "✅"
                        if completed_by:
                            charter_goals_md += f"- {status_icon} ~~{goal_text}~~ *(completed in {completed_by[:8]})*\n"
                        else:
                            charter_goals_md += f"- {status_icon} ~~{goal_text}~~\n"
                    else:
                        charter_goals_md += f"- ⬜ {goal_text}\n"
                else:
                    # Fallback for plain strings (legacy format)
                    charter_goals_md += f"- ⬜ {item}\n"

            md_content = f"""# Project Context: {charter_data.get('project_name', 'Unknown')}

## Overview
{charter_data.get('description', 'No description available')}

## Architecture
{charter_data.get('architecture_overview', 'No architecture details available')}

## Technology Stack
{chr(10).join('- ' + tech for tech in charter_data.get('tech_stack', []))}

## Key Directories
{chr(10).join('- **' + k + '**: ' + v for k, v in charter_data.get('key_directories', {}).items())}
{charter_goals_md}{api_endpoints_md}{key_functions_md}{interactions_md}{patterns_md}
## Development Setup
{charter_data.get('development_setup', 'No setup information available')}

---
*Last updated from commit: {state.get('last_analyzed_commit', 'N/A')[:8] if state.get('last_analyzed_commit') != 'N/A' else 'N/A'}*
*This file is automatically maintained by Vibe Assist.*
"""
            with open(charter_file_path, 'w') as f:
                f.write(md_content)
            print(f"✅ Charter written successfully to {charter_file_path}")
        except Exception as e:
            print(f"❌ Error writing charter to {charter_file_path}: {e}")


def _check_charter_alignment(commit, diff_content, charter_items):
    """
    Check if a commit completes any charter goals.
    Returns a CharterAlignmentCheck object or None if an error occurs.
    """
    if not client:
        return None

    # Format charter items for the prompt
    charter_items_text = ""
    for i, item in enumerate(charter_items):
        goal_text = item.goal if isinstance(item, CharterItem) else item.get('goal', str(item))
        is_completed = False
        if isinstance(item, CharterItem):
            is_completed = item.completed
        elif isinstance(item, dict):
            is_completed = item.get('completed', False)

        status = "✓ COMPLETED" if is_completed else "○ PENDING"
        charter_items_text += f"{i}. [{status}] {goal_text}\n"

    alignment_prompt = f"""
    Analyze this commit to determine if it completes any of the project charter goals.

    Commit Message: {commit.message.strip()}

    Commit Changes Summary:
    {diff_content[:50000]}

    Project Charter Goals:
    {charter_items_text}

    Question: Which charter goals (if any) does this commit meaningfully complete or fulfill?

    Respond with:
    - completed_goals: List of goal indices (0-based) that this commit completes. Only include goals that are substantially fulfilled by this commit. Empty list if none.
    - reasoning: Brief explanation (1-2 sentences) of why these goals are considered complete.

    Be conservative - only mark a goal as complete if the commit truly fulfills it, not just makes progress toward it.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=alignment_prompt,
            config={
                'max_output_tokens': 500,
                'response_mime_type': 'application/json',
                'response_json_schema': CharterAlignmentCheck.model_json_schema(),
            },
        )

        if response.text:
            return CharterAlignmentCheck.model_validate_json(response.text)
        return None
    except Exception as e:
        print(f"⚠️  Error checking charter alignment: {e}")
        return None

def analyze_deep_path(commit, state, lock, state_file_path, context_file_path):
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
        if not charter.get('initialized'):
            print("⚠️  Project charter not initialized, skipping deep analysis.")
            print("="*60 + "\n")
            return

    # Get commit diff
    try:
        # Comparing to the first parent of the commit
        parent = commit.parents[0] if commit.parents else None
        diff_text = commit.diff(parent, create_patch=True)
        diff_content = "\n".join([d.diff.decode('utf-8', 'ignore') for d in diff_text])
    except Exception as e:
        print(f"❌ Error getting diff for commit {commit.hexsha}: {e}")
        return

    if not diff_content.strip():
        print("📝 No textual changes in commit, skipping analysis.")
        with lock:
            state['last_analyzed_commit'] = commit.hexsha
        _save_state_and_charter_files(state, lock, state_file_path, context_file_path)
        print("="*60 + "\n")
        return

    print(f"📝 Analyzing {len(diff_content)} characters of commit changes...")

    prompt = f"""
    As a senior engineer, your task is to maintain the project's context by analyzing this new commit.
    
    Here is the current project charter:
    {json.dumps(charter, indent=2)}

    Here is the diff from the latest commit:
    ---
    {diff_content[:100000]}
    ---

    Based on the commit message and the code changes, update ALL fields of the project charter:
    - Refine the `description` if the commit clarifies the project's purpose
    - Update `tech_stack` if dependencies change
    - Update `key_directories` if new important folders/modules are added
    - Update `charter_items` to reflect evolving goals (add new goals if needed, refine existing goals, but DO NOT change completion status - that's handled separately)
    - Update `architecture_overview` if architectural changes occurred
    - Update `api_endpoints` if new routes/endpoints were added or modified
    - Update `key_functions` if critical functions/classes changed
    - Update `component_interactions` if integration patterns changed
    - Update `coding_patterns` if new patterns were introduced
    - Update `development_setup` if setup/deployment changed

    IMPORTANT: For charter_items, preserve any existing completion status. Each item must have: goal (string), completed (boolean), completed_by_commit (string).

    Respond with the COMPLETE, UPDATED project charter as a single JSON object with ALL fields.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
            config={
                'max_output_tokens': 16000,
                'response_mime_type': 'application/json',
                'response_json_schema': ProjectCharter.model_json_schema(),
            },
        )

        print("✅ Commit analysis complete")
        if response.text:
            charter_update = ProjectCharter.model_validate_json(response.text)
            print("📋 Proposed Charter Update:")
            print(f"  Project: {charter_update.project_name}")
            print(f"  Tech Stack: {', '.join(charter_update.tech_stack[:3])}...")
            print(f"  Charter Items: {len(charter_update.charter_items)} goals")

            try:
                with lock:
                    # Update the in-memory state with all fields from parsed Pydantic model
                    state['project_charter'].update({
                        'project_name': charter_update.project_name,
                        'description': charter_update.description,
                        'tech_stack': charter_update.tech_stack,
                        'key_directories': charter_update.key_directories,
                        'charter_items': [item.model_dump() for item in charter_update.charter_items],
                        # Enhanced fields
                        'architecture_overview': charter_update.architecture_overview,
                        'api_endpoints': [ep.model_dump() for ep in charter_update.api_endpoints],
                        'key_functions': [func.model_dump() for func in charter_update.key_functions],
                        'component_interactions': [ci.model_dump() for ci in charter_update.component_interactions],
                        'coding_patterns': charter_update.coding_patterns,
                        'development_setup': charter_update.development_setup,
                    })
                    state['last_analyzed_commit'] = commit.hexsha

                # --- Check Charter Alignment ---
                print("\n🎯 Checking charter alignment...")
                alignment_check = _check_charter_alignment(commit, diff_content, charter_update.charter_items)

                if alignment_check and alignment_check.completed_goals:
                    print(f"✅ Commit completes {len(alignment_check.completed_goals)} charter goal(s)!")
                    print(f"   Reasoning: {alignment_check.reasoning}")

                    with lock:
                        # Mark goals as completed
                        for goal_index in alignment_check.completed_goals:
                            if 0 <= goal_index < len(state['project_charter']['charter_items']):
                                state['project_charter']['charter_items'][goal_index]['completed'] = True
                                state['project_charter']['charter_items'][goal_index]['completed_by_commit'] = commit.hexsha
                                goal_text = state['project_charter']['charter_items'][goal_index]['goal']
                                print(f"   ✓ Goal {goal_index}: {goal_text[:60]}...")

                # Persist the changes to disk
                _save_state_and_charter_files(state, lock, state_file_path, context_file_path)

            except Exception as e:
                print(f"❌ Error updating charter: {e}")

        else:
            print("⚠️  Empty response from AI, no charter update.")

        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error in deep path analysis: {e}")
        print("="*60 + "\n")

def initialize_project_context_full(project_path, state, lock, state_file_path, context_file_path):
    """
    Initialize project context by analyzing the entire codebase.
    Creates state.json and context.vibe files.
    """
    print("\n" + "="*60)
    print("📋 INITIALIZING PROJECT CONTEXT (FULL SCAN)")
    print("="*60)

    if not client:
        print("⚠️  Gemini client not initialized, skipping initialization")
        return

    print(f"📂 Analyzing all files in: {project_path}")

    try:
        repo = Repo(project_path)
        latest_commit = repo.head.commit.hexsha
    except exc.InvalidGitRepositoryError:
        print("⚠️  Not a git repository. Cannot check for ignored files.")
        repo = None
        latest_commit = "N/A"

    # --- 1. Load ignore patterns ---
    ignore_patterns = _load_ignore_patterns(project_path)

    # --- 2. Gather all code files ---
    all_files_content = []
    file_count = 0
    total_size = 0
    skipped_by_ignore = 0

    print("📄 Analyzing files...")

    # Common non-code file extensions to skip
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp', '.pdf', '.zip', '.gz', '.tar', '.rar', '.exe', '.dll', '.so', '.o', '.a', '.lib', '.class', '.pyc', '.pyd', '.egg', '.jar', '.war', '.ear', '.docx', '.xlsx', '.pptx', '.odt', '.ods', '.odp'}

    # Common dependency/build directories to skip
    skip_dirs = {'node_modules', '.git', 'venv', 'env', 'dist', 'build', '__pycache__', '.vscode', '.idea', '.vibe-assist'}

    project_path_obj = Path(project_path)

    for p in project_path_obj.rglob('*'):
        # Skip common build/dependency directories
        if any(part in skip_dirs for part in p.parts):
            continue

        if not p.is_file():
            continue

        # Check against .vibe-assist.ignore patterns
        if _should_ignore_path(p, project_path_obj, ignore_patterns):
            skipped_by_ignore += 1
            continue

        # Check if file is in gitignore (if repo exists)
        if repo:
            try:
                # Use relative path for gitignore check
                rel_path = str(p.relative_to(project_path))
                # repo.ignored returns list of ignored paths
                if list(repo.ignored(rel_path)):
                    continue
            except Exception:
                # If gitignore check fails, skip this file to be safe
                continue

        # Skip binary files
        if p.suffix.lower() in binary_extensions:
            continue

        try:
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
                rel_path_display = p.relative_to(project_path)
                print(f"  ✓ {rel_path_display} ({len(content)} bytes)")
                all_files_content.append(f"--- FILE: {rel_path_display} ---\n{content}")
                file_count += 1
                total_size += len(content)
        except (UnicodeDecodeError, IOError) as e:
            # Skip files that can't be read as text
            print(f"  ⊘ {p.relative_to(project_path)} (unreadable: {type(e).__name__})")
            continue
    
    print(f"✅ Found and read {file_count} code files (Total size: {total_size / 1024:.2f} KB).")
    if skipped_by_ignore > 0:
        print(f"ℹ️  Skipped {skipped_by_ignore} file(s) via .vibe-assist.ignore")
    full_codebase_text = "\n\n".join(all_files_content)

    # --- 2. Generate analysis with Gemini ---
    analysis_prompt = f"""
    As a senior software architect, perform a comprehensive analysis of this codebase to create a detailed project context document for an AI coding assistant.

    Here is the full codebase:
    ---
    {full_codebase_text[:900000]}
    ---

    Analyze the code and provide a JSON response with these fields:

    1. "project_name": The project name (from package.json, setup.py, README, or infer from structure).

    2. "description": A concise paragraph describing what this project does and its main purpose.

    3. "tech_stack": List all key technologies, frameworks, languages, and libraries used.

    4. "key_directories": Map important directories/modules to their purpose.

    5. "charter_items": List 5-7 high-level goals or objectives this project aims to achieve. Each item should have a "goal" field with the goal description, "completed" set to false, and "completed_by_commit" as empty string.

    6. "architecture_overview": Explain in 2-3 paragraphs how components interact, the system architecture, data flow, and component relationships.

    7. "api_endpoints": List key API endpoints/routes found in the code. For each include: path, HTTP method, and purpose. If no APIs exist, return empty list.

    8. "key_functions": List 8-12 critical functions/classes with: name, location (filepath:line), and purpose. Focus on entry points, main business logic, and integration points.

    9. "component_interactions": List 5-8 key interactions between different parts of the system (modules, services, external APIs, databases, etc.). Show how components communicate.

    10. "coding_patterns": List 5-7 important patterns, conventions, or architectural decisions observed (validation approaches, state management, error handling, testing patterns, etc.).

    11. "development_setup": Describe how to run and develop this project (package managers, dependencies, build commands, environment setup, required env variables).

    Base analysis solely on the provided code. Be accurate and project-agnostic.
    """

    print("🤖 Analyzing project structure with AI (this may take a moment)...")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=analysis_prompt,
            config={
                'max_output_tokens': 8000,
                'response_mime_type': 'application/json',
                'response_json_schema': ProjectCharter.model_json_schema(),
            },
        )

        if not response.text:
            print("❌ CRITICAL: Empty response from API during initialization.")
            return

        context_data = ProjectCharter.model_validate_json(response.text)

        # --- 3. Update state and save files ---
        with lock:
            state['project_charter'] = {
                'initialized': True,
                'project_name': context_data.project_name,
                'description': context_data.description,
                'tech_stack': context_data.tech_stack,
                'key_directories': context_data.key_directories,
                'charter_items': [item.model_dump() for item in context_data.charter_items],
                # Enhanced fields
                'architecture_overview': context_data.architecture_overview,
                'api_endpoints': [ep.model_dump() for ep in context_data.api_endpoints],
                'key_functions': [func.model_dump() for func in context_data.key_functions],
                'component_interactions': [ci.model_dump() for ci in context_data.component_interactions],
                'coding_patterns': context_data.coding_patterns,
                'development_setup': context_data.development_setup,
            }
            state['last_analyzed_commit'] = latest_commit

        _save_state_and_charter_files(state, lock, state_file_path, context_file_path)

        print("✅ Project context initialized successfully!")
        print(f"📋 Project: {context_data.project_name}")
        print(f"🔧 Tech Stack: {', '.join(context_data.tech_stack)}")
        print(f"📂 Key Directories: {len(context_data.key_directories)}")
        print(f"🎯 Charter Items: {len(context_data.charter_items)}")
        print(f"🔗 API Endpoints: {len(context_data.api_endpoints)}")
        print(f"⚙️  Key Functions: {len(context_data.key_functions)}")
        print(f"🔄 Component Interactions: {len(context_data.component_interactions)}")
        print("="*60 + "\n")

    except Exception as e:
        print(f"❌ Error during full project initialization: {e}")
        import traceback
        print(traceback.format_exc())
        print("="*60 + "\n")
        # Ensure we don't leave a partially initialized state
        with lock:
            state['project_charter']['initialized'] = False

class TriagedSuggestion(BaseModel):
    """Schema for a triaged and prioritized suggestion."""
    type: str
    description: str
    severity: str
    priority_score: int  # 1-5, where 5 is highest priority

class SuggestionTriage(BaseModel):
    """Schema for triaged suggestions with deduplication and prioritization."""
    suggestions: List[TriagedSuggestion]
    reasoning: str  # Brief explanation of prioritization

def triage_suggestions(new_suggestion, existing_issues, state, lock):
    """
    Triage a new suggestion against existing issues to determine if it should be added.
    Uses AI to deduplicate, cluster, and prioritize suggestions.

    Returns: (should_add: bool, triaged_suggestion: dict or None)
    """
    # First, check against user feedback (dismissed and false positives)
    with lock:
        user_feedback = state.get('user_feedback', {})
        false_positives = user_feedback.get('false_positives', [])

        # Check if this matches a known false positive
        for fp in false_positives:
            fp_desc = fp.get('description', '')
            if fp_desc and new_suggestion.description:
                fp_words = set(fp_desc.lower().split())
                new_words = set(new_suggestion.description.lower().split())
                if fp_words and new_words:
                    overlap = len(fp_words & new_words) / len(fp_words | new_words)
                    if overlap > 0.7:  # 70% match with false positive
                        print(f"   Triage: Skipped - matches false positive pattern")
                        return False, None

    if not client:
        # Fallback to simple duplicate check if no AI available
        for existing_issue in existing_issues:
            existing_desc = existing_issue.get("description", "")
            if existing_desc and new_suggestion.description:
                existing_words = set(existing_desc.lower().split())
                new_words = set(new_suggestion.description.lower().split())
                if existing_words and new_words:
                    overlap = len(existing_words & new_words) / len(existing_words | new_words)
                    if overlap > 0.8:
                        return False, None
        # If not duplicate, add with default priority
        return True, {
            "type": f"Proactive - {new_suggestion.suggestion_type}",
            "description": new_suggestion.description,
            "severity": new_suggestion.severity,
            "priority_score": 3  # Default medium priority
        }

    # Format existing issues for context
    existing_issues_text = ""
    if existing_issues:
        existing_issues_text = "Existing tracked issues:\n"
        for i, issue in enumerate(existing_issues[-15:], 1):  # Last 15 issues
            existing_issues_text += f"{i}. [{issue.get('severity', 'Unknown')}] {issue.get('type', '')}: {issue.get('description', '')[:80]}\n"

    triage_prompt = f"""
    You are an intelligent issue triage system for a development assistant. REJECT low-value suggestions aggressively.

    New suggestion detected:
    Type: {new_suggestion.suggestion_type}
    Description: {new_suggestion.description}
    Severity: {new_suggestion.severity}

    {existing_issues_text}

    NOTE: This suggestion already passed initial screening against user feedback (false positives/dismissed issues).
    Your job is to verify it's truly strategic/urgent and assign priority.

    Your task:
    1. First, determine if this is truly strategic or urgent:
       - Is it a security vulnerability, critical bug, or blocking error?
       - Does it have clear business/technical impact?
       - Would a senior engineer prioritize fixing this today?

    2. If yes, check for duplicates against existing issues

    3. If unique AND high-value, assign priority score (4-5 only, reject anything below 4):
       - 5 = Critical: Security issue, production bug, blocks all work
       - 4 = High: Significant bug, architectural flaw, blocks feature work
       - 3 or below = REJECT (not strategic enough)

    Respond with:
    - suggestions: Empty list if duplicate OR low-value (priority < 4), OR a list with one item:
      - type: Issue type (use "Proactive - {new_suggestion.suggestion_type}")
      - description: Clear, actionable description
      - severity: "High" or "Critical"
      - priority_score: 4 or 5 only
    - reasoning: Brief explanation (why rejected or why priority X)

    IMPORTANT: Reject 90% of suggestions. Only the most critical issues should pass.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=triage_prompt,
            config={
                'max_output_tokens': 500,
                'response_mime_type': 'application/json',
                'response_json_schema': SuggestionTriage.model_json_schema(),
            },
        )

        if response.text:
            triage_result = SuggestionTriage.model_validate_json(response.text)

            if not triage_result.suggestions:
                # Marked as duplicate
                print(f"   Triage: Duplicate - {triage_result.reasoning}")
                return False, None

            # Unique suggestion, add it
            triaged = triage_result.suggestions[0]
            print(f"   Triage: Priority {triaged.priority_score}/5 - {triage_result.reasoning}")
            return True, triaged.model_dump()

        # Empty response, use conservative fallback - only add if severity is High
        if new_suggestion.severity == "High":
            return True, {
                "type": f"Proactive - {new_suggestion.suggestion_type}",
                "description": new_suggestion.description,
                "severity": new_suggestion.severity,
                "priority_score": 4
            }
        else:
            print(f"   Triage: Rejected - only High severity accepted in fallback mode")
            return False, None
    except Exception as e:
        print(f"⚠️  Error in triage: {e}, using fallback")
        # Fallback to simple duplicate check - only for High severity
        if new_suggestion.severity != "High":
            print(f"   Triage: Rejected - severity not High")
            return False, None

        for existing_issue in existing_issues:
            existing_desc = existing_issue.get("description", "")
            if existing_desc and new_suggestion.description:
                existing_words = set(existing_desc.lower().split())
                new_words = set(new_suggestion.description.lower().split())
                if existing_words and new_words:
                    overlap = len(existing_words & new_words) / len(existing_words | new_words)
                    if overlap > 0.8:
                        return False, None
        return True, {
            "type": f"Proactive - {new_suggestion.suggestion_type}",
            "description": new_suggestion.description,
            "severity": new_suggestion.severity,
            "priority_score": 4
        }

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
            active_issues = state.get('active_issues', [])
            security_score = state.get('security_score', 100)
            user_feedback = state.get('user_feedback', {})
            false_positives = user_feedback.get('false_positives', [])
            dismissed_issues = user_feedback.get('dismissed_issues', [])

        # Log feedback context being used
        feedback_count = len(false_positives) + len(dismissed_issues)
        if feedback_count > 0:
            print(f"📚 Using {len(false_positives)} false positive(s) + {len(dismissed_issues)} dismissed pattern(s) as learning context")

        # Format existing issues for context
        existing_issues_text = ""
        if active_issues:
            existing_issues_text = "\n\nExisting tracked issues (DO NOT report these again):\n"
            for i, issue in enumerate(active_issues[-10:], 1):  # Last 10 issues
                existing_issues_text += f"{i}. [{issue.get('severity', 'Unknown')}] {issue.get('description', '')[:80]}\n"

        # Format user feedback - what they've rejected
        feedback_context = ""
        if false_positives or dismissed_issues:
            feedback_context = "\n\nUser has marked these as NOT worth tracking (DO NOT report similar issues):\n"

            # Show false positives
            for i, fp in enumerate(false_positives[-5:], 1):  # Last 5 FPs
                feedback_context += f"FP{i}. {fp.get('type', '')}: {fp.get('description', '')[:80]}\n"

            # Show recently dismissed
            for i, dm in enumerate(dismissed_issues[-5:], 1):  # Last 5 dismissed
                feedback_context += f"DM{i}. {dm.get('type', '')}: {dm.get('description', '')[:80]}\n"

        prompt = f"""You are a senior software architect analyzing a development screenshot. Your job is to identify ONLY strategic or urgent issues that need immediate attention.

Current project status: Security Score {security_score}/100, {len(active_issues)} active issues{existing_issues_text}{feedback_context}

IGNORE these (they are NOT worth reporting):
- IDE lightbulb hints, suggestions, or code actions
- Untracked files or uncommitted changes in git (unless blocking)
- Minor code style or formatting issues
- Generic linter warnings
- Auto-update notifications
- Missing imports that are already highlighted by IDE

ONLY report if you see:
1. **STRATEGIC ISSUES** (High impact):
   - Security vulnerabilities in visible code (SQL injection, XSS, exposed secrets, auth bypass)
   - Critical architectural flaws or anti-patterns
   - Memory leaks, race conditions, or concurrency bugs in code
   - Breaking API changes or incompatible dependencies

2. **URGENT ISSUES** (Blocks work):
   - Runtime errors or exceptions actively preventing execution
   - Build/compilation failures blocking development
   - Test failures indicating broken functionality
   - Deployment errors or production issues

CRITICAL: Be extremely selective. When in doubt, DO NOT report. Most IDE warnings are not worth tracking.

Respond with a JSON object:
- has_suggestion: true ONLY for strategic or urgent issues, false otherwise
- suggestion_type: "error", "security", "bug", or "architecture" (empty string if no suggestion)
- description: brief description under 40 words explaining impact and urgency (empty string if no suggestion)
- severity: "High" for strategic/urgent issues (default to "High" if reporting)

If the screenshot shows normal development (code editing, git status, IDE hints), set has_suggestion to false."""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            ],
            config={
                'max_output_tokens': 5000,
                'response_mime_type': 'application/json',
                'response_json_schema': ProactiveSuggestion.model_json_schema(),
                'safety_settings': [
                    {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
                    {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
                    {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
                    {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
                ],
            },
        )

        # Parse response
        if not response.text:
            print("⚠️  Empty response from API")
            # Check for safety ratings or blocked content
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    print(f"    Finish reason: {candidate.finish_reason}")
                if hasattr(candidate, 'safety_ratings'):
                    print(f"    Safety ratings: {candidate.safety_ratings}")
            print("    Possible causes: safety filter, rate limit, or content policy")
            print("="*60 + "\n")
            return

        try:
            suggestion = ProactiveSuggestion.model_validate_json(response.text)
        except Exception as e:
            print(f"⚠️  Error parsing response: {e}")
            print(f"    Raw response: {response.text[:200]}")
            print("="*60 + "\n")
            return

        if suggestion.has_suggestion and suggestion.description:
            print("💡 POTENTIAL ISSUE DETECTED!")
            print("-" * 60)
            print(f"Type: {suggestion.suggestion_type}")
            print(f"Severity: {suggestion.severity}")
            print(f"Description: {suggestion.description}")
            print("-" * 60)

            # Use intelligent triage system
            with lock:
                active_issues = state.get("active_issues", [])

            should_add, triaged_suggestion = triage_suggestions(suggestion, active_issues, state, lock)

            if should_add and triaged_suggestion:
                with lock:
                    state["active_issues"].append(triaged_suggestion)
                    print(f"✅ STRATEGIC ISSUE ADDED (Priority: {triaged_suggestion.get('priority_score', 4)}/5)")
                    print(f"🚨 Total Active Issues: {len(state['active_issues'])}")
            else:
                print("⊘ Rejected by triage - not strategic/urgent enough")
        else:
            print("✅ No critical issues detected")

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

        Respond with a JSON object containing:
        - optimized_prompt: The complete, detailed prompt ready to use with another AI (be specific and actionable)
        - key_context_points: List of 3-5 key context points extracted from the screenshot and project context
        - suggested_approach: Brief description of the recommended approach to achieve the goal
        """

        print("🤖 Generating optimized prompt...")

        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[
                prompt_engineering_prompt,
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            ],
            config={
                'max_output_tokens': 1000,
                'response_mime_type': 'application/json',
                'response_json_schema': OraclePrompt.model_json_schema(),
            },
        )

        if not response.text:
            print("⚠️  Empty response from API")
            print("="*60 + "\n")
            return "Error: Empty response from API"

        oracle_result = OraclePrompt.model_validate_json(response.text)

        print("✅ Oracle prompt generated!")
        print("-" * 60)
        print(f"📋 Optimized Prompt:\n{oracle_result.optimized_prompt}\n")
        print(f"🔑 Key Context Points:")
        for point in oracle_result.key_context_points:
            print(f"  - {point}")
        print(f"\n💡 Suggested Approach:\n{oracle_result.suggested_approach}")
        print("="*60 + "\n")

        return oracle_result.optimized_prompt
    except Exception as e:
        error_msg = f"Error generating prompt: {str(e)}"
        print(f"❌ {error_msg}")
        print("="*60 + "\n")
        return error_msg