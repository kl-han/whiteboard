Subsystem development matrix
============================

Every command below comes from a ``package.json`` script, a README, or a
command we actually ran. "Debug" lists only mechanisms that exist in the
repository.

.. list-table::
   :header-rows: 1
   :widths: 12 12 16 16 22 22

   * - Subsystem
     - Language/runtime
     - Setup
     - Build
     - Test
     - Debug / observe
   * - CLI + servers
     - TS / Node 24
     - ``pnpm install``
     - ``pnpm --filter @dev.fast/review build``
     - ``pnpm --filter @dev.fast/review test`` (``test:node`` for the Node
       project)
     - ``pnpm review <cmd>`` (tsx from source); ``--json`` events;
       ``whiteboard version --verbose``; ``DEV_FAST_REVIEW_TELEMETRY_DEBUG``
       (telemetry debug sink)
   * - Headless authoring
     - TS / Node 24
     - Build first
     - (same)
     - ``whiteboard server start --state-dir D`` +
       ``whiteboard --state-dir D api …``
     - ``server status --json``; ``api tools``
   * - Canvas
     - TSX / Chromium
     - ``pnpm --filter @dev.fast/review-canvas exec playwright install chromium --only-shell``
     - ``pnpm --filter @dev.fast/review-canvas build``
     - ``test`` / ``test:node`` / ``test:browser``
     - ``test:browser:watch`` (headed); reload the Desktop window
   * - Desktop workbench (fork)
     - TS / Electron
     - Node 24.18.0 + native toolchain;
       ``bash apps/review-desktop/scripts/code-oss-dependencies.sh``
     - ``pnpm desktop:build`` (``pnpm dev`` for the fast path)
     - ``pnpm --filter @dev.fast/review-desktop test``; ``typecheck``;
       ``test:e2e:lsp``; ``test:e2e:telemetry``
     - ``pnpm desktop:watch``; ``DEV_FAST_REVIEW_REMOTE_DEBUGGING_PORT``;
       ``dev:background``
   * - Semantic diff (diffr)
     - Rust native (external)
     - ``pnpm --filter @dev.fast/review ensure:diffr``
     - In the ``devdotfast/diffr`` repository (``cargo build --locked``)
     - ``pnpm --filter @dev.fast/review test:integration:diffr``
     - ``REVIEW_DIFFR_BINARY=<local build>``; run ``diffr --format ndjson``
       by hand; ``diffr config show --json``
   * - Protocols
     - TS / Zod
     - —
     - ``pnpm --filter @dev.fast/review-protocol build`` (and trace/share)
     - ``… test``
     - ``pnpm --filter @dev.fast/review-desktop protocol:sync``
   * - Trace
     - TS / Node + optional ``aws`` CLI, hosted login
     - ``whiteboard login``; ``trace storage use s3|hosted``
     - ``pnpm --filter @dev.fast/trace-core build``
     - ``pnpm --filter @dev.fast/trace-core test``
     - ``whiteboard trace status [--session]``; ``trace repair``
   * - local-vcs
     - TS / Node + git, jj
     - —
     - ``pnpm --filter @dev.fast/local-vcs build``
     - ``… test``
     - —
   * - Agent plugins
     - JSON / JS / Markdown
     - Install Desktop, or build the CLI and link ``~/.local/bin/whiteboard``
     - None
     - ``agent-plugins.test.ts`` (in the review tests); MCP smoke test (see
       :doc:`verification_matrix`)
     - ``whiteboard_status`` tool; ``whiteboard instances``
   * - Latency harness
     - Python 3.12 / uv
     - ``cd scripts/review-latency``
     - —
     - ``uv run review-latency list`` / ``run``
     - ``render``, ``dashboards``
   * - Docs
     - Python / Sphinx
     - ``python3 -m pip install -r docs/requirements.txt``
     - ``sphinx-build -W -b html docs docs/_build/html``
     - Mermaid render check (see :doc:`verification_matrix`)
     - ``python3 docs/tools/component_registry.py`` regenerates the registry
