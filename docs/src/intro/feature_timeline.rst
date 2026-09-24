Feature timeline
================

Each row links a capability to the code that supports it and to the evidence
for it. "Stage" refers to the stages in :doc:`project_history`. "Pre-import"
means the capability already existed in the 2026-08-18 import commit.

.. list-table::
   :header-rows: 1
   :widths: 14 16 20 14 10 10 16

   * - Feature or capability
     - User-facing purpose
     - Supporting components/modules
     - Evidence source
     - Approx. stage
     - Current status
     - Notes or uncertainties
   * - Desktop app on a vendored Code - OSS fork
     - A review-focused editor with VS Code navigation and LSP
     - ``apps/review-desktop``, ``code-oss/src/vs/review``
     - ``d1c6463c``, ``UPSTREAM``, README "On vendoring Code OSS"
     - Pre-import
     - Active (v0.1.1)
     - The date of the original vendoring is unknown
   * - Embedded server in a UtilityProcess
     - One global server per Desktop instance, restarted on crash
     - ``reviewServerSupervisor.ts``, ``packages/review/src/server/desktop-host.ts``
     - Source code
     - Pre-import (inferred)
     - Active
     - The supervisor's restart delays live in ``common/reviewReconnect.ts``
   * - ``whiteboard`` / ``review`` CLI
     - Launch the app, author headlessly, manage traces and sharing
     - ``packages/review/src/cli.ts``, ``cli-runner.ts``
     - ``package.json`` ``bin``; #90, #367
     - Pre-import; release pipeline in Stage 5
     - Active
     - Both bin names point to ``dist/cli.js``
   * - Agent trace capture (decision log)
     - Link agent reasoning and user quotes to code
     - ``trace-core``, ``trace-protocol``, ``trace-cli.ts``, ``ReviewTraceView.tsx``
     - #13, #27, #63, #125, #160, #253–#256, #365
     - Pre-import; reshaped in Stages 3–5
     - Active, experimental opt-in
     - The hosted store server is not in this repository
   * - Hosted trace store
     - Team-wide trace listing and upload status
     - ``trace-core/src/store-client.ts``, ``trace-protocol``
     - #125, #191 (S3/R2 restored), #207, #250, #252
     - Stage 3–4
     - Active, selected explicitly
     - Needs ``whiteboard login``
   * - Interactive tutorial / onboarding
     - First-run walkthrough on a sample review
     - ``packages/review/tutorial``, ``tutorial-service.ts``
     - #40, #44, #211, #319, #462
     - Stage 2
     - Active
     - ``packages/progressive-review/tutorial`` looks like leftover data
   * - Preview release channel
     - Early builds with a distinct icon and identity
     - ``review-desktop-preview.yml``, ``release-channel.mjs``
     - #65, #67, #79, #192
     - Stage 2
     - Active
     - macOS arm64 only; Linux publishes to Fedora repositories
   * - Anti-slop lint rules
     - Code quality enforced in CI
     - ``tools/oxlint/anti-slop``, ``.oxlintrc.json``
     - #95, #229, #246, #248
     - Stage 2–3
     - Active
     - Vendored from ``dmmulroy/anti-slop``
   * - Comments, threads and "Ask agent"
     - Discuss a review inline and hand off to an agent
     - (removed)
     - #83, #119–#122, #201 → removed in #258
     - Stage 3
     - **Removed**
     - Replaced by Copy for Agent (#261)
   * - JSON review store and authoring API
     - Validated, versioned documents that agents edit through tools
     - ``review-api/store.ts``, ``http.ts``, ``authoring-tools.ts``
     - #161, #264–#270, #296, #312, #322, #325
     - Stage 4
     - Active (the core)
     - SQLite ``review-api.db`` under ``DEV_REVIEW_HOME``
   * - MCP server for agents
     - Agents call ``session_*`` tools over stdio
     - ``review-api/mcp.ts``, ``public-tools.ts``, ``agent-plugins/*``
     - #268, #506, #539, #554
     - Stage 4 → 6
     - Active
     - Internal names are ``review_*``, exposed as ``session_*``
   * - Sharing reviews
     - Send an immutable review to another machine
     - ``src/sharing``, ``review-share-protocol``
     - #338, #388, #410, #430
     - Stage 4–5
     - Active
     - README: updates after sharing need a re-share
   * - Semantic / structural diff
     - Hide noise and summarize large additions
     - ``@dev.fast/diffr``, ``server/structural-diff.ts``, ``reviewStructuralDiff*.ts``
     - #245, #394, #396, #429, #447, #471
     - Stage 5
     - Active, on by default
     - The diffr source (Rust) lives outside this repository
   * - Headless / CI authoring
     - Author reviews without Desktop, including from GitHub Actions
     - ``server/headless-host.ts``, ``whiteboard server start``
     - #356, #357, ``CONTEXT.md``
     - Stage 5
     - Active (batch drafts removed in #469)
     -
   * - Scratchpad
     - One global document the agent draws on during a conversation
     - ``instructions/scratchpad.md``, ``review-preferences.ts``
     - #392, #425, #428, #446
     - Stage 5
     - Behind a feature flag, off by default
     -
   * - Live drawing ("courier")
     - Watch the agent's edits land on the canvas
     - ``app/src/courier.tsx``, ``lastEdit`` in versions
     - #417–#427, #546
     - Stage 5
     - Active
     -
   * - File lenses
     - Group changed files into reviewer-oriented filters
     - ``review-api/file-lenses.ts``, ``session_lens_edit``
     - #483–#490, #521, #525
     - Stage 5
     - Active
     - Written by a subagent under a ``lenses`` lease
   * - Instance selection
     - Run dev and installed Desktops side by side
     - ``desktop-discovery.ts``, ``review-instances.ts``, ``cli.ts``
     - #511, ``CONTRIBUTING.md``
     - Stage 6
     - Active
     - ``DEV_REVIEW_INSTANCE``, ``whiteboard instances use``
   * - Telemetry contract
     - Anonymous usage and reliability data with a public contract
     - ``review-telemetry.ts``, ``ui-telemetry-events.ts``, ``docs/telemetry.md``
     - #3, #12, #533, #550, #570, #572
     - Pre-import → Stage 6
     - Active, on by default and can be turned off
     - PostHog; ``DO_NOT_TRACK`` honored
   * - Whiteboard rename
     - The new product name
     - Branding in the fork, CLI name, MCP tools
     - #478–#482, reverted in #500; #506, #507, #516, #543
     - Stage 6
     - Partial by design
     - Packages and directories still use ``review``
   * - Local VCS helpers (Git + Jujutsu)
     - Pin revisions and read diffs from local checkouts
     - ``packages/local-vcs``
     - Package source; override note in ``pnpm-workspace.yaml``
     - Pre-import (inferred)
     - Active, published as ``@dev.fast/local-vcs`` 0.1.0
     -
