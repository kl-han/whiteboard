Package roles
=============

There are 12 workspace projects (``pnpm install`` reports "Scope: all 12
workspace projects"). They come from ``pnpm-workspace.yaml``:
``packages/*``, ``packages/agent-plugins/opencode``,
``packages/agent-plugins/pi``, ``packages/review/app`` and ``apps/*``.

.. list-table::
   :header-rows: 1
   :widths: 25 12 13 50

   * - Package (path)
     - Published?
     - Build
     - Role
   * - ``@dev.fast/review`` (``packages/review``)
     - npm (public)
     - tsdown
     - The ``whiteboard`` / ``review`` CLI, servers, JSON API, MCP and
       sharing. Workspace libraries are bundled in and listed as dev
       dependencies.
   * - ``@dev.fast/review-canvas`` (``packages/review/app``)
     - private
     - Vite
     - The React canvas, copied into Desktop
   * - ``@dev.fast/review-desktop`` (``apps/review-desktop``)
     - private
     - ``build.sh`` (Code - OSS gulp/esbuild)
     - The desktop app, packaging and release scripts
   * - ``@dev.fast/review-protocol``
     - private
     - tsc
     - Shared contracts. Also generated into the fork.
   * - ``@dev.fast/review-share-protocol``
     - npm (0.1.1)
     - tsc
     - Portable immutable review-sharing envelope
   * - ``@dev.fast/trace-core``
     - private
     - tsdown
     - Trace capture, storage and read logic
   * - ``@dev.fast/trace-protocol``
     - npm (0.5.0)
     - tsc
     - Hosted trace store contract
   * - ``@dev.fast/local-vcs``
     - npm (0.1.0)
     - tsdown
     - Git and jj helpers
   * - ``@dev.fast/json``
     - private
     - tsc
     - JSON decoding helpers
   * - ``@dev.fast/opencode-whiteboard``
     - npm (0.1.1)
     - none (plain JS)
     - OpenCode plugin that registers the MCP server
   * - ``@dev.fast/pi-whiteboard``
     - npm (0.1.1)
     - none
     - Pi package that ships ``skills/whiteboard/SKILL.md``
   * - root ``@dev.fast/review-workspace``
     - private
     - —
     - Workspace scripts, lint, format and TypeScript toolchain

Claude, Codex and Cursor plugins are **not** workspace packages. They are
directories of manifests, referenced by ``.claude-plugin/marketplace.json``
and ``.agents/plugins/marketplace.json``.

Key external runtime dependencies
---------------------------------

* ``hono`` and ``@hono/node-server``: the HTTP servers.
* ``@modelcontextprotocol/sdk``: the stdio MCP server.
* ``commander``: CLI parsing.
* ``zod`` 4: every schema and contract.
* ``pino``: logging.
* ``sharp``: image decoding to PNG. It is disabled on Linux Desktop because
  of crashes (#439).
* ``@xyflow/react``, ``elkjs``, ``react`` 19, ``zustand``: the canvas.
* ``@dev.fast/diffr``: the structural diff engine and its types. It is
  fetched as a binary with ``diffr-fetch``.
* ``isomorphic-git`` (dev) and ``git-url-parse``: Git utilities.
