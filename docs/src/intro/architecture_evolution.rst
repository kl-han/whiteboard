Architecture evolution
======================

:doc:`project_history` tells the feature story. This page tells the
**structural** story: when each subsystem appeared, what it replaced, and
what remains. The evidence is ``git log --reverse -- <path>``, rename
detection (``git show -M --stat``), and package trees at key commits (all
HISTORY).

Package layout over time
------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Commit
     - ``packages/`` (and ``apps/``)
   * - ``d1c6463c`` import (08-18)
     - ``progressive-review``, ``review-protocol``, ``local-vcs``;
       ``apps/review-desktop``
   * - ``9ae532cd`` (08-18)
     - Added ``trace-shared``
   * - ``0c0c795f`` #277 (09-15)
     - Added ``traces`` (the standalone ``@dev.fast/traces`` CLI, ``dev-traces``)
   * - ``5a9a387a`` #256 (09-15)
     - ``trace-shared`` → ``trace-protocol``; added ``trace-core``; ``json``
       split out of ``review-protocol``
   * - ``a48bff33`` #259 (09-15)
     - ``progressive-review`` → ``review`` (595 files; a remnant ``tutorial/data.ts`` stays)
   * - ``baf324d3`` #338 (09-17)
     - Added ``review-share-protocol``
   * - ``84bbc584`` #365 (09-21)
     - ``traces`` removed; tracing consolidated into the ``review`` CLI
   * - ``365a8c51`` #475 (09-23)
     - Added ``agent-plugins/{claude,codex,cursor,opencode,pi}`` and
       marketplace manifests

Subsystem first appearances
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 12 48

   * - Path
     - Commits
     - First commit
   * - ``apps/review-desktop`` (incl. ``code-oss/src/vs/review``)
     - 217 (127)
     - ``d1c6463c`` import
   * - ``packages/review-protocol``
     - 96
     - ``d1c6463c`` import
   * - ``packages/local-vcs``
     - 20
     - ``d1c6463c`` import
   * - ``packages/progressive-review`` → ``review``
     - 114 + 192
     - ``d1c6463c`` → renamed in #259
   * - ``tools/oxlint``
     - 3
     - #95
   * - ``scripts/review-latency``
     - 14
     - #157
   * - ``packages/trace-core`` / ``trace-protocol`` / ``json``
     - 17 / 7 / 2
     - #256
   * - ``packages/review/src/review-api``
     - 91
     - #264 (JSON Review 1/5)
   * - ``review-api/mcp.ts``
     - 13
     - #268 (JSON Review 4/5)
   * - ``server/structural-diff.ts``
     - 8
     - ``9af69be2`` (the structural diff integration stack, merged in #245)
   * - ``packages/review/src/sharing`` + ``review-share-protocol``
     - 20 / 4
     - #338
   * - ``server/headless-host.ts``
     - 11
     - #356
   * - ``packages/agent-plugins``
     - 6
     - #475

Architectural eras
------------------

.. mermaid::

   flowchart TD
       E1["Era 1 · Imported MDX app (08-18)<br/>progressive-review: MDX compiler, native-agent,<br/>skills/dev-review; fork + review-protocol"]
       E2["Era 2 · Trace system extraction (08-18 → 09-15)<br/>trace-shared → trace-protocol, trace-core, json;<br/>standalone traces CLI; hosted store (#125)"]
       E3["Era 3 · JSON Review (09-15 → 09-18)<br/>rename to packages/review; server-owned JSON store;<br/>thin CLI and MCP; MDX, Ask and comments removed"]
       E4["Era 4 · External engines and headless (09-16 → 09-22)<br/>diffr structural diff; headless server; canvas split (#366);<br/>traces folded into the CLI (#365); sharing"]
       E5["Era 5 · Agent platform + Whiteboard (09-23 → 09-24)<br/>agent-plugins, generated connect prompts; instances;<br/>telemetry contract; visible rename"]
       E1 --> E2 --> E3 --> E4 --> E5

.. list-table::
   :header-rows: 1
   :widths: 12 18 20 18 16 16

   * - Era
     - Problem being solved
     - Components introduced
     - Contracts introduced
     - Replaced / removed
     - Current remnants
   * - 1 Imported MDX app
     - Ship a review app quickly
     - Fork workbench; MDX compiler (``src/compiler``); ``native-agent``;
       ``skills/dev-review``
     - review-protocol (discovery, CLI install)
     - —
     - The legacy importer; ``packages/progressive-review`` remnant; the
       ``review`` bin
   * - 2 Trace extraction
     - Share trace code between the CLI and the hosted store
     - trace-core, trace-protocol, json; ``packages/traces``
     - trace-protocol (npm, #125)
     - ``trace-shared``
     - All still present (``traces`` later folded in)
   * - 3 JSON Review
     - Agents editing MDX were fragile; drift and validation problems
     - ``review-api`` store and HTTP; MCP and ``api`` adapters
     - The tool catalog; block schemas; ``review-source:`` links;
       ``commandId`` receipts
     - The MDX compiler and worker (#322); the legacy runtime (#325); Ask,
       comments and native agent terminals (#258)
     - ``review_*`` internal names; ``reviewId`` inside the API
   * - 4 External engines + headless
     - Noisy diffs; CI authoring; package separation
     - The diffr integration; headless host; sharing; canvas package split
     - diffr NDJSON v4; review-share-protocol
     - The standalone traces CLI (#365); batch authoring (added in #356,
       removed in #469)
     - ``REVIEW_DIFFR_BINARY``; the ``bin/diffr`` convention
   * - 5 Agent platform + Whiteboard
     - Easy agent onboarding; running several Desktops; product identity
     - agent-plugins; ``connect`` prompts; instances; the telemetry contract
     - The ``session_*`` public names; discovery v3 with ``key`` and
       ``channel``
     - Config-writing agent setup; the first rename stack (#478 to #482,
       reverted in #500)
     - The ``Review``-named update zip (#553); package names

Historical decisions that still shape the code
----------------------------------------------

* **The rename that stopped at the surface.** The #500 revert and the
  narrower redo explain why packages, directories and APIs still say
  ``review``, and why ``public-tools.ts`` rewrites names at the boundary.
* **Server-owned JSON (Era 3).** This is why agents must go through tools,
  and why the MCP adapter can stay thin.
* **Trace protocol published separately (Era 2).** The hosted store
  deploys independently, so the npm version must match exactly.
* **diffr kept external (Era 4).** The largest algorithmic component is
  outside this repository, so Whiteboard needs no Rust toolchain.
* **Delegation to the bundled CLI.** This came from version-skew problems
  between standalone CLIs and Desktop (see the comments in ``cli.ts``).
