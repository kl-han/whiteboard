Desktop startup
===============

From launching the app to a ready Home screen.

.. mermaid::

   sequenceDiagram
       actor User
       participant OS as OS / whiteboard app launch
       participant M as Electron main (main.ts, app.ts)
       participant Sup as reviewServerSupervisor
       participant U as UtilityProcess (desktop-host.ts)
       participant FS as ~/.dev
       participant R as Renderer (workbench)
       participant Cv as Canvas
       User->>OS: open app (or CLI launches bundle, background unless --focus)
       OS->>M: start Electron
       M->>M: import VS Code-family settings, crash breadcrumb (pre-bootstrap)
       M->>Sup: start (random 32-byte token, instanceId)
       Sup->>U: UtilityProcess.start(entry, env DEV_FAST_REVIEW_SERVER_*)
       U->>FS: open review-api.db, import legacy reviews
       U->>FS: write instances/KEY.json (url, token, pids, cliPath)
       U-->>Sup: stdout {"event":"ready", ...}
       Note over Sup,U: 30 s ready timeout, restarts at 250/1000/2000 ms
       M->>R: open window (Review entry for empty windows)
       R->>M: IPC getConnection
       M-->>R: {serverUrl, token}
       R->>U: HTTP catalog / watch
       R->>Cv: import() canvas bundle, mountReviewCanvas()
       Cv-->>User: Home

.. list-table::
   :widths: 25 75

   * - Initiating actor
     - The user, or ``whiteboard app launch``
   * - Entrypoints
     - ``code-oss/src/main.ts`` → ``vs/code/electron-main/app.ts`` →
       ``vs/review/electron-main/*``
   * - Contracts
     - The ready event (``ReviewReadyEventReader``); the discovery record
       v3; IPC ``getConnection``
   * - Persistence
     - ``$DEV_REVIEW_HOME/review-desktop/{instances,state}``,
       ``review-api.db``
   * - Transitions
     - Electron main (Node) → UtilityProcess (Node) → renderer (Chromium) →
       canvas module (same renderer)
   * - Failure points
     - The server is not ready in 30 s. Restarts are exhausted. An
       unreadable legacy ``review.json`` (#349 tolerates it). A missing
       canvas bundle. Two Desktops sharing a home: a database-backed process
       claim prevents duplicate workspace jobs (#511).
   * - Verification
     - NOT run in this environment (no display, and the build is blocked).
       The sequence is reconstructed from code (CONFIRMED by reading).
