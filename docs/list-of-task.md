# Modular Implementation Prompts (Desktop Media Player)

This document contains a series of highly structured, interlinked prompts designed for an AI to implement the project in modular steps. Each prompt follows industry standards, clean code conventions, and high-performance patterns.

---

## 🛠️ Prompt 1: Dockerized Foundation & Project Initialization
**Goal:** Initialize a Tauri v2 project with a Vite+React+TypeScript frontend, integrated with Tailwind CSS v4, all within a containerized development environment.

### 📝 Instructions:
1.  **Project Shell:** Use `npx create-tauri-app@latest` to initialize a Tauri v2 project named `media-player`.
2.  **Frontend Setup:** Configure Vite with React and TypeScript.
3.  **Tailwind v4 Setup:** Install and configure Tailwind CSS v4. Ensure zero-runtime overhead by following the official v4 CSS-first approach.
4.  **Dockerization:**
    *   Create a `Dockerfile.dev` that includes the necessary Rust, Node.js, and GTK/Webview dependencies for Linux development.
    *   Create a `docker-compose.yml` that mounts the source code and allows running Tauri in a way that can forward the X11/Wayland display to the host.
5.  **Project Structure:** Organize the project into:
    *   `/src-tauri`: Rust backend.
    *   `/src`: React frontend.
    *   `/docs`: Architecture and tasks.

---

## ⚡ Prompt 2: Native Media Engine Bridge (Rust + libmpv)
**Goal:** Implement the Rust backend bridge to `libmpv` and expose commands to the frontend.

### 📝 Instructions:
1.  **libmpv Integration:** Add the `libmpv` dependency to `src-tauri/Cargo.toml`.
2.  **Modular Backend:**
    *   Create a `player_engine.rs` module that initializes and manages the `mpv_handle`.
    *   Implement an asynchronous event loop in Rust that listens to mpv events (property changes, logs) and broadcasts them to the Tauri frontend via `app.emit()`.
3.  **Tauri Commands:**
    *   Implement `load_video(path)`, `toggle_pause()`, `seek(seconds)`, and `set_volume(level)` commands.
    *   Ensure thread-safety using `Arc<Mutex<Player>>` or similar patterns.
4.  **Error Handling:** Use a custom `Result` type with structured errors for playback failures.

---

## 💎 Prompt 3: Premium Glassmorphism UI System
**Goal:** Design a "WOW" factor, moderately dark, glassmorphic UI using Tailwind CSS v4 and Framer Motion.

### 📝 Instructions:
1.  **Design System:**
    *   Define a dark, premium color palette in `tailind.css` using CSS variables (Base: `#0f172a`, Glass: `rgba(255, 255, 255, 0.05)`).
    *   Implement a global "Glassmorphism" utility class with `backdrop-filter: blur(20px)`.
2.  **Layout Components:**
    *   **VideoSurface:** A full-screen container for the video output.
    *   **ControlsContainer:** A floating, bottom-aligned bar that appears on mouse move and hides after 3s of inactivity.
    *   **Sidebar:** A retractable playlist/settings sidebar with a semi-transparent blur effect.
3.  **Animations:**
    *   Use **Framer Motion** for smooth transitions: control bar sliding in/out, volume slider expansion, and play/pause icon morphing.

---

## 🎮 Prompt 4: Real-Time Playback Logic & Event Bus
**Goal:** Connect the React UI to the Rust backend using a robust event system.

### 📝 Instructions:
1.  **React Hook (`usePlayer`):**
    *   Create a custom hook that manages playback state (currentTime, duration, isPaused, volume).
    *   Subscribe to Tauri events emitted from Prompt 2 to keep the UI in sync with the `libmpv` state.
2.  **Interaction Logic:**
    *   Implement a high-performance timeline slider that allows smooth scrubbing without lag.
    *   Add keyboard shortcuts (Space for Pause, Arrows for Seeking, M for Mute).
3.  **Responsive Video Surface:**
    *   Ensure the video expands to fill the window while maintaining aspect ratio, using Tauri's native window resizing events.

---

## 🚀 Prompt 5: Advanced Media Features & Optimizations
**Goal:** Implement pro-level features like Hardware Acceleration, Subtitles, and GPU filters.

### 📝 Instructions:
1.  **Hardware Acceleration:**
    *   Configure `libmpv` in the Rust backend to prefer GPU hardware decoding (VA-API, NVENC, or DXVA2).
2.  **Subtitle Service:**
    *   Implement a subtitle track selector that reads embedded tracks via `libmpv`.
    *   Add support for external `.srt` and `.vtt` file loading via drag-and-drop.
3.  **Performance Tuning:**
    *   Optimize the UI render cycle to ensure zero impact on video playback FPS.
    *   Implement a "Picture-in-Picture" (PiP) mode using Tauri's multi-window capabilities.

---

## 📦 Prompt 6: Production Build & Cross-Platform Packaging
**Goal:** Finalize the project for distribution across Windows, macOS, and Linux.

### 📝 Instructions:
1.  **Asset Management:** Ensure all icons and fonts are optimized and bundled.
2.  **Tauri Bundle Config:**
    *   Set up icons for all platforms.
    *   Configure `allowlist` for security.
3.  **Build Workflow:**
    *   Create a GitHub Action (CI/CD) that builds the binary for all three platforms.
    *   Implement a final optimization pass for the binary size and memory footprint.
