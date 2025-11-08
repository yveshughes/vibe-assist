//
//  MacWidget.swift
//  MacWidget
//
//  Created by Yves Hughes on 11/8/25.
//

import WidgetKit
import SwiftUI

struct Provider: AppIntentTimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), configuration: ConfigurationAppIntent())
    }

    func snapshot(for configuration: ConfigurationAppIntent, in context: Context) async -> SimpleEntry {
        SimpleEntry(date: Date(), configuration: configuration)
    }
    
    func timeline(for configuration: ConfigurationAppIntent, in context: Context) async -> Timeline<SimpleEntry> {
        var entries: [SimpleEntry] = []

        // Generate a timeline consisting of five entries an hour apart, starting from the current date.
        let currentDate = Date()
        for hourOffset in 0 ..< 5 {
            let entryDate = Calendar.current.date(byAdding: .hour, value: hourOffset, to: currentDate)!
            let entry = SimpleEntry(date: entryDate, configuration: configuration)
            entries.append(entry)
        }

        return Timeline(entries: entries, policy: .atEnd)
    }

//    func relevances() async -> WidgetRelevances<ConfigurationAppIntent> {
//        // Generate a list containing the contexts this widget is relevant in.
//    }
}

struct SimpleEntry: TimelineEntry {
    let date: Date
    let configuration: ConfigurationAppIntent
}

struct MacWidgetEntryView : View {
    var entry: Provider.Entry
    @Environment(\.widgetRenderingMode) var renderingMode

    var body: some View {
        GlassEffectContainer(spacing: 20.0) {
            VStack(spacing: 16) {
                VStack(spacing: 4) {
                    Text("Time:")
                        .font(.caption)
                        .widgetAccentable()
                    Text(entry.date, style: .time)
                        .font(.title2)
                        .fontWeight(.semibold)
                }
                .padding()
                .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 12))
                
                VStack(spacing: 4) {
                    Text("Favorite Emoji:")
                        .font(.caption)
                        .widgetAccentable()
                    Text(entry.configuration.favoriteEmoji)
                        .font(.largeTitle)
                }
                .padding()
                .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 12))
            }
            .padding()
        }
    }
}

struct MacWidget: Widget {
    let kind: String = "MacWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: kind, intent: ConfigurationAppIntent.self, provider: Provider()) { entry in
            MacWidgetEntryView(entry: entry)
                .containerBackground(for: .widget) {
                    // Use a subtle, semi-transparent background
                    Color.clear
                }
        }
        .containerBackgroundRemovable(true) // Allow background to be removed for Liquid Glass effect
    }
}
