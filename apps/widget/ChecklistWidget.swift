// macOS Widget using SwiftUI and WidgetKit
// File: ChecklistWidget.swift

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
struct ChecklistProvider: TimelineProvider {
    func placeholder(in context: Context) -> ChecklistEntry {
        ChecklistEntry(date: Date(), items: [
            ChecklistItem(id: "1", title: "Loading...", completed: false)
        ])
    }

    func getSnapshot(in context: Context, completion: @escaping (ChecklistEntry) -> ()) {
        let entry = ChecklistEntry(date: Date(), items: [
            ChecklistItem(id: "1", title: "Sample Task", completed: false)
        ])
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<ChecklistEntry>) -> ()) {
        fetchChecklist { items in
            let entry = ChecklistEntry(date: Date(), items: items)

            // Refresh every 15 minutes
            let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: Date())!
            let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))

            completion(timeline)
        }
    }

    private func fetchChecklist(completion: @escaping ([ChecklistItem]) -> Void) {
        // Replace with your actual Next.js API URL
        guard let url = URL(string: "http://localhost:3000/api/checklist") else {
            completion([])
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data, error == nil else {
                completion([])
                return
            }

            do {
                let response = try JSONDecoder().decode(ChecklistResponse.self, from: data)
                completion(response.items)
            } catch {
                print("Error decoding: \(error)")
                completion([])
            }
        }.resume()
    }
}

// MARK: - Timeline Entry
struct ChecklistEntry: TimelineEntry {
    let date: Date
    let items: [ChecklistItem]
}

// MARK: - Widget View
struct ChecklistWidgetView: View {
    var entry: ChecklistProvider.Entry
    @Environment(\.widgetFamily) var family

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Checklist")
                .font(.headline)
                .foregroundColor(.primary)

            ForEach(entry.items.prefix(maxItems)) { item in
                HStack(spacing: 8) {
                    Image(systemName: item.completed ? "checkmark.circle.fill" : "circle")
                        .foregroundColor(item.completed ? .green : .gray)
                        .font(.system(size: 14))

                    Text(item.title)
                        .font(.system(size: 12))
                        .foregroundColor(item.completed ? .secondary : .primary)
                        .strikethrough(item.completed)
                        .lineLimit(1)

                    Spacer()
                }
            }

            Spacer()
        }
        .padding()
        .background(Color(.windowBackgroundColor))
    }

    private var maxItems: Int {
        switch family {
        case .systemSmall:
            return 4
        case .systemMedium:
            return 6
        case .systemLarge:
            return 10
        default:
            return 5
        }
    }
}

// MARK: - Widget Configuration
@main
struct ChecklistWidget: Widget {
    let kind: String = "ChecklistWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: ChecklistProvider()) { entry in
            ChecklistWidgetView(entry: entry)
        }
        .configurationDisplayName("Checklist")
        .description("Display your daily checklist.")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}

// MARK: - Preview
struct ChecklistWidget_Previews: PreviewProvider {
    static var previews: some View {
        ChecklistWidgetView(entry: ChecklistEntry(
            date: Date(),
            items: [
                ChecklistItem(id: "1", title: "Review pull requests", completed: true),
                ChecklistItem(id: "2", title: "Update documentation", completed: false),
                ChecklistItem(id: "3", title: "Deploy to staging", completed: false),
            ]
        ))
        .previewContext(WidgetPreviewContext(family: .systemMedium))
    }
}
