# watcher.py
import time
from git import Repo, exc
from . import analysis

def start(project_path, state, state_lock, state_file_path, context_file_path):
    """Thread for watching git diff and file changes."""
    print(f"Git watcher starting for: {project_path}")

    try:
        repo = Repo(project_path)
    except exc.InvalidGitRepositoryError:
        print(f"ERROR: {project_path} is not a valid git repository")
        print("Git watcher will not run.")
        return

    try:
        last_commit_hash = repo.head.commit.hexsha
        print(f"Starting from commit: {last_commit_hash[:8]}")
    except Exception as e:
        print(f"ERROR: Could not get HEAD commit: {e}")
        return

    last_diff_text = ""

    while True:
        try:
            # --- Live Changes (Fast Path) ---
            # Get uncommitted changes
            current_diff = repo.index.diff(None)

            if current_diff:
                # Convert diff to text
                diff_text = ""
                for item in current_diff:
                    try:
                        if item.diff:
                            diff_text += item.diff.decode('utf-8', 'ignore')
                    except Exception as e:
                        print(f"Error reading diff: {e}")

                # Only trigger if diff content actually changed
                if diff_text and diff_text != last_diff_text:
                    print(f"Uncommitted changes detected ({len(diff_text)} chars)")
                    analysis.analyze_fast_path(diff_text, state, state_lock)
                    last_diff_text = diff_text
            else:
                # No uncommitted changes, reset
                if last_diff_text:
                    print("Uncommitted changes cleared")
                    last_diff_text = ""

            # --- New Commits (Deep Path) ---
            current_commit_hash = repo.head.commit.hexsha
            if current_commit_hash != last_commit_hash:
                print(f"New commit detected: {current_commit_hash[:8]}")
                commit = repo.commit(current_commit_hash)
                analysis.analyze_deep_path(commit, state, state_lock, state_file_path, context_file_path)
                last_commit_hash = current_commit_hash

        except Exception as e:
            print(f"Error in watcher loop: {e}")

        time.sleep(2)  # Check every 2 seconds

