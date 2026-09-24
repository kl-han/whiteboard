MCP tool reference
==================

Generated on 2026-09-24 from ``whiteboard api tools`` on a headless server
built from this commit. MCP serves the same catalog. Mutating tools take a
UUID ``commandId``, and ``leaseId`` while a lease is held. Read the full
input schemas with ``whiteboard api tools``.

.. list-table::
   :header-rows: 1
   :widths: 24 8 24 10 34

   * - Tool
     - Method
     - Route (``/reviews-api``)
     - Command
     - Summary (first sentence)
   * - ``whiteboard_status``
     - GET
     - ``/status``
     - —
     - Name the Whiteboard instance this session talks to: key (stable, preview or dev-<checkout>), channel, checkout, appVersion, cliVersion, instanceId, url, home and desktopAvailable.
   * - ``session_capabilities``
     - GET
     - ``/capabilities``
     - —
     - Discover whether Desktop is available and optional software-map generation is enabled.
   * - ``session_get_instructions``
     - GET
     - ``/instructions``
     - —
     - Read Whiteboard's guidance before creating or editing a Whiteboard.
   * - ``session_activity``
     - POST
     - ``/:reviewId/activity``
     - —
     - Acquire an exclusive authoring session for one scope of a review: begin with a fresh leaseId, pass that leaseId on every write in that scope, and end when finished.
   * - ``session_delete``
     - POST
     - ``/commands``
     - delete
     - Permanently delete this review and its history.
   * - ``session_attention``
     - POST
     - ``/commands``
     - attention
     - Mark a review viewed, dismissed or restored without changing its content.
   * - ``session_create``
     - POST
     - ``/commands``
     - create
     - Create a review of saved working files, immutable commits or a GitHub PR.
   * - ``session_set_target``
     - POST
     - ``/commands``
     - set_target
     - Change the review target, preserving document and component IDs.
   * - ``session_edit``
     - POST
     - ``/commands``
     - edit
     - Edit a document component.
   * - ``session_lens_edit``
     - POST
     - ``/commands``
     - lens
     - Edit one Diff-view lens.
   * - ``session_rename``
     - POST
     - ``/commands``
     - rename
     - Change the review title.
   * - ``session_repin``
     - POST
     - ``/commands``
     - repin
     - Update source pins or PR identity while preserving the document and component IDs.
   * - ``session_restore``
     - POST
     - ``/commands``
     - restore
     - Restore title, source pins, PR identity and content from a saved version.
   * - ``session_list``
     - GET
     - ``/``
     - —
     - List saved reviews.
   * - ``session_get``
     - GET
     - ``/:reviewId/inspect``
     - —
     - Read a readable, nested text outline with editable IDs.
   * - ``session_lens_get``
     - GET
     - ``/:reviewId/lenses``
     - —
     - Read the review's Diff-view lenses as authored (ids, titles, targets), each lens's resolved fileCount (and unavailable reason, if any), and uncategorized: the changed lines no lens selects yet, by file.
   * - ``session_history``
     - GET
     - ``/:reviewId/history``
     - —
     - List saved document versions.
   * - ``session_open``
     - POST
     - ``/:reviewId/open``
     - —
     - Show an existing review immediately and prepare current pinned checkouts in the background.
   * - ``session_environment``
     - POST
     - ``/:reviewId/environment``
     - —
     - Acquire and recheck this review's current base/head language checkouts (not historical or selected commits).
   * - ``session_workspace_cleanup``
     - POST
     - ``/workspace-cleanup``
     - —
     - Inspect failed cleanup of retired Whiteboard-owned checkouts.
   * - ``session_register_repository``
     - POST
     - ``/repositories``
     - —
     - Register a local Git or jj repository.
   * - ``session_resolve_pins``
     - POST
     - ``/pins``
     - —
     - Resolve base and head revisions to immutable commit IDs for create or repin.
   * - ``session_upload``
     - POST
     - ``/resources``
     - —
     - Retain an image, trace or software map for use in a review.
   * - ``session_source``
     - POST
     - ``/:reviewId/source``
     - —
     - Read an exact code range from the current target.
   * - ``session_file``
     - GET
     - ``/:reviewId/file``
     - —
     - Read a complete source file from the current target; version selects retained history.
   * - ``session_tree``
     - GET
     - ``/:reviewId/tree``
     - —
     - List immediate directory entries in the target, including working files for worktree targets.
   * - ``session_diff``
     - GET
     - ``/:reviewId/diff``
     - —
     - Read this review's changes.
   * - ``session_commits``
     - GET
     - ``/:reviewId/commits``
     - —
     - List commits in this review's pinned comparison.

In degraded mode (no reachable server), ``tools/list`` returns only
``session_get_instructions`` and ``whiteboard_status`` (CONFIRMED by the
smoke test).
