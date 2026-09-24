Verification matrix
===================

This page records Phase 2 subsystem-by-subsystem verification (2026-09-24,
fork ``main`` at ``e53193d``). The environment is the same as in
:doc:`verification_results`.

Failure classes: CODE FAILURE · ENVIRONMENT FAILURE · NETWORK FAILURE ·
MISSING CREDENTIAL · MISSING TOOLCHAIN · PLATFORM LIMITATION · UNVERIFIED
EXTERNAL SERVICE.

.. list-table::
   :header-rows: 1
   :widths: 24 34 12 30

   * - Target
     - Command
     - Result
     - Class / note
   * - Root install
     - ``pnpm install --frozen-lockfile``
     - PASS
     - —
   * - Root build
     - ``pnpm run build``
     - PASS
     - —
   * - Root typecheck
     - ``pnpm run typecheck``
     - FAIL
     - NETWORK FAILURE (the fork's ``tsgo`` dependencies could not install)
   * - Typecheck without the fork
     - ``pnpm -r --filter '!@dev.fast/review-desktop' typecheck``
     - PASS
     - —
   * - Root lint / format
     - ``pnpm lint``, ``pnpm format:check``
     - PASS
     - —
   * - Root script tests
     - ``node --test "scripts/**/*.test.mjs"``
     - PASS (11)
     - —
   * - CLI + server tests
     - ``pnpm --filter @dev.fast/review test``
     - PASS (1185, 12 skipped)
     - Needs Git ``safe.directory`` when run as root: ENVIRONMENT FAILURE
       otherwise
   * - CLI entrypoint
     - ``pnpm review version``, ``--help``
     - PASS
     - —
   * - Headless server
     - ``server start`` + ``api`` create, edit, get, diff
     - PASS
     - —
   * - MCP smoke test
     - stdio ``initialize`` → ``tools/list`` (28) → ``tools/call``
     - PASS
     - Without a server: 2 tools and actionable errors
   * - Canvas build / tests
     - ``pnpm --filter @dev.fast/review-canvas build`` / ``test``
     - PASS (517)
     - Needed a Chromium shim: ENVIRONMENT FAILURE (browser build mismatch)
   * - Agent-plugin validation
     - ``agent-plugins.test.ts`` (inside the review tests)
     - PASS
     - Real agent hosts: UNVERIFIED EXTERNAL SERVICE
   * - trace-core / trace-protocol
     - ``pnpm --filter … test``
     - PASS (250 / 17)
     - Real stores: MISSING CREDENTIAL
   * - local-vcs
     - ``pnpm --filter @dev.fast/local-vcs test``
     - PASS (69, 6 skipped)
     - The skips are ``skipIf(no jj)``: MISSING TOOLCHAIN (CONFIRMED)
   * - review-protocol / share-protocol
     - ``… test``
     - PASS (76 / 5)
     - —
   * - diffr fetch
     - ``pnpm --filter @dev.fast/review ensure:diffr --required``
     - PASS
     - GitHub releases reachable
   * - diffr run
     - ``diffr --format ndjson --stream-annotations 9f8088d~1 9f8088d``
     - PASS
     - Wire v4; test file hidden by the plugin
   * - diffr failure probes
     - Scratch repository (unsupported, parse error, too large)
     - PASS
     - Text-diff fallbacks as documented
   * - diffr integration tests
     - ``pnpm --filter @dev.fast/review test:integration:diffr``
     - PASS (9)
     - —
   * - Rust build / tests (diffr)
     - —
     - N/A
     - No diffr Rust source in this repository
   * - Rust toolchain sanity (LSP fixture)
     - ``cargo check`` in ``scripts/e2e/fixtures/lsp/rust``
     - PASS
     - A fixture only, not a component
   * - WASM build
     - —
     - N/A
     - No first-party WASM build. ``libavoid.wasm`` is prebuilt and
       exercised by the canvas tests.
   * - WASM integration (diffr plugins)
     - —
     - NOT RUN
     - No external plugin or WIT definition available (UNVERIFIED)
   * - Code - OSS dependency install
     - ``app:build`` → ``npm ci``
     - FAIL
     - NETWORK FAILURE (``electronjs.org`` headers)
   * - Desktop build
     - ``pnpm --filter @dev.fast/review-desktop app:build``
     - FAIL
     - NETWORK FAILURE
   * - Desktop fast tests
     - ``pnpm --filter @dev.fast/review-desktop test``
     - PASS (105 + 197)
     - —
   * - Desktop launch
     - ``pnpm dev``
     - NOT RUN
     - Depends on the build; needs a display (PLATFORM LIMITATION in this
       container)
   * - Latency harness
     - ``uv run review-latency --help``
     - PASS
     - Real runs need ``/Applications/Whiteboard.app`` (PLATFORM LIMITATION)
   * - Hosted store, share service, PostHog, update feed
     - —
     - NOT RUN
     - UNVERIFIED EXTERNAL SERVICE (hosts blocked here)
   * - Sphinx
     - ``sphinx-build -W -b html docs docs/_build/html``
     - PASS
     - —
   * - Mermaid validation
     - Render every diagram with ``mermaid@11`` in headless Chromium
     - PASS
     - 23 of 23 diagrams. Two failed at first because ``;`` ends a statement in Mermaid sequence messages; both are fixed.
