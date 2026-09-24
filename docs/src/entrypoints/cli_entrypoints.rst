CLI entrypoints
===============

Binaries
--------

``packages/review/package.json`` declares two bins with the same target:
``whiteboard`` and ``review`` → ``dist/cli.js``. From a checkout, run
``pnpm review <args>`` or ``pnpm --filter @dev.fast/review whiteboard <args>``.
Both run ``tsx src/cli.ts``.

Bootstrap (``src/cli.ts``, confirmed)
-------------------------------------

1. **Delegation.** A *built* standalone CLI (``…/dist/cli.js``) hands the
   whole command to the CLI bundled with the selected running Desktop, so
   the CLI version never drifts from the server's. It prefers the app's
   Electron-as-Node runtime (``ELECTRON_RUN_AS_NODE=1``). Delegation is
   skipped for ``api``, ``mcp``, ``server`` and ``instances``, for
   ``--state-dir``, and when ``DEV_FAST_REVIEW_CLI_NO_DELEGATE`` is set.
   Checkout runs through ``tsx`` never delegate.
2. **Node floor check.** A system Node older than 24 gets a clear message.
   Electron's runtime is trusted as it is.
3. ``runReviewCli`` in ``cli-runner.ts`` builds the Commander program named
   ``whiteboard``. Every command accepts ``--json``, which switches stdout
   to one JSON event per line.
4. A ``preAction`` hook records a telemetry ``command`` start and sets trace
   attributes (``commandRunId``).

Command map
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Command
     - Purpose
     - Defined in
   * - ``server start`` / ``server status``
     - Foreground headless authoring server and its readiness check
     - ``cli-runner.ts`` → ``server/headless-host.ts``
   * - ``version [--verbose]``
     - Package version and runtime info
     - ``cli-runner.ts``, ``cli-runtime-info.ts``
   * - ``app`` / ``app launch [--focus]`` / ``app pick [--session|--review] [--view]``
     - Start Desktop in the background, or open a review in a tab
     - ``review-app.ts``, ``review-app-launcher.ts``, ``review-app-picker.ts``
   * - ``instances`` / ``instances use <key>`` / ``instances clear``
     - List Desktops and choose the machine default
     - ``review-instances.ts``, ``desktop-discovery.ts``
   * - ``info [--all]``
     - List active reviews bound to this worktree (read-only)
     - ``review-info.ts``
   * - ``connect [target…]``
     - Print the prompt that connects a coding agent
     - ``connect-prompts.ts``
   * - ``migrate apply [--force]``
     - Migrate legacy review data
     - ``migrate.ts``
   * - ``share`` / ``share revoke <id>``
     - Upload an immutable snapshot and return a link
     - ``sharing/cli.ts``
   * - ``login`` / ``logout`` / ``whoami``
     - GitHub login for sharing and the hosted trace store
     - ``cli-runner.ts``, ``trace-core/store-auth.ts``
   * - ``trace …`` (``storage use``, ``config migrate``, ``enable``,
       ``disable``, ``repair``, ``status``, ``sessions``, ``show``, ``sync``,
       ``pull``, ``blame``, ``allow``/``deny``, ``uninstall-hooks`` …)
     - Agent trace capture and reading
     - ``trace-cli.ts``, ``trace-storage-cli.ts``, ``trace-core/src/trace-*commands.ts``
   * - ``api <tool> '<json>'`` / ``api tools``
     - Call one authoring tool over HTTP
     - ``review-api/agent-cli.ts``
   * - ``mcp``
     - Serve the same tools over stdio MCP
     - ``review-api/mcp.ts``

``install`` also exists for headless environments (``install.ts`` and
``cli-install.ts``). Desktop normally performs installation itself.

How package scripts map to runtime behavior
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Script
     - Runtime effect
   * - ``pnpm review …`` (root)
     - ``pnpm --filter @dev.fast/review review`` → ``tsx src/cli.ts``
   * - ``pnpm --filter @dev.fast/review build``
     - Its ``prebuild`` builds the workspace dependencies. Then tsdown emits
       ``dist/cli.js``, ``dist/server/desktop-host.js`` and the other entries.
   * - ``pnpm desktop:run``
     - ``run.sh`` rebuilds the stale review server and canvas, then launches
       Electron. Electron runs ``dist/server/desktop-host.js``.
   * - ``node scripts/pack-review-cli.mjs``
     - Packs the npm tarball published by ``review-cli-release.yml``
