//
//  VibeAssistApp.swift
//  VibeAssist
//
//  Created by Yves Hughes on 11/8/25.
//

import SwiftUI

@main
struct VibeAssistApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    // Set window to always stay on top and make it transparent
                    if let window = NSApplication.shared.windows.first {
                        window.level = .floating
                        window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
                        window.isOpaque = false
                        window.backgroundColor = .clear
                        window.alphaValue = 0.85 // 85% opacity (15% transparent)
                    }
                }
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)

        // Menu bar widget launcher with custom icon
        MenuBarExtra {
            Button("Show Vibe Assist") {
                NSApplication.shared.activate(ignoringOtherApps: true)
                if let window = NSApplication.shared.windows.first {
                    window.makeKeyAndOrderFront(nil)
                }
            }
            .keyboardShortcut("v", modifiers: [.command, .shift])

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

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Ensure all windows stay on top and are transparent
        for window in NSApplication.shared.windows {
            window.level = .floating
            window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
            window.isOpaque = false
            window.backgroundColor = .clear
            window.alphaValue = 0.85 // 85% opacity (15% transparent)
        }
    }

    func applicationDidBecomeActive(_ notification: Notification) {
        // Keep window on top and transparent when app becomes active
        for window in NSApplication.shared.windows {
            window.level = .floating
            window.isOpaque = false
            window.backgroundColor = .clear
            window.alphaValue = 0.85
        }
    }
}
