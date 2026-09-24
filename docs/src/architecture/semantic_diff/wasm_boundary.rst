WASM boundary
=============

Summary
-------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Boundary
     - Status
     - Evidence
   * - TypeScript → Rust through WASM
     - **Does not exist**
     - ``structural-diff.ts`` uses ``child_process.spawn``. No ``.wasm``
       file, ``wasm-bindgen`` glue or ``WebAssembly.instantiate`` touches
       diffr (CONFIRMED).
   * - TypeScript → Rust through a native process and NDJSON
     - **The real boundary**
     - Wire version 4, validated by Zod (CONFIRMED by running it)
   * - diffr → plugins through WASM (wasmtime)
     - Exists inside diffr
     - wasmtime, WASI, WASI-HTTP and wit-bindgen are linked into the binary
       (INFERRED)
   * - Canvas → ``libavoid.wasm``
     - Exists, unrelated to diff
     - ``copy-canvas.mjs`` requires the asset; ``reviewCanvasPart.ts``
       passes ``wasmUrl`` (CONFIRMED)

The native process boundary in detail
-------------------------------------

**Mechanism.** ``structuralDiff()`` in ``packages/review/src/server/structural-diff.ts``:

* **Executable.** Resolved in this order: ``REVIEW_DIFFR_BINARY``, then
  ``<package>/bin/diffr``, then ``diffr`` on ``PATH``.
* **Arguments.** ``--repo <path> --format ndjson --stream-annotations
  <base> <head> -- [paths]``. The working directory is the repository, so
  diffr reads the user's own config and keys.
* **stdio.** stdin is ignored. stdout is split into lines by ``readline``.
  stderr keeps only its last 16 KiB, for error messages.

**Data in.** Only the repository path and revisions. diffr reads the Git
objects itself, so file contents never cross the boundary inbound.

**Data out.** Full file text on each side, syntax spans (with
``--syntax``), a region tree (``leaf`` or ``fold``, ``alignment_id``,
``fold_state_id``, changed spans), stats and visibility. Lines are
zero-based, columns are UTF-8 bytes, and ranges are half-open (contract
header).

**Errors.**

* ``ENOENT`` becomes "Cannot find diffr at …" with setup guidance.
* A malformed line becomes "Malformed diffr protocol record."
* A wrong first event or version becomes "Unsupported diffr stream
  protocol."
* A record over 64 MiB is rejected.
* Data after ``complete`` is rejected.
* Exit code 2 is tolerated only when the stream already reported failures.
* Per-file failures are ``file`` events with ``error``. They are not
  exceptions.

**Versioning.** ``STRUCTURAL_DIFF_WIRE_VERSION = 4``, with base version 3
without annotations. ``@dev.fast/diffr`` is pinned to exactly 0.1.3 in both
``review-protocol`` and ``review``. It is also in the
``minimumReleaseAgeExclude`` list in ``pnpm-workspace.yaml``.

The config boundary
-------------------

``diffr-config.ts`` runs ``diffr config show --json [--reveal]`` and
``diffr config set <key> <value>`` with ``execFile``. It has a 30 s timeout,
a 16 MiB buffer and serialized writes. Error messages are **scrubbed** on
purpose, because arguments can contain API keys: "diffr could not complete
the operation. Check its configuration and credentials." A config write
calls ``invalidateStructuralComparisons()``, which bumps a generation number
so that cached comparisons are recomputed.
