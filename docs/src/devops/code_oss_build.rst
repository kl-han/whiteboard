Building the Code - OSS desktop
===============================

The desktop build is **Code - OSS's own build**, wrapped by
``apps/review-desktop/scripts/build.sh``. It follows upstream rules, not
the monorepo's.

Rules (DOCUMENTED, desktop README)
----------------------------------

* Run Code - OSS commands **with npm from** ``code-oss/`` and never with the
  monorepo's pnpm.
* Use Node **24.18.0** (``code-oss/.nvmrc``). ``code-oss-dependencies.sh``
  switches versions with ``fnm`` or ``nvm``, and fails if neither exists
  and the active Node differs.
* Linux needs ``libx11-dev libxkbfile-dev libkrb5-dev libsecret-1-dev``,
  Python 3 and a C/C++ toolchain. macOS needs the Xcode Command Line Tools.

What ``app:build`` does (CONFIRMED from ``build.sh``)
-----------------------------------------------------

1. ``ensure_code_oss_dependencies``: ``npm ci --no-audit --no-fund
   --prefer-offline`` in ``code-oss/``, skipped when the package-lock digest
   stamp matches.
2. Copies the dompurify manifest, then materializes curated extensions
   (``curated-extensions.mjs``; ``--only=$DEV_REVIEW_EXTENSIONS`` in fast
   mode).
3. Unless ``REVIEW_DESKTOP_COMPILE_ONLY=1``, downloads Electron
   (``npm run electron``) when the binary is missing or its version differs
   from ``.npmrc`` ``target``. On macOS full builds, it applies the adaptive
   icon.
4. Runs ``protocol:sync``, which generates ``src/vs/review/common/reviewProtocol.ts``.
5. Compiles the client and extensions. Fast mode uses esbuild
   ``transpile-client`` without a typecheck. ``REVIEW_DESKTOP_CI_FAST=1``
   transpiles while ``tsgo`` typechecks in the background.

What you may change casually
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Path
     - Guidance
   * - ``code-oss/src/vs/review/**``
     - Yes. Use ``pnpm desktop:watch`` and **Developer: Reload Window**.
   * - ``apps/review-desktop/scripts/**``
     - Yes, with the script tests
       (``pnpm --filter @dev.fast/review-desktop test``).
   * - Upstream files already listed in ``UPSTREAM``
     - Carefully. Keep hunks minimal, and update the entry.
   * - Any other upstream file
     - No, unless you add an ``UPSTREAM`` entry. Prefer a contribution
       under ``src/vs/review``.
   * - ``code-oss/package-lock.json``
     - Only for security bumps within existing ranges, with npm.
   * - ``reviewProtocol.ts``
     - Never. It is generated.

Validation tiers
----------------

* **Fast tier**, no Code - OSS dependencies needed: ``pnpm --filter
  @dev.fast/review-desktop test``. It runs ``node --test`` over the scripts
  and ``tsx --test`` over ``src/vs/review/**/*.test.ts``. **Passed here**
  (105 + 197).
* **Typecheck tier**: ``pnpm --filter @dev.fast/review-desktop typecheck``,
  which runs ``tsgo`` from the Code - OSS dependencies. **Blocked here.**
* **Build and e2e tiers**: ``app:build``, ``test:e2e:lsp`` and
  ``test:e2e:telemetry`` under ``xvfb-run``. **Blocked here.**

See :doc:`native_dependencies` for why the dependency install fails
without network access to ``electronjs.org``.
