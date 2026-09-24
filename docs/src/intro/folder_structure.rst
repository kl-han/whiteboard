Folder structure
================

This page covers the directories that matter and what each one owns. It is not
a full file listing.

.. code-block:: text

   whiteboard/
   ├── apps/review-desktop/        Desktop app: Code - OSS fork + build/package scripts
   │   ├── code-oss/               Vendored VS Code (upstream 8a7abeba) — mostly upstream
   │   │   └── src/vs/review/      Whiteboard-owned workbench code (electron-main, services, contrib)
   │   └── scripts/                build.sh, run.sh, package-*.sh, e2e/, protocol-sync.mjs
   ├── packages/
   │   ├── review/                 @dev.fast/review: `whiteboard` CLI, embedded server, JSON API, MCP
   │   │   ├── src/                Node runtime (CLI, server/, review-api/, sharing/, telemetry)
   │   │   ├── app/                @dev.fast/review-canvas: React canvas built with Vite
   │   │   ├── instructions/       Markdown served to agents by session_get_instructions
   │   │   └── tutorial/           Onboarding sample review (document.json, trace.json …)
   │   ├── review-protocol/        Shared Zod contracts between server, canvas and desktop fork
   │   ├── review-share-protocol/  Portable, immutable review sharing envelope (published to npm)
   │   ├── trace-core/             Agent trace capture, hooks, storage, hosted-store client
   │   ├── trace-protocol/         Contract with the hosted trace store (published to npm)
   │   ├── local-vcs/              Git and Jujutsu helpers (published to npm)
   │   ├── json/                   Small JSON value helpers used at decode boundaries
   │   ├── agent-plugins/          Claude, Codex, Cursor, OpenCode, Pi connectors
   │   └── progressive-review/     Remnant of the original main package (renamed in #259)
   ├── scripts/                    CLI release, packing, smoke and clean scripts (+ tests)
   ├── tools/oxlint/anti-slop/     Custom oxlint JS plugin rules (vendored from dmmulroy/anti-slop)
   ├── docs/                       privacy.md, telemetry.md, README assets, this Sphinx site
   ├── .github/workflows/          CI, desktop preview/release, CLI release, Linux packaging
   ├── .claude-plugin/, .agents/   Plugin marketplace manifests for Claude Code and Codex
   └── package.json, pnpm-workspace.yaml, tsconfig.base.json, .oxlintrc.json, .oxfmtrc.json

Important modules
-----------------

``packages/review`` — the heart of the system
   This package builds five tsdown entries (``tsdown.config.ts``):
   ``src/cli.ts`` (the ``whiteboard`` and ``review`` bins),
   ``src/server/desktop-host.ts`` (the server that Desktop runs),
   ``src/runtime.ts``, ``src/sharing/index.ts`` and
   ``src/software-map-model.ts``. Its most important subdirectories:

   * ``src/review-api/``: the JSON review store (SQLite ``review-api.db``),
     HTTP routes (``http.ts``), authoring tools (``authoring-tools.ts``,
     ``public-tools.ts``), the MCP adapter (``mcp.ts``) and the CLI adapter
     (``agent-cli.ts``).
   * ``src/server/``: the Desktop host (``desktop-host.ts`` and
     ``desktop-server.ts``), the headless host (``headless-host.ts``),
     structural diff through ``diffr``, bug reports, crash reports and
     telemetry plumbing.
   * ``src/sharing/``: publishing and importing immutable shared reviews.
   * ``src/review-import/``: migration of legacy MDX reviews into the JSON
     store.

``packages/review/app`` — the canvas
   A React 19 app (``@xyflow/react``, ``elkjs``, ``zustand``), built by Vite
   from ``desktop.vite.config.ts``. ``apps/review-desktop/scripts/copy-canvas.mjs``
   copies it into Desktop. It renders documents (``api-document.tsx`` and
   ``blocks.tsx``), diagrams, traces (``ReviewTraceView.tsx``), commits and
   diffs.

``apps/review-desktop/code-oss/src/vs/review`` — the desktop integration
   Whiteboard-owned code inside the fork:

   * ``electron-main/reviewServerSupervisor.ts`` starts and restarts the
     embedded server in an Electron ``UtilityProcess``.
   * ``services/`` holds API catalog and source services, diff views,
     structural diff and lenses.
   * ``contrib/`` holds install, settings, sharing, telemetry, update and
     verbs.

   The fork's copy of the protocol, ``common/reviewProtocol.ts``, is
   generated from ``packages/review-protocol`` by ``protocol:sync``. It is
   not committed.

``packages/trace-core`` and ``packages/trace-protocol``
   Trace capture hooks for Claude, Codex, OpenCode and Pi
   (``agent-trace-hooks.ts``), Git hook and Jujutsu trailer integration
   (``trace-repository-hooks.ts`` and ``trace-git-hook-runner.ts``), S3/R2
   and hosted storage (``trace-storage/``, ``store-client.ts``), and trace
   reading and search. ``trace-protocol`` holds only schemas, limits and
   route builders.

``packages/local-vcs``
   A ``LocalVcs`` interface over Git and Jujutsu (``jj``). It provides
   revision resolution, merge base, diffs, blob batch reads, file locks and
   Git notes.

``packages/agent-plugins``
   Manifest-only connectors. Claude, Codex and Cursor each have a
   ``plugin.json`` and an MCP config that runs
   ``$HOME/.local/bin/whiteboard mcp``. OpenCode has a small JS plugin that
   injects the same MCP server. Pi has a ``SKILL.md`` that runs
   ``whiteboard api``.

Build outputs you will see locally
----------------------------------

* ``packages/*/dist/``: tsdown and tsc output (git-ignored).
* ``packages/review/bin/diffr``: fetched by ``ensure:diffr`` (git-ignored).
* ``packages/review/tutorial/.bundle``: tutorial assets from
  ``ensure:tutorial-assets``.
* ``apps/review-desktop/code-oss/out`` and ``.build``: Code - OSS compile
  output and the downloaded Electron.
* ``~/.dev/``: runtime state (``DEV_REVIEW_HOME``). See
  :doc:`../architecture/descriptive_language`.
