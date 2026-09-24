Project setup
=============

This page lists the setup commands and what each one does. For the results of
running them in a clean Linux container, see :doc:`verification_results`.

Prerequisites
-------------

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Tool
     - Version
     - Source of truth
   * - Node.js (monorepo)
     - ``>=24 <25``
     - ``.nvmrc`` (``24``), root ``package.json`` ``engines``
   * - Node.js (Code - OSS fork)
     - ``24.18.0`` exactly
     - ``apps/review-desktop/code-oss/.nvmrc``. The build scripts switch
       versions with ``fnm`` or ``nvm`` when either is installed.
   * - pnpm
     - ``>=11 <12``, pinned to ``pnpm@11.1.2``
     - root ``package.json`` ``packageManager`` and ``engines``
   * - Python 3 and a C/C++ toolchain
     - any recent
     - Needed for native modules in the Code - OSS build. On macOS, install
       the Xcode Command Line Tools.
   * - Linux system libraries
     - —
     - ``libx11-dev libxkbfile-dev libkrb5-dev libsecret-1-dev``
   * - ``zstd``
     - —
     - Only for the release payload handoff
   * - Python docs toolchain
     - see ``docs/requirements.txt``
     - Only for building this documentation

Enable pnpm with Corepack (``corepack enable``) or install pnpm 11 directly.
pnpm 11 enforces ``engines``, so running under Node 22 fails.

Environment variables
---------------------

None are required for the everyday commands. These change behavior (all
confirmed in code or package scripts):

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Variable
     - Effect
   * - ``DEV_REVIEW_HOME``
     - Root of all runtime state. Defaults to ``~/.dev``. It holds reviews,
       ``review-api.db``, ``review-desktop/`` discovery and profile, and
       ``trace/``.
   * - ``DEV_REVIEW_INSTANCE``
     - Selects the Desktop instance for CLI and MCP (``stable``, ``preview``,
       a dev key …)
   * - ``DEV_REVIEW_SERVER_DIR`` / ``--state-dir``
     - An isolated headless profile for ``server``, ``api`` and ``mcp``
   * - ``REVIEW_DESKTOP_DEV_FAST=1``
     - Fast incremental desktop build. ``pnpm dev`` sets it.
   * - ``DEV_FAST_REVIEW_DESKTOP_BACKGROUND=1``
     - Launch without taking focus. ``pnpm dev:background`` sets it.
   * - ``DEV_REVIEW_EXTENSIONS``
     - ``all`` (the default), ``none``, or a comma-separated list of curated
       extension groups for dev launches
   * - ``DEV_FAST_REVIEW_DESKTOP_STATE_ROOT``
     - Moves the Code - OSS profile to an isolated directory (used by tests)
   * - ``REVIEW_DIFFR_BINARY``
     - Path to a ``diffr`` executable for structural diffs
   * - ``DEV_FAST_REVIEW_CLI_NO_DELEGATE``
     - Stops a standalone CLI from delegating to the Desktop-bundled CLI
   * - ``DO_NOT_TRACK`` (and others in ``docs/telemetry.md``)
     - Turns off telemetry
   * - ``REVIEW_LEGACY_CORPUS``
     - Required by ``test:legacy-corpus``
   * - Signing and notarization (``CODESIGN_IDENTITY``, ``APPLE_*``, ``NOTARY_KEYCHAIN_PROFILE``)
     - Only for signed macOS packaging. See ``apps/review-desktop/README.md``.

Install dependencies
--------------------

.. code-block:: sh

   pnpm install

``pnpm-workspace.yaml`` sets ``minimumReleaseAge: 10080``, which means
dependencies must have been published for at least seven days. It also sets
``minimumReleaseAgeStrict``, so a newly added dependency younger than a week
fails to resolve unless you add it to ``minimumReleaseAgeExclude`` with a
justification. The ``@dev.fast/local-vcs`` override points the published
range at the workspace copy. The comment in the file says not to remove it.

On a fresh checkout, pnpm prints ``Failed to create bin … dist/cli.js``
warnings. They are harmless: ``dist/`` does not exist until the first build.

Develop and run
---------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Command
     - What it does
   * - ``pnpm dev``
     - Fast desktop build (``REVIEW_DESKTOP_DEV_FAST=1 pnpm desktop:build``),
       then ``pnpm desktop:run``. Needs a display.
   * - ``pnpm dev:background``
     - Same, but the window does not take focus
   * - ``pnpm desktop:build``
     - ``apps/review-desktop/scripts/build.sh``. Installs Code - OSS npm
       dependencies, curated extensions and Electron, syncs the protocol, and
       compiles and typechecks the client.
   * - ``pnpm desktop:run``
     - ``scripts/run.sh``. Rebuilds a stale server or canvas, then launches
       Electron.
   * - ``pnpm desktop:watch``
     - Incremental Code - OSS compiler for work on ``src/vs/review``
   * - ``pnpm --filter @dev.fast/review-canvas build``
     - Rebuild the canvas, then reload the Desktop window
   * - ``pnpm review <args>`` / ``pnpm --filter @dev.fast/review whiteboard <args>``
     - Run the CLI from source through ``tsx``
   * - ``pnpm clean``
     - Reset generated Code - OSS artifacts and the local Desktop profile.
       Authored reviews are kept.

Build, check, test
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Command
     - What it does
   * - ``pnpm run build``
     - ``pnpm -r --if-present build``: tsc and tsdown for the packages, and
       Vite for the canvas
   * - ``pnpm run typecheck``
     - Runs each package's ``typecheck`` one at a time. **Includes the
       desktop fork** (``tsgo``), so it needs the Code - OSS dependencies.
   * - ``pnpm run lint``
     - ``oxlint --disable-nested-config .`` (Code - OSS is ignored)
   * - ``pnpm run format`` / ``format:check``
     - ``oxfmt`` over ``apps/`` and ``packages/`` sources and root JSON
   * - ``pnpm run test``
     - ``node --test scripts/**/*.test.mjs``, then each package's ``test``
       (Vitest, plus ``node --test`` for desktop scripts)
   * - ``pnpm run ci``
     - Desktop ``app:build``, then ``check:tutorial``, lint, format:check,
       typecheck and test
   * - ``pnpm --filter @dev.fast/review test:integration:diffr``
     - Structural-diff integration tests (fetch ``diffr`` first)

Browser tests
-------------

DOM-facing canvas tests run in Chromium through Vitest Browser Mode and the
Playwright provider:

.. code-block:: sh

   pnpm --filter @dev.fast/review-canvas exec playwright install chromium --only-shell
   pnpm --filter @dev.fast/review-canvas test:browser

On a bare Linux host, also run ``playwright install-deps chromium``, as CI
does. ``CONTRIBUTING.md`` spells the filter ``@dev.fast/review``, but the
``test:browser`` scripts live in ``@dev.fast/review-canvas``
(``packages/review/app/package.json``).

Documentation build
-------------------

.. code-block:: sh

   python3 -m pip install -r docs/requirements.txt
   sphinx-build -b html docs docs/_build/html

Open ``docs/_build/html/index.html``. If ``sphinxcontrib-mermaid`` is not
installed, diagrams show their Mermaid source instead (see ``docs/conf.py``).

Packaging and deployment
------------------------

* **macOS**: ``SKIP_NOTARIZE=1 pnpm --filter @dev.fast/review-desktop app:package:macos``
  builds an unsigned ``Whiteboard.app``. Signed releases come from the
  **Review Desktop Release** workflow. That workflow compiles the payload
  on Linux (``review_big_boy``) and signs it on ``macos-15-xlarge``.
* **Linux**: ``pnpm desktop:package:linux``. Fedora RPM repositories are
  built by ``review-linux-build.yml``.
* **CLI**: ``review-cli-release.yml`` packs ``@dev.fast/review``, runs a
  smoke test, and publishes it to npm with provenance.
* Updates are served from ``https://update.dev.fast`` on the ``stable`` and
  ``preview`` channels.
