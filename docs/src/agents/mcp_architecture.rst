MCP architecture
================

``whiteboard mcp`` is a **thin, stateless stdio adapter** over the server's
HTTP API (``packages/review/src/review-api/mcp.ts``). Everything below is
CONFIRMED by code reading and the stdio smoke test, unless marked.

Lifecycle
---------

.. mermaid::

   sequenceDiagram
       participant Host as Agent host (Claude/Codex/Cursor/OpenCode)
       participant MCP as whiteboard mcp
       participant Disc as ~/.dev/review-desktop/instances
       participant Srv as Whiteboard server
       Host->>MCP: spawn sh -c 'exec $HOME/.local/bin/whiteboard mcp'
       Host->>MCP: initialize (protocol 2025-06-18)
       MCP-->>Host: serverInfo {name:"whiteboard"}, capabilities {tools:{listChanged:true}}
       Host->>MCP: tools/list
       MCP->>Disc: selectReviewInstance (latched key, if any)
       alt server reachable
         MCP->>Srv: GET /reviews-api/authoring (x-review-token)
         Srv-->>MCP: catalog (review_* names)
         MCP-->>Host: session_get_instructions + whiteboard_status + 26 more (renamed session_*)
       else unreachable
         MCP-->>Host: session_get_instructions + whiteboard_status only
         Note over MCP: announceCatalog = true, listedWhileDown = true
       end
       Host->>MCP: tools/call X {args}
       MCP->>Disc: rediscover (every call)
       MCP->>Srv: HTTP route for X (commandType → POST /commands)
       opt first success after being down
         MCP-->>Host: notifications/tools/list_changed
       end
       Srv-->>MCP: result
       MCP-->>Host: {content:[{type:"text", text}]} or {isError:true, ...}

Key properties
--------------

.. list-table::
   :widths: 28 72

   * - Process model
     - One child process per agent session, spawned by the host from the
       plugin's MCP config. stdin and stdout carry JSON-RPC; stderr carries
       diagnostics such as ``whiteboard mcp: Review server is not ready…``.
   * - State
     - None persisted. In memory: the last catalog, the ``announceCatalog``
       and ``listedWhileDown`` flags, and the **latched instance key**.
   * - Instance latch
     - "One session follows one instance key, through that Desktop's
       restarts; it never hops to another key once others start." The first
       successful connection latches it.
   * - Reconnection
     - No persistent connection. Each request calls ``connect(latched)``, so
       a restarted Desktop is picked up with no reconnect logic.
   * - Tool naming
     - The server's ``review_*`` names are renamed to ``session_*``, and
       ``reviewId`` becomes ``sessionId`` (``public-tools.ts``). Passing
       ``reviewId`` fails with "Use sessionId with session tools."
   * - Guidance delivery
     - The shared authoring guidance is prepended to the
       ``session_get_instructions`` *description*. Some clients prepend
       server instructions to every tool, so it lives there instead
       (``instructions`` is empty in ``initialize``).
   * - Hosts that ignore ``list_changed``
     - The first ``session_get_instructions`` result after a down-listing
       is prefixed with ``RELOAD_TOOLS``, which asks the agent to reconnect.
   * - Error model
     - Errors never become JSON-RPC errors. ``{isError:true,
       content:[text]}`` carries the message. Offline
       ``session_get_instructions`` returns ``RECOVERY`` text, and offline
       ``whiteboard_status`` returns an offline status object.
   * - Telemetry
     - ``onToolCall`` reports the tool name (catalog names only), ``via:
       "mcp"``, ok and duration.
   * - Headless use
     - ``whiteboard --state-dir D mcp``, or ``DEV_REVIEW_SERVER_DIR``,
       targets a headless server and bypasses Desktop discovery.
   * - Trust
     - The agent runs as the local user. Access is gated only by the
       loopback token in a private discovery file. The server validates
       every input; the adapter validates none.

Installed vs. development instances
-----------------------------------

The plugin command runs ``~/.local/bin/whiteboard``, the shim Desktop
installs. Standalone and dev CLIs delegate to the Desktop-bundled CLI,
**except** for ``mcp``, ``api``, ``server`` and ``instances``. Those run in
the invoking CLI because "their tool catalog comes from the server". To aim
an agent at a dev build, set ``DEV_REVIEW_INSTANCE=<dev key>`` in the shell
you start the agent from, or run ``whiteboard instances use <key>``, then
reconnect MCP (``CONTRIBUTING.md``).
