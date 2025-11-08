# Vibe Assist macOS Widget# Checklist Widget for macOS



This directory contains the Xcode project for the Vibe Assist macOS widget. The widget is designed to display a checklist of tasks or system statuses fetched from a Next.js API endpoint.A macOS widget that displays a checklist fetched from a Next.js API endpoint.



## How to Run the Widget## Setup Instructions



### Prerequisites### 1. Next.js API Setup



1.  **Xcode:** You must have Xcode installed on your Mac. You can download it from the Mac App Store.1. Copy `api-checklist.ts` to your Next.js project:

2.  **Running Web Server:** The widget requires the Next.js development server to be running to fetch its data.   ```bash

   cp api-checklist.ts <your-nextjs-project>/pages/api/checklist.ts

### Step-by-Step Instructions   ```



1.  **Start the Web Server:**2. Start your Next.js dev server:

    Before launching the widget, you need to start the web server from the root of the `vibe-assist` project.   ```bash

    ```sh   npm run dev

    # In the root directory of the vibe-assist project   ```

    pnpm dev

    ```3. Test the API endpoint:

    This will start the Next.js server, which provides the API endpoint for the widget.   ```bash

   curl http://localhost:3000/api/checklist

2.  **Open the Xcode Project:**   ```

    Navigate to the `apps/widget/VibeAssist` directory and open the `VibeAssist.xcodeproj` file.

    ```sh### 2. macOS Widget Setup

    # You can open the project from the terminal

    open apps/widget/VibeAssist/VibeAssist.xcodeproj1. Open Xcode

    ```2. Create a new project: **File > New > Project**

3. Select **Widget Extension** under macOS

3.  **Select the Correct Target:**4. Name it "ChecklistWidget"

    In Xcode, you need to select the correct target to run. The target is the `MacWidget` extension.5. Replace the generated widget code with the contents of `ChecklistWidget.swift`

    *   At the top of the Xcode window, next to the play and stop buttons, you'll see a dropdown menu.6. Update the API URL in `ChecklistWidget.swift` (line 52):

    *   Click on it and select **MacWidget**.   ```swift

   guard let url = URL(string: "YOUR_API_URL_HERE") else {

4.  **Build and Run:**   ```

    With the `MacWidget` target selected, you can now build and run the project.

    *   Click the **play button** or press **⌘R**.### 3. Build and Run



5.  **Add the Widget to Your Mac:**1. In Xcode, select your Mac as the target

    *   Once the project is running, click the **date and time** in your Mac's menu bar to open the Notification Center.2. Build and run (⌘R)

    *   Scroll down and click **Edit Widgets**.3. Add the widget to your notification center:

    *   Find the **VibeAssist** widget in the list and add it to your screen.   - Click the date/time in menu bar

   - Scroll down and click "Edit Widgets"

You should now see the widget running on your Mac, displaying the checklist data from your local web server.   - Find "ChecklistWidget" and add it


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
