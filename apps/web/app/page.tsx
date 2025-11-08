"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

interface ChecklistItem {
  id: string;
  title: string;
  completed: boolean;
}

interface ChecklistResponse {
  items: ChecklistItem[];
  lastUpdated: string;
}

export default function Home() {
  const [data, setData] = useState<ChecklistResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setError(null);
      const response = await fetch("/api/checklist");

      if (!response.ok) {
        throw new Error("Failed to fetch checklist data");
      }

      const result: ChecklistResponse = await response.json();
      setData(result);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchData();

    // Set up real-time polling every 5 seconds
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
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
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <div className={styles.header}>
          <h1 className={styles.title}>Vibe Assist</h1>
          <p className={styles.subtitle}>Real-time Code Security Monitor</p>
        </div>

        <div className={styles.dashboard}>
          <div className={styles.statusCard}>
            <div className={styles.statusHeader}>
              <h2>System Status</h2>
              <span className={styles.lastUpdated}>
                Last updated: {data ? new Date(data.lastUpdated).toLocaleTimeString() : "N/A"}
              </span>
            </div>

            <div className={styles.checklist}>
              {data?.items.map((item) => (
                <div
                  key={item.id}
                  className={`${styles.checklistItem} ${item.completed ? styles.completed : styles.pending}`}
                >
                  <div className={styles.checkmark}>
                    {item.completed ? "✓" : "○"}
                  </div>
                  <div className={styles.itemContent}>
                    <span className={styles.itemTitle}>{item.title}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.footer}>
            <div className={styles.autoRefresh}>
              <div className={styles.pulse}></div>
              <span>Auto-refreshing every 5 seconds</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
