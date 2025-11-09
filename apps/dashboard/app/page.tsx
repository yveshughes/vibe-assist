"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

interface Issue {
  type: string;
  description: string;
  severity: string;
  priority_score?: number;
  file_path?: string;
  line_number?: number;
}

interface DaemonState {
  security_score: number;
  active_issues: Issue[];
  project_charter: {
    initialized: boolean;
    charter_items?: Array<{ completed?: boolean }>;
  };
  last_analyzed_commit?: string;
  user_feedback?: {
    dismissed_issues: any[];
    false_positives: any[];
  };
}

const DAEMON_URL = process.env.NEXT_PUBLIC_DAEMON_URL || "http://localhost:8000";

export default function Home() {
  const [state, setState] = useState<DaemonState | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const fetchState = async () => {
    try {
      setError(null);
      const response = await fetch(`${DAEMON_URL}/state`);

      if (!response.ok) {
        throw new Error("Failed to fetch daemon state");
      }

      const result: DaemonState = await response.json();
      setState(result);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Daemon not running");
      setLoading(false);
    }
  };

  const handleAction = async (issueIndex: number, action: "dismiss" | "false_positive" | "resolve", note?: string) => {
    setActionLoading(issueIndex);
    try {
      const response = await fetch(`${DAEMON_URL}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          issue_index: issueIndex,
          action,
          note: note || ""
        })
      });

      if (!response.ok) {
        throw new Error("Failed to submit feedback");
      }

      // Refresh state after action
      await fetchState();
    } catch (err) {
      console.error("Action failed:", err);
      alert(`Failed to ${action} issue`);
    } finally {
      setActionLoading(null);
    }
  };

  const handleClearAll = async () => {
    if (!confirm("Clear all issues? This cannot be undone.")) return;

    try {
      const response = await fetch(`${DAEMON_URL}/issues/clear`, {
        method: "POST"
      });

      if (!response.ok) {
        throw new Error("Failed to clear issues");
      }

      await fetchState();
    } catch (err) {
      console.error("Clear failed:", err);
      alert("Failed to clear issues");
    }
  };

  const recalculateScore = async () => {
    try {
      const response = await fetch(`${DAEMON_URL}/state/recalculate`, {
        method: "POST"
      });

      if (!response.ok) {
        throw new Error("Failed to recalculate score");
      }

      // Refresh state to get updated score
      await fetchState();
    } catch (err) {
      console.error("Recalculate failed:", err);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchState();

    // Set up real-time polling every 5 seconds
    const stateInterval = setInterval(fetchState, 5000);

    // Set up security score recalculation every 10 seconds
    const recalcInterval = setInterval(recalculateScore, 10000);

    return () => {
      clearInterval(stateInterval);
      clearInterval(recalcInterval);
    };
  }, []);

  if (loading) {
    return (
      <div className={styles.page}>
        <main className={styles.main}>
          <div className={styles.header}>
            <h1 className={styles.title}>Vibe Assist</h1>
            <p className={styles.subtitle}>Real-time Code Security Monitor</p>
          </div>
          <div className={styles.loader}>Loading...</div>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.page}>
        <main className={styles.main}>
          <div className={styles.header}>
            <h1 className={styles.title}>Vibe Assist</h1>
            <p className={styles.subtitle}>Real-time Code Security Monitor</p>
          </div>
          <div className={styles.error}>
            <h2>Error</h2>
            <p>{error}</p>
            <p className={styles.errorHint}>Make sure the daemon is running on port 8000</p>
          </div>
        </main>
      </div>
    );
  }

  const charterItems = state?.project_charter?.charter_items || [];
  const completedCharter = charterItems.filter(item => item.completed).length;
  const totalCharter = charterItems.length;
  const dismissedCount = state?.user_feedback?.dismissed_issues?.length || 0;
  const fpCount = state?.user_feedback?.false_positives?.length || 0;

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <div className={styles.header}>
          <h1 className={styles.title}>Vibe Assist</h1>
          <p className={styles.subtitle}>Your Context, Always in Sync</p>
        </div>

        {/* Status Banner */}
        <div className={styles.statusBanner}>
          <div className={styles.statusIcon}>✓</div>
          <div className={styles.statusContent}>
            <h3 className={styles.statusTitle}>Context is Up to Date</h3>
            <p className={styles.statusDescription}>
              Working across multiple contributors, LLMs, and IDEs? We've got you covered.
              VibeAssist tracks your changes, organizes context, and identifies conflicts—so you can make informed decisions.
            </p>
          </div>
        </div>

        <div className={styles.dashboard}>
          {/* Security Score Card */}
          <div className={styles.scoreCard}>
            <div className={styles.scoreValue}>
              {state?.security_score || 0}
            </div>
            <div className={styles.scoreLabel}>Security Score</div>
            <div className={styles.scoreBar}>
              <div
                className={styles.scoreBarFill}
                style={{ width: `${state?.security_score || 0}%` }}
              />
            </div>
          </div>

          {/* Stats Cards */}
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{state?.active_issues.length || 0}</div>
              <div className={styles.statLabel}>Active Issues</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{dismissedCount}</div>
              <div className={styles.statLabel}>Dismissed</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{fpCount}</div>
              <div className={styles.statLabel}>False Positives</div>
            </div>
            {totalCharter > 0 && (
              <div className={styles.statCard}>
                <div className={styles.statValue}>{completedCharter}/{totalCharter}</div>
                <div className={styles.statLabel}>Charter Progress</div>
              </div>
            )}
          </div>

          {/* Issues List */}
          <div className={styles.issuesSection}>
            <div className={styles.issuesHeader}>
              <h2>Potential Conflicts & Issues</h2>
              {state && state.active_issues.length > 0 && (
                <button
                  className={styles.clearAllBtn}
                  onClick={handleClearAll}
                >
                  Clear All
                </button>
              )}
            </div>

            {state?.active_issues.length === 0 ? (
              <div className={styles.noIssues}>
                <div className={styles.successIcon}>✓</div>
                <p>No conflicts or issues detected</p>
                <p className={styles.valueMessage}>
                  🎯 Your codebase context is clean and ready to share with any LLM or team member
                </p>
              </div>
            ) : (
              <div className={styles.issuesList}>
                {state?.active_issues.map((issue, index) => (
                  <div key={index} className={styles.issueCard}>
                    <div className={styles.issueHeader}>
                      <span className={`${styles.severityBadge} ${styles[issue.severity.toLowerCase()]}`}>
                        {issue.severity}
                      </span>
                      <span className={styles.issueType}>{issue.type}</span>
                      {issue.priority_score && (
                        <span className={styles.priorityBadge}>P{issue.priority_score}</span>
                      )}
                    </div>
                    <p className={styles.issueDescription}>{issue.description}</p>
                    {issue.file_path && (
                      <div className={styles.issueLocation}>
                        📄 {issue.file_path}
                        {issue.line_number && `:${issue.line_number}`}
                      </div>
                    )}
                    <div className={styles.issueActions}>
                      <button
                        className={`${styles.actionBtn} ${styles.resolveBtn}`}
                        onClick={() => handleAction(index, "resolve")}
                        disabled={actionLoading === index}
                      >
                        {actionLoading === index ? "..." : "✓ Resolve"}
                      </button>
                      <button
                        className={`${styles.actionBtn} ${styles.dismissBtn}`}
                        onClick={() => handleAction(index, "dismiss")}
                        disabled={actionLoading === index}
                      >
                        {actionLoading === index ? "..." : "✕ Dismiss"}
                      </button>
                      <button
                        className={`${styles.actionBtn} ${styles.fpBtn}`}
                        onClick={() => handleAction(index, "false_positive")}
                        disabled={actionLoading === index}
                      >
                        {actionLoading === index ? "..." : "⚠ False Positive"}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Value Proposition Footer */}
          <div className={styles.valueProposition}>
            <h3>Why VibeAssist?</h3>
            <p>
              <strong>Lost context is the #1 pain point</strong> when coding with multiple contributors, LLMs, and IDEs.
              VibeAssist reviews your changes and keeps everything organized in a centralized location,
              so you can make informed decisions about how to continue—without constantly re-explaining yourself.
            </p>
          </div>

          <div className={styles.footer}>
            <div className={styles.autoRefresh}>
              <div className={styles.pulse}></div>
              <span>Context synced • Auto-refreshing every 5s</span>
            </div>
            {state?.last_analyzed_commit && (
              <div className={styles.commitInfo}>
                Last analyzed: {state.last_analyzed_commit.substring(0, 8)}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
