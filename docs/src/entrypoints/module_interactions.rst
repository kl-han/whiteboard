Module interactions
===================

Agent authoring sequence
------------------------

The requested sequence had the CLI "submit a request" that the server
forwards to the app. In the code, the MCP adapter is a **thin HTTP client**.
The server validates each edit, saves it as a version, and pushes it to
watchers. The canvas pulls updates over a watch stream. This diagram reflects
``review-api/mcp.ts``, ``agent-client.ts``, ``review-api/README.md`` and
``packages/review/instructions/authoring.md``:

.. mermaid::

   sequenceDiagram
       participant User
       participant Agent as Coding Agent
       participant MCP as whiteboard mcp (stdio)
       participant Server as Embedded Server (/reviews-api)
       participant VCS as local-vcs (git/jj)
       participant Store as review-api.db
       participant App as Desktop canvas
       User->>Agent: "Review my branch in Whiteboard"
       Agent->>MCP: session_get_instructions
       MCP->>Server: GET /instructions (token from discovery record)
       Server-->>Agent: authoring guide (instructions/authoring.md)
       Agent->>MCP: session_register_repository {path}
       MCP->>Server: POST /repositories
       Agent->>MCP: session_create {title, target}
       MCP->>Server: POST /commands {commandId, operation:create}
       Server->>VCS: resolve base/head to immutable commits
       Server->>Store: save version 0
       Server->>App: open new review (when Desktop attached)
       Agent->>MCP: session_activity begin (lease)
       Agent->>MCP: session_diff
       MCP->>Server: GET /:id/diff
       Server->>VCS: read committed objects
       loop incremental authoring
           Agent->>MCP: session_edit {insert/update/...}
           MCP->>Server: POST /commands {leaseId}
           Server->>VCS: validate review-source links and ranges
           Server->>Store: save version N with lastEdit
           Store-->>App: watch stream delivers version N
           App-->>User: courier draws the edit as it lands
       end
       Agent->>MCP: session_activity end
       App-->>User: review marked ready (lease ended)

Where each module sits
----------------------

* **The agent plugin** only tells the agent how to start ``whiteboard mcp``,
  or which ``whiteboard api`` command to run.
* **The MCP adapter** lists tools from the server (``GET /authoring``),
  renames ``review_*`` to ``session_*`` (``public-tools.ts``), and forwards
  each call. It never imports the store or validates content
  (``review-api/README.md``).
* **The server** owns validation, versioning, leases and source reads.
* **local-vcs** resolves revisions and reads committed objects. It never
  reads working-copy files for pinned reviews.
* **The canvas** renders snapshots and animates each version's ``lastEdit``.

Trace-linked explanation
------------------------

.. mermaid::

   sequenceDiagram
       participant Harness as Agent harness (Claude/Codex/OpenCode/Pi)
       participant Hook as whiteboard trace hook
       participant Git as Git hook / jj trailer
       participant Store as Trace store (local, S3/R2, hosted)
       participant Server as Embedded Server
       participant Agent as Authoring agent
       Harness->>Hook: session lifecycle events
       Hook->>Store: capture / sync session transcript
       Git->>Hook: commit made during a session
       Hook->>Store: associate session with commit
       Agent->>Server: session_get_instructions {topic:"trace-archaeology"}
       Agent->>Store: whiteboard trace show / blame / FFF search
       Agent->>Server: session_edit with trace quotes
       Server-->>Agent: quote validated against retained trace
