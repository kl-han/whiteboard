Repository topology
===================

**Where source lives.** This view says nothing about processes or build
order. For those, see :doc:`build_topology` and :doc:`runtime_topology`.

.. mermaid::

   flowchart LR
       Root["/ (pnpm workspace root)<br/>package.json, pnpm-workspace.yaml,<br/>tsconfig.base.json, .oxlintrc.json"]
       Root --> Apps["apps/"]
       Apps --> Desktop["review-desktop/<br/>scripts/ (sh, mjs, py)"]
       Desktop --> CodeOSS["code-oss/ (VENDORED, 6,406 files)"]
       CodeOSS --> Owned["src/vs/review/ (Whiteboard-owned, 149)"]
       Root --> Pk["packages/"]
       Pk --> Review["review/ (CLI, servers, API, MCP)"]
       Review --> Canvas["review/app/ (canvas)"]
       Review --> Instr["review/instructions/, tutorial/"]
       Pk --> Proto["review-protocol/, review-share-protocol/,<br/>trace-protocol/, json/"]
       Pk --> Trace["trace-core/"]
       Pk --> VCS["local-vcs/"]
       Pk --> Plugins["agent-plugins/ (claude, codex, cursor,<br/>opencode, pi)"]
       Pk --> Legacy["progressive-review/ (LEGACY remnant)"]
       Root --> Scripts["scripts/ (CLI release, smoke, clean;<br/>review-latency/ Python)"]
       Root --> Tools["tools/oxlint/anti-slop/ (partly vendored)"]
       Root --> Mkt[".claude-plugin/, .agents/ (marketplaces)"]
       Root --> Docs["docs/ (Sphinx, privacy.md, telemetry.md)"]
       Root --> GH[".github/workflows/"]
       Ext["NOT IN REPO: devdotfast/diffr (Rust),<br/>hosted store, PostHog, update feed"]

Legend: the "VENDORED" and "LEGACY" labels mark ownership classes. See
:doc:`component_registry` for every component's ownership field.
