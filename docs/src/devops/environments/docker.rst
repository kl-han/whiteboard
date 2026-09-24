Docker
======

**Status: not provided by the repository.**

Evidence checked
----------------

``git ls-files`` finds no ``Dockerfile``, ``docker-compose.*`` or
``.dockerignore`` outside ``apps/review-desktop/code-oss/``. The files under
``code-oss/.devcontainer/`` belong to VS Code upstream (see
:doc:`devcontainer`). No workflow builds or runs a container.

When a container could still help
---------------------------------

A container can run the **non-GUI** part of the project: package builds,
lint, format, the package unit tests, headless ``whiteboard server start``,
and this documentation build. The desktop app needs Electron with a display,
so it is a poor fit.

Suggested (unverified) setup
----------------------------

.. code-block:: dockerfile

   # Sketch only — not part of the repository and not tested by CI.
   FROM node:24-bookworm
   RUN corepack enable && apt-get update && apt-get install -y git python3-pip
   WORKDIR /src
   COPY . .
   RUN pnpm install --frozen-lockfile && pnpm run build

Pros and cons
-------------

* Pros: reproducible Node 24 and pnpm 11 without changing the host.
* Cons: no display for Desktop. Browser tests also need
  ``playwright install-deps``. Bind-mounting ``~/.dev`` shares state with
  the host app.

Verification commands
---------------------

``docker build .`` has nothing to build, because the repository has no
Dockerfile. After you create one, run the commands from :doc:`local`.

Failure modes
-------------

* Alpine images: the Code - OSS native modules and Electron expect glibc.
* A missing ``git`` or ``jj`` breaks ``local-vcs`` and the tutorial asset
  build, which creates a Git repository.
