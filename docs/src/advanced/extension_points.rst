Extension points
================

.. list-table::
   :header-rows: 1
   :widths: 22 38 40

   * - Extension point
     - Where
     - Notes
   * - New block kind
     - ``packages/review/src/review-api/blocks/<kind>.ts`` + ``blocks/index.ts``;
       a canvas renderer in ``packages/review/app/src/blocks.tsx``
     - ``index.ts`` requires a definition for every ``BlockType`` (a compile
       error otherwise). Add a migration if the stored shape changes.
   * - New authoring tool
     - ``review-api/authoring-tools.ts`` (+ route in ``http.ts``)
     - MCP and ``api`` get it from ``GET /authoring``. It is published as
       ``session_*`` automatically.
   * - Agent guidance
     - ``packages/review/instructions/*.md``; ``DEV-REVIEW.md`` in a user
       repository or in ``$DEV_REVIEW_HOME``
     - Topics are listed in ``INSTRUCTION_TOPICS`` (``instructions.ts``)
   * - New agent connector
     - ``packages/agent-plugins/<agent>`` + marketplace manifests;
       ``connect-prompts.ts``; trace hooks in ``trace-core/agent-trace-hooks.ts``
     - ``AgentTraceHookAgent`` lists the harnesses that get trace hooks
   * - Structural diff behavior
     - ``diffr`` configuration and WASM plugins (README); ``diffr-config.ts``;
       ``REVIEW_DIFFR_BINARY``
     - The settings UI has plugin and summary settings (#396)
   * - Trace store
     - ``trace-core/src/trace-storage/``, ``store-client.ts``; ``trace-protocol``
     - S3-compatible stores work beyond R2 (#63). The hosted store must match
       the protocol version exactly.
   * - Desktop workbench features
     - ``apps/review-desktop/code-oss/src/vs/review/{contrib,services}``
     - Record every fork divergence in ``UPSTREAM``. Run ``pnpm desktop:watch``.
   * - Curated editor extensions
     - ``apps/review-desktop/scripts/curated-extensions.manifest.mjs``
     - Groups are selectable with ``DEV_REVIEW_EXTENSIONS``
   * - Lint rules
     - ``tools/oxlint/anti-slop/rules`` and ``.oxlintrc.json``
     - Record provenance in ``tools/oxlint/anti-slop/UPSTREAM.md``
   * - CI authoring
     - ``whiteboard server start`` + ``whiteboard api`` in GitHub Actions
       (#357, #409)
     - Share the result with ``whiteboard share``
