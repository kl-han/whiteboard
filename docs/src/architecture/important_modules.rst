Important modules
=================

"Kind" uses these labels: core logic, interface, infrastructure, protocol,
agent integration, tooling or configuration. "Basis" says whether the
description is **confirmed** (read in code or docs, or executed) or
**inferred**.

.. list-table::
   :header-rows: 1
   :widths: 18 26 20 14 12 10

   * - Module
     - Responsibility and main exports
     - Depends on → / ← depended on by
     - Kind
     - Behavior checked by
     - Basis
   * - ``packages/review/src/review-api/store.ts``, ``document.ts``
     - The JSON review store on SQLite: reviews, versions, receipts,
       repositories, resources, attention, authoring sessions (leases).
       Throws ``ReviewInputError`` for errors that are safe to show clients.
     - → local-vcs, review-protocol, json · ← http.ts, both hosts
     - Core logic
     - ``review-api.test.ts``, ``authoring-session.test.ts``
     - Confirmed
   * - ``review-api/http.ts`` (``createReviewApi``)
     - Hono routes under ``/reviews-api`` (see :doc:`../entrypoints/server_entrypoints`)
     - → store, local-data, traces · ← desktop-server, headless-host
     - Interface
     - Headless smoke test
     - Confirmed
   * - ``review-api/authoring-tools.ts``, ``public-tools.ts``
     - The tool catalog (``review_*`` internally, ``session_*`` publicly),
       with Zod input schemas mapped to HTTP routes
     - → read-schemas, store schemas · ← mcp.ts, agent-cli.ts
     - Agent integration
     - ``public-tools.test.ts``; ``api tools`` run
     - Confirmed
   * - ``review-api/mcp.ts``, ``agent-cli.ts``, ``agent-client.ts``
     - Thin stdio MCP and CLI adapters. They discover a server, attach its
       token, and forward calls.
     - → desktop-discovery, server-discovery, MCP SDK
     - Agent integration
     - ``agent-client.test.ts``
     - Confirmed
   * - ``review-api/instructions.ts`` + ``packages/review/instructions/*.md``
     - Serves the authoring guide and the ``file-lenses``, ``scratchpad``
       and ``trace-archaeology`` topics
     - ← ``session_get_instructions``
     - Agent integration
     - ``instructions.test.ts``
     - Confirmed
   * - ``src/server/desktop-host.ts``, ``desktop-server.ts``
     - The process entry for Desktop's server. Owns discovery, CLI install,
       tutorial, bug and crash reports, UI telemetry and structural diff.
     - → review-api, sharing, trace-core · ← Electron supervisor
     - Infrastructure
     - ``desktop-server-*.test.ts``
     - Confirmed
   * - ``src/server/headless-host.ts``
     - A foreground server per state directory, with a file lock
     - → review-api, sharing · ← ``server start``
     - Infrastructure
     - Run in verification
     - Confirmed
   * - ``src/server/structural-diff.ts``
     - Runs ``diffr`` and streams validated records
     - → ``@dev.fast/diffr`` binary · ← desktop-server, reviewStructuralDiff*
     - Core logic (semantic diff)
     - ``structural-diff.test.ts``
     - Confirmed
   * - ``src/desktop-discovery.ts``, ``review-instances.ts``
     - Chooses the active Desktop instance and manages the machine default
     - → review-home-paths · ← cli, agent-client
     - Infrastructure
     - ``desktop-discovery.test.ts``
     - Confirmed
   * - ``src/sharing/*`` + ``review-share-protocol``
     - Publishes and imports immutable review bundles, with GitHub auth
     - → local-vcs · ← CLI ``share``, desktop-server
     - Core logic + protocol
     - ``sharing/*.test.ts``
     - Confirmed
   * - ``src/review-import/*``, ``migrate.ts``, ``stored-*-migration.ts``
     - Migration from legacy MDX and older schemas into JSON
     - ← startup importer, ``migrate apply``
     - Core logic (migration)
     - ``legacy-review-fixtures.test.ts`` (golden files)
     - Confirmed
   * - ``review-telemetry.ts``, ``ui-telemetry-events.ts``, ``error-telemetry.ts``
     - PostHog events, the cleaned error payloads and the telemetry-off
       rules
     - → posthog-capture-client · ← CLI, servers, canvas relay
     - Infrastructure (telemetry)
     - ``*telemetry*.test.ts``, ``test:telemetry-privacy``
     - Confirmed
   * - ``packages/review/app`` (canvas)
     - React rendering of documents, diagrams (React Flow + ELK), traces,
       commits and diffs; the courier live-draw animation
     - → review-protocol, review (types) · ← Desktop webviews
     - Interface (UI)
     - 517 canvas tests (unit + browser)
     - Confirmed
   * - ``code-oss/src/vs/review/electron-main``
     - Server supervisor, menubar, crash dumps, update dialog, background
       launch
     - → common/reviewDesktopBootstrap · ← Code - OSS main
     - Infrastructure (desktop shell)
     - ``reviewServerSupervisor.test.ts``
     - Confirmed
   * - ``code-oss/src/vs/review/services``
     - Connects the workbench to the API: catalog, source, diff views,
       structural diff client, lenses, editor tabs
     - → generated reviewProtocol · ← contrib, canvas host
     - Interface
     - desktop ``test`` (197 tests)
     - Confirmed
   * - ``packages/review-protocol``
     - Zod contracts shared by the server, canvas and fork (discovery, CLI
       install, bug report, code-peek diff, structural diff). Re-exports
       ``@dev.fast/diffr``.
     - → json, trace-protocol, diffr · ← everything above
     - Protocol
     - 76 tests
     - Confirmed
   * - ``packages/trace-core``
     - Trace hooks per harness, Git and jj integration, storage (S3/R2 and
       hosted), sync, read, consent, upload status
     - → trace-protocol, local-vcs, json · ← review CLI, servers
     - Core logic (trace)
     - 250 tests
     - Confirmed
   * - ``packages/trace-protocol``
     - Schemas, limits, route builders and matchers for the hosted trace store
     - → zod · ← trace-core, the hosted store (external)
     - Protocol
     - 17 tests
     - Confirmed
   * - ``packages/local-vcs``
     - The ``LocalVcs`` interface over Git and jj: ``detectLocalVcs``,
       ``resolveRevision``, ``mergeBase``, ``defaultBase``, ``diff``, blob
       batch reader, file locks, notes
     - → git-url-parse, proper-lockfile · ← review, trace-core
     - Infrastructure (VCS)
     - 69 tests
     - Confirmed
   * - ``packages/json``
     - JSON value types and guards (``jsonObject``, ``jsonString``,
       ``parseJsonText``) for decoding at the boundary (#103)
     - → zod · ← most packages
     - Utility
     - typecheck
     - Confirmed
   * - ``packages/agent-plugins/*``
     - Connector manifests for five agents
     - → the installed ``whiteboard`` shim
     - Agent integration / configuration
     - ``agent-plugins.test.ts``
     - Confirmed
   * - ``tools/oxlint/anti-slop``
     - Custom lint rules (for example ``no-array-filter-map`` and
       ``no-chained-type-assertions``)
     - ← ``.oxlintrc.json`` ``jsPlugins`` (``./tools/oxlint/anti-slop/index.ts``)
     - Tooling
     - ``pnpm lint``
     - Confirmed
