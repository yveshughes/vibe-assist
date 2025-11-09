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
        current_head = repo.head.commit.hexsha
        print(f"Current HEAD: {current_head[:8]}")
    except Exception as e:
        print(f"ERROR: Could not get HEAD commit: {e}")
        return

    # Check if there are unprocessed commits
    with state_lock:
        last_analyzed = state.get('last_analyzed_commit')

    if last_analyzed and last_analyzed != current_head:
        try:
            print(f"Processing commits since {last_analyzed[:8]}...")
            # Get all commits between last_analyzed and HEAD
            commits_to_process = list(repo.iter_commits(f'{last_analyzed}..HEAD'))
            commits_to_process.reverse()  # Process oldest first

            print(f"Found {len(commits_to_process)} unprocessed commit(s)")
            for commit in commits_to_process:
                print(f"Processing historical commit: {commit.hexsha[:8]}")
                analysis.analyze_deep_path(commit, state, state_lock, state_file_path, context_file_path)
        except Exception as e:
            print(f"Warning: Could not process historical commits: {e}")
            print(f"Continuing from current HEAD...")

    last_commit_hash = current_head
    last_diff_text = ""

    while True:
        try:
            # --- Live Changes (Fast Path) ---
            # Get ALL uncommitted changes (both staged and unstaged)
            # repo.index.diff(None) = staged changes vs working tree
            # repo.head.commit.diff(None) = HEAD vs working tree (all changes)
            current_diff = repo.head.commit.diff(None)

            if current_diff:
                # Log which files changed
                changed_files = [item.a_path or item.b_path for item in current_diff]

                # Convert diff to text
                diff_text = ""
                for item in current_diff:
                    try:
                        if item.diff:
                            diff_text += item.diff.decode('utf-8', 'ignore')
                    except Exception as e:
                        print(f"⚠️  Error reading diff for {item.a_path}: {e}")

                # Only trigger if diff content actually changed
                if diff_text and diff_text != last_diff_text:
                    print(f"📝 Uncommitted changes detected in {len(changed_files)} file(s): {', '.join(changed_files[:5])}")
                    if len(changed_files) > 5:
                        print(f"   ... and {len(changed_files) - 5} more file(s)")
                    print(f"   Total diff size: {len(diff_text)} chars")
                    analysis.analyze_fast_path(diff_text, state, state_lock)
                    last_diff_text = diff_text
            else:
                # No uncommitted changes, reset
                if last_diff_text:
                    print("✓ Uncommitted changes cleared")
                    last_diff_text = ""

            # --- New Commits (Deep Path) ---
            current_commit_hash = repo.head.commit.hexsha
            if current_commit_hash != last_commit_hash:
                print(f"📦 New commit detected: {current_commit_hash[:8]}")
                commit = repo.commit(current_commit_hash)
                analysis.analyze_deep_path(commit, state, state_lock, state_file_path, context_file_path)
                last_commit_hash = current_commit_hash

        except Exception as e:
            print(f"❌ Error in watcher loop: {e}")

        time.sleep(1)  # Check every 1 second (reduced from 2s for faster detection)

