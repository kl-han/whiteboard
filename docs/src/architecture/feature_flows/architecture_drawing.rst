Architecture drawing
====================

The user asks an agent to explain a change; the agent draws it on the
Whiteboard.

.. mermaid::

   sequenceDiagram
       actor User
       participant Agent as Coding agent
       participant MCP as whiteboard mcp (Node)
       participant Srv as Embedded server (Node)
       participant DB as review-api.db
       participant Git as local-vcs (git/jj)
       participant WB as Workbench (renderer)
       participant Cv as Canvas (React)
       User->>Agent: "Review my branch in Whiteboard"
       Agent->>MCP: tools/call session_get_instructions
       MCP->>Srv: GET /reviews-api/instructions
       Agent->>MCP: session_register_repository {path}
       MCP->>Srv: POST /repositories
       Agent->>MCP: session_create {title, target, commandId}
       MCP->>Srv: POST /commands {operation:{type:"create"}}
       Srv->>Git: resolve base/head to commit ids (pins)
       Srv->>DB: version 0 + receipt
       Srv->>WB: open review (Desktop attached)
       Agent->>MCP: session_activity begin {leaseId, scope:"document"}
       loop each block
         Agent->>MCP: session_edit {sessionId, edit, leaseId, commandId}
         MCP->>Srv: POST /commands {operation:{type:"edit"}}
         Srv->>Git: validate review-source links and code ranges
         Srv->>DB: version N with lastEdit
         DB-->>Srv: data_version change (≤250 ms)
         Srv-->>Cv: /watch NDJSON line
         Cv-->>User: courier draws lastEdit
       end
       Agent->>MCP: session_activity end
       Cv-->>User: review marked ready

.. list-table::
   :widths: 25 75

   * - Initiating actor
     - The user, through a coding agent
   * - Entrypoint
     - ``whiteboard mcp`` (``review-api/mcp.ts``) or ``whiteboard api``
   * - Tools
     - ``session_get_instructions``, ``session_register_repository``,
       ``session_create``, ``session_activity``, ``session_diff``,
       ``session_edit``
   * - Internal handlers
     - ``callPublicTool`` → ``ReviewApiClient`` → ``http.ts`` →
       ``store.ts``, which validates with ``blocks/*`` and ``local-data.ts``
   * - Shared contracts
     - The tool catalog from ``GET /authoring``; block schemas; the
       ``review-source:`` link syntax
   * - Persistence
     - ``review-api.db`` (versions, receipts, authoring_sessions)
   * - Transitions
     - Agent → Node (stdio) → Node (HTTP) → SQLite; server → Chromium
       (NDJSON)
   * - Presentation
     - Canvas blocks and diagrams (React Flow + ELK), with live drawing
   * - Failure points
     - No live Desktop, so the agent sees only 2 tools. HTTP 409 lease
       conflicts. ``ReviewInputError`` on bad ranges or links. ``Use
       sessionId`` errors. A missing ``commandId`` gives "Invalid UUID".
