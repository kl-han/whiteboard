Native dependencies
===================

This page analyzes the failure from :doc:`verification_results`: the
desktop build stopped while rebuilding ``@parcel/watcher`` because node-gyp
could not fetch ``https://electronjs.org/headers/v42.10.0/node-v42.10.0-headers.tar.gz``.

The chain of cause
------------------

.. mermaid::

   flowchart TD
       A["pnpm desktop:build → build.sh"] --> B["code-oss-dependencies.sh:<br/>npm ci in code-oss/ (Node 24.18.0)"]
       B --> C[".npmrc: runtime=electron, target=42.10.0,<br/>disturl=https://electronjs.org/headers,<br/>build_from_source=true"]
       C --> D["postinstall.ts removes @parcel/watcher-* prebuilds<br/>(removeParcelWatcherPrebuild)"]
       D --> E["node-gyp rebuild of each native module<br/>(bundled node-gyp from build/npm/gyp)"]
       E --> F["download Electron 42.10.0 headers from disturl"]
       F -->|"egress proxy denies electronjs.org"| X["FAIL: gyp ERR! Request was cancelled"]

Answers
-------

.. list-table::
   :widths: 30 70

   * - Package that triggered node-gyp
     - ``@parcel/watcher`` 2.5.6, the first native module rebuilt (CONFIRMED
       in the npm log)
   * - Why it compiles
     - ``.npmrc`` sets ``build_from_source="true"`` and
       ``runtime="electron"``, so every native addon is compiled against
       Electron's ABI. ``postinstall.ts`` also deletes the platform
       prebuilds of ``@parcel/watcher`` on purpose (UPSTREAM behavior).
   * - Other native modules affected
     - The same path applies to ``@vscode/sqlite3``, ``@vscode/spdlog``,
       ``node-pty``, ``native-keymap``, ``@vscode/native-watchdog``,
       ``@vscode/deviceid`` and others (from ``code-oss/package.json``;
       INFERRED that they rebuild the same way)
   * - Electron version
     - 42.10.0 (``package.json`` ``devDependencies.electron``, ``.npmrc``
       ``target``); ``ms_build_id`` 15109253
   * - Headers URL
     - ``https://electronjs.org/headers/v42.10.0/node-v42.10.0-headers.tar.gz``
       (from the npm log)
   * - Prebuilt binaries
     - Deliberately bypassed by ``build_from_source``. Upstream VS Code
       builds natives from source for ABI safety (UPSTREAM).
   * - Electron binary itself
     - ``npm run electron`` → ``build/lib/electron.ts``. With an empty
       ``product.electronArtifactFeed`` (it is empty here), it downloads
       from Electron's GitHub releases (CONFIRMED in the code comment and
       ``product.json``).
   * - Host architectures
     - Packaged: macOS arm64 (releases), Linux x64 (RPM). diffr exists only
       for these two targets.
   * - macOS tooling
     - Xcode Command Line Tools. Signing and notarization need
       ``CODESIGN_IDENTITY`` and the ``APPLE_*`` or
       ``NOTARY_KEYCHAIN_PROFILE`` variables (desktop README).
   * - Offline caching
     - node-gyp caches headers in its dev dir (``~/.cache/node-gyp/<version>``),
       and ``npm_config_nodedir`` can point at pre-extracted headers
       (standard node-gyp behavior, UPSTREAM; not tested here). The
       repository documents no offline mode.
   * - Container-specific?
     - **Yes.** The organization egress policy denied ``electronjs.org``,
       ``open-vsx.org`` and ``marketplace.visualstudio.com``. The npm
       registry and GitHub release downloads worked: ``diffr-fetch``
       succeeded.

Classification
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Layer
     - Verdict
   * - Whiteboard problem
     - No. Whiteboard adds no native modules of its own.
   * - Code - OSS dependency
     - It is the *source* of the native build requirement (UPSTREAM).
   * - Electron dependency
     - It is the *source* of the headers and the ABI target.
   * - CI/container/network
     - **The actual failure: NETWORK FAILURE** (egress policy).
