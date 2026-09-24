System overview: provenance × runtime
=====================================

The combined high-level picture. Colors show **provenance**; boxes show
**processes**. The Phase 2 plan's "Rust / WASM (?)" question is resolved:
diffr is a **native Rust process** reached over NDJSON. WASM is used
*inside* diffr (plugins) and, separately, in the canvas (libavoid).

.. mermaid::

   flowchart TD
       classDef ext fill:#eee,stroke:#888,color:#333
       classDef own fill:#dbeafe,stroke:#1d4ed8,color:#111
       classDef vend fill:#fde68a,stroke:#b45309,color:#111
       classDef gen fill:#dcfce7,stroke:#15803d,color:#111
       Agent["EXTERNAL AGENT<br/>Claude Code / Codex / Cursor / OpenCode / Pi"]:::ext
       Plugin["Agent integration<br/>plugins + skills (Whiteboard)"]:::own
       MCP["whiteboard mcp / api<br/>TS · Node · stdio child"]:::own
       Server["Whiteboard server<br/>TS · Node UtilityProcess<br/>review-api + SQLite"]:::own
       Proto["review-protocol<br/>(generated copy in fork)"]:::gen
       Canvas["Canvas · React/TS<br/>Chromium renderer<br/>+ libavoid.wasm (LGPL)"]:::own
       Shell["Desktop shell<br/>src/vs/review (Whiteboard)"]:::own
       Code["Code - OSS 1.129.1 @ 8a7abeba<br/>+ Electron 42.10.0"]:::vend
       Diffr["diffr · Rust native binary<br/>difftastic + tree-sitter + git2<br/>wasmtime plugin host"]:::ext
       VCS["local-vcs → git / jj"]:::own
       Trace["trace-core + trace-protocol"]:::own
       Stores["app.dev.fast / S3-R2 (aws CLI)"]:::ext
       Agent -->|MCP stdio| Plugin --> MCP
       MCP -->|HTTP + token| Server
       Server --- Proto
       Canvas -->|HTTP / NDJSON| Server
       Shell -->|IPC + HTTP| Server
       Shell --> Canvas
       Shell --- Code
       Server -->|spawn · NDJSON v4| Diffr
       Server --> VCS
       Diffr -->|libgit2| Repo[("Local repository")]:::ext
       VCS --> Repo
       Trace --> Stores
       Server --> Trace

Legend: blue = Whiteboard-owned; amber = vendored upstream; green =
generated; grey = external (a separate repository or service).
