import { NextRequest, NextResponse } from "next/server";

export interface ChecklistItem {
  id: string;
  title: string;
  completed: boolean;
}

export interface ChecklistResponse {
  items: ChecklistItem[];
  lastUpdated: string;
}

interface DaemonState {
  security_score: number;
  active_issues: Array<{
    type: string;
    description: string;
    severity: string;
  }>;
  project_charter: Record<string, any>;
}

export async function GET(req: NextRequest) {
  try {
    // Fetch data from Python daemon
    const daemonUrl = process.env.DAEMON_URL || "http://localhost:8000";
    const response = await fetch(`${daemonUrl}/state`, {
      cache: "no-store", // Disable caching for real-time data
    });

    if (!response.ok) {
      throw new Error("Failed to fetch from daemon");
    }

    const daemonState: DaemonState = await response.json();

    // Convert daemon state to checklist items
    const items: ChecklistItem[] = [
      {
        id: "security",
        title: `Security Score: ${daemonState.security_score}/100`,
        completed: daemonState.security_score === 100,
      },
    ];

    // Add active issues as checklist items
    daemonState.active_issues.forEach((issue, index) => {
      items.push({
        id: `issue-${index}`,
        title: `[${issue.severity}] ${issue.type}: ${issue.description.substring(0, 60)}...`,
        completed: false,
      });
    });

    // If no issues, add a success message
    if (daemonState.active_issues.length === 0 && daemonState.security_score === 100) {
      items.push({
        id: "all-clear",
        title: "✅ No security issues detected",
        completed: true,
      });
    }

    const checklistData: ChecklistResponse = {
      items,
      lastUpdated: new Date().toISOString(),
    };

    return NextResponse.json(checklistData);
  } catch (error) {
    console.error("Error fetching from daemon:", error);

    // Fallback data if daemon is not available
    const fallbackData: ChecklistResponse = {
      items: [
        { id: "1", title: "⚠️ Daemon not running", completed: false },
        { id: "2", title: "Start daemon: cd apps/daemon && python -m src.daemon", completed: false },
      ],
      lastUpdated: new Date().toISOString(),
    };

    return NextResponse.json(fallbackData);
  }
}
