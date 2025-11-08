//
//  ContentView.swift
//  VibeAssist
//
//  Created by Yves Hughes on 11/8/25.
//

import SwiftUI
import WebKit

class WebViewNavigationDelegate: NSObject, WKNavigationDelegate {
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        print("✅ WebView loaded successfully: \(webView.url?.absoluteString ?? "unknown")")
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("❌ WebView failed to load: \(error.localizedDescription)")
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        print("❌ WebView failed provisional navigation: \(error.localizedDescription)")
    }
}

struct WebView: NSViewRepresentable {
    let url: URL

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject {
        let delegate = WebViewNavigationDelegate()
    }

    func makeNSView(context: Context) -> WKWebView {
        let preferences = WKPreferences()
        let configuration = WKWebViewConfiguration()
        configuration.preferences = preferences

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.navigationDelegate = context.coordinator.delegate

        print("🌐 Loading URL: \(url.absoluteString)")
        webView.load(URLRequest(url: url))

        // Auto-refresh every 5 seconds to match the web app's polling
        Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { _ in
            webView.reload()
        }

        return webView
    }

    func updateNSView(_ nsView: WKWebView, context: Context) {
        // No need to update
    }
}

struct ContentView: View {
    @State private var webURL = "http://localhost:3000"
    @State private var showSettings = false

    var body: some View {
        VStack(spacing: 0) {
            // Top toolbar
            HStack {
                Text("Vibe Assist")
                    .font(.headline)
                    .fontWeight(.bold)

                Spacer()

                Button(action: {
                    showSettings.toggle()
                }) {
                    Image(systemName: "gear")
                }
                .buttonStyle(.plain)
            }
            .padding()
            .background(Color(NSColor.windowBackgroundColor))

            // WebView displaying the Next.js frontend
            if let url = URL(string: webURL) {
                WebView(url: url)
            } else {
                VStack(spacing: 20) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 50))
                        .foregroundColor(.red)

                    Text("Invalid URL")
                        .font(.title)

                    Text("Please check your settings")
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .sheet(isPresented: $showSettings) {
            SettingsView(webURL: $webURL)
        }
    }
}

struct SettingsView: View {
    @Binding var webURL: String
    @Environment(\.dismiss) var dismiss

    var body: some View {
        VStack(spacing: 20) {
            Text("Settings")
                .font(.title)
                .fontWeight(.bold)

            Form {
                TextField("Web App URL", text: $webURL)
                    .textFieldStyle(.roundedBorder)

                Text("Default: http://localhost:3000")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()

            HStack {
                Button("Cancel") {
                    dismiss()
                }
                .keyboardShortcut(.cancelAction)

                Button("Save") {
                    dismiss()
                }
                .keyboardShortcut(.defaultAction)
            }
        }
        .padding()
        .frame(width: 400, height: 200)
    }
}

#Preview {
    ContentView()
}
