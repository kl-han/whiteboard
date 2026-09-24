Recommendations
===============

These are proposals only. Nothing here was changed as part of the
investigation. They are ordered by value to a new contributor.

Documentation-only
------------------

1. **Say plainly that semantic diff is external.** The README says "we wrote
   a semantic, AST-aware diff viewer in Rust" but never mentions
   ``devdotfast/diffr``. A one-line pointer would save newcomers from
   searching for Rust in this repository. (README edits need maintainer
   permission, per ``AGENTS.md``.)
2. **Fix the** ``CONTRIBUTING.md`` **filter** for browser tests
   (``@dev.fast/review-canvas``, not ``@dev.fast/review``) and the issue
   link (``devdotfast/review`` → ``devdotfast/whiteboard``).
3. **Publish the MCP lifecycle** (see :doc:`../agents/mcp_architecture`) in
   ``packages/review/README.md``.

Build-system improvements
-------------------------

4. Add top-level scripts per subsystem, such as ``pnpm verify:cli``,
   ``verify:canvas`` and ``verify:desktop-fast``. They would mirror
   :doc:`../devops/subsystem_development`, so a failure points at one tier.
5. Document an **offline or proxied native build**: a mirror ``disturl`` or
   a pre-fetched ``nodedir``, plus Open VSX caching.
6. Make ``pnpm run typecheck`` skip the fork with a clear message when the
   Code - OSS dependencies are absent, instead of failing with ``tsgo: not
   found``.

Test improvements
-----------------

7. **An MCP stdio integration test.** It would cover initialize, a listing
   while down, ``list_changed`` and ``isError``, similar to the smoke
   script used here.
8. **A diffr contract canary.** A CI job that runs Whiteboard's
   ``test:integration:diffr`` against the diffr release candidate before the
   exact pin moves.
9. Make the legacy-fixture tests independent of Git ownership, for example
   by passing ``-c safe.directory=*`` in the fixture helper, so root
   containers pass.

Architecture improvements
-------------------------

10. **Deduplicate instance selection.** ``cli.ts`` copies the logic of
    ``selectReviewInstance``. A shared, dependency-free module would remove
    the drift risk (R13).
11. Add **explicit versioning to the REST API**, or at least an
    ``/authoring`` catalog version. That would let external MCP clients
    detect a skew without relying on CLI delegation.

Cleanup
-------

12. Remove ``packages/progressive-review`` once Q8 is resolved.
13. Remove the ``.gitignore`` entries for tooling that no longer exists
    (``packages/code-graph``, ``.devbox``, Terraform state).
14. Continue the internal ``review`` → ``whiteboard`` rename only as a
    planned, staged migration. #500 shows the cost of a broad rename stack.
