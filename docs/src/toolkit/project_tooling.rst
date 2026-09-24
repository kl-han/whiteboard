Project tooling
===============

This page covers only the tools that shape everyday work. Official
documentation links are listed at the end.

pnpm workspace
--------------

* **Use**: dependency management and filtered script runs
  (``pnpm --filter @dev.fast/review …``, ``pnpm -r --if-present build``).
* **Why it matters**: ``pnpm-workspace.yaml`` sets ``nodeLinker: hoisted``
  (a flat ``node_modules`` for Electron and tooling compatibility,
  inferred), ``enableGlobalVirtualStore``, and a **7-day**
  ``minimumReleaseAge`` with a strict exclusion list. It also sets
  ``allowBuilds`` (only ``esbuild`` may run install scripts) and security
  ``overrides``.
* **Where**: ``pnpm-workspace.yaml``, ``pnpm-lock.yaml``, root
  ``package.json``.
* **Commands**: ``pnpm install``, ``pnpm install --frozen-lockfile`` (CI),
  ``pnpm --filter <pkg> <script>``.
* **What can go wrong**: adding a dependency younger than 7 days fails
  resolution. Removing the ``@dev.fast/local-vcs`` override makes
  ``@dev.fast/review`` resolve the registry copy. Running pnpm inside
  ``code-oss/`` is wrong: use ``npm`` there (desktop README).

Node.js and pnpm versions
-------------------------

* Monorepo: Node ``>=24 <25`` (``.nvmrc`` = 24) and pnpm ``11.1.2``
  (``packageManager``).
* Code - OSS fork: Node ``24.18.0`` exactly (``code-oss/.nvmrc``). The
  scripts switch versions with ``fnm`` or ``nvm``.
* **What can go wrong**: pnpm 11 enforces ``engines``. The CLI refuses a
  system Node older than 24, except under Electron.

TypeScript
----------

* **Use**: all packages. ``tsconfig.base.json`` targets ES2022 with
  ``lib: ES2025`` for iterator helpers and ``moduleResolution: bundler``.
  ``paths`` map ``@dev.fast/*`` to ``packages/*/src``. The repository does
  **not** use project references.
* **Versions**: the root uses ``typescript@7.0.1-rc`` (the native ``tsgo``
  compiler) through ``pnpm -w exec tsc``. Packages pin ``typescript@6.0.3``
  for tooling. The fork runs ``tsgo`` from its own npm dependencies.
* **Commands**: ``pnpm run typecheck``, or
  ``pnpm --filter <pkg> typecheck``.
* **What can go wrong**: ``tsgo: not found`` when the fork's dependencies
  are missing (see :doc:`../devops/verification_results`).

oxlint
------

* **Use**: linting with the ``typescript``, ``oxc``, ``react``,
  ``jsx-a11y`` and ``vitest`` plugins, plus the custom ``anti-slop`` JS
  plugin (``tools/oxlint/anti-slop/index.ts``).
* **Commands**: ``pnpm lint`` (``oxlint --disable-nested-config .``).
* **What can go wrong**: ``code-oss/**`` is ignored on purpose. The new
  anti-slop rules start as warnings (#229).

oxfmt
-----

* **Use**: formatting for ``apps/`` and ``packages/`` TS, JS, JSON and CSS,
  and root JSON. It sorts imports (``.oxfmtrc.json``).
* **Commands**: ``pnpm format`` and ``pnpm format:check``.
* **What can go wrong**: files outside those globs, including this
  ``docs/`` tree, are not formatted.

Vitest and ``node --test``
--------------------------

* **Use**: Vitest 4 for package tests. ``@dev.fast/review`` defines projects
  (``shared-module-graph`` for Node, plus a diffr integration config). The
  canvas defines ``canvas-node`` and ``browser`` projects. ``node --test``
  runs ``scripts/**/*.test.mjs`` and the desktop script tests. ``tsx
  --test`` runs ``code-oss/src/vs/review/**/*.test.ts``.
* **Commands**: ``pnpm test``,
  ``pnpm --filter @dev.fast/review test:node``,
  ``pnpm --filter @dev.fast/review-canvas test:browser``.
* **What can go wrong**: tests that create Git repositories fail under
  ``root`` with "dubious ownership". The ``pretest`` hooks build tutorial
  assets, which needs ``git``.

Playwright and Chromium (Vitest Browser Mode)
---------------------------------------------

* **Use**: DOM tests through ``@vitest/browser-playwright`` (#276). The
  desktop e2e and smoke scripts also use ``playwright`` directly.
* **Commands**:
  ``pnpm --filter @dev.fast/review-canvas exec playwright install chromium --only-shell``,
  plus ``install-deps`` on bare Linux.
* **What can go wrong**: the Playwright version is pinned (1.62.1). A
  different preinstalled browser build is not found.

Vite
----

* **Use**: builds the canvas (``desktop.vite.config.ts`` with
  ``@vitejs/plugin-react``). Vite is overridden to ``8.0.16`` workspace-wide.
* **Commands**: ``pnpm --filter @dev.fast/review-canvas build``.

tsdown
------

* **Use**: bundles ``@dev.fast/review``, ``trace-core`` and ``local-vcs``
  (rolldown-based), targeting Node 24.

Desktop build and package tooling
---------------------------------

* **Use**: Code - OSS gulp and esbuild tasks, the Electron download
  (``npm run electron``), curated extensions (``curated-extensions.mjs``),
  ``package-macos.sh`` (sign, notarize, DMG and Squirrel zips) and
  ``package-linux*.sh`` (RPM repositories via ``build-linux-repository.py``).
* **What can go wrong**: blocked downloads from ``electronjs.org``,
  ``open-vsx.org`` or ``marketplace.visualstudio.com``. The ``tsgo`` and
  native module builds need Python and a C++ toolchain.

Sphinx documentation toolchain
------------------------------

* **Use**: this site. ``docs/conf.py`` enables ``sphinxcontrib.mermaid``,
  ``myst_parser`` and ``sphinx_rtd_theme`` when they are installed, and
  falls back to alabaster and plain-source diagrams when they are not.
* **Commands**: ``python3 -m pip install -r docs/requirements.txt`` and
  ``sphinx-build -b html docs docs/_build/html``. Add ``-W`` to treat
  warnings as errors.
* **What can go wrong**: Mermaid renders in the browser from a CDN, so an
  offline viewer sees nothing unless ``mermaid_use_local`` is configured.
  The existing ``docs/*.md`` files are excluded from the build on purpose.

Official references
-------------------

Our environment's egress policy blocked most documentation hosts. Only
``github.com/mgaitan/sphinxcontrib-mermaid`` and ``nodejs.org`` were
fetched and checked. The others are the canonical official locations:

* Sphinx: https://www.sphinx-doc.org/en/master/usage/configuration.html and
  toctree https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree
* sphinxcontrib-mermaid: https://github.com/mgaitan/sphinxcontrib-mermaid
  (``extensions += ["sphinxcontrib.mermaid"]``, ``mermaid_version``,
  ``mermaid_init_config``, ``mermaid_use_local``)
* Mermaid syntax: https://mermaid.js.org/syntax/flowchart.html,
  https://mermaid.js.org/syntax/sequenceDiagram.html
* sphinx-rtd-theme: https://sphinx-rtd-theme.readthedocs.io/
* MyST parser: https://myst-parser.readthedocs.io/
* pnpm workspaces and settings: https://pnpm.io/workspaces,
  https://pnpm.io/settings
* TypeScript project references (not used here):
  https://www.typescriptlang.org/docs/handbook/project-references.html
* Playwright browsers: https://playwright.dev/docs/browsers
* Vitest Browser Mode: https://vitest.dev/guide/browser/
* Vite: https://vite.dev/guide/
* Electron ``utilityProcess``: https://www.electronjs.org/docs/latest/api/utility-process
* oxlint and oxfmt: https://oxc.rs/docs/guide/usage/linter,
  https://oxc.rs/docs/guide/usage/formatter
* Node.js test runner: https://nodejs.org/api/test.html
* Model Context Protocol: https://modelcontextprotocol.io/
