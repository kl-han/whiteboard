Server entrypoints
==================

Two hosts, one API
------------------

``packages/review/src/review-api/README.md`` states: "Desktop and
``review server start`` share ``review-api.db`` under ``DEV_REVIEW_HOME``."
Both hosts mount the same routes, with token authentication and a bounded
JSON request reader.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Desktop host (``desktop-host.ts`` / ``desktop-server.ts``)
     - Headless host (``headless-host.ts``)
   * - Started by
     - Electron ``UtilityProcess`` (supervised and restarted)
     - ``whiteboard server start`` (foreground; stop with Ctrl-C or SIGTERM)
   * - State
     - ``$DEV_REVIEW_HOME`` (default ``~/.dev``)
     - ``--state-dir`` / ``DEV_REVIEW_SERVER_DIR``, locked with ``headless-server.lock``
   * - Discovery
     - ``review-desktop/instances/<key>.json``, written atomically and privately
     - ``review-server`` record in the state directory
   * - HTTP framework
     - Hono on Node ``http``, with SSE for some streams
     - Hono via ``createNodeRequestListener``
   * - Extra duties
     - Workspace preparation and cleanup, CLI and skill install, tutorial,
       structural diff, bug and crash reports, UI telemetry relay, sharing
     - Sharing publisher; no workspace manager
   * - Port
     - ``DEV_FAST_REVIEW_SERVER_PORT`` (``0`` = OS-chosen)
     - ``--port`` (default ``0``)

Confirmed by running it (see :doc:`../devops/verification_results`):
``server start`` prints ``Review server ready at http://127.0.0.1:<port>``
and creates ``review-api.db``, ``headless-server.lock`` and a
``review-server`` discovery file.

Configuration loading
---------------------

* **Paths**: ``review-home-paths.ts`` (``devReviewHome``,
  ``reviewInstanceDiscoveryPath``, ``reviewLegacyDiscoveryPath``).
  ``cli.ts`` keeps its own copy of the path logic, because it runs before
  the Node version check.
* **Preferences**: ``review-preferences.ts`` (for example the scratchpad
  flag).
* **Telemetry**: ``telemetry-config.ts`` and the environment variables in
  ``docs/telemetry.md``. The Desktop host strips
  ``DEV_FAST_REVIEW_TELEMETRY_DISABLED`` from its telemetry environment and
  uses the in-app setting instead.
* **Trace storage**: ``$DEV_REVIEW_HOME/trace/config.json``
  (``packages/review/README.md``).
* **Review guidance**: ``DEV-REVIEW.md`` at the repository root takes
  precedence over ``$DEV_REVIEW_HOME/DEV-REVIEW.md``.
* **diffr**: ``REVIEW_DIFFR_BINARY``, the bundled ``bin/diffr``, then
  ``diffr`` on ``PATH`` (``server/structural-diff.ts``).

Main routes (from ``review-api/README.md``)
-------------------------------------------

All paths are relative to ``/reviews-api``: ``GET /`` (catalog),
``GET /watch`` (NDJSON), ``GET /:id/inspect``, ``POST /commands`` (create,
edit, rename, repin, restore, lens, attention, delete),
``POST /:id/activity`` (authoring lease), ``POST /repositories``,
``POST /pins``, ``POST /resources``, ``POST /:id/source``,
``GET /:id/file|tree|diff|commits``, and ``POST /:id/open``.
``GET /authoring`` returns the tool catalog that both ``api`` and ``mcp``
adapt.
