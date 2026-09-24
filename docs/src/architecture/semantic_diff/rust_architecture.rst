Rust architecture of diffr
==========================

.. warning::

   The diffr Rust source is **not** in this repository. Everything below
   comes from the release binary 0.1.3 (``x86_64-unknown-linux-gnu``, ELF,
   about 149 MB, not stripped), its ``--help`` and ``config show --json``
   output, and the ``@dev.fast/diffr`` README. Treat internal structure as
   INFERRED.

Where it comes from
-------------------

.. list-table::
   :widths: 30 70

   * - Source repository
     - ``https://github.com/devdotfast/diffr`` (``package.json``
       ``repository``)
   * - Release artifacts
     - ``diffr-<version>-<target>.tar.gz`` on GitHub releases; targets
       ``aarch64-apple-darwin`` and ``x86_64-unknown-linux-gnu`` only
   * - Integrity
     - sha256 hashes pinned in ``@dev.fast/diffr/pins.json``, checked by
       ``diffr-fetch``
   * - How Whiteboard gets it
     - ``pnpm --filter @dev.fast/review ensure:diffr``
       (``diffr-fetch --into bin``) for checkouts. Desktop bundles it at
       ``bin/diffr`` under its runtime (#394).
   * - Compilation trigger
     - None in this repository. It is built with ``cargo build --locked`` in
       the diffr repository (diffr README "Release").

Crates identified in the binary
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Crate / project
     - Evidence and role
   * - difftastic
     - The strings "Glob in difftastic source should be well-formed",
       ``src/parse/guess_language.rs`` and ``DFT_OVERRIDE_COLUMNS``. It
       provides the language table and the structural diff algorithm
       (INFERRED).
   * - ``tree-sitter`` 0.26.10
     - Parsing, and the ``--syntax`` capture names.
   * - ``git2`` 0.20.4
     - libgit2 bindings. diffr reads repositories itself; ``--repo`` and
       Git-style arguments (``--cached``, ``--merge-base``, ``-M``).
   * - ``wasmtime`` 34.0.2, ``wasmtime-wasi``, ``wasmtime-wasi-http``, ``wit-bindgen`` 0.60
     - WASM component plugin host (see :doc:`wasm_boundary`).
   * - ``tokio`` 1.53
     - Async runtime, e.g. ``--jobs`` concurrent file diffs (default 16).

How languages are represented
-----------------------------

difftastic's language table maps names and file globs to tree-sitter
grammars. One string table in the binary names about 45 languages,
including Ada, C/C++, C#, CSS, Elixir, Go, Haskell, Java, JavaScript/JSX,
Kotlin, Lua, Nix, OCaml, PHP, Python, R, Scala, SQL, Swift, TypeScript/TSX
and Zig (CONFIRMED by strings). Rust is supported too: our probe got a
"Rust parse errors" fallback. The full list needs the diffr source
(UNVERIFIED). A file with no grammar falls back to a text diff (see
:doc:`failure_modes`).

Why Rust rather than TypeScript?
--------------------------------

The README gives only the outcome (DOCUMENTED). Likely reasons, all
INFERRED: reuse of difftastic and the native tree-sitter grammars; the
graph-diff cost on large files (``diff.graph_limit`` 3,000,000); and a
sandboxed plugin host through wasmtime. Separately, the diffr README names a
terminal UI (``tui/packages/hunk``) as another consumer. So diffr is a
standalone product that Whiteboard uses, not a Whiteboard subsystem.
