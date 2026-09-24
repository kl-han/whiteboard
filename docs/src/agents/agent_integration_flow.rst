Agent integration flow
======================

How a coding agent connects (confirmed)
---------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - Agent
     - Artifact in this repository
     - Mechanism
   * - Claude Code
     - ``packages/agent-plugins/claude/.claude-plugin/plugin.json``, ``.mcp.json``;
       marketplace ``.claude-plugin/marketplace.json`` (``devfast``)
     - MCP server ``whiteboard``: ``sh -c 'exec "$HOME/.local/bin/whiteboard" mcp'``
   * - Codex
     - ``packages/agent-plugins/codex/.codex-plugin/plugin.json``, ``.mcp.json``;
       marketplace ``.agents/plugins/marketplace.json``
     - Same MCP command. The bundled Codex skill was removed in #545.
   * - Cursor
     - ``packages/agent-plugins/cursor/.cursor-plugin/plugin.json``, ``mcp.json``
     - Same MCP command
   * - OpenCode
     - ``@dev.fast/opencode-whiteboard`` (``index.js``)
     - The plugin's ``config`` hook adds a local MCP server with the same
       command
   * - Pi
     - ``@dev.fast/pi-whiteboard`` → ``skills/whiteboard/SKILL.md``
     - The skill tells Pi to run
       ``whiteboard api session_get_instructions '{}'`` and follow the result

Every connector depends on the ``~/.local/bin/whiteboard`` shim that Desktop
installs. Desktop's welcome screen also prints connection prompts
(``whiteboard connect``, ``connect-prompts.ts``, #475) instead of editing
agent configs.

The full loop
-------------

.. mermaid::

   flowchart LR
       subgraph Agent side
         A[Coding agent] --> P[Plugin / skill]
         P --> M["whiteboard mcp / api"]
         H[Harness trace hook] --> T["whiteboard trace ..."]
       end
       subgraph Machine state
         D[(~/.dev/review-desktop/instances)]
         DB[(review-api.db)]
         TS[(trace store + ~/.dev/trace-search)]
       end
       subgraph Desktop
         S[Embedded server]
         C[Canvas]
       end
       M -->|select instance| D
       M -->|HTTP + token| S
       S --> DB
       S -->|watch| C
       T --> TS
       S -->|trace resources, quotes| TS
       C -->|Copy for Agent| A

1. **Discovery.** ``whiteboard mcp`` picks an instance (see
   :doc:`../entrypoints/runtime_entrypoints`). If Whiteboard is not running,
   only ``session_get_instructions`` is useful, and the MCP guidance tells the
   agent to reload tools after Whiteboard starts.
2. **Instructions.** The server serves the authoring guide. It is
   opinionated: an RFC-style document with what/why, requirements, design
   and implementation sections. Lenses are written by a subagent, and the
   guide tells the agent to "write incrementally".
3. **Authoring.** ``session_create``, a lease, ``session_diff``,
   ``session_edit`` … (see :doc:`../entrypoints/module_interactions`).
4. **Traces** (optional and experimental). Hooks for Claude Code and Codex
   (hook settings), Pi (a managed extension) and OpenCode (a managed plugin
   in ``~/.config/opencode/plugins/review-trace.ts``) capture sessions. Git
   hooks or jj templates add ``Agent-Session`` trailers. The
   ``trace-archaeology`` topic teaches the agent to use
   ``whiteboard trace blame`` → ``pull`` → FFF search → ``show``, and to
   quote the trace in the document.
5. **Feedback.** The user selects content and uses **Copy for Agent**, then
   pastes it into the agent, which revises the document.

Inferences and open points
--------------------------

* The MCP tool list changes with capabilities. For example, the scratchpad
  guidance appears only when the scratchpad is available. This is inferred
  from ``mcpAuthoringGuidance`` in ``mcp.ts``.
* ``whiteboard_status`` is the one public tool without the ``session_``
  prefix. It reports which instance the agent is talking to.
