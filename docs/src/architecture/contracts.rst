Contract map
============

Every contract below crosses a process, package or repository boundary.

.. mermaid::

   flowchart LR
       Server["Server (packages/review)"] -- "Tool catalog GET /authoring" --> MCP["MCP / api adapters"]
       MCP -- "MCP JSON-RPC" --> Agent["Agents"]
       Server -- "REST + NDJSON /reviews-api" --> Canvas["Canvas"]
       Server -- "REST + NDJSON" --> Fork["Fork services"]
       Server -- "ready event + discovery v3" --> Main["Electron main / CLI"]
       Diffr["diffr"] -- "NDJSON wire v4" --> Server
       TraceCore["trace-core"] -- "trace-protocol 0.5.0" --> Hosted["Hosted store"]
       Share["sharing"] -- "review-share-protocol 0.1.1" --> Hosted
       Server -- "stored JSON schema + migrations" --> DB[("review-api.db")]
       RP["review-protocol src"] -- "generated reviewProtocol.ts" --> Fork

.. list-table::
   :header-rows: 1
   :widths: 14 12 11 12 12 13 13 13

   * - Contract
     - Owner
     - Serialization
     - Versioning
     - Compatibility
     - Validation
     - Tests
     - Failure behavior
   * - review-protocol (discovery, CLI install, bug report, code peek, structural diff)
     - ``packages/review-protocol`` (private)
     - JSON / Zod
     - ``REVIEW_DESKTOP_DISCOVERY_VERSION = 3``; the rest is unversioned
       (shipped together)
     - The discovery schema tolerates unknown keys; "readers must ignore
       fields they do not understand"
     - Zod on both sides
     - 76 tests
     - Rejects an unsupported discovery version
   * - Generated fork protocol
     - Generated from review-protocol by ``generate-native-source.mjs``
     - TS source
     - Regenerated each build (``protocol:sync``)
     - Always matches (built together)
     - Typecheck
     - Desktop tests
     - Stale if ``protocol:sync`` is skipped
   * - MCP tool catalog (``session_*``)
     - ``authoring-tools.ts`` + ``public-tools.ts``
     - JSON Schema (from Zod)
     - Implicit; served live by the server
     - Adapters "cannot skew" (the catalog comes from the server)
     - Server-side Zod
     - ``public-tools.test.ts``, MCP smoke test
     - ``isError`` text results
   * - Server REST API ``/reviews-api``
     - ``review-api/http.ts``
     - JSON; NDJSON streams
     - None explicit
     - The CLI delegates to the Desktop-bundled CLI to avoid skew
     - Zod query and command schemas
     - ``review-api.test.ts``
     - 4xx ``{error}``, 409, 500
   * - Canvas watch
     - ``http.ts`` ``/watch``
     - NDJSON arrays of ``{value}|{error}|null``
     - None
     - A reconnect restarts from the snapshot
     - Client decode
     - Canvas tests
     - An error row per subscription
   * - Desktop ↔ server ready event and IPC
     - ``reviewDesktopBootstrap.ts``
     - A JSON line on stdout; IPC objects
     - None (same build)
     - Same build
     - ``ReviewReadyEventReader``
     - ``reviewServerSupervisor.test.ts``
     - Startup fails or restarts
   * - diffr NDJSON
     - ``devdotfast/diffr`` (``src/protocol/mod.rs``); mirrored by ``@dev.fast/diffr``
     - NDJSON
     - ``STRUCTURAL_DIFF_WIRE_VERSION = 4`` + an exact npm pin
     - Cross-repository checklist in the diffr README
     - Zod per line; first line must be version 4
     - ``test:integration:diffr`` (9)
     - Throws "Unsupported diffr stream protocol."
   * - trace-protocol
     - ``packages/trace-protocol`` (published 0.5.0)
     - JSON / Zod; gzipped objects
     - The npm version must match the server **exactly**; tag
       ``trace-protocol-v<version>``
     - Additive minor releases (for example 0.4 added
       ``listUploadsQuerySchema``)
     - Zod
     - 17 tests
     - ``StoreApiError``
   * - review-share-protocol
     - Published 0.1.1
     - JSON envelope
     - The package version
     - Immutable bundles
     - Zod
     - 5 tests
     - Import rejection
   * - Stored review format
     - ``store.ts``, ``stored-*-migration.ts``, ``review-import``
     - SQLite + JSON snapshots
     - ``REVIEW_SCHEMA_VERSION``
     - Migrations and legacy import; golden fixtures
     - Strict block schemas
     - Legacy fixture tests; ``test:legacy-corpus``
     - The version is rejected; the importer reports what needs an agent
   * - ``review-source:`` links
     - The server Markdown parser
     - URL syntax in Markdown
     - None
     - Stable syntax
     - Checked against pinned source before save
     - ``source-links.test.ts``
     - The edit is rejected
   * - Agent-Session trailer / Git notes
     - trace-core
     - Commit trailer; ``refs/notes/dev-fast/*``
     - None
     - Survives squash merges through a PR scan (#61)
     - —
     - trace-core tests
     - Provenance is missing
