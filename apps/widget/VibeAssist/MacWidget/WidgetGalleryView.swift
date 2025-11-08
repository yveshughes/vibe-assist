//
//  WidgetGalleryView.swift
//  VibeAssist
//
//  Created by Yves Hughes on 11/8/25.
//

import SwiftUI

struct WidgetGalleryView: View {
    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Header
                VStack(spacing: 8) {
                    Image(systemName: "square.grid.2x2.fill")
                        .font(.system(size: 60))
                        .foregroundStyle(.tint)
                    
                    Text("VibeAssist Widgets")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Text("Add these widgets to your desktop for quick access")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                .padding(.top, 40)
                
                // Widget Cards
                VStack(spacing: 16) {
                    WidgetCard(
                        title: "MacWidget",
                        description: "Shows the current time and your favorite emoji with beautiful Liquid Glass design",
                        icon: "clock.fill",
                        color: .blue
                    )
                    
                    WidgetCard(
                        title: "MacWidget Control",
                        description: "Control Center widget for quick timer access",
                        icon: "timer",
                        color: .orange
                    )
                    
                    // Uncomment when VibeAssistWidget is ready
                    // WidgetCard(
                    //     title: "VibeAssist Widget",
                    //     description: "Your main VibeAssist widget",
                    //     icon: "waveform",
                    //     color: .purple
                    // )
                }
                .padding(.horizontal, 40)
                
                // Action Button
                Button {
                    openWidgetCenter()
                } label: {
                    Label("Open Widget Center", systemImage: "plus.square.fill")
                        .font(.headline)
                        .foregroundStyle(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(.tint)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                .buttonStyle(.plain)
                .padding(.horizontal, 40)
                .padding(.top, 8)
                
                // Instructions
                VStack(alignment: .leading, spacing: 12) {
                    Text("How to Add Widgets")
                        .font(.headline)
                        .padding(.bottom, 4)
                    
                    InstructionRow(
                        number: 1,
                        text: "Click 'Open Widget Center' above or press ⌘⇧W"
                    )
                    
                    InstructionRow(
                        number: 2,
                        text: "Find 'VibeAssist' in the widget list"
                    )
                    
                    InstructionRow(
                        number: 3,
                        text: "Drag your favorite widget to your desktop"
                    )
                    
                    InstructionRow(
                        number: 4,
                        text: "Enjoy the beautiful Liquid Glass design!"
                    )
                }
                .padding(20)
                .background(Color(.textBackgroundColor).opacity(0.5))
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .padding(.horizontal, 40)
                .padding(.top, 16)
                
                Spacer(minLength: 40)
            }
        }
        .frame(minWidth: 600, minHeight: 700)
    }
    
    private func openWidgetCenter() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.Widgets-Settings.extension") {
            NSWorkspace.shared.open(url)
        }
    }
}

struct WidgetCard: View {
    let title: String
    let description: String
    let icon: String
    let color: Color
    
    var body: some View {
        HStack(spacing: 16) {
            // Icon
            ZStack {
                Circle()
                    .fill(color.gradient)
                    .frame(width: 60, height: 60)
                
                Image(systemName: icon)
                    .font(.system(size: 28))
                    .foregroundStyle(.white)
            }
            
            // Content
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                
                Text(description)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }
            
            Spacer()
        }
        .padding()
        .background(Color(.controlBackgroundColor))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color(.separatorColor), lineWidth: 0.5)
        )
    }
}

struct InstructionRow: View {
    let number: Int
    let text: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text("\(number)")
                .font(.headline)
                .foregroundStyle(.white)
                .frame(width: 28, height: 28)
                .background(Circle().fill(.tint))
            
            Text(text)
                .font(.subheadline)
            
            Spacer()
        }
    }
}

#Preview {
    WidgetGalleryView()
}
