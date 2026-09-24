Overview
========

What Whiteboard does
--------------------

Whiteboard is "an open-source IDE for thoughtful software design"
(``README.md``). It is a desktop app where a person and a coding agent share
one workspace. The agent describes its work by writing a structured document
onto an in-app canvas. The document holds prose, sequence and flow diagrams,
call stacks, software maps, code peeks, and quotes from the agent's own
session trace. The person reads it next to the real code, with VS Code
navigation and language services.

The README names three product pillars:

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Pillar
     - What the user gets
     - Main code (confirmed)
   * - Diagrams that lead to code
     - Clicking a diagram node, a sequence step or a trace quote jumps to the
       code it describes.
     - ``packages/review/app`` (canvas), ``apps/review-desktop/code-oss/src/vs/review``
   * - Semantic diff viewer
     - An AST-aware diff hides noise. Large added functions are summarized,
       and tests and docs are collapsed. WASM plugins can customize it.
     - External Rust ``diffr`` binary (``devdotfast/diffr``, run as a child
       process), ``packages/review/src/server/structural-diff.ts``,
       ``packages/review-protocol/src/structural-diff.ts``. See
       :doc:`../architecture/semantic_diff/index`.
   * - Decision log
     - Agents query and link their own session traces, so readers can see
       which decisions the agent made on its own.
     - ``packages/trace-core``, ``packages/trace-protocol``, ``packages/review/src/trace-cli.ts``

Who it is for
-------------

* **Developers who review agent-written code.** They get an explanation of a
  branch, a pull request or a subsystem.
* **Coding agents**, such as Claude Code, Codex, Cursor, OpenCode and Pi.
  They connect through an MCP server (``whiteboard mcp``) or a shell command
  (``whiteboard api``).
* **Contributors to this repository.** They work on the desktop fork, the
  CLI and server, the canvas, or the trace system.

How humans and agents use it together
-------------------------------------

The README Quickstart describes this confirmed loop:

1. The user installs Whiteboard Desktop and connects an agent from the
   welcome screen. Desktop writes a ``whiteboard`` command shim to
   ``~/.local/bin`` and gives the agent a generated connection prompt
   (commit ``365a8c51``, #475).
2. The user asks the agent to review a branch or explain a system "in
   Whiteboard".
3. The agent calls ``session_get_instructions`` and then ``session_create``,
   ``session_edit`` and related tools. The server validates each edit against
   pinned source revisions, then saves it as a new document version.
4. Desktop watches the review and draws each edit as it lands (the
   "courier" animation, #420 to #427).
5. The user reads the document, jumps to code, and copies a selection back to
   the agent with **Copy for Agent**. The agent then revises the document.

Where new developers should start
---------------------------------

1. Read :doc:`folder_structure` for the map.
2. Follow :doc:`../devops/project_setup` to install dependencies. Node 24
   and pnpm 11 are required.
3. Read :doc:`../entrypoints/runtime_entrypoints`, then
   :doc:`../architecture/workflow_core_logic`.
4. For the agent-facing API, read ``packages/review/src/review-api/README.md``
   in the repository. It is the most complete description of the server
   contract.

Code categories
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Category
     - Where
   * - Product code
     - ``packages/review/src`` (CLI, server, API, sharing), ``packages/review/app``
       (canvas), ``apps/review-desktop/code-oss/src/vs/review`` (desktop workbench)
   * - Protocol code
     - ``packages/review-protocol``, ``packages/review-share-protocol``,
       ``packages/trace-protocol``, ``packages/json``
   * - Agent integration code
     - ``packages/agent-plugins/*``, ``.claude-plugin/marketplace.json``,
       ``.agents/plugins/marketplace.json``, ``packages/review/instructions``,
       ``packages/review/src/review-api/mcp.ts``
   * - Trace and VCS infrastructure
     - ``packages/trace-core``, ``packages/local-vcs``
   * - DevOps code
     - ``.github/workflows``, ``scripts/``, ``apps/review-desktop/scripts``
   * - Tooling
     - ``tools/oxlint/anti-slop`` (custom lint rules), ``.oxlintrc.json``, ``.oxfmtrc.json``
   * - Documentation
     - ``README.md``, ``CONTRIBUTING.md``, ``docs/privacy.md``, ``docs/telemetry.md``,
       package READMEs, and this Sphinx site
   * - Tests
     - Co-located ``*.test.ts``, ``*.browser.test.tsx`` and ``scripts/**/*.test.mjs``;
       e2e journeys in ``apps/review-desktop/scripts/e2e``
   * - Vendored upstream code
     - ``apps/review-desktop/code-oss`` (a Code - OSS fork pinned at
       ``8a7abeba``), ``tools/oxlint/anti-slop/vendor``

How to read this documentation
------------------------------

Pages cite repository paths in ``literal`` style. They cite history as short
commit hashes and pull request numbers, such as ``810005f1`` (#161). Pull
request numbers refer to the upstream ``devdotfast/whiteboard`` repository.
This checkout is the ``kl-han/whiteboard`` fork.
