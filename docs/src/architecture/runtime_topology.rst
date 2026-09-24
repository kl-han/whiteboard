Runtime topology
================

**Processes, and how they talk.** Every edge is a runtime channel. Build
steps are not shown.

.. mermaid::

   flowchart TD
       Agent["Coding agent (external process)"] -->|"MCP JSON-RPC / stdio"| MCP["whiteboard mcp<br/>(Node child of the agent)"]
       Agent -->|"exec"| ApiCLI["whiteboard api / trace ...<br/>(one-shot Node)"]
       Hooks["Harness hooks + Git prepare-commit-msg"] -->|"exec"| ApiCLI
       MCP -->|"HTTP loopback + token"| Server
       ApiCLI -->|"HTTP loopback + token"| Server
       subgraph Desktop["Whiteboard Desktop (Electron)"]
         Main["main process<br/>(supervisor, menubar, updates)"]
         Server["UtilityProcess: embedded server<br/>desktop-host.ts"]
         Renderer["renderer: workbench + canvas + libavoid.wasm"]
         ExtHost["extension host: LSP servers"]
         Main -->|"spawn + env; stdout ready"| Server
         Renderer -->|"IPC getConnection"| Main
         Renderer -->|"HTTP / NDJSON"| Server
         Renderer --> ExtHost
       end
       Server -->|"spawn, NDJSON"| Diffr["diffr (native)"]
       Server -->|"execFile"| GitCLI["git / jj"]
       Server --> DB[("review-api.db")]
       Server -->|"writes"| Disc[("instances/KEY.json")]
       MCP -->|"reads"| Disc
       ApiCLI -->|"reads"| Disc
       Headless["whiteboard server start<br/>(headless, optional)"] --> DB2[("state-dir/review-api.db")]
       ApiCLI -.->|"--state-dir"| Headless
       Server -->|HTTPS| PostHog["us.i.posthog.com"]
       ApiCLI -->|"HTTPS / aws CLI"| Traces["app.dev.fast or S3/R2"]
       Main -->|HTTPS| Update["update.dev.fast"]

Process inventory
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Process
     - Lifetime
     - Started by
   * - Electron main
     - The app session
     - The user, the OS, or ``whiteboard app launch``
   * - Embedded server (UtilityProcess)
     - Supervised; up to 3 restarts with backoff
     - Electron main
   * - Renderer(s)
     - Per window
     - Electron main
   * - Extension host
     - Per window
     - Code - OSS
   * - ``whiteboard mcp``
     - The agent session
     - The agent host, from plugin ``.mcp.json``
   * - ``whiteboard api`` / ``trace``
     - One command
     - Agent skills, hooks, users
   * - diffr
     - One comparison (cached replay)
     - The embedded server
   * - Headless server
     - Foreground, until SIGTERM
     - ``whiteboard server start``
