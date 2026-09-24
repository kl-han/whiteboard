Decisions and trade-offs
========================

Each decision cites its evidence. Where the rationale is not written down,
it is marked *inferred*.

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Decision
     - Rationale
     - Trade-off
     - Evidence
   * - Vendor Code - OSS instead of keeping patches
     - "coding agents have a hard time with patches". Much of stock VS Code
       (Copilot) is not needed.
     - The team must merge upstream security fixes by hand. ``UPSTREAM``
       lists each backport and CVE.
     - README "On vendoring Code OSS", ``UPSTREAM``, #41, #243
   * - One global embedded server per Desktop, in a UtilityProcess
     - One window owns one server. Sessions are routes, not extra ports.
       The server restarts on crash without taking down the UI.
     - Discovery and instance selection become necessary once several
       Desktops share a home (#511).
     - ``apps/review-desktop/README.md``, ``reviewServerSupervisor.ts``
   * - The server owns the JSON document (replacing MDX that agents edited)
     - Validation before save, immutable versions, stable ids, and
       idempotent commands
     - A large migration (#264 to #325) and a legacy importer to maintain
     - #161, #187, JSON Review 1/5 to 5/5, #322, #325
   * - Thin MCP and CLI adapters over one HTTP API
     - Adapters "cannot skew" from the server. The tool catalog comes from
       ``GET /authoring``.
     - Every agent call needs a running server (Desktop or headless).
     - ``cli.ts`` comments, ``review-api/README.md``
   * - The standalone CLI delegates to the Desktop-bundled CLI
     - Avoids a version skew between the CLI and the server. Lets an old
       system Node still work through Electron's runtime.
     - Delegation logic is duplicated in ``cli.ts``, which runs before the
       Node check.
     - ``cli.ts``
   * - Connect agents with generated prompts instead of writing their configs
     - Fewer writes into other tools' configuration (inferred)
     - The user must paste the prompt or reconnect.
     - #475, ``connect-prompts.ts``
   * - Trace capture is opt-in and experimental; there is a choice of store
     - Privacy: full transcripts leave the machine only with consent.
     - More setup: FFF, a store and hooks
     - #27, #125, #191, #207, ``trace-archaeology.md``
   * - Publish the trace and share protocols as separate npm packages
     - The CLI and the hosted store deploy separately and must agree
       exactly.
     - Contract versions must be bumped and tagged on release.
     - ``trace-protocol/README.md``, #125, #256
   * - Semantic diff lives in an external Rust binary (diffr)
     - Performance and AST awareness. WASM plugins allow customization.
     - A native binary to sign and bundle per platform (#429, #494)
     - README, #394, #429
   * - Remove features that do not pay off
     - Keep the product focused.
     - Some churn for users
     - Removed: comments and Ask (#258), batch authoring (#469), section
       status (#454), UI stall watchdog (#571)
   * - A seven-day minimum release age for dependencies
     - Supply-chain safety
     - Urgent upgrades need an explicit exclusion with a justification.
     - ``pnpm-workspace.yaml``
   * - Strict custom lint (anti-slop)
     - Keep agent-written code idiomatic.
     - Custom rules to maintain; some are warnings first
     - #95, #229, #246
   * - Do not add change-detector tests
     - Test behavior, not implementation.
     - Contributors must delete such tests and flag it in the PR.
     - ``AGENTS.md``, ``CONTRIBUTING.md``, #186
   * - Rename the visible product only, not the internal identifiers
     - The first full rename (#478 to #482) was reverted "to be rebuilt
       separately with a narrower scope".
     - Mixed terminology in the codebase
     - #500, #506, #507
