//
//  VibeAssistWidget.swift
//  VibeAssist
//
//  Created by Yves Hughes on 11/8/25.
//

import WidgetKit
import SwiftUI

// MARK: - Data Model
struct WidgetContent: Codable {
    let title: String
    let message: String
    let timestamp: Date?
    
    // Add any other fields your Next.js API returns
    enum CodingKeys: String, CodingKey {
        case title
        case message
        case timestamp
    }
}

// MARK: - Timeline Entry
struct VibeAssistEntry: TimelineEntry {
    let date: Date
    let content: WidgetContent?
    let isPlaceholder: Bool
}

// MARK: - Timeline Provider
struct VibeAssistProvider: TimelineProvider {
    // The URL of your Next.js API endpoint
    // TODO: Replace this with your actual API URL
    private let apiURL = "https://your-nextjs-app.vercel.app/api/widget-data"
    
    func placeholder(in context: Context) -> VibeAssistEntry {
        VibeAssistEntry(
            date: Date(),
            content: WidgetContent(
                title: "Vibe Assist",
                message: "Loading...",
                timestamp: Date()
            ),
            isPlaceholder: true
        )
    }
    
    func getSnapshot(in context: Context, completion: @escaping (VibeAssistEntry) -> Void) {
        let entry = VibeAssistEntry(
            date: Date(),
            content: WidgetContent(
                title: "Vibe Assist",
                message: "Preview Content",
                timestamp: Date()
            ),
            isPlaceholder: false
        )
        completion(entry)
    }
    
    func getTimeline(in context: Context, completion: @escaping (Timeline<VibeAssistEntry>) -> Void) {
        Task {
            let currentDate = Date()
            
            // Fetch content from your Next.js API
            let content = await fetchContent()
            
            let entry = VibeAssistEntry(
                date: currentDate,
                content: content,
                isPlaceholder: false
            )
            
            // Refresh the widget every 15 minutes
            let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: currentDate)!
            let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
            
            completion(timeline)
        }
    }
    
    // MARK: - Network Fetch
    private func fetchContent() async -> WidgetContent? {
        guard let url = URL(string: apiURL) else {
            print("Invalid URL")
            return nil
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(from: url)
            
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                print("Invalid response")
                return nil
            }
            
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            let content = try decoder.decode(WidgetContent.self, from: data)
            return content
            
        } catch {
            print("Error fetching content: \(error)")
            return nil
        }
    }
}

// MARK: - Widget View
struct VibeAssistWidgetView: View {
    let entry: VibeAssistEntry
    
    var body: some View {
        if let content = entry.content {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image(systemName: "sparkles")
                        .font(.title2)
                        .foregroundStyle(.tint)
                    
                    Text(content.title)
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    Spacer()
                }
                
                Text(content.message)
                    .font(.body)
                    .foregroundStyle(.secondary)
                
                Spacer()
                
                if let timestamp = content.timestamp {
                    Text(timestamp, style: .relative)
                        .font(.caption2)
                        .foregroundStyle(.tertiary)
                }
            }
            .padding()
        } else {
            VStack {
                Image(systemName: "exclamationmark.triangle")
                    .font(.title)
                    .foregroundStyle(.orange)
                Text("Unable to load content")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding()
        }
    }
}

// MARK: - Widget Configuration
struct VibeAssistWidget: Widget {
    let kind: String = "VibeAssistWidget"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: VibeAssistProvider()) { entry in
            VibeAssistWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("Vibe Assist")
        .description("Stay updated with your vibe content.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

// Note: The widget bundle is defined in MacWidgetBundle.swift
// This widget will be added to that bundle

// MARK: - Preview
#Preview(as: .systemSmall) {
    VibeAssistWidget()
} timeline: {
    VibeAssistEntry(
        date: Date(),
        content: WidgetContent(
            title: "Vibe Assist",
            message: "Everything is looking great!",
            timestamp: Date()
        ),
        isPlaceholder: false
    )
    
    VibeAssistEntry(
        date: Date().addingTimeInterval(60),
        content: WidgetContent(
            title: "Vibe Assist",
            message: "New update available",
            timestamp: Date()
        ),
        isPlaceholder: false
    )
}
