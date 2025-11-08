# VibeAssist Widget Setup Guide

## Overview
This widget fetches content from your Next.js/React backend and displays it on the iOS/iPadOS Home Screen.

## Steps to Set Up

### 1. Add Widget Extension to Your Xcode Project

1. In Xcode, go to **File > New > Target**
2. Search for and select **Widget Extension**
3. Name it "VibeAssistWidget"
4. Uncheck "Include Configuration Intent" (unless you want user-configurable options)
5. Click **Finish**

### 2. Replace the Generated Widget Code

1. Delete the auto-generated widget files in the WidgetExtension folder
2. Add the `VibeAssistWidget.swift` file to your Widget Extension target
3. Make sure it's checked in the Target Membership

### 3. Configure Your API Endpoint

In `VibeAssistWidget.swift`, update this line with your actual Next.js API URL:

```swift
private let apiURL = "https://your-nextjs-app.vercel.app/api/widget-data"
```

### 4. Set Up Your Next.js API

Create an API route in your Next.js project that returns JSON in this format:

```json
{
  "title": "Your Title",
  "message": "Your message content",
  "timestamp": "2025-11-08T12:00:00Z"
}
```

See `nextjs-api-example.js` for a complete example.

### 5. Update App Transport Security (if using HTTP for testing)

If you're testing with a local server or non-HTTPS URL, add this to your `Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

**Note:** For production, always use HTTPS.

### 6. Build and Run

1. Select your app scheme in Xcode
2. Build and run on a device or simulator
3. Long-press on the Home Screen
4. Tap the "+" button in the top corner
5. Search for "Vibe Assist"
6. Add the widget to your Home Screen

## Customization Options

### Change Update Frequency

In `getTimeline()`, modify the update interval:

```swift
// Update every 15 minutes (default)
let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: currentDate)!

// Or update hourly
let nextUpdate = Calendar.current.date(byAdding: .hour, value: 1, to: currentDate)!
```

### Add More Widget Sizes

Update the `supportedFamilies` array:

```swift
.supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
```

### Customize the Data Model

Modify the `WidgetContent` struct to match your API response:

```swift
struct WidgetContent: Codable {
    let title: String
    let message: String
    let timestamp: Date?
    let imageUrl: String?  // Add new fields
    let count: Int?        // as needed
}
```

### Style the Widget View

Edit the `VibeAssistWidgetView` to change colors, fonts, and layout.

## Troubleshooting

### Widget shows "Unable to load content"

1. Check that your API URL is correct
2. Verify your API returns valid JSON
3. Check network connectivity
4. Look at the Xcode console for error messages

### Widget doesn't update

- Widgets update on Apple's schedule, not immediately
- You can force a refresh by removing and re-adding the widget
- Check the Timeline policy in `getTimeline()`

### CORS errors (if testing from browser)

Add CORS headers to your Next.js API (already included in the example).

## Production Considerations

1. **Use HTTPS** - Required for production apps
2. **Handle errors gracefully** - Show useful fallback content
3. **Optimize image sizes** - If showing images, keep them small
4. **Respect privacy** - Don't send sensitive data
5. **Test on device** - Simulator doesn't perfectly replicate widget behavior
6. **Background refresh** - Ensure your app has appropriate background modes if needed

## Next Steps

- Add authentication to your API if needed
- Implement deep linking to open your app from the widget
- Add multiple widget configurations
- Create different views for different widget sizes
- Add App Intents for interactive widgets

Enjoy your VibeAssist widget! 🎉
