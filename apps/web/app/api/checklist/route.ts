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

export async function GET(req: NextRequest) {
  // Replace this with your actual data source (database, etc.)
  const checklistData: ChecklistResponse = {
    items: [
      { id: "1", title: "Review pull requests", completed: true },
      { id: "2", title: "Update documentation", completed: false },
      { id: "3", title: "Deploy to staging", completed: false },
      { id: "4", title: "Team standup meeting", completed: true },
    ],
    lastUpdated: new Date().toISOString(),
  };

  return NextResponse.json(checklistData);
}
