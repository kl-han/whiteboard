Semantic diff overview
======================

The actual pipeline
-------------------

.. mermaid::

   flowchart TD
       Pins["Review pins {repositoryId, base, head}<br/>review-api store"] --> Checkout["ensureReviewPinnedCheckout()<br/>prepared worktree at head"]
       Checkout --> Cache["StructuralComparisons<br/>replay cache (keeps 2 idle)"]
       Cache -->|"spawn: diffr --repo R --format ndjson<br/>--stream-annotations base head -- paths"| Diffr
       subgraph Diffr["diffr process (Rust, external)"]
         G["git2: read trees and blobs"] --> L["guess_language<br/>(difftastic tables)"]
         L --> P["tree-sitter parse"]
         P --> D["structural diff<br/>(difftastic-derived)"]
         D --> Pl["plugin chain (plugins.order):<br/>context, hide-files, deleted-bodies,<br/>summarize, test-bodies, removed-runs, group"]
         Pl --> W["NDJSON v4 writer"]
       end
       W -->|"start, file*, annotations*, complete"| Val["structural-diff.ts<br/>decodeStructuralDiffEvent (zod)"]
       Val --> Route["GET /reviews-api/:id/structural-diff<br/>application/x-ndjson"]
       Route --> Client["StructuralDiffClient<br/>(fork, renderer)"]
       Client --> UI["reviewStructuralDiff.ts<br/>collapsed bands, labels, visible counts"]
       Val --> Counts["structuralChangeCounts()<br/>Home and lens diff counts"]

Step by step (CONFIRMED unless noted)
-------------------------------------

1. **Input.** A review's pins name immutable base and head commits. The
   server prepares a pinned checkout (``local-data.ts``
   ``structuralChanges``). If that fails, the error is "Cannot prepare the
   pinned repository for structural diffing."
2. **Invocation.** ``StructuralComparisons`` deduplicates concurrent readers
   of the same comparison and replays events to late subscribers.
   ``structuralDiff()`` spawns diffr with the ``trees`` form, ``base head``.
   A ``merge-base`` form (``base...head``) exists in the type but is not
   used by this path.
3. **Inside diffr** (INFERRED from ``--help``, config output and binary
   strings): diffr reads the Git objects itself with libgit2, detects the
   language with difftastic's tables (about 50 languages, plus globs such
   as ``*.ts``), parses with tree-sitter, computes a structural diff, then
   runs the plugin chain.
4. **Wire.** diffr streams NDJSON version 4:

   * ``start``: snapshots and the file list with status and tags;
   * one ``file`` per path: a ``text`` or ``binary`` diff, stats, regions,
     visibility or an error;
   * ``annotations``: deferred plugin labels, such as summaries;
   * ``complete``: succeeded and failed counts.

5. **Validation.** Every line is parsed by the Zod schemas in
   ``@dev.fast/diffr`` (re-exported by ``review-protocol``). The first line
   must be ``start`` with version 4.
6. **Transport to UI.** The server re-streams events as
   ``application/x-ndjson``. The fork's ``StructuralDiffClient`` decodes
   them with the generated protocol copy.
7. **Presentation.** Regions become collapsible bands in the Monaco diff
   editor. ``visibility.label`` supplies text such as "Test file · hidden
   by default". Annotations supply summaries. Stats separate ``textual``
   from ``visible`` line counts.

What makes a change "semantic"
------------------------------

Observed on commit ``9f8088d`` (CONFIRMED): a test file with 26 added lines
reported ``visible: {added: 0}``. Its ``visibility`` was
``{collapsed: true, label: "Test file · hidden by default"}``, the effect of
the ``hide-files`` plugin with tags ``generated``, ``vendored`` and ``test``.
A source file reported ``textual`` 3/1 and ``visible`` 3/0. The structural
comparison itself (which AST nodes changed, and alignment ids) comes from
difftastic-style graph diffing inside diffr (INFERRED; the source is not
here).

Summaries and filtering
-----------------------

Pseudocode summaries are **the** ``bundled.summarize`` **plugin**, not
TypeScript code. It is off by default, uses provider ``gemini``, and needs
``GEMINI_API_KEY``/``GOOGLE_API_KEY`` or a saved key. Whiteboard's Settings
UI writes these values through ``diffr config set`` (``diffr-config.ts``,
#396). Summaries arrive later, as ``annotations`` events
(``--stream-annotations``), so the diff shows before they are ready.

Can it be developed independently?
----------------------------------

Yes. The engine lives in ``devdotfast/diffr``, with its own Rust release and
the ``diffr-ts`` package. Inside Whiteboard, point ``REVIEW_DIFFR_BINARY``
at a local build and run
``pnpm --filter @dev.fast/review test:integration:diffr`` (9 tests; they pass
with the pinned 0.1.3). A wire change needs coordinated updates, listed in
the diffr README: ``src/protocol/mod.rs``, ``diffr-ts/src/contract.ts``, and
the exact version pins in ``packages/review-protocol/package.json`` and
``packages/review/package.json``.
