Remote VM and CI runners
========================

**Status: used by CI; not documented as a developer environment.**

Evidence checked
----------------

``.github/workflows`` uses three runner types:

* ``ubuntu-latest``: ``review-desktop-ci.yml`` (lint, format, desktop build,
  typecheck, tests, diffr integration, LSP and telemetry e2e under
  ``xvfb-run``) and ``review-cli-release.yml``.
* ``review_big_boy``: a self-hosted or large Linux runner. It compiles the
  darwin payload and builds Fedora packages.
* ``macos-15-xlarge``: signs, notarizes and smoke-tests the macOS app.

The team also works in cloud agent containers. This page was written in one
(see :doc:`../verification_results`).

When to use it
--------------

* Headless work on a Linux VM: package builds, tests, the headless server
  and docs.
* GUI checks on a VM: wrap commands in ``xvfb-run -a`` as CI does, for
  example ``xvfb-run -a pnpm --filter @dev.fast/review-desktop test:e2e:lsp``.

Setup steps
-----------

Follow :doc:`local`. On a VM without Node 24, download the official
``linux-x64`` tarball from nodejs.org into a local prefix and put it first
on ``PATH``.

Pros and cons
-------------

* Pros: matches CI. Plenty of CPU for the Code - OSS compile.
* Cons: no interactive display. Outbound network policies can block the
  Electron, extension or ``diffr`` downloads.

Verification commands
---------------------

.. code-block:: sh

   pnpm install --frozen-lockfile
   pnpm lint && pnpm format:check
   pnpm run build && pnpm run test

Failure modes
-------------

* Blocked egress: ``ensure:diffr``, ``npm run electron`` and the curated
  extension downloads fail.
* Missing ``playwright install-deps``: browser tests fail to launch
  Chromium.
