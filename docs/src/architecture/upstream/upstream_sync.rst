Upstream synchronization
========================

Process (DOCUMENTED in ``UPSTREAM`` and the desktop README)
-----------------------------------------------------------

1. **Serialize the fork**:
   ``git diff code-oss-upstream-8a7abeba..HEAD -- apps/review-desktop/code-oss``.
   This needs the tag, which is **absent** in this checkout. Without it,
   clone ``microsoft/vscode`` at ``8a7abeba`` into a temporary directory,
   apply the vendor-time exclusions, and compare recursively. The only
   differences left must be the paths listed in ``UPSTREAM``.
2. **Security fixes** are cherry-picked by upstream commit reference. Each
   is recorded in ``UPSTREAM`` under "Post-vendor security and reliability
   backports". Advisories that do not apply are explained there.
3. **Dependency CVEs** in vendored lockfiles are fixed within existing
   ranges (Dependabot PRs such as #35 to #82, and #19, #237).
4. **Keep divergence as direct commits** above the tag. The desktop README
   says: "Every upstream exclusion or intentional edit must be recorded in
   ``UPSTREAM``."

Evidence from Git (HISTORY)
---------------------------

* 179 commits touch ``code-oss/``: 127 touch ``src/vs/review``, and 86
  touch other paths.
* Most edits to upstream paths are Dependabot bumps inside
  ``code-oss/test/*`` and ``code-oss/build/*`` lockfiles, version stamps in
  ``product.json``, and targeted features: #493 restores upstream
  navigation modules, #498 opens source in a native Code - OSS window, #517
  restores the webview API.
* There is **no** merge of a newer upstream commit in this history. The pin
  has stayed at ``8a7abeba`` since the import. Only cherry-picks have been
  applied.

Risks
-----

See :doc:`../risk_register` (R1, "Vendored Code - OSS synchronization").
