//
//  MacWidget.swift
//  MacWidget
//
//  Created by Yves Hughes on 11/8/25.
//

import WidgetKit
import SwiftUI

// MARK: - Data Models
struct ChecklistItem: Codable, Identifiable {
    let id: String
    let title: String
    let completed: Bool
}

struct ChecklistResponse: Codable {
    let items: [ChecklistItem]
    let lastUpdated: String
}

// MARK: - Timeline Provider
struct Provider: AppIntentTimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(
            date: Date(),
            configuration: ConfigurationAppIntent(),
            checklistData: ChecklistResponse(
                items: [
                    ChecklistItem(id: "1", title: "Loading...", completed: false)
                ],
                lastUpdated: Date().ISO8601Format()
            )
        )
    }

    func snapshot(for configuration: ConfigurationAppIntent, in context: Context) async -> SimpleEntry {
        if context.isPreview {
            return SimpleEntry(
                date: Date(),
                configuration: configuration,
                checklistData: ChecklistResponse(
                    items: [
                        ChecklistItem(id: "1", title: "Security Score: 100/100", completed: true),
                        ChecklistItem(id: "2", title: "✅ No security issues detected", completed: true)
                    ],
                    lastUpdated: Date().ISO8601Format()
                )
            )
        }

        let data = await fetchChecklistData()
        return SimpleEntry(date: Date(), configuration: configuration, checklistData: data)
    }

    func timeline(for configuration: ConfigurationAppIntent, in context: Context) async -> Timeline<SimpleEntry> {
        let currentDate = Date()
        let data = await fetchChecklistData()
        let entry = SimpleEntry(date: currentDate, configuration: configuration, checklistData: data)

        // Refresh every 5 minutes (300 seconds)
        let nextUpdate = Calendar.current.date(byAdding: .minute, value: 5, to: currentDate)!

        return Timeline(entries: [entry], policy: .after(nextUpdate))
    }

    // MARK: - API Fetch
    private func fetchChecklistData() async -> ChecklistResponse {
        // Default fallback data
        let fallbackData = ChecklistResponse(
            items: [
                ChecklistItem(id: "error", title: "⚠️ Unable to connect to Vibe Assist", completed: false)
            ],
            lastUpdated: Date().ISO8601Format()
        )

        guard let url = URL(string: "http://localhost:3000/api/checklist") else {
            return fallbackData
        }

        do {
            let (data, response) = try await URLSession.shared.data(from: url)

            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return fallbackData
            }

            let decoder = JSONDecoder()
            let checklistData = try decoder.decode(ChecklistResponse.self, from: data)
            return checklistData
        } catch {
            print("Error fetching checklist data: \(error)")
            return fallbackData
        }
    }
}

// MARK: - Timeline Entry
struct SimpleEntry: TimelineEntry {
    let date: Date
    let configuration: ConfigurationAppIntent
    let checklistData: ChecklistResponse
}

// MARK: - Widget View
struct MacWidgetEntryView: View {
    var entry: Provider.Entry
    @Environment(\.widgetRenderingMode) var renderingMode

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Header
            HStack {
                Text("Vibe Assist")
                    .font(.headline)
                    .fontWeight(.bold)

                Spacer()

                Text(formatTime(entry.checklistData.lastUpdated))
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            Divider()

            // Checklist Items
            VStack(alignment: .leading, spacing: 8) {
                ForEach(entry.checklistData.items.prefix(5)) { item in
                    HStack(alignment: .top, spacing: 8) {
                        Image(systemName: item.completed ? "checkmark.circle.fill" : "circle")
                            .foregroundStyle(item.completed ? .green : .red)
                            .font(.system(size: 16))

                        Text(item.title)
                            .font(.caption)
                            .lineLimit(2)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
            }

            Spacer()
        }
        .padding()
        .containerBackground(for: .widget) {
            Color.clear
        }
    }

    private func formatTime(_ isoString: String) -> String {
        let formatter = ISO8601DateFormatter()
        if let date = formatter.date(from: isoString) {
            let timeFormatter = DateFormatter()
            timeFormatter.timeStyle = .short
            return timeFormatter.string(from: date)
        }
        return "Now"
    }
}

// MARK: - Widget Configuration
struct MacWidget: Widget {
    let kind: String = "MacWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: kind, intent: ConfigurationAppIntent.self, provider: Provider()) { entry in
            MacWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("Vibe Assist Monitor")
        .description("Real-time code security monitoring")
        .supportedFamilies([.systemMedium, .systemLarge])
        .containerBackgroundRemovable(true)
    }
}

// MARK: - Preview
#Preview(as: .systemMedium) {
    MacWidget()
} timeline: {
    SimpleEntry(
        date: .now,
        configuration: ConfigurationAppIntent(),
        checklistData: ChecklistResponse(
            items: [
                ChecklistItem(id: "1", title: "Security Score: 95/100", completed: false),
                ChecklistItem(id: "2", title: "[HIGH] Potential SQL Injection", completed: false),
                ChecklistItem(id: "3", title: "✅ All tests passing", completed: true)
            ],
            lastUpdated: Date().ISO8601Format()
        )
    )
}
