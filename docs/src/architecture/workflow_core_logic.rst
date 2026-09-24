Core workflow and logic
=======================

The core workflow is a **versioned, validated document pinned to source
revisions**. Most of this page is confirmed by
``packages/review/src/review-api/README.md`` and the code it describes.

The review document
-------------------

* **Goal**: an explanation of a change or system that cannot drift away from
  the code it describes.
* **How**: a review has a *target*. It is either ``commits``
  (``{repositoryId, base?, head}``) or ``worktree`` (a live checkout, with an
  optional base). The server resolves the target to *pins*, which are
  immutable commit ids (``POST /pins``). The content is a tree of Markdown
  and self-contained components. The block kinds live in
  ``review-api/blocks/``: ``section``, ``markdown``, ``code``,
  ``code_peek``, ``call_stack_diff``, ``sequence``, ``flow_diagram``,
  ``database_lens``, ``software_map``, ``trace_quote``, ``callout``,
  ``image``, ``divider`` and ``tutorial``. ``definition.ts`` holds the shared
  ``BlockDefinition`` helper: a strict schema, plus a ``check`` that throws
  ``ReviewInputError``.
* **Data flow**: each accepted command produces one saved version with
  ``lastEdit`` metadata. Reads return a compact outline (``/inspect``), one
  component (``targetId``) or a full snapshot.
* **Assumptions**: the repositories are local Git or jj checkouts registered
  with the server. Source is read from **committed objects**, not the working
  copy. A live ``worktree`` target is the exception: it follows the
  checkout.
* **Errors**: schema validation runs on inputs, and on field patches after
  they are merged. A relationship pass checks diagram actors, store fields
  and base/head sides. Source and resource providers check
  ``review-source:`` links and ranges **before** a version is saved. Errors
  that are safe to show clients use ``ReviewInputError``. Unexpected errors
  return HTTP 500.

Authoring leases
----------------

* **Goal**: one author per scope at a time, and a clear "ready" signal.
* **How**: ``session_activity begin|renew|end`` with a caller-chosen
  ``leaseId`` UUID. The scopes are ``document`` and ``lenses``, so a
  subagent can write lenses while the main author writes the document. Every
  accepted mutation extends the lease. A lease expires after **3 minutes**
  without a write or renewal.
* **Errors**: a write with another lease, or with no lease while the review
  is owned, gets HTTP 409. The review counts as *ready* once it has content
  and no live lease. There is no per-section status; it was removed in
  #454.

Idempotency and concurrency
---------------------------

* Every command carries a ``commandId`` (a UUID). A retry with the same id
  replays the stored receipt instead of editing twice.
* There is no expected-version parameter. Later edits to the same field win.
* Multiple processes share one SQLite database. Each connection checks
  ``data_version`` every 250 ms and refreshes its subscriptions. Only Desktop
  prepares and cleans workspaces. A database-backed process claim prevents
  two Desktops from running duplicate jobs.

Pull-request reviews
--------------------

``session_create {pullRequestUrl}`` resolves the PR with ``gh pr view``
(falling back to the public GitHub API). It fetches
``refs/pull/N/head`` into ``refs/review/github/<owner>/<repo>/pull/N/*``
without moving branches, and pins the head and the merge base. It returns
the existing review for the same PR unless ``reuseExisting:false`` is set
(#455, #476).

Live drawing
------------

The canvas watches ``GET /:id/watch`` (NDJSON). It draws each version's
``lastEdit``: a paragraph lands, a diagram unit is traced where it attaches,
or a whole diagram is drawn in one quick pass. If the reader falls behind,
the stream coalesces updates. A reconnect starts from the current snapshot.

Stable contracts vs. implementation details
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Stable contract (changes need migration or versioning)
     - Implementation detail
   * - ``/reviews-api`` routes and the ``session_*`` tool names and schemas
     - How the store lays out SQLite tables internally
   * - The ``review-source:`` link syntax
     - Canvas animation timing (courier, draw queue)
   * - ``@dev.fast/trace-protocol`` (published; server and CLI must match exactly)
     - Trace normalization layout under ``~/.dev/trace-search``
   * - ``@dev.fast/review-share-protocol`` (published)
     - Sharing upload strategy
   * - Discovery record shape (``REVIEW_DESKTOP_DISCOVERY_VERSION``)
     - Supervisor restart delays
   * - The stored review schema (``REVIEW_SCHEMA_VERSION``) plus migrations
     - Tutorial asset build

How to extend or replace a component
------------------------------------

See :doc:`../advanced/extension_points`. In short:

* **Add a block kind**: add a schema file in ``review-api/blocks/`` and a
  renderer in the canvas component registry (#288).
* **Add a tool**: add it to ``authoring-tools.ts`` with an HTTP mapping. MCP
  and ``api`` pick it up automatically from ``GET /authoring``.
* **Replace the diff engine**: point ``REVIEW_DIFFR_BINARY`` at another
  ``diffr``-compatible executable. It must produce the record schema in
  ``review-protocol/structural-diff.ts``.
