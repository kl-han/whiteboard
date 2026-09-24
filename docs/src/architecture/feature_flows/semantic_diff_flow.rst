Semantic diff flow
==================

The user opens a review's Diff view; changed files render as structural
diffs.

.. mermaid::

   sequenceDiagram
       actor User
       participant WB as Workbench (renderer)
       participant Cl as StructuralDiffClient
       participant Srv as Embedded server
       participant LD as local-data.ts
       participant SC as StructuralComparisons
       participant D as diffr (native)
       User->>WB: open Diff view / file
       WB->>Cl: streamComparison()
       Cl->>Srv: GET /reviews-api/:id/structural-diff?… (x-review-token)
       Srv->>LD: structuralChanges({pins, file})
       LD->>LD: ensureReviewPinnedCheckout(head)
       LD->>SC: stream({kind:"trees", base, head, paths})
       alt no cached comparison
         SC->>D: spawn diffr --format ndjson --stream-annotations base head -- paths
         D-->>SC: start v4, file…, annotations…, complete
       end
       SC-->>Srv: validated events (replayed to every reader)
       Srv-->>Cl: application/x-ndjson
       Cl-->>WB: StructuralEvent
       WB-->>User: diff with collapsed bands, labels, summaries

.. list-table::
   :widths: 25 75

   * - Initiating actor
     - The user (Diff view), or server-side coverage counting
   * - Entrypoint
     - ``GET /reviews-api/:id/structural-diff``
   * - Internal handlers
     - ``http.ts`` → ``local-data.ts#structuralChanges`` →
       ``structural-comparisons.ts`` → ``structural-diff.ts``
   * - Shared contracts
     - diffr NDJSON v4 (``@dev.fast/diffr``), plus ``{type:"error"}`` from
       Whiteboard
   * - Persistence
     - None. There is an in-memory replay cache that keeps at most 2 idle
       comparisons.
   * - Transitions
     - Chromium → Node (HTTP) → Rust native process (stdout NDJSON) → Node
       → Chromium
   * - Presentation
     - Monaco multi-diff editor with collapsed regions
       (``reviewStructuralDiff.ts``) and visible-line counts
   * - Failure points
     - diffr missing or on an unsupported platform. A pinned checkout that
       cannot be prepared. The 120 s idle timeout. Text-diff fallbacks
       (``unsupported_language``, ``parse_error``, ``too_large``). A
       summary plugin without a key.

Details: :doc:`../semantic_diff/index`.
