Architecture risk register
==========================

.. list-table::
   :header-rows: 1
   :widths: 5 15 17 15 17 13 18

   * - ID
     - Risk
     - Impact
     - Affected components
     - Current mitigation
     - Verification
     - Open questions
   * - R1
     - Vendored Code - OSS drifts from upstream
     - Missed security fixes; a costly refresh
     - ``code-oss/``
     - ``UPSTREAM`` inventory; cherry-picked advisories; guard tests
     - Guard tests pass. The serialization tag is missing here.
     - When is the next rebase? Who owns it? Where is the tag published?
   * - R2
     - The Node/native/Electron toolchain is fragile
     - Contributors cannot build Desktop
     - ``build.sh``, ``.npmrc``, native modules
     - Stamps; ``pnpm dev`` fast mode; CI on larger runners
     - The build FAILED here (network)
     - Offline header cache? Documented mirrors?
   * - R3
     - Whiteboard/Review/Progressive Review naming debt
     - Confusion; mistakes in docs and code
     - Packages, CLI bins, APIs (``reviewId`` vs. ``sessionId``), and
       ``progressive-review:`` storage keys in the canvas
     - The rename rules in #500 and #506
     - Partial
     - Is a full internal rename planned?
   * - R4
     - Drift between the Rust (diffr) and TypeScript contracts
     - Structural diff breaks at runtime
     - diffr, ``@dev.fast/diffr``, review-protocol
     - Exact pins; wire version check; integration tests
     - 9/9 integration tests pass with 0.1.3
     - Is there CI that tests diffr ``main`` against Whiteboard?
   * - R5
     - diffr covers only macOS arm64 and Linux x64
     - No semantic diff on Windows, Intel Mac or ARM Linux
     - ``diffr-fetch``
     - Documented in the diffr README
     - CONFIRMED in the fetcher
     - A roadmap for more targets?
   * - R6
     - Behavior that only works in Desktop
     - Headless users miss the workspace, LSP, the scratchpad and opening
       reviews
     - review-api, fork
     - ``desktopAvailable`` capability flag
     - The headless path is verified
     - —
   * - R7
     - Agent MCP host compatibility
     - Tools are not listed; there are reload issues
     - ``mcp.ts``, plugins
     - ``tools/list_changed`` plus a ``RELOAD_TOOLS`` hint
     - Smoke-tested with a generic client only
     - Is there a test matrix per agent host?
   * - R8
     - Trace service availability and consent
     - Decision log gaps
     - trace-core, hosted store
     - Opt-in; S3 alternative; memory transport
     - Unit tests only
     - Hosted store SLA? Is the server open source?
   * - R9
     - Stored-data migrations
     - Data loss for legacy reviews
     - review-import, migrations
     - Golden fixtures; a private corpus run
     - Fixtures pass
     - When can legacy import be retired?
   * - R10
     - Cross-platform limits
     - Linux has packages but macOS is the main target; no Windows
     - Packaging, diffr
     - Fedora RPM repositories
     - —
     - Windows plans?
   * - R11
     - Browser version pinning for tests
     - Flaky CI when the Playwright browser is missing
     - Canvas tests
     - CI installs the browser
     - Needed a shim here
     - —
   * - R12
     - Multi-repository limits
     - Reviews that span repositories
     - The pins model (one ``repositoryId``)
     - Scratchpad pins per reference
     - DOCUMENTED limitation
     - —
   * - R13
     - Multiple Desktops share one home
     - Commands reach the wrong instance
     - Discovery, MCP latch
     - Instance keys; per-session latch; ``whiteboard_status``
     - Code reviewed
     - —
   * - R14
     - Security of the loopback token
     - A local process could read the discovery file
     - The server
     - Private atomic write; constant-time compare
     - Code reviewed
     - Are file permissions checked on read?
   * - R15
     - Dependencies released recently
     - Supply-chain risk
     - pnpm
     - A 7-day ``minimumReleaseAge`` with a justified exclusion list
     - Config reviewed
     - —
