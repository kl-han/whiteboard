Trace-linked decision log
=========================

An agent's past session becomes a quote on the Whiteboard that is checked
against the retained transcript.

.. mermaid::

   sequenceDiagram
       participant H as Agent harness
       participant Hook as whiteboard trace (hooks)
       participant G as git prepare-commit-msg
       participant S as Trace store (app.dev.fast or S3/R2)
       participant A as Authoring agent
       participant Srv as Embedded server
       participant Cv as Canvas
       H->>Hook: session lifecycle hook (Claude/Codex settings, Pi extension, OpenCode plugin)
       G->>Hook: whiteboard trace git-hook prepare-commit-msg
       Hook-->>G: Agent-Session: ID trailer
       Hook->>S: sync session (gzip, presigned URL or aws s3api)
       A->>Srv: session_get_instructions {topic:"trace-archaeology"}
       A->>Hook: whiteboard trace blame FILE -L a,b --json
       A->>S: whiteboard trace pull --agent-session ID
       S-->>A: normalized JSONL under ~/.dev/trace-search (sha256-checked)
       A->>A: FFF search, then whiteboard trace show
       A->>Srv: session_upload {kind:"trace", trace:{label, events}}
       A->>Srv: session_edit insert trace_quote {traceId, eventId, text}
       Srv->>Srv: textIncludesQuote(event.text, quote)?
       Srv-->>Cv: version with trace_quote
       Cv-->>A: (user sees the quote, Trace tab reads the resource)

.. list-table::
   :widths: 25 75

   * - Initiating actor
     - The agent harness (capture); the authoring agent (use)
   * - Entrypoints
     - Harness hooks and Git hooks → ``whiteboard trace …``
       (``trace-core``); ``session_upload`` and ``session_edit``
   * - Shared contracts
     - ``@dev.fast/trace-protocol`` (hosted store); the ``Agent-Session``
       trailer; the ``trace_quote`` block ``{traceId, eventId, text}``
   * - Persistence
     - The remote store; ``~/.dev/trace-search``; Git notes
       ``refs/notes/dev-fast/*``; a ``resources`` row (immutable trace
       bytes)
   * - Transitions
     - Harness → shell hook → Node CLI → HTTPS or the ``aws`` CLI; agent →
       MCP → server → SQLite → canvas
   * - Presentation
     - Inline quotes and the Trace tab (``ReviewTraceView.tsx``)
   * - Failure points
     - No consent or storage configured: capture stays off. A missing
       hosted login gives "Run ``review login``". The quote does not match
       ("Quote does not match the retained trace event."). The trace store
       is unreachable. FFF is not installed (human-owned setup).
