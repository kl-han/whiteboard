Component interactions
======================

This graph shows **build-time and runtime dependencies** between packages. We
built it from ``package.json`` dependencies, imports and scripts. The
requested draft had ``Agent plugins → CLI → Server → Canvas``. In the code,
the canvas is a separate bundle that *reads from* the server, and Desktop
hosts both.

.. mermaid::

   flowchart TD
       AgentPlugins[packages/agent-plugins] -->|"runs whiteboard mcp / api"| ReviewCLI[packages/review CLI<br/>src/cli.ts]
       ReviewCLI -->|"HTTP + token (discovery)"| ReviewServer[packages/review server<br/>src/server + src/review-api]
       ReviewCLI -->|"server start"| ReviewServer
       ReviewCanvas["packages/review/app<br/>@dev.fast/review-canvas"] -->|"HTTP/NDJSON watch"| ReviewServer
       ReviewServer --> ReviewProtocol[packages/review-protocol]
       ReviewCanvas --> ReviewProtocol
       ReviewServer --> ShareProtocol[packages/review-share-protocol]
       ReviewServer --> TraceCore[packages/trace-core]
       ReviewCLI -->|"trace commands"| TraceCore
       TraceCore --> TraceProtocol[packages/trace-protocol]
       ReviewProtocol --> TraceProtocol
       ReviewServer --> LocalVCS[packages/local-vcs]
       TraceCore --> LocalVCS
       ReviewServer -->|spawns| Diffr["diffr binary<br/>@dev.fast/diffr"]
       ReviewProtocol --> Json[packages/json]
       TraceCore --> Json
       DesktopApp[apps/review-desktop] -->|"UtilityProcess: dist/server/desktop-host.js"| ReviewServer
       DesktopApp -->|"copy-canvas.mjs"| ReviewCanvas
       DesktopApp -->|"protocol-sync.mjs (generated)"| ReviewProtocol
       DesktopApp --> CodeOSS[Vendored Code - OSS]
       Scripts[scripts/] -->|"pack, release, smoke"| ReviewCLI
       Scripts --> Workspace[Monorepo tooling]

Edge notes
----------

* **agent-plugins → CLI**: manifests run ``$HOME/.local/bin/whiteboard mcp``
  (Claude, Codex, Cursor, OpenCode) or ``whiteboard api`` (Pi skill).
* **CLI → server**: ``agent-client.ts`` reads the discovery record for the
  URL and token. ``server start`` runs the headless host in-process.
* **canvas → server**: the canvas uses ``review-api-client.ts`` from
  review-protocol and watch streams. It never touches the store directly.
* **server → review-protocol / share-protocol**: these are the shared Zod
  contracts. tsdown bundles the workspace libraries into ``dist/``. They are
  listed as dev dependencies of ``@dev.fast/review``
  (``packages/review/README.md``).
* **server and CLI → trace-core**: trace commands, and trace lookups for
  quotes and the Trace tab. trace-core also runs standalone, through hooks.
* **trace-core → trace-protocol**: the contract for the hosted store.
  review-protocol also depends on trace-protocol for the trace types.
* **→ local-vcs**: revision resolution, diffs and blob reads. The
  ``pnpm-workspace.yaml`` override makes the published range resolve to the
  workspace copy.
* **server → diffr**: a child process (``structural-diff.ts``).
  ``@dev.fast/diffr`` also provides TypeScript types, re-exported by
  review-protocol.
* **desktop → server**: the supervisor starts
  ``packages/review/dist/server/desktop-host.js`` (``run.sh`` sets
  ``REVIEW_SERVER``).
* **desktop → canvas**: ``copy-canvas.mjs`` copies the Vite build into the
  fork.
* **desktop → review-protocol**: ``protocol-sync.mjs`` generates
  ``code-oss/src/vs/review/common/reviewProtocol.ts``. The build script
  bundles the native runtime from
  ``packages/review-protocol/scripts/bundle-native-runtime.mjs``.
* **scripts → CLI**: ``pack-review-cli.mjs``, ``review-cli-release.mjs`` and
  ``smoke-review-cli.mjs`` power the CLI release workflow.
  ``clean-review-desktop.mjs`` backs ``pnpm clean``.
