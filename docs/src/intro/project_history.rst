Project history
===============

.. admonition:: Sources and limits

   This history comes from the Git history of this checkout: 429 commits,
   from 2026-08-18 to 2026-09-24, fetched in full with
   ``git fetch --unshallow``. It also draws on ``README.md``,
   ``CONTRIBUTING.md``, package READMEs and ``apps/review-desktop/UPSTREAM``.
   The repository has **no Git tags, CHANGELOG or release notes**. Desktop
   versions come from ``chore(review-desktop): bump version`` commits. Pull
   request numbers (``#NNN``) come from squash-merge commit subjects in the
   upstream ``devdotfast/whiteboard`` repository.

   The first commit, ``d1c6463c`` "Import Review Desktop", adds 6,762 files
   at desktop version 0.0.23. **Everything before 2026-08-18 happened in
   another repository and is not visible here.** Claims about that period
   are inferences.

Before this repository (inferred)
---------------------------------

The import commit already contains the Code - OSS fork, the MDX-based review
runtime, trace capture, telemetry and a published desktop at version 0.0.23.
Several names come from earlier product names:

* ``progressive-review``: ``packages/progressive-review``, the
  ``PROGRESSIVE_REVIEW_TELEMETRY_DISABLED`` variable, and commit subjects
  such as ``fix(progressive-review): …``.
* ``Review`` and ``Review Desktop``: every package and directory name.
* ``dev.fast``: the npm scope and bundle identifier ``dev.fast.review``.

The product was probably called "Progressive Review", then "Review", and
then "Whiteboard". Only the last rename is fully recorded here, in #478 to
#482, the #500 revert, then #506, #507 and #516.

Stages
------

Stage 1 — Import and stabilization (2026-08-18 → 08-25, v0.0.23–0.0.27)
   The monorepo is imported. The team adds hang-correlation and
   update-lifecycle telemetry (#3, #12), expires idle trace sessions (#13),
   and experiments with diff caching (#20 to #24, adding and removing
   caches). Trace storage becomes **experimental and opt-in** (#27).
   Desktop releases use semver tags (#29).

Stage 2 — Onboarding, channels, lint discipline (08-26 → 09-02, v0.0.28–0.0.3x)
   The team reworks the interactive tutorial (#40, #44). It adds a
   **preview release channel** with a distinct identity (#65, #67, #79),
   S3-compatible trace stores beyond R2 (#63), and bundles the CLI with
   skill installs (#55). It also adds **anti-slop oxlint rules** and
   enforces lint and format in CI (#95). This stage includes many
   Dependabot bumps inside ``code-oss/test`` and one VS Code security
   backport (#41).

Stage 3 — Collaboration features, then pruning (09-03 → 09-15)
   The team adds stacked PR navigation (#104), comment threads (#119 to
   #122), "Ask agent" with per-harness agent servers (#83, #201), OpenCode
   support (#84) and OpenCode trace capture (#160). It adds a **hosted
   trace store** and publishes ``@dev.fast/trace-protocol`` (#125). Software
   maps and review documents become **JSON data** (#161). Runtime MDX
   bundling is replaced by native document construction (#187). The trace
   runtime and protocol are split into their own packages (#253 to #256),
   and the package directory is renamed (#259). The stage ends with a large
   **removal**: comments, Ask and the native agent terminals (#258), and
   ``review wait`` (#263). DOM tests move to Vitest Browser Mode (#276).

Stage 4 — The JSON Review migration (09-16 → 09-18)
   A five-part stack, "[1/5]…[5/5] JSON Review" (#264, #265, #267, #268,
   #270), introduces **server-owned JSON snapshots with pinned source**,
   renders them in the existing canvas, and exposes **thin CLI and MCP
   authoring clients**. Legacy MDX reviews are imported (#296). The team
   stops writing legacy reviews (#312) and removes the MDX compiler (#322)
   and the legacy runtime (#325). The stage also adds sharing through
   GitHub checkouts (#338), live worktree targets (#335) and a per-journey
   Desktop e2e suite (#344).

Stage 5 — Structural diff, headless authoring, the canvas as a whiteboard (09-19 → 09-23)
   **Structural (semantic) diffs** are integrated (#245), and the ``diffr``
   binary is bundled through ``@dev.fast/diffr`` (#394, #396). The feature is
   turned off by default (#429, #447) and then turned on again (#471). The
   team adds headless authoring and authoring from GitHub Actions (#356,
   #357), consolidates tracing into the Review CLI (#365), separates the
   canvas from the Node runtime (#366), and publishes CLI releases from
   version bumps (#367). It adds the **scratchpad** (#392, feature-flagged
   in #446). A burst of canvas work (#417 to #428: "flow units", "courier",
   "draw queue", "node with link") makes the agent's edits draw live. File
   **lenses** become review data (#486, #487).

Stage 6 — The Whiteboard rename and 0.1 release (09-23 → 09-24, v0.0.34–0.1.1)
   A first rename stack (#478 to #482) is **reverted in full** by #500 "so
   the user-facing rename can be rebuilt separately with a narrower scope".
   The rename is then redone in smaller pieces: MCP tools, skills and agent
   connections (#506), desktop branding (#507), release artifacts (#543)
   and the README (#516). Agents now connect through **generated prompts**
   instead of written config (#475). Several Desktops can share one home
   through **instances** (#511). Telemetry gets a documented contract
   (#533, #550, #570). Install prompts point at ``devdotfast/whiteboard``
   (#576). Versions 0.1.0 and 0.1.1 follow release-packaging fixes (#578).

Recurring themes
----------------

* **Adding, then removing.** Caches (#20 to #24), Ask and comments (#83 to
  #258), batch authoring (#356 to #469), and bundling Rust and Go language
  servers by default (#557 to #564) were all added and later removed. The
  team rolls back quickly when a feature does not pay off.
* **Contracts in separate packages.** Trace protocol, share protocol and
  review protocol are published or bundled separately. This lets the CLI,
  the hosted store and the desktop fork move on different schedules.
* **The server owns the data.** Content moved from files and MDX that
  agents edited to a JSON store owned by the server, which agents reach
  only through validated commands.

Open questions
--------------

* What the pre-import repository looked like, and when the Code - OSS fork
  was first vendored. ``UPSTREAM`` gives the pin (``8a7abeba``) but no
  date.
* Whether ``packages/progressive-review`` is still used. It holds only
  ``tutorial/data.ts``, which predates the rename.
* The status of the hosted trace store server. Its code is not in this
  repository; only the client and contract are.
* ``CONTRIBUTING.md`` still links issues at ``devdotfast/review``, while the
  install prompts point at ``devdotfast/whiteboard``. The repository was
  probably renamed recently.
