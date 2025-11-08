# Checklist Widget for macOS

A macOS widget that displays a checklist fetched from a Next.js API endpoint.

## Setup Instructions

### 1. Next.js API Setup

1. Copy `api-checklist.ts` to your Next.js project:
   ```bash
   cp api-checklist.ts <your-nextjs-project>/pages/api/checklist.ts
   ```

2. Start your Next.js dev server:
   ```bash
   npm run dev
   ```

3. Test the API endpoint:
   ```bash
   curl http://localhost:3000/api/checklist
   ```

### 2. macOS Widget Setup

1. Open Xcode
2. Create a new project: **File > New > Project**
3. Select **Widget Extension** under macOS
4. Name it "ChecklistWidget"
5. Replace the generated widget code with the contents of `ChecklistWidget.swift`
6. Update the API URL in `ChecklistWidget.swift` (line 52):
   ```swift
   guard let url = URL(string: "YOUR_API_URL_HERE") else {
   ```

### 3. Build and Run

1. In Xcode, select your Mac as the target
2. Build and run (⌘R)
3. Add the widget to your notification center:
   - Click the date/time in menu bar
   - Scroll down and click "Edit Widgets"
   - Find "ChecklistWidget" and add it

## Customization

### Update Checklist Data

Modify the `items` array in `api-checklist.ts` or connect it to your database/data source.

### Styling

Adjust colors, fonts, and spacing in the `ChecklistWidgetView` in `ChecklistWidget.swift`.

### Refresh Rate

Default is 15 minutes. Change in `getTimeline()` function:
```swift
let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: Date())!
```

## Notes

- For production, replace `localhost:3000` with your deployed Next.js URL
- You may need to configure App Transport Security in Info.plist for HTTP connections
- The widget supports small, medium, and large sizes
