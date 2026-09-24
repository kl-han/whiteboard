Fork boundary
=============

Where Whiteboard ends and Code - OSS begins
-------------------------------------------

.. mermaid::

   flowchart TB
       subgraph Upstream["Upstream Code - OSS at 8a7abeba"]
         Preserved["Preserved: most of src/vs/**, extensions/*,<br/>build system, Electron shell"]
         Removed["Removed: copilot, src/vs/sessions (605 files),<br/>18 built-in extensions, Windows natives"]
         Modified["Modified (enumerated in UPSTREAM):<br/>main.ts, app.ts, workbench.ts, menubar.ts,<br/>product.json, build/*, editor parts, webview pre/index.html"]
       end
       subgraph Owned["Whiteboard-owned inside the fork"]
         Review["src/vs/review/** (149 files,<br/>dev.fast copyright header)"]
         Generated["Generated, gitignored:<br/>src/vs/review/common/reviewProtocol.ts"]
         Curated["Materialized, gitignored:<br/>curated extensions under extensions/"]
       end
       Modified -->|imports / registers| Review
       Review -->|uses platform APIs| Preserved
       Generated --> Review

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Area
     - Class
     - Rule
   * - ``src/vs/review/**``
     - Whiteboard-owned
     - Edit freely. Tests run in the fast tier (``node --import tsx --test``).
   * - ``src/vs/review/common/reviewProtocol.ts``
     - Generated
     - Never edit it. Change ``packages/review-protocol/src``, then run
       ``protocol:sync``.
   * - Files listed under "Intentional fork divergence" in ``UPSTREAM``
     - Modified upstream
     - Edit only with a matching ``UPSTREAM`` entry. Keep hunks small.
   * - Everything else in ``code-oss/``
     - Preserved upstream
     - Do not edit casually. Prefer a contribution under ``src/vs/review``.
       If you must change it, add an ``UPSTREAM`` entry.
   * - ``code-oss/package-lock.json``, ``build/**/package-lock.json``
     - Upstream lockfiles with security bumps
     - Use npm in ``code-oss/``, never pnpm (desktop README).

How Whiteboard code is wired in (CONFIRMED)
-------------------------------------------

* ``src/main.ts`` imports VS Code-family settings and keybindings, and
  records a crash breadcrumb before bootstrap. It is held to the
  pre-bootstrap import rules and tested by
  ``main-bootstrap-imports.test.mjs``.
* ``src/vs/code/electron-main/app.ts`` owns the embedded server lifecycle
  and registers the Review connection channel. It swaps the menubar and
  update dialog services.
* ``src/vs/code/electron-browser/workbench/workbench.ts`` loads the native
  code navigator entry for workspace windows, and the Review entry for empty
  windows.
* ``build/next/index.ts`` adds the Review desktop entry points and CSS
  bundle, and inlines Review's browser dependencies (zod,
  eventsource-parser).
* ``product.json`` sets the Whiteboard identity, ``reviewVersion``, the
  update feed ``update.dev.fast``, no extension gallery, and telemetry
  opt-outs.

Guard tests (CONFIRMED to exist and pass)
-----------------------------------------

``apps/review-desktop/scripts`` contains ``vendor-integrity.test.mjs``,
``vscode-security-backports.test.mjs``, ``product-hardening.test.mjs``,
``main-bootstrap-imports.test.mjs``, ``editor-actions-contract.test.mjs`` and
``titlebar-navigation-contract.test.mjs``. They are part of the 105 desktop
script tests we ran.
