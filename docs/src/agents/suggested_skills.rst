Suggested skills
================

These are skills and specialized assistants that would help people who
**work on this repository**. They are suggestions. None of them ship with the
repository, except the product's own ``whiteboard`` skill (Pi) and the
MCP-served instructions.

.. list-table::
   :header-rows: 1
   :widths: 14 20 20 24 22

   * - Skill name
     - Brief description
     - Use case
     - Required project knowledge
     - Risk or limitation
   * - Codebase explorer
     - Answers "where does X live?" across packages and the fork
     - Onboarding, triage
     - :doc:`../intro/folder_structure`; know that ``review`` means Whiteboard;
       skip ``code-oss/`` except ``src/vs/review``
     - Can drown in the 6k+ vendored files
   * - Documentation writer
     - Keeps this Sphinx site, package READMEs and ``docs/telemetry.md``
       current
     - After API or CLI changes
     - ``AGENTS.md`` (ask before editing README.md), the telemetry-doc rule
       in CONTRIBUTING
     - Can invent behavior. Every claim must be checked.
   * - Test generator
     - Writes Vitest and browser tests for behavior
     - New features, bug fixes
     - Vitest projects; "no change detector tests"; the fixture golden files
     - Brittle snapshot-style tests go against repository policy
   * - DevOps verifier
     - Runs install, build, lint, typecheck and test, and records the
       results
     - CI failures, environment drift
     - Node 24 and 24.18.0 pins, ``tsgo`` dependencies, Playwright
       browser builds
     - The desktop build needs network access and time
   * - Dependency auditor
     - Reviews upgrades against ``minimumReleaseAge`` and overrides
     - Dependabot PRs, CVEs
     - ``pnpm-workspace.yaml`` policy; the vendored lockfiles under ``code-oss``
     - Excluding a package from the release-age rule needs a written
       justification
   * - Architecture diagrammer
     - Produces Mermaid or Whiteboard diagrams of flows
     - Design docs and reviews
     - :doc:`../architecture/component_interactions`
     - Diagrams go stale. Tie them to code paths.
   * - Feature historian
     - Reconstructs why a feature exists from commits, PRs and traces
     - "Why is this like this?"
     - ``whiteboard trace blame``, the squash-merge PR numbers
     - History before 2026-08-18 is not in this repository
   * - Component interaction mapper
     - Derives dependency graphs from imports and ``package.json``
     - Refactors, package splits
     - The workspace list, the tsdown bundling of workspace dependencies
     - Runtime edges (HTTP, UtilityProcess) are invisible to import graphs
   * - Agent integration reviewer
     - Checks plugin manifests, MCP tool descriptions and instructions
     - Before release; new agent support
     - ``agent-plugins/*``, ``public-tools.ts``, ``instructions/*.md``
     - Agent host behavior changes outside this repository
   * - Refactoring planner
     - Plans multi-PR changes (for example the JSON Review 1/5 to 5/5 stack)
     - Large migrations
     - Stable contracts vs. implementation details
       (:doc:`../architecture/workflow_core_logic`)
     - The #500 revert shows the cost of over-broad stacks
   * - API contract reviewer
     - Reviews Zod schemas, route changes and protocol version bumps
     - Changes to review-protocol, trace-protocol, share-protocol
     - ``REVIEW_SCHEMA_VERSION``, discovery version, npm publish flow
     - Contract breaks can strand installed Desktops or CLIs
   * - Security reviewer
     - Audits token auth, path handling, trace consent and fork backports
     - Each release; ``UPSTREAM`` updates
     - ``SECURITY.md``, ``UPSTREAM`` CVE list, ``review-network-policy.mjs``
     - Report upstream VS Code issues to Microsoft
   * - Release note generator
     - Summarizes merged PRs between version bumps
     - Desktop and CLI releases
     - ``chore(review-desktop): bump version`` commits; there are no tags or
       CHANGELOG
     - Must group rename, revert and redo sequences correctly
   * - Telemetry reviewer
     - Checks new events against ``docs/telemetry.md`` and the privacy rules
     - Any telemetry change
     - ``ui-telemetry-events.ts``, ``test:telemetry-privacy``,
       ``telemetry-clean-text.ts``
     - Leaking code, paths or identifiers breaks the published contract
