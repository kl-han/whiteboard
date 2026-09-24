Semantic diff
=============

The README describes "a semantic, AST-aware diff viewer in Rust" with "a
WASM-based plugin system". This section traces how that works in the code.

.. admonition:: Headline findings

   * The Rust engine is **diffr**, an **external** program from the separate
     ``devdotfast/diffr`` repository. There is **no Rust source, Cargo
     workspace or WASM build for it in this repository** (CONFIRMED by a
     file census).
   * Whiteboard runs diffr as a **native child process** and reads **NDJSON
     over stdout**. It does not call it through WASM (CONFIRMED in
     ``server/structural-diff.ts``, and by running it).
   * The diffr binary embeds **difftastic**, **tree-sitter 0.26**, **git2**
     and **wasmtime 34** with WASI. WASM is diffr's *plugin* runtime, inside
     that process (INFERRED from the binary).

.. toctree::
   :maxdepth: 1

   overview
   rust_architecture
   wasm_boundary
   plugin_system
   failure_modes
