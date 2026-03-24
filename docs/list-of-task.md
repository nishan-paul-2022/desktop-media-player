# Modular Implementation Prompts (Desktop Media Player)

This document contains a series of highly structured, interlinked prompts designed for an AI to implement the project in modular steps. Each prompt follows industry standards, clean code conventions, and high-performance patterns.

Use each prompt with explicit acceptance checks. Do not advance to the next prompt until the current prompt passes its own checks.

Mandatory baseline for all prompts: follow [Engineering Standards Charter](engineering-standards.md).

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
    *   Treat Docker as optional for GUI development; provide native host run steps as the default fallback path.
5.  **Project Structure:** Organize the project into:
    *   `/src-tauri`: Rust backend.
    *   `/src`: React frontend.
    *   `/docs`: Architecture and tasks.

### ✅ Acceptance Checklist
- [ ] Frontend starts locally with a single documented command.
- [ ] Tauri dev mode starts locally with a single documented command.
- [ ] Tailwind v4 styles are confirmed from the main stylesheet (CSS-first flow).
- [ ] No legacy config-only Tailwind setup is required for styling to work.
- [ ] Setup docs include both native workflow and optional Docker workflow.

---

## ⚡ Prompt 2: Native Media Engine Bridge (Rust + libmpv)
**Goal:** Implement the Rust backend bridge to `libmpv` and expose commands to the frontend.

### 📝 Instructions:
1.  **libmpv Integration:** Add the `libmpv` dependency to `src-tauri/Cargo.toml`.
2.  **Modular Backend:**
    *   Create a `player_engine.rs` module that initializes and manages the `mpv_handle`.
    *   Implement an asynchronous event loop in Rust that listens to mpv events (property changes, logs) and broadcasts them to the Tauri frontend via `app.emit()`.
    *   Use a command queue or single-writer pattern so all mpv mutations occur on one controlled path.
3.  **Tauri Commands:**
    *   Implement `load_video(path)`, `toggle_pause()`, `seek(seconds)`, and `set_volume(level)` commands.
    *   Ensure thread-safety using `Arc<Mutex<Player>>` or a channel-driven worker model.
    *   Validate inputs and return structured errors for invalid paths, seek out-of-range, and unavailable engine state.
4.  **Error Handling:** Use a custom `Result` type with structured errors for playback failures.

### ✅ Acceptance Checklist
- [ ] All commands return without blocking UI interactions.
- [ ] Command failures return typed/structured errors.
- [ ] Engine emits pause, position, duration, track-change, and playback-end events.
- [ ] Repeated rapid seek input does not deadlock backend worker paths.
- [ ] Repeated rapid seek input does not crash process or corrupt playback state.

---

## 💎 Prompt 3: Premium Glassmorphism UI System
**Goal:** Design a "WOW" factor, moderately dark, glassmorphic UI using Tailwind CSS v4 and Framer Motion.

### 📝 Instructions:
1.  **Design System:**
    *   Define a dark, premium color palette in `tailwind.css` (or main global stylesheet) using CSS variables (Base: `#0f172a`, Glass: `rgba(255, 255, 255, 0.05)`).
    *   Implement a global "Glassmorphism" utility class with `backdrop-filter: blur(20px)`.
2.  **Layout Components:**
    *   **VideoSurface:** A full-screen container for the video output.
    *   **ControlsContainer:** A floating, bottom-aligned bar that appears on mouse move and hides after 3s of inactivity.
    *   **Sidebar:** A retractable playlist/settings sidebar with a semi-transparent blur effect.
3.  **Animations:**
    *   Use **Framer Motion** for smooth transitions: control bar sliding in/out, volume slider expansion, and play/pause icon morphing.

### ✅ Acceptance Checklist
- [ ] Core controls are reachable and usable via keyboard-only navigation.
- [ ] Visible focus states are present for interactive controls.
- [ ] UI animation remains smooth on reference hardware.
- [ ] Animations do not cause visible playback stutter.
- [ ] Controls remain usable on desktop and narrow window widths.

---

## 🎮 Prompt 4: Real-Time Playback Logic & Event Bus
**Goal:** Connect the React UI to the Rust backend using a robust event system.

### 📝 Instructions:
1.  **React Hook (`usePlayer`):**
    *   Create a custom hook that manages playback state (currentTime, duration, isPaused, volume).
    *   Subscribe to Tauri events emitted from Prompt 2 to keep the UI in sync with the `libmpv` state.
    *   Define event payload types and one canonical mapping layer from backend event names to frontend state updates.
2.  **Interaction Logic:**
    *   Implement a high-performance timeline slider that allows smooth scrubbing without lag.
    *   Add keyboard shortcuts (Space for Pause, Arrows for Seeking, M for Mute).
    *   Throttle high-frequency updates (for example, timeline position events) to avoid unnecessary re-renders.
3.  **Responsive Video Surface:**
    *   Ensure the video expands to fill the window while maintaining aspect ratio, using Tauri's native window resizing events.

### ✅ Acceptance Checklist
- [ ] Continuous playback for 10 minutes shows no noticeable UI-state drift.
- [ ] Timeline drag/scrub remains smooth while playback is active.
- [ ] Keyboard shortcuts work for media controls.
- [ ] Shortcut handling does not trigger while typing in text fields.
- [ ] Event throttling keeps render frequency stable under position-update load.

---

## 🚀 Prompt 5: Advanced Media Features & Optimizations
**Goal:** Implement pro-level features like Hardware Acceleration, Subtitles, and GPU filters.

### 📝 Instructions:
1.  **Hardware Acceleration:**
    *   Configure `libmpv` in the Rust backend to prefer GPU hardware decoding (VA-API, NVENC, or DXVA2).
    *   Add graceful fallback to software decoding with user-visible status.
2.  **Subtitle Service:**
    *   Implement a subtitle track selector that reads embedded tracks via `libmpv`.
    *   Add support for external `.srt` and `.vtt` file loading via drag-and-drop.
3.  **Performance Tuning:**
    *   Optimize the UI render cycle to keep playback smooth and avoid dropped frames caused by UI work.
    *   Implement a "Picture-in-Picture" (PiP) mode using Tauri's multi-window capabilities.

### ✅ Acceptance Checklist
- [ ] Embedded subtitle tracks can be switched during playback without restart.
- [ ] External `.srt` and `.vtt` files can be loaded and switched during playback.
- [ ] Hardware decode is attempted first when supported.
- [ ] Software decode fallback activates cleanly when hardware decode is unavailable.
- [ ] PiP window open/control/close cycle leaves no orphaned state.

---

## 📦 Prompt 6: Production Build & Cross-Platform Packaging
**Goal:** Finalize the project for distribution across Windows, macOS, and Linux.

### 📝 Instructions:
1.  **Asset Management:** Ensure all icons and fonts are optimized and bundled.
2.  **Tauri Bundle Config:**
    *   Set up icons for all platforms.
    *   Configure Tauri v2 capability/permission files for security with least privilege.
3.  **Build Workflow:**
    *   Create a GitHub Action (CI/CD) that builds the binary for all three platforms.
    *   Implement a final optimization pass for the binary size and memory footprint.

### ✅ Acceptance Checklist
- [ ] CI creates release artifacts for Linux, Windows, and macOS.
- [ ] CI can be triggered via tagged release or manual dispatch.
- [ ] Tauri v2 capability/permission files are explicit and least-privilege.
- [ ] No broad file/system permissions are granted unless justified and documented.
- [ ] Release process includes signing/notarization strategy per platform.
- [ ] Release process includes a smoke-test script for install and first-run validation.

---

## How to use prompt

```
Prompt @number from @list-of-task.md, strictly following @engineering-standards.md, and do not proceed until all Acceptance Checklist items for Prompt @number are satisfied.
```
