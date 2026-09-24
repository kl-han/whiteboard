Plugin system
=============

Bundled plugins (CONFIRMED from ``diffr config show --json``)
-------------------------------------------------------------

The default ``plugins.order``:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Plugin
     - Default
     - Effect
   * - ``bundled.context``
     - on, ``lines: 3``
     - Unchanged context lines (also the default for ``-U``)
   * - ``bundled.hide-files``
     - on; tags ``generated``, ``vendored``, ``test``; ``deleted: true``
     - Collapses whole files by tag, e.g. "Test file · hidden by default"
   * - ``bundled.deleted-bodies``
     - on, ``min_lines: 12``
     - Folds large deleted bodies
   * - ``bundled.summarize``
     - **off**; provider ``gemini``, model ``gemini-3.8-flash``,
       ``min_lines: 20``, ``retries: 3``, ``request_timeout_ms: 60000``
     - LLM pseudocode summaries of long function bodies, emitted as
       ``annotations``
   * - ``bundled.test-bodies``
     - on, ``min_lines: 3``
     - Folds test bodies
   * - ``bundled.removed-runs``
     - on, ``min_lines: 5``
     - Folds long runs of removed lines
   * - ``bundled.group``
     - on
     - Groups related changes (INFERRED from the name)

``plugins.external`` is empty by default. That is the likely place where
user WASM plugins are registered (INFERRED). How an external plugin is
declared, its WIT interface and its capabilities are **UNVERIFIED**,
because the diffr source and docs are not in this repository.

Where plugin rules execute
--------------------------

Inside the diffr process. Bundled plugins are part of the binary. External
plugins would run under the embedded wasmtime, and WASI-HTTP suggests they
may be allowed network access (INFERRED). Whiteboard never runs plugin code
itself. It only:

* reads and writes config through ``diffr config`` (``diffr-config.ts``);
* exposes the summary settings in its Settings UI (``/diffr-config``,
  ``/diffr-config/summarizer`` and ``/diffr-config/summarizer/test`` in
  ``desktop-server.ts``);
* renders the ``visibility`` and ``annotations`` the plugins produce.

The summarizer test route diffs a built-in Rust sample
(``SUMMARY_SAMPLE``) with only ``bundled.summarize`` enabled, in a temporary
config. It redacts the API key from any label it returns.
