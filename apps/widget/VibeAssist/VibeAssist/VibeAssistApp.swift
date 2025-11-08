//
//  VibeAssistApp.swift
//  VibeAssist
//
//  Created by Yves Hughes on 11/8/25.
//

import SwiftUI

@main
struct VibeAssistApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        
        // Menu bar widget launcher with custom icon
        MenuBarExtra {
            Button("Open Widget Center") {
                openWidgetCenter()
            }
            .keyboardShortcut("w", modifiers: [.command, .shift])
            
            Divider()
            
            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q", modifiers: .command)
        } label: {
            // Use your custom image from Assets
            Image("MenuBarIcon")
                .renderingMode(.template) // This makes it adapt to light/dark mode
        }
    }
    
    private func openWidgetCenter() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.Widgets-Settings.extension") {
            NSWorkspace.shared.open(url)
        }
    }
}
