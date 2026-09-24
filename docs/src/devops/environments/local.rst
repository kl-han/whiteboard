Local development
=================

**Status: supported.** This is the only environment the repository documents
for developers (``CONTRIBUTING.md`` and ``apps/review-desktop/README.md``).

When to use it
--------------

Use it for everything: CLI and server work, canvas work, desktop fork work,
and packaging. The desktop app needs a real display, or ``xvfb-run`` on
Linux.

Setup steps
-----------

1. Install Node 24 (``nvm install 24`` or ``fnm install 24``). Also install
   ``fnm`` or ``nvm`` so the desktop scripts can switch to Code - OSS's
   exact Node ``24.18.0``.
2. ``corepack enable`` so that ``pnpm@11.1.2`` from ``packageManager`` is
   used.
3. On Linux, install ``libx11-dev libxkbfile-dev libkrb5-dev libsecret-1-dev``,
   Python 3 and a C/C++ toolchain. On macOS, install the Xcode Command Line
   Tools.
4. ``pnpm install``
5. ``pnpm dev`` (desktop), or ``pnpm review --help`` (CLI only).

Pros and cons
-------------

* Pros: this is what maintainers and CI use (CI runs on ``ubuntu-latest``);
  fast incremental builds with ``REVIEW_DESKTOP_DEV_FAST``; real GPU and
  display.
* Cons: the first desktop build is heavy. It downloads Electron and curated
  extensions and installs Code - OSS's npm dependencies. A dev build shares
  ``~/.dev`` with any installed Whiteboard unless you set
  ``DEV_REVIEW_HOME``.

Known limitations
-----------------

* macOS arm64 is the only packaged platform with signed release channels.
* A dev Desktop and an installed Desktop share data. Use
  ``whiteboard instances`` and ``DEV_REVIEW_INSTANCE`` to choose one, and
  reconnect the agent's MCP server after you switch.

Verification commands
---------------------

.. code-block:: sh

   node --version            # v24.x
   pnpm --version            # 11.x
   pnpm install
   pnpm run build && pnpm run lint && pnpm run format:check
   pnpm run test
   pnpm review version
   pnpm run ci               # full suite, includes the desktop build

Failure modes
-------------

* ``ERR_PNPM_UNSUPPORTED_ENGINE`` or a Node-version error: you are not on
  Node 24.
* ``tsgo: not found`` during ``typecheck``: the Code - OSS dependencies are
  not installed. Run ``bash apps/review-desktop/scripts/code-oss-dependencies.sh``
  or ``pnpm desktop:build``.
* ``Review Desktop binary is not built``: run ``pnpm desktop:build`` before
  ``desktop:run``.
