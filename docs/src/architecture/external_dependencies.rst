External dependencies
=====================

Whiteboard says multi-repository work is not well supported *for users*,
yet its own implementation spans several repositories and services. This
page separates them. The reachability column records what our egress-limited
container could reach on 2026-09-24.

Source incorporated into this repository
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 22 56

   * - Source
     - Where
     - Notes
   * - Code - OSS @ ``8a7abeba`` (1.129.1)
     - ``apps/review-desktop/code-oss``
     - Vendored; divergences listed in ``UPSTREAM``
   * - anti-slop lint rules
     - ``tools/oxlint/anti-slop``
     - Partial copy from ``dmmulroy/anti-slop`` (``UPSTREAM.md``)
   * - eslint-stylistic pieces
     - ``tools/oxlint/anti-slop/vendor``
     - Vendored along with anti-slop

Build and runtime dependencies
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 11 11 10 12 12 10 10 10

   * - System
     - Version
     - Integration
     - Local / remote
     - Source or runtime
     - Compatibility owner
     - If unavailable
     - Mockable
     - Offline dev
   * - Node.js
     - 24 (monorepo); 24.18.0 (fork)
     - Runtime and toolchain
     - Local
     - Both
     - Node project; pinned by ``.nvmrc``
     - Nothing runs
     - —
     - Yes, once installed
   * - pnpm
     - 11.1.2
     - Package manager
     - Local; npm registry
     - Build
     - pnpm
     - No install
     - —
     - With a warm store
   * - Electron
     - 42.10.0
     - Desktop runtime; node-gyp target
     - Downloaded (GitHub releases; headers from electronjs.org)
     - Both
     - Electron, pinned by the fork
     - No desktop build (see :doc:`../devops/native_dependencies`)
     - No
     - Only with cached headers and zips
   * - Chromium (Playwright)
     - Playwright 1.62.1's build
     - Browser tests
     - Local download
     - Test
     - Playwright
     - Canvas browser tests fail
     - The Node project can run alone
     - With a cached browser
   * - diffr
     - 0.1.3 exact
     - Native child process, NDJSON v4
     - GitHub releases download
     - Runtime
     - ``devdotfast/diffr``
     - Structural diff unavailable; UI errors
     - ``REVIEW_DIFFR_BINARY`` can point at a fake
     - After one fetch
   * - Rust toolchain
     - —
     - **Not needed** for Whiteboard
     - —
     - —
     - —
     - —
     - —
     - —
   * - git / jj
     - Any recent
     - ``execFile``, and libgit2 inside diffr
     - Local
     - Runtime
     - Git and Jujutsu
     - No pins or diffs
     - Test fixtures create real repositories
     - Yes
   * - ``gh`` CLI / GitHub API
     - —
     - PR resolution for ``session_create {pullRequestUrl}``; sharing
     - Remote
     - Runtime
     - GitHub
     - PR reviews fail; public API fallback
     - Tests inject providers
     - No
   * - ``aws`` CLI
     - —
     - S3/R2 trace storage (``s3api``)
     - Remote
     - Runtime
     - AWS / Cloudflare
     - S3 trace mode unavailable
     - ``isS3MockMode()``, memory transport
     - No
   * - Hosted store ``app.dev.fast``
     - trace-protocol 0.5.0
     - HTTPS + Bearer + presigned S3
     - Remote
     - Runtime
     - dev.fast (the server is not in this repository)
     - Hosted traces and sharing unavailable
     - Memory transport in tests
     - No
   * - PostHog ``us.i.posthog.com``
     - —
     - Telemetry HTTPS
     - Remote
     - Runtime
     - PostHog
     - Events dropped (queued)
     - Debug sink (``telemetry-debug-sink.ts``)
     - Yes (``DO_NOT_TRACK=1``)
   * - Update feed ``update.dev.fast``
     - —
     - Squirrel / update service
     - Remote
     - Runtime
     - dev.fast
     - No auto-updates
     - —
     - Yes
   * - Open VSX ``open-vsx.org``
     - Per the manifest
     - Curated extension download at build
     - Remote
     - Build
     - Extension publishers
     - No LSP extensions
     - ``DEV_REVIEW_EXTENSIONS=none``
     - With cached VSIXes
   * - Gemini API
     - ``gemini-3.8-flash`` default
     - Called by diffr's summarize plugin
     - Remote
     - Runtime (optional)
     - Google
     - No summaries
     - —
     - Summaries off
   * - FFF (file search MCP)
     - —
     - Installed by trace setup; searches traces
     - Local
     - Runtime (optional)
     - ``dmtrKovalenko/fff``
     - Trace archaeology degrades
     - —
     - Yes
   * - rust-analyzer and other LSPs
     - Per the curated manifest
     - Extension host
     - Downloaded
     - Runtime
     - Upstream projects
     - No navigation for that language
     - —
     - After download

Agent ecosystems
----------------

.. list-table::
   :header-rows: 1
   :widths: 18 30 52

   * - Agent
     - Integration
     - Compatibility risk
   * - Claude Code
     - Plugin marketplace plus ``.mcp.json``; trace hooks in its settings
     - The plugin and hook formats are owned by Anthropic
   * - Codex
     - ``.codex-plugin`` plus ``.mcp.json``; trace hooks
     - Sandbox and proxy rules (#215 to #217)
   * - Cursor
     - ``.cursor-plugin`` plus ``mcp.json``
     - Skill install flow changes (#324, #534)
   * - OpenCode
     - JS plugin; trace capture through a managed plugin plus ``opencode export``
     - Its own session database
   * - Pi
     - Skill package; managed trace extension
     - The skill runs ``whiteboard api``, not MCP

External protocols and contracts
--------------------------------

MCP (``@modelcontextprotocol/sdk`` 1.30.0; stdio), LSP (through the Code -
OSS extension host), Git and the Jujutsu CLI, the Git hook protocol
(``prepare-commit-msg``, ``core.hooksPath``), WebAssembly (libavoid; diffr
plugins), the VS Code extension API (curated extensions), the S3 API
(presigned URLs), and HTTP/NDJSON.
