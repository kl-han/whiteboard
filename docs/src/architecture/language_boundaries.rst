Language and runtime boundaries
===============================

This page lists every place where control crosses a process, language or
runtime boundary. Each boundary is written as "A invokes B through C; B
receives D and returns E; errors cross as F".

Languages actually used
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - Language
     - Where it runs
     - Why it exists
   * - TypeScript / TSX
     - CLI, servers, canvas, fork workbench, protocols, trace, local-vcs
     - The whole first-party product (CONFIRMED)
   * - Rust
     - The external ``diffr`` binary only. The vendored upstream ``cli/`` and
       ``build/win32`` Rust is never built.
     - Tree-sitter + difftastic structural diffing and the wasmtime plugin
       host (CONFIRMED from the binary; the rationale is DOCUMENTED in the
       README)
   * - C++ → WebAssembly
     - ``libavoid.wasm`` in the canvas
     - Orthogonal edge routing (CONFIRMED, ``THIRD_PARTY_NOTICES.md``)
   * - JavaScript (ESM)
     - Build, release and packaging scripts; the OpenCode plugin
     - Tooling glue (CONFIRMED)
   * - Bash
     - ``build.sh``, ``run.sh``, packaging, Git hook dispatchers
     - Orchestrating Code - OSS, Electron and hooks (CONFIRMED)
   * - Python
     - Linux repository publishing, ``scripts/review-latency``, ``docs/conf.py``
     - Tooling only; nothing Python ships in the product (CONFIRMED)
   * - Go / Rust / Python fixtures
     - ``apps/review-desktop/scripts/e2e/fixtures/lsp``
     - LSP end-to-end test inputs, not components (CONFIRMED)

Boundary map
------------

.. mermaid::

   flowchart LR
       subgraph AgentProc["Agent process (external)"]
         Agent[Coding agent]
       end
       subgraph McpProc["whiteboard mcp (Node, stdio child)"]
         MCP[mcp.ts]
       end
       subgraph Electron["Whiteboard Desktop (Electron 42)"]
         Main[Electron main<br/>reviewServerSupervisor]
         subgraph Utility["UtilityProcess (Node)"]
           Server[desktop-host.ts<br/>review-api]
         end
         subgraph Renderer["Renderer (Chromium)"]
           Workbench[Code - OSS workbench<br/>src/vs/review]
           Canvas[Canvas ES module]
           Wasm[libavoid.wasm]
           ExtHost[Extension host / LSP]
         end
       end
       Diffr[diffr native binary<br/>Rust + wasmtime]
       Git[(git / jj executables)]
       Store[(review-api.db SQLite)]
       Hosted[(app.dev.fast / S3 via aws CLI)]
       Agent -- "B1: JSON-RPC over stdio" --> MCP
       MCP -- "B2: HTTP + x-review-token" --> Server
       Main -- "B3: spawn, env, stdout ready line" --> Server
       Workbench -- "B4: Electron IPC getConnection" --> Main
       Workbench -- "B5: dynamic import() + mount" --> Canvas
       Canvas -- "B6: HTTP / NDJSON watch" --> Server
       Canvas -- "B7: WebAssembly instantiate" --> Wasm
       Server -- "B8: spawn, NDJSON stdout" --> Diffr
       Server -- "B9: execFile" --> Git
       Diffr -- "libgit2 in-process" --> Git
       Server -- "B10: SQLite" --> Store
       Server -- "B11: HTTPS / aws CLI" --> Hosted
       Workbench -- "B12: fetch NDJSON structural-diff" --> Server

Boundary details
----------------

.. list-table::
   :header-rows: 1
   :widths: 10 18 18 18 18 18

   * - ID
     - Mechanism and processes
     - Data and schema
     - Timeouts, retries and lifecycle
     - Errors
     - Contract owner and trust
   * - B1 Agent → MCP
     - The agent host spawns ``whiteboard mcp``; JSON-RPC 2.0 over stdio.
       Separate process; asynchronous.
     - MCP ``initialize``/``tools/list``/``tools/call`` (protocol
       ``2025-06-18`` in our smoke test). Tool input schemas come from the
       server's Zod definitions.
     - Lives as long as the agent session. No retries: every call
       rediscovers the server. ``tools/list_changed`` is sent once the
       server becomes reachable.
     - Tool failures come back as ``{isError: true, content:[text]}``, not
       JSON-RPC errors (CONFIRMED by smoke test).
     - Whiteboard owns the tool catalog; the MCP spec owns framing. The
       agent is trusted as the local user.
   * - B2 MCP / CLI → server
     - ``fetch`` to ``http://127.0.0.1:<port>/reviews-api/...``. Separate
       processes.
     - JSON bodies; ``commandId`` (UUID) for idempotency; NDJSON for watch
       streams.
     - No client retries; a ``commandId`` replay makes retries safe.
       Server-side streams have their own bounds.
     - HTTP 4xx with ``{error}`` for ``ReviewInputError``; 409 for lease
       conflicts; 500 for unexpected errors.
     - ``packages/review`` owns the API. The token (header
       ``x-review-token`` or ``?token=``) is compared in constant time
       (``hono-http.ts``).
   * - B3 Electron main → server
     - ``UtilityProcess`` of type ``review-desktop-host``; environment
       variables ``DEV_FAST_REVIEW_SERVER_{ENTRY,PORT,TOKEN}``,
       ``DEV_FAST_REVIEW_APP_PID`` and others.
     - A ``ready`` JSON event on stdout, validated by
       ``ReviewReadyEventReader``. Non-ready lines are logs.
     - Ready timeout 30 s; restarts after 250, 1000 and 2000 ms
       (``REVIEW_SERVER_RESTART_DELAYS``); a 2 s shutdown grace.
     - A malformed ready event, or unexpected credentials in it, throws.
       Crashes are reported through telemetry.
     - Whiteboard owns both sides. Main generates a 32-byte random token.
   * - B4 Renderer → main
     - VS Code IPC channel (``reviewDesktopChannel.ts``), command
       ``getConnection``.
     - ``ReviewDesktopConnection`` (server URL and token).
     - The renderer reconnects with delays 250, 1000, 2000 and 4000 ms
       (``REVIEW_CLIENT_RECONNECT_DELAYS``).
     - Surfaced as workbench notifications.
     - Whiteboard, inside the fork.
   * - B5 Workbench → canvas
     - Same renderer process. ``await import()`` of the Vite bundle, then
       ``mountReviewCanvas()`` (``reviewCanvasPart.ts``).
     - The bridge object: content, the server connection, ``wasmUrl``,
       callbacks.
     - Mounted and reused per review tab.
     - "Whiteboard canvas bundle has no mount function." if the bundle
       shape is wrong.
     - Whiteboard. Trusted Types policy in ``desktop-trusted-types.ts``.
   * - B6 Canvas → server
     - HTTP from Chromium to loopback.
     - JSON snapshots; NDJSON ``/watch`` (a coalesced array per line).
     - Reconnects restart from the current snapshot.
     - Error rows in the watch array.
     - ``review-protocol`` (``review-api-client.ts``).
   * - B7 Canvas → libavoid
     - WebAssembly in the renderer.
     - Graph geometry in, routed edges out.
     - Synchronous calls after async instantiation.
     - Instantiation failure breaks map and lens routing (INFERRED).
     - External (LGPL).
   * - B8 Server → diffr
     - ``child_process.spawn`` with ``--format ndjson --stream-annotations``.
       Separate native process, with ``cwd`` set to the repository.
     - NDJSON wire version 4 (``STRUCTURAL_DIFF_WIRE_VERSION``). The first
       line must be ``start`` with version 4.
     - 120 s idle timeout, refreshed per line. Each record is capped at
       64 MiB. Closing the consumer kills the child.
     - Launch failure, a malformed line or an unexpected exit throws. Exit
       code 2 is accepted when failures were already reported in the stream.
       Per-file errors are data.
     - The ``devdotfast/diffr`` repository owns the wire;
       ``@dev.fast/diffr`` mirrors it and is pinned to exactly 0.1.3.
   * - B9 Server → Git/jj
     - ``execFile`` of ``git`` and ``jj`` (``local-vcs``).
     - CLI output parsing.
     - Bounded buffers; locks for notes.
     - Command failures become ``ReviewInputError`` where they are safe to
       show.
     - Git/jj CLI compatibility is external.
   * - B10 Server → SQLite
     - In-process library.
     - Tables listed in the review-api README.
     - ``data_version`` is polled every 250 ms across connections.
     - Transaction failures become HTTP 500.
     - Whiteboard owns the schema (``REVIEW_SCHEMA_VERSION``, migrations).
   * - B11 CLI/server → trace stores
     - Hosted: HTTPS with ``Authorization: Bearer`` and presigned S3 URLs.
       S3/R2: shells out to the ``aws`` CLI (``s3api``).
     - ``@dev.fast/trace-protocol`` schemas; gzipped session objects; sha256
       checks on download.
     - Upload links last 15 min and download links 5 min (DOCUMENTED).
     - ``StoreApiError``. Presigned URLs are never printed.
     - Whiteboard owns the protocol; dev.fast runs the hosted store
       (UNVERIFIED service).
   * - B12 Workbench → structural diff
     - ``fetch`` of ``/reviews-api/:id/structural-diff`` (NDJSON).
     - ``decodeReviewStructuralDiffEvent``: the diffr events plus
       ``{type:"error"}``.
     - Aborted with the editor.
     - A stream ``error`` event is rethrown. A non-NDJSON content type
       means "The Whiteboard host must be updated".
     - ``review-protocol`` (generated into the fork).

The suspected Rust/WASM → TypeScript boundary
---------------------------------------------

The Phase 2 plan expected TypeScript to call the Rust engine through WASM.
**It does not** (CONFIRMED). ``structural-diff.ts`` spawns a native
executable and reads NDJSON from stdout. WASM exists at two other places:

1. **Inside diffr**, which links wasmtime 34, wasmtime-wasi,
   wasmtime-wasi-http and wit-bindgen. This is the plugin host for the
   README's "WASM-based plugin system" (INFERRED from the binary; how
   plugins are loaded is UNVERIFIED without the diffr source).
2. **In the canvas**, as ``libavoid.wasm``, which has nothing to do with
   diffing.

Whiteboard code ↔ vendored Code - OSS
-------------------------------------

This is a **compile-time** boundary, not a runtime one. ``src/vs/review`` is
compiled by the Code - OSS build into the same bundles as upstream code. The
entry manifests (``review.desktop.main.ts`` and others) import Whiteboard
contributions, and a small set of upstream files is edited to hook them in
(``app.ts``, ``workbench.ts``, ``main.ts``, the menubar and more). See
:doc:`upstream/fork_boundary`.
