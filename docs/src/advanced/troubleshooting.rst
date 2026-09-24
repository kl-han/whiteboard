Troubleshooting
===============

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Symptom
     - Likely cause
     - Fix
   * - ``ERR_PNPM_UNSUPPORTED_ENGINE`` or "Whiteboard needs Node.js 24"
     - Wrong Node version
     - ``nvm use 24``. The fork additionally needs ``24.18.0``.
   * - ``Failed to create bin … dist/cli.js`` during install
     - The CLI is not built yet
     - Harmless. Run ``pnpm run build``.
   * - ``tsgo: not found`` in ``pnpm typecheck``
     - The Code - OSS npm dependencies are missing
     - ``bash apps/review-desktop/scripts/code-oss-dependencies.sh`` or
       ``pnpm desktop:build``
   * - ``gyp … electronjs.org/headers … Request was cancelled``
     - Network egress blocked during the fork's native module build
     - Allow ``electronjs.org`` (and the extension marketplaces), or build
       elsewhere
   * - ``Executable doesn't exist at …/chromium_headless_shell-XXXX``
     - The Playwright browser build does not match the pinned version
     - ``pnpm --filter @dev.fast/review-canvas exec playwright install chromium --only-shell``
   * - ``fatal: detected dubious ownership`` in legacy fixture tests
     - Tests run as a user other than the repository owner (for example
       root in a container)
     - Run as the owner, or set ``safe.directory`` in a disposable
       environment
   * - ``Review Desktop binary is not built``
     - ``desktop:run`` ran before a build
     - ``pnpm desktop:build`` (or ``pnpm dev``)
   * - ``review`` opens a browser or shows old options
     - A legacy CLI shadows the current one on ``PATH``
     - ``command -v review``; put ``~/.local/bin`` first (``packages/review/README.md``)
   * - The agent sees only ``session_get_instructions``
     - The agent listed tools before Whiteboard started
     - Reconnect the ``whiteboard`` MCP server or start a new agent session
   * - Commands talk to the wrong Desktop (dev vs. installed)
     - Instance selection
     - ``whiteboard instances``; ``whiteboard instances use <key>`` or
       ``DEV_REVIEW_INSTANCE``; then reconnect MCP
   * - ``Use sessionId with session tools.``
     - ``reviewId`` was passed to a ``session_*`` tool
     - Rename the field to ``sessionId``
   * - ``Invalid UUID → at commandId``
     - Mutating tools need a UUID ``commandId``
     - Generate one per logical command, and reuse it on retry
   * - HTTP 409 on edit
     - Another authoring lease owns that scope
     - Wait up to 3 minutes for expiry, or use the owning ``leaseId``
   * - ``Cannot find diffr``
     - The structural diff binary is missing
     - ``pnpm --filter @dev.fast/review ensure:diffr``, or set
       ``REVIEW_DIFFR_BINARY``
   * - A review whose checkout is missing opens degraded
     - The repository moved or was deleted
     - Re-register the path. The review degrades instead of failing (#355).
   * - Mermaid diagrams show as code in these docs
     - ``sphinxcontrib-mermaid`` is not installed
     - ``python3 -m pip install -r docs/requirements.txt``
