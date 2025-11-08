# Vibe Assist

Vibe Assist is a powerful tool that combines a macOS widget with a monitoring core to help you keep track of your system's key metrics. This repository contains the source code for the macOS widget, the public-facing website, and the core monitoring engine.

## Components

This project is a monorepo that includes the following components:

### 1. macOS Widget

A native macOS widget that displays a checklist of tasks or system statuses, fetched from a Next.js API endpoint.

**Features:**

-   Displays a list of items with their completion status.
-   Fetches data from a live API endpoint.
-   Customizable refresh rate.
-   Supports small, medium, and large widget sizes.

### 2. Website

The public-facing website, built with Next.js, that explains what Vibe Assist does, how it works, and how to install it. The `apps/web` directory contains the source code for the website.

### 3. Monitoring Core

The core of the application, responsible for monitoring system files and powering the app's features. This component is under development and will be located in the `packages` directory.

## Getting Started

To get started with development, you'll need to have [pnpm](https://pnpm.io/installation) and [Node.js](https://nodejs.org/) installed.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/yveshughes/vibe-assist.git
    cd vibe-assist
    ```

2.  **Install dependencies:**
    ```sh
    pnpm install
    ```

3.  **Start the development servers:**
    This will start the development servers for both the website and the API endpoint for the widget.
    ```sh
    pnpm dev
    ```

## Useful Links

-   [Turborepo Documentation](https://turborepo.org/docs)
-   [Next.js Documentation](https://nextjs.org/docs)
-   [SwiftUI Documentation](https://developer.apple.com/xcode/swiftui/)
