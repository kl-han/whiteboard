Semantic diff failure modes
===========================

Observed by experiment
----------------------

We built a scratch Git repository with four changed files and ran the
pinned diffr 0.1.3 exactly as the server does (CONFIRMED):

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Case
     - Result
     - Meaning
   * - Supported language (``ok.ts``)
     - ``text`` diff, no fallback
     - Structural diff
   * - Unknown extension (``notes.xyzq``)
     - ``fallback: {code: "unsupported_language", message: "no tree-sitter grammar for this file"}``
     - Degrades to a line diff; not an error
   * - Syntax error (``broken.rs``)
     - ``fallback: {code: "parse_error", message: "2 Rust parse errors … exceeded diff.parse_error_limit (0)"}``
     - Degrades to a line diff; the limit is configurable
   * - Large file (``big.js``, 1.2 MiB)
     - ``fallback: {code: "too_large", message: "… exceeded diff.byte_limit (1000000)"}``
     - Degrades to a line diff

All four counted as ``succeeded`` in ``complete``, and the exit code was 0.

From code
---------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Failure
     - Behavior
   * - diffr missing
     - "Cannot find diffr at …", with instructions (``ensure:diffr`` or
       ``REVIEW_DIFFR_BINARY``)
   * - Unsupported platform
     - ``diffr-fetch``: "no diffr release for <platform>-<arch>". Only
       macOS arm64 and Linux x64 are supported.
   * - Download blocked
     - A warning, and Whiteboard continues without diffr, unless
       ``--required`` is set. A hash mismatch always fails.
   * - Stalled diffr
     - Aborted after 120 s without a new line
   * - Protocol mismatch
     - "Unsupported diffr stream protocol." (a version other than 4)
   * - Pinned checkout not preparable
     - ``ReviewInputError``: "Cannot prepare the pinned repository …"
   * - Summaries without an API key
     - The Settings UI refuses to enable them: "Add a Gemini API key before
       enabling summaries."
   * - Summary network failure
     - The ``annotations`` event carries ``error``. The diff itself still
       renders.
   * - macOS signing
     - #429 fixed diffr signing in the app bundle. Structural diffs were
       disabled by default (#429, #447), then enabled again (#471).
   * - Server stream error
     - Sent to the UI as ``{type:"error", message}``, and rethrown by
       ``StructuralDiffClient``.
