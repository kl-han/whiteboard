Build topology
==============

**What builds what.** The requested draft had a Cargo branch for semantic
diff. There is none in this repository. diffr arrives as a **prebuilt
binary** (CONFIRMED).

.. mermaid::

   flowchart TD
       PNPM["pnpm 11 (Node 24)"] --> JsonPkg["json (tsc)"]
       PNPM --> TP["trace-protocol (tsc)"]
       PNPM --> RP["review-protocol (tsc)"]
       PNPM --> RSP["review-share-protocol (tsc)"]
       PNPM --> LV["local-vcs (tsdown)"]
       PNPM --> TC["trace-core (tsdown)"]
       PNPM --> RV["review (tsdown)<br/>dist/cli.js, dist/server/desktop-host.js, ..."]
       PNPM --> CV["review-canvas (Vite 8)"]
       JsonPkg --> RP
       TP --> RP
       TP --> TC
       LV --> TC
       RP --> RV
       RSP --> RV
       TC --> RV
       LV --> RV
       NPMREG["npm: @dev.fast/diffr 0.1.3"] -->|"diffr-fetch (ensure:diffr)"| Bin["review/bin/diffr<br/>(prebuilt from GitHub releases)"]
       NPMREG --> RP
       RDesk["review-desktop app:build (build.sh)"] -->|"npm ci (Node 24.18.0) + node-gyp vs Electron 42.10.0 headers"| CodeDeps["code-oss/node_modules"]
       RDesk -->|"protocol-sync.mjs"| Gen["code-oss/src/vs/review/common/reviewProtocol.ts (generated)"]
       RP --> Gen
       RDesk -->|"curated-extensions.mjs (open-vsx.org)"| Ext["extensions/*"]
       RDesk -->|"npm run electron (GitHub releases)"| Electron[".build/electron"]
       CodeDeps --> Gulp["Code - OSS gulp/esbuild compile + tsgo typecheck"]
       Gen --> Gulp
       Gulp --> Out["code-oss/out"]
       RunSh["run.sh"] -->|"rebuild if stale"| RV
       RunSh -->|"copy-canvas.mjs"| CV
       Out --> App["Runnable Desktop"]
       Electron --> App
       Bin -.->|"bundled at packaging (#394)"| App
       Pack["package-macos.sh / package-linux*.sh"] --> Artifacts["DMG, Squirrel zips, RPM repos"]
       App --> Pack
       PY["Python 3 + Sphinx"] --> DocsOut["docs/_build/html"]
       UV["uv (Python 3.12)"] --> Lat["scripts/review-latency"]

Notes (CONFIRMED from scripts):

* ``packages/review``'s ``prebuild`` builds its workspace dependencies with
  ``build:workspace-deps``. tsdown then **bundles** them into ``dist/``.
* The fork **never** runs pnpm. It uses npm with its own lockfiles and
  ``.npmrc`` (``runtime=electron``, ``build_from_source=true``).
* ``REVIEW_DESKTOP_DEV_FAST=1`` skips fresh client and extension outputs,
  based on stamps in ``code-oss/.build/dev-fast``.
* The macOS release splits the build. Linux (``review_big_boy``) compiles
  the darwin payload (``compile-darwin-payload.sh``), and
  ``macos-15-xlarge`` signs and notarizes it. This is the "Linux-to-macOS
  build handoff" in the desktop README.
