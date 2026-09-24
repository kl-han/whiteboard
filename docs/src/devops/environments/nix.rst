Nix
===

**Status: not provided.**

Evidence checked
----------------

There is no ``flake.nix``, ``shell.nix``, ``default.nix``, ``.envrc`` or
``devbox.json`` in the repository. ``.gitignore`` mentions ``.devbox/`` and
Terraform state under a "DevBox local cloud state" heading. These are
leftover ignore entries for tooling that is not in this repository
(inferred).

When to use it
--------------

Only if your team already uses Nix. A dev shell would need ``nodejs_24``,
``pnpm`` 11, ``python3``, a C toolchain and the X11 and secret libraries
listed in :doc:`local`.

Pros and cons
-------------

* Pros: pinned toolchains.
* Cons: Electron and the curated-extension downloads expect an FHS layout.
  On NixOS you would need ``steam-run`` or an FHS environment (inferred;
  not tested).

Verification commands
---------------------

None. Once a shell exists, run the commands in :doc:`local`.

Failure modes
-------------

* pnpm 11 enforces ``engines``, so a Nix ``nodejs`` other than 24 fails
  immediately.
