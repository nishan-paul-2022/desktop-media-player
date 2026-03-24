# Engineering Standards Charter (Desktop Media Player)

This document defines mandatory engineering standards for architecture, design patterns, naming, code conventions, and delivery quality.

## 1) Scope And Priority
- These standards apply to all backend, frontend, infrastructure, and documentation changes.
- If a prompt conflicts with this file, this file wins unless an approved Architecture Decision Record (ADR) says otherwise.

## 2) System Design Principles
- Keep clear boundaries: UI -> command boundary -> engine service -> libmpv.
- Use event-driven synchronization between backend and frontend.
- Use least-privilege permissions for Tauri v2 capabilities.
- Prefer measurable reliability and performance goals over subjective claims.
- Design for graceful degradation (for example, GPU decode fallback to software decode).

## 3) Required Design Patterns
- Backend command execution: single-writer command queue (or equivalent) for mpv mutations.
- Error handling: typed domain errors with stable error codes and user-safe messages.
- Frontend state: unidirectional state updates via canonical event mapping.
- Side effects: isolate IO boundaries (filesystem, window API, mpv calls) from pure state logic.
- Observability: structured logs with event name, severity, timestamp, and correlation id where possible.

## 4) Naming Conventions
### 4.1 File And Directory Naming
- Frontend components: PascalCase (example: VideoSurface.tsx).
- Frontend hooks/utilities: camelCase with prefixes where relevant (example: usePlayer.ts, formatTime.ts).
- Rust modules/files: snake_case (example: player_engine.rs, event_bus.rs).
- Test files:
  - Frontend: <name>.test.ts or <name>.test.tsx
  - Rust: module-level tests in mod tests or tests/<name>.rs
- Docs: kebab-case markdown filenames (example: engineering-standards.md).

### 4.2 Code Symbol Naming
- TypeScript:
  - Types/interfaces/enums/classes: PascalCase
  - Variables/functions/methods: camelCase
  - Constants: UPPER_SNAKE_CASE only for true constants
- Rust:
  - Modules/functions/variables: snake_case
  - Structs/enums/traits: PascalCase
  - Constants/static values: UPPER_SNAKE_CASE
- Event names:
  - Format: domain:event_name (example: player:time_pos, player:playback_end)
  - Keep names stable once published; version if breaking changes are required.

## 5) Code Conventions
### 5.1 Frontend (TypeScript/React)
- Strict TypeScript mode enabled.
- No any unless documented with a temporary TODO and expiration plan.
- Hooks should be deterministic and side-effect boundaries explicit.
- Accessibility is required for controls: keyboard support, focus visibility, and semantic labels.

### 5.2 Backend (Rust/Tauri)
- Avoid panics in runtime paths; return typed errors.
- Validate command inputs at Tauri command boundary.
- Long-running work should not block command handlers.
- Use ownership/concurrency patterns that prevent lock contention in hot paths.

### 5.3 Styling
- Tailwind v4 CSS-first approach only.
- Use CSS variables for theme tokens and keep naming semantic.
- Keep visual effects (blur, animation) under performance budgets.

## 6) Performance And Reliability Budgets
- Control commands (play/pause/seek): p95 < 100 ms on reference hardware.
- Warm startup target: p95 < 2.5 s.
- 1080p H.264 playback memory target: < 220 MB after 5 min.
- No critical crashes in validation smoke runs.

## 7) Testing Standards
- Every feature prompt must include executable acceptance checks.
- Add regression checks for open/play/seek/subtitle/PiP before major merges.
- Include stress scenario for rapid seek/event bursts.
- CI must run lint + tests + build for all supported platforms where feasible.

## 8) Security Standards
- Tauri v2 capabilities must be explicit and minimal.
- Avoid broad filesystem/system permissions unless justified and documented.
- Validate file paths and user inputs before passing to engine APIs.

## 9) Documentation Standards
- Public behavior and command/event contracts must be documented when changed.
- Keep architecture docs, task prompts, and standards in sync.
- Use concrete, testable language (avoid ambiguous terms like fast, smooth without threshold).

## 10) Definition Of Done (DoD)
A change is done only if all are true:
- Naming and file conventions are followed.
- Lint/tests/build pass for impacted modules.
- Acceptance checklist items for the relevant prompt are completed.
- No new critical errors or known regressions introduced.
- Relevant docs are updated.

## 11) Exceptions Process
- Any deviation requires a short ADR note in docs with:
  - Reason for exception
  - Scope and expiry (if temporary)
  - Risk and mitigation
