Descriptive language
====================

A glossary of the terms you will meet in the code, the UI and agent
instructions.

Whiteboard vs. review vs. session
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Term
     - Meaning
   * - **Whiteboard**
     - The product name since Stage 6 (#506, #507, #516). In the UI and in
       agent instructions, "a Whiteboard" also means one document.
   * - **Review**
     - The older product name, and the name still used in code: packages
       (``@dev.fast/review``), directories (``apps/review-desktop``), the
       ``review`` bin, ``/reviews-api``, ``reviewId`` and ``review-api.db``.
       ``CONTRIBUTING.md``: "The product is named Whiteboard, but package
       names and directories still use ``review``."
   * - **Session** (``sessionId``)
     - The public agent-facing name for a review document.
       ``public-tools.ts`` rewrites ``review_*`` tools to ``session_*`` and
       ``reviewId`` to ``sessionId``, and it rejects ``reviewId`` in session
       tools ("Use sessionId with session tools.", confirmed by running it).
       Do not confuse it with an **agent session** (a trace).
   * - **Progressive Review**
     - The earlier product name (inferred). It survives in
       ``packages/progressive-review``, commit scopes and a telemetry
       opt-out variable.
   * - **dev.fast**
     - The organization, npm scope (``@dev.fast/*``) and domain
       (``install.dev.fast``, ``update.dev.fast``).

Domain terms
------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Term
     - Meaning (source)
   * - Workspace
     - (1) The monorepo's pnpm workspace. (2) In Desktop, a pinned worktree
       prepared so that source and LSP work for a review. Only Desktop
       prepares and cleans these (``session_workspace_cleanup``).
   * - Canvas
     - The React UI that renders a review (``@dev.fast/review-canvas``).
   * - Home
     - Desktop's start page. It lists reviews by last update.
   * - Target
     - What a review describes: ``commits`` (base..head) or ``worktree``
       (a live checkout).
   * - Pins
     - ``{repositoryId, base, head}`` resolved to immutable commit ids.
       Repinning keeps the content and component ids.
   * - Local checkout
     - A registered Git or jj repository on disk (``POST /repositories``).
       Clients get an id and a display name, never the path.
   * - ``review-source:`` link
     - ``[label](review-source:head/src/x.ts#L10-L24)``. A validated link
       to pinned code.
   * - Code peek
     - An inline, read-only view of a pinned code range (``code_peek``).
   * - Lens / file lens
     - A named group of changed files in the Diff view
       (``session_lens_edit``). Lenses are written under the ``lenses``
       lease scope.
   * - Lease / authoring activity
     - Exclusive authoring ownership per scope (``document`` or
       ``lenses``), held with ``session_activity``. It expires after 3
       minutes.
   * - Ready
     - A review with content and no live lease.
   * - Courier
     - The canvas animation that draws each version's ``lastEdit``.
   * - Scratchpad
     - A global document with the id ``scratchpad``. It has no target and
       is behind a feature flag.
   * - Software map
     - A generated architecture map resource (``software-map-*.ts``). It is
       optional and gated by ``softwareMapEnabled``.
   * - Semantic / structural diff
     - An AST-aware diff produced by ``diffr`` (Rust, WASM plugins per the
       README).
   * - Trace / agent session
     - A transcript of a coding agent's session, captured by hooks. Commits
       record ``Agent-Session: <id>`` trailers
       (``instructions/trace-archaeology.md``).
   * - Decision log
     - The README's name for trace-linked reasoning. In code it appears as
       trace quotes (``trace_quote``), the Trace tab and trace archaeology.
   * - Trace store
     - Where traces go: an S3/R2 bucket or the hosted store. The choice is
       made with ``whiteboard trace storage use s3|hosted``.
   * - FFF
     - An external file-search MCP server used to search normalized traces
       in ``~/.dev/trace-search``.
   * - Active instance
     - The Desktop that the CLI and MCP talk to (``stable``, ``preview`` or
       ``dev-<checkout>``). Selection is described in
       :doc:`../entrypoints/runtime_entrypoints`.
   * - Discovery record
     - The private JSON file a server writes with its URL, token, PID and
       version.
   * - Channel
     - A release channel: ``stable`` or ``preview``. Preview builds have an
       orange icon and a distinct identity.
   * - Share
     - An immutable uploaded snapshot of a review. Later edits need a
       re-share.
   * - Headless authoring
     - "Creating and editing a Review without installing or running the
       desktop application, including from a CI job" (``CONTEXT.md``).

MCP and server terminology
--------------------------

* **MCP server**: ``whiteboard mcp``, a stdio server built with
  ``@modelcontextprotocol/sdk``. It serves the same catalog as
  ``whiteboard api tools``. It tells the agent to reload tools when
  Whiteboard starts after the agent listed them (``RELOAD_TOOLS`` in
  ``mcp.ts``).
* **Embedded server**: the Desktop host process. **Headless server**:
  ``whiteboard server start``.
* **Instructions topics**: ``authoring`` (the default), ``file-lenses``,
  ``scratchpad`` and ``trace-archaeology``.

Configuration names
-------------------

The main ones are ``DEV_REVIEW_HOME``, ``DEV_REVIEW_INSTANCE``,
``DEV_REVIEW_SERVER_DIR``, ``REVIEW_DIFFR_BINARY``, ``DEV-REVIEW.md``
(guidance file) and ``$DEV_REVIEW_HOME/trace/config.json``. The full list is
in :doc:`../devops/project_setup`.

Workflow state names
--------------------

* **Commands**: ``create``, ``set_target``, ``edit`` (``insert``,
  ``update``, ``move``, ``remove``, ``replace``), ``rename``, ``repin``,
  ``restore``, ``lens``, ``attention`` (``view``, ``dismiss``, ``restore``)
  and ``delete``.
* **Activity actions**: ``begin``, ``renew`` and ``end``.
* **Instance state** in ``whiteboard instances``: ``running`` or
  ``stopped``. The ``selectedBy`` field says how the instance was chosen.
* **The** ``lastEdit`` **fields**: ``type``, ``targetId``, ``blockId``,
  ``kind``, ``unit``, ``linkId``, ``fields`` and ``units``.
