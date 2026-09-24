Verification results
====================

These commands were run on **2026-09-24** against commit ``c14db21``
(desktop version 0.1.1). The machine was an ephemeral Linux cloud container
with 4 CPUs, 15 GB RAM and no display, running as ``root``. Outbound network
access was restricted by an egress proxy. The container shipped with Node
22.22.2, so we installed the official Node 24.21.0 tarball into a local
prefix and put it first on ``PATH``. For the desktop build, we also installed
Node 24.18.0, the version pinned in ``code-oss/.nvmrc``.

.. list-table::
   :header-rows: 1
   :widths: 18 14 8 22 18 20

   * - Command
     - Purpose
     - Result
     - Error summary
     - Likely cause
     - Suggested fix
   * - ``pnpm install --frozen-lockfile``
     - Install workspace dependencies
     - **Passed** (5 s)
     - 4 warnings: ``Failed to create bin … dist/cli.js``
     - ``@dev.fast/review`` bins point at ``dist/``, which does not exist
       before the first build
     - Harmless. Run ``pnpm run build``, then ``pnpm install`` again, to get
       the bin links.
   * - ``pnpm run build``
     - Build all packages (tsc, tsdown, Vite)
     - **Passed** (53 s)
     - —
     - —
     - —
   * - ``pnpm run lint``
     - oxlint including the anti-slop rules
     - **Passed** (4 s)
     - —
     - —
     - —
   * - ``pnpm run format:check``
     - oxfmt check
     - **Passed** (2 s)
     - —
     - —
     - —
   * - ``pnpm run typecheck``
     - Typecheck every package, one at a time
     - **Failed** at ``@dev.fast/review-desktop``
     - ``sh: 1: tsgo: not found`` from ``npm --prefix code-oss run typecheck-client``
     - Code - OSS's own npm dependencies were not installed. The desktop
       build that installs them was blocked (see below).
     - Run ``bash apps/review-desktop/scripts/code-oss-dependencies.sh`` or
       ``pnpm desktop:build`` first, with network access.
   * - ``pnpm -r --filter '!@dev.fast/review-desktop' typecheck``
     - Typecheck everything except the fork
     - **Passed**
     - —
     - —
     - —
   * - ``pnpm run test`` (first run)
     - Root script tests and all package tests
     - **Failed**
     - 3 tests in ``legacy-review-fixtures.test.ts``: ``git … fatal: detected
       dubious ownership``
     - The fixtures create Git repositories whose owner is not the ``root``
       user running the tests, so Git's ``safe.directory`` check refuses
       them
     - Environment only. ``git config --global --add safe.directory '*'`` in
       a disposable container, or run as a normal user.
   * - ``pnpm run test`` (after ``safe.directory``)
     - Same
     - **Partially passed**
     - Root scripts 11/11. json, trace-protocol 17, share-protocol 5,
       local-vcs 69 (6 skipped), review-protocol 76, trace-core 250 and
       review 1185 (12 skipped) passed. The canvas suite failed to launch
       Chromium.
     - The pinned Playwright 1.62.1 expects ``chromium_headless_shell-1234``,
       but the container provides build ``1194``
     - ``pnpm --filter @dev.fast/review-canvas exec playwright install chromium --only-shell``
       (as CI does)
   * - ``pnpm --filter @dev.fast/review-canvas test``
     - Canvas unit and browser tests
     - **Passed** (93 files, 517 tests)
     - —
     - Run with a local ``PLAYWRIGHT_BROWSERS_PATH`` shim that maps build
       1234 onto the preinstalled 1194 headless shell. This is a workaround
       for this environment only.
     - On a normal machine, install the matching browser instead.
   * - ``pnpm --filter @dev.fast/review-desktop test``
     - Desktop script tests and ``src/vs/review`` unit tests
     - **Passed** (105 + 197 tests, 1 skipped)
     - —
     - —
     - —
   * - ``pnpm --filter @dev.fast/review check:tutorial``
     - Validate the tutorial review
     - **Passed**
     - —
     - —
     - —
   * - ``pnpm review version`` / ``pnpm review --help``
     - CLI entrypoint from source (tsx)
     - **Passed** (prints ``0.0.1``)
     - —
     - —
     - —
   * - ``whiteboard server start --state-dir …`` + ``api`` calls
     - Headless authoring loop
     - **Passed**
     - ``session_register_repository``, ``session_create`` (commits target
       ``a02de1c..c14db21``), ``session_edit``, ``session_get`` and
       ``session_diff`` all succeeded
     - —
     - —
   * - ``pnpm --filter @dev.fast/review-desktop app:build``
     - Build the Code - OSS desktop
     - **Failed** (29 s)
     - ``node-gyp`` could not download
       ``https://electronjs.org/headers/v42.10.0/…`` (``Request was
       cancelled``) while it rebuilt ``@parcel/watcher``
     - Egress policy blocked ``electronjs.org``. Electron,
       ``open-vsx.org`` and ``marketplace.visualstudio.com`` were blocked
       too.
     - Build on a machine with open network access, or allow those hosts.
   * - ``pnpm dev``
     - Build and launch Desktop
     - **Skipped**
     - —
     - Depends on ``app:build`` (blocked). It also needs a display.
     - Run locally, or under ``xvfb-run -a`` in CI.
   * - ``pnpm run ci``
     - Full CI suite
     - **Not run as one command**
     - —
     - Its first step is ``app:build``, which is blocked. We ran every
       other step on its own (above).
     - —
   * - ``sphinx-build -b html docs docs/_build/html``
     - Build this documentation
     - **Passed** with no warnings
     - —
     - —
     - Used Sphinx 9.0.4, sphinx-rtd-theme 3.1.0, sphinxcontrib-mermaid and
       myst-parser 5.1.0. ``-W`` (warnings as errors) also passes. The
       fallback build without the Mermaid and RTD packages also passes.
   * - Mermaid diagram render check
     - Catch diagram syntax errors that Sphinx cannot see
     - **Passed** (6 of 6 diagrams)
     - One label with ``@`` failed at first. It is now quoted.
     - Mermaid parses in the browser, so ``sphinx-build`` never reports
       syntax errors
     - Each diagram was rendered with ``mermaid@11`` in headless Chromium.
       Rerun this check whenever diagrams change.

What could not be verified
--------------------------

* Launching Desktop, the embedded server under Electron's
  ``UtilityProcess``, instance selection against a live Desktop, and
  ``whiteboard app launch``.
* ``whiteboard mcp`` against a real agent. The MCP code path shares the
  HTTP client with ``whiteboard api``, which was verified.
* Structural diff with ``diffr``. ``ensure:diffr`` was not run, and
  ``test:integration:diffr`` needs the binary.
* Trace capture against real agent harnesses, S3/R2 or the hosted store.
  These need credentials.
* macOS packaging, signing and notarization, and the Linux RPM builds.
* The LSP and telemetry end-to-end journeys (``test:e2e:*``).
