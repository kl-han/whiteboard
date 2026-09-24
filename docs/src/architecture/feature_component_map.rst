Feature-to-component map
========================

This page maps each user-facing feature to the components that implement it.
The requested starting diagram had a "Diff / Review Logic" box. We replaced
it with the concrete pieces: the JSON review store and the external
``diffr`` engine. We also added the MCP adapter, which is how agents
actually connect.

.. mermaid::

   flowchart LR
       F1[Agent-assisted architecture workspace] --> C1[Desktop app<br/>apps/review-desktop]
       F1 --> C2[Canvas<br/>packages/review/app]
       F1 --> C3[Agent plugins<br/>packages/agent-plugins]
       F1 --> C13[MCP / api adapters<br/>review-api/mcp.ts, agent-cli.ts]
       F1 --> C14[JSON review store<br/>review-api/store.ts]
       F2[Semantic diff review] --> C4[diffr engine<br/>@dev.fast/diffr + server/structural-diff.ts]
       F2 --> C15[File lenses<br/>review-api/file-lenses.ts]
       F2 --> C5[Local VCS helpers<br/>packages/local-vcs]
       F2 --> C1
       F3[Decision log and trace-linked reasoning] --> C6[Trace core<br/>packages/trace-core]
       F3 --> C7[Trace protocol<br/>packages/trace-protocol]
       F3 --> C2
       F4[CLI-driven local workflow] --> C8[whiteboard CLI<br/>src/cli.ts]
       F4 --> C9[Embedded / headless server<br/>src/server]
       F4 --> C10[Instance selection<br/>desktop-discovery.ts]
       F5[Desktop packaging and runtime] --> C11[review-desktop scripts<br/>build.sh, package-*.sh]
       F5 --> C12[Vendored Code - OSS<br/>code-oss/]
       F6[Sharing reviews] --> C16[src/sharing + review-share-protocol]
       F7[Scratchpad] --> C14
       F7 --> C2
       F8[Telemetry and bug reports] --> C17[review-telemetry.ts, server/bug-report.ts]

How to read the edges
---------------------

* **F1 → C13, C14**: an agent's document exists only as versions in the JSON
  store, and the agent writes them only through the adapters. The canvas
  (C2) renders them, and Desktop (C1) hosts the canvas.
* **F2 → C4**: the server runs ``diffr`` for structural records
  (``structural-diff.ts``). The fork's ``reviewStructuralDiff*.ts`` services
  display them. **C15**: lenses are stored on the review and group changed
  files. **C5**: diffs and pins come from Git or jj.
* **F3 → C6, C7**: hooks capture sessions, and the store contract defines the
  hosted uploads. The canvas's Trace tab and ``trace_quote`` blocks render
  retained trace resources.
* **F4 → C8, C9, C10**: the CLI either discovers a Desktop instance or starts
  a headless server.
* **F5 → C11, C12**: ``build.sh`` compiles the fork. ``package-macos.sh`` and
  ``package-linux*.sh`` produce the artifacts.
* **F6 → C16**: ``whiteboard share`` uploads an immutable bundle that follows
  ``@dev.fast/review-share-protocol``.
* **F7**: the scratchpad is a special document with the fixed id
  ``scratchpad`` in the same store (``instructions/scratchpad.md``).
* **F8**: telemetry events and explicit bug reports (``bug-report.ts`` and
  ``bug-report-dialog.tsx``).

Feature distribution by package
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 15 15

   * - Feature
     - review (Node)
     - review-canvas
     - review-desktop fork
     - trace-*
     - local-vcs
   * - Authoring and versioning
     - ●
     - ○ (render)
     - ○ (open, tabs)
     -
     - ○ (pins)
   * - Semantic diff
     - ● (diffr runner)
     - ○
     - ● (diff views)
     -
     - ○
   * - Decision log / traces
     - ○ (CLI, trace routes)
     - ● (Trace view)
     -
     - ●
     - ○ (notes, hooks)
   * - Instance selection
     - ●
     -
     - ○ (writes identity)
     -
     -
   * - Sharing
     - ●
     - ○
     - ○ (contrib/sharing)
     -
     - ○

● = primary owner, ○ = participates.
