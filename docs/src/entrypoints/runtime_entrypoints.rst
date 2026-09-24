Runtime entrypoints
===================

Whiteboard has four kinds of runtime entrypoints. Every one of them ends at
the same HTTP API, mounted under ``/reviews-api`` by
``packages/review/src/review-api/http.ts``.

.. list-table::
   :header-rows: 1
   :widths: 22 38 40

   * - Entrypoint
     - File
     - Started by
   * - Desktop main process
     - ``apps/review-desktop/code-oss/src/vs/review/electron-main/*``, loaded
       from the fork's ``main``
     - The user opens the app, or ``whiteboard app launch``
   * - Embedded (Desktop) server
     - ``packages/review/src/server/desktop-host.ts`` → ``desktop-server.ts``
     - ``reviewServerSupervisor.ts`` starts it as an Electron
       ``UtilityProcess`` of type ``review-desktop-host``
   * - Headless server
     - ``packages/review/src/server/headless-host.ts``
     - ``whiteboard server start [--state-dir] [--port]``
   * - CLI
     - ``packages/review/src/cli.ts`` → ``cli-runner.ts``
     - A shell, an agent, or the ``~/.local/bin/whiteboard`` shim
   * - Agent adapters
     - ``review-api/mcp.ts`` (stdio MCP), ``review-api/agent-cli.ts`` (``api``)
     - ``whiteboard mcp`` from a plugin's MCP config; ``whiteboard api`` from a skill
   * - Canvas
     - ``packages/review/app/src/*`` (Vite bundle)
     - Loaded into Desktop webviews after ``copy-canvas.mjs`` copies it in

High-level relationships
------------------------

We checked the requested starting diagram against the code and changed it in
three ways:

* The agent plugins **do not** call the CLI's ordinary commands. They start
  ``whiteboard mcp``, a long-lived stdio MCP server. The Pi skill runs
  ``whiteboard api …``.
* The CLI **does not start** the embedded server. Desktop's main process
  does. The CLI **discovers** a running server through
  ``~/.dev/review-desktop/instances/<key>.json``, or starts a separate
  headless server.
* Trace capture mostly happens **outside** the server. Agent-harness hooks
  and Git hooks call ``whiteboard trace …``. The server reads the stored
  traces.

.. mermaid::

   flowchart TD
       User[User] --> Desktop[Whiteboard Desktop<br/>Electron main process]
       User --> CLI[whiteboard CLI]
       Agent[Coding agent] --> Plugin[Agent plugin / skill]
       Plugin -->|"whiteboard mcp (stdio)"| MCP[MCP adapter]
       Plugin -->|"whiteboard api tool json"| CLI
       MCP --> Discovery[Instance discovery<br/>~/.dev/review-desktop/instances]
       CLI --> Discovery
       Desktop -->|UtilityProcess| Server[Embedded server<br/>desktop-host.ts]
       Server -->|writes discovery record| Discovery
       Discovery -->|url + token| Server
       CLI -->|server start| Headless[Headless server<br/>headless-host.ts]
       Server --> Store[(review-api.db<br/>JSON review store)]
       Headless --> Store
       Server --> VCS[local-vcs<br/>git / jj]
       VCS --> Code[Local repository checkout]
       Server --> Traces[Trace storage<br/>~/.dev/trace, S3/R2, hosted]
       Hooks[Agent + Git hooks] -->|whiteboard trace ...| Traces
       Server -->|watch / NDJSON| Canvas[Canvas in Desktop webviews]
       Desktop --> Canvas

Startup sequence of Desktop (confirmed from code and README)
------------------------------------------------------------

1. Electron starts the Code - OSS main process. Whiteboard's
   ``electron-main`` contributions register the menubar, crash telemetry,
   the update dialog and the server supervisor.
2. The supervisor resolves the server entry (``resolveReviewServerEntry``
   in ``common/reviewDesktopBootstrap.ts``) and starts it in a
   ``UtilityProcess``. It passes ``DEV_FAST_REVIEW_SERVER_PORT`` (``0``
   lets the OS choose a port), ``DEV_FAST_REVIEW_APP_PID`` and related
   environment variables.
3. ``runDesktopHost`` creates the telemetry client and the store profile,
   ensures bundled tools (for example rust-analyzer), and calls
   ``createGlobalReviewServer``.
4. The server writes a private, atomic discovery record for its instance
   (``reviewInstanceDiscoveryPath``) and emits a ready event. The
   supervisor reads that event (``ReviewReadyEventReader``).
5. The workbench connects (``reviewDesktopConnectionService``) and opens
   **Home**. No repository is needed. Reviews open on demand. The startup
   importer migrates any legacy MDX reviews first.
6. If the server crashes, the supervisor restarts it with the backoff
   delays in ``common/reviewReconnect.ts``.

Local state selection
---------------------

``DEV_REVIEW_HOME`` (default ``~/.dev``) is the root. The CLI chooses a
Desktop instance in this order (``cli.ts`` ``selectedDiscoveryFile``, which
mirrors ``selectReviewInstance``):

1. ``DEV_REVIEW_INSTANCE``
2. The machine default in ``review-desktop/default-instance`` (set by
   ``whiteboard instances use <key>``)
3. The only live instance, if exactly one is running
4. ``stable``
5. The legacy ``review-desktop/server.json``

A record counts as "live" only if its ``serverPid`` is running. For
headless work, ``--state-dir`` or ``DEV_REVIEW_SERVER_DIR`` bypasses
instance selection entirely.

External integrations at startup
--------------------------------

* PostHog telemetry, unless it is turned off (``docs/telemetry.md``).
* The update feed at ``https://update.dev.fast`` (signed builds only).
* Agent detection and CLI and skill installation offers. These re-sync
  after every app update (``packages/review/README.md``).
* Structural diff runs the bundled ``diffr`` binary on demand, not at
  startup.
