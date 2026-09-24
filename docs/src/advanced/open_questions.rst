Open-question register
======================

Questions the repository alone cannot answer. Each has an ID, the evidence
we checked, and the research that would close it.

.. list-table::
   :header-rows: 1
   :widths: 6 30 32 32

   * - ID
     - Question
     - Evidence checked
     - Research needed
   * - Q1
     - How does diffr load external WASM plugins? What is the WIT interface,
       and what capabilities do plugins get (WASI-HTTP)?
     - Binary strings (wasmtime 34, wasi, wasi-http, wit-bindgen);
       ``plugins.external`` is ``{}``
     - Read ``devdotfast/diffr`` source and docs; write a sample plugin
   * - Q2
     - Which difftastic version is vendored in diffr, and how far does it
       diverge?
     - The strings "difftastic source", ``guess_language.rs``
     - diffr ``Cargo.toml`` and source tree
   * - Q3
     - What is the full language list, and how do ``group`` and
       ``removed-runs`` behave in detail?
     - ``config show --json``; one string table
     - diffr source or tests
   * - Q4
     - Where is the ``code-oss-upstream-8a7abeba`` tag published?
     - ``git tag`` is empty in this fork
     - Ask maintainers; check ``devdotfast/whiteboard`` tags
   * - Q5
     - When is the next Code - OSS rebase, and who owns it?
     - ``UPSTREAM`` records only cherry-picks since the import
     - Maintainer roadmap
   * - Q6
     - What is the hosted store (``app.dev.fast``)? Its implementation,
       availability, and whether it is open source?
     - Client and protocol only
     - dev.fast documentation
   * - Q7
     - What did the pre-import (before 2026-08-18) history look like?
     - The import commit has 6,762 files
     - The original repository, if it is accessible
   * - Q8
     - Is ``packages/progressive-review/tutorial/data.ts`` still consumed?
     - No ``package.json``. ``git grep`` finds no importer of the path. The
       string survives only as a canvas storage-key prefix
       (``app/src/host/review-client.ts``) and in test fixtures.
     - Ask the author, then delete the directory. Keep the storage prefix,
       because changing it would reset stored UI state.
   * - Q9
     - Does ``libavoid.wasm`` distribution meet the LGPL notice
       requirements in every artifact?
     - ``THIRD_PARTY_NOTICES.md``, ``code-oss/licenses/``
     - Inspect packaged DMG and RPM contents
   * - Q10
     - What is the desktop launch behavior on Linux under Wayland/X11 in CI
       (``xvfb-run``)?
     - Workflows use ``xvfb-run -a``
     - A CI run log from upstream
   * - Q11
     - How can Electron headers be cached for offline or proxied builds?
     - ``.npmrc`` ``disturl``; the node-gyp failure
     - Test ``npm_config_nodedir`` with pre-fetched headers
   * - Q12
     - How is the telemetry key embedded (``embed-posthog-key.mjs``) in
       releases, and is there a dev key?
     - The script exists
     - Release workflow secrets (maintainers)
