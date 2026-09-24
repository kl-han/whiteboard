Code - OSS provenance
=====================

.. list-table::
   :widths: 30 70

   * - Upstream repository
     - ``https://github.com/microsoft/vscode.git`` (DOCUMENTED, ``UPSTREAM``)
   * - Upstream commit
     - ``8a7abeba6e03ea3af87bfbce9a1b7e48fed567b8``
   * - Upstream version
     - ``code-oss-dev`` **1.129.1** (``code-oss/package.json``, CONFIRMED)
   * - Serialization tag
     - ``code-oss-upstream-8a7abeba``. The tag is **not present** in this
       checkout: ``git tag`` is empty (UNVERIFIED).
   * - License
     - MIT (Microsoft). ``apps/review-desktop/LICENSE``;
       ``code-oss/ThirdPartyNotices.txt``; fork-added notices in
       ``code-oss/licenses/``.
   * - Electron
     - 42.10.0 (``code-oss/package.json`` and ``.npmrc`` ``target``),
       updated from 42.9.3 as a backport
   * - Node for the fork
     - 24.18.0 exactly (``code-oss/.nvmrc``)
   * - First appearance here
     - ``d1c6463c`` "Import Review Desktop" (2026-08-18), already
       diverged (HISTORY)

Why vendor instead of patching
------------------------------

README (DOCUMENTED): "coding agents have a hard time with patches", and much
of stock VS Code (Copilot) is not needed. The fork is kept **enumerable**:
every difference from upstream must be listed in ``UPSTREAM``.

What was removed
----------------

The removals below are all DOCUMENTED in ``UPSTREAM``.

* **At vendor time**: ``.git/``, ``.github/``, ``.vscode/``,
  ``build/azure-pipelines/``, ``extensions/copilot/``, the colorize test
  extensions and ``test/monaco/dist/``.
* **Pruned built-in extensions** (18), including ``emmet``,
  ``github-authentication``, ``microsoft-authentication``, ``ipynb``,
  ``notebook-renderers``, ``php-language-features``, ``terminal-suggest``
  and ``tunnel-forwarding``.
* **The Agents window**: all 605 files under ``src/vs/sessions/``.
* **Native dependencies Whiteboard never reaches**: Windows-only natives,
  ``kerberos``, ``@vscode/policy-watcher`` and more. Their typings are
  replaced by ``src/typings/removed-native-modules.d.ts``.
* **Services not registered at runtime**: the terminal pty host, web
  content extractor, the ``playwright`` channel and the agent network
  filter.

What was restored
-----------------

The extension webview API files (``mainThreadWebviews.ts`` and others) were
missing from the vendored tree. They were restored byte-for-byte in #517,
so they are not a divergence.

Security backports
------------------

``UPSTREAM`` lists each cherry-picked upstream commit (the Electron 42.10.0
update, hardening, and the September 2026 advisories). It also explains the
advisories that do not apply at this pin or are "Not remediated, by
decision": three Agent Network Filter CVEs in a service that is inert in
Whiteboard. Relevant PRs: #41 and #243 (HISTORY).
