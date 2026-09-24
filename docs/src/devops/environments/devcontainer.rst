Devcontainer
============

**Status: not provided for Whiteboard.**

Evidence checked
----------------

``apps/review-desktop/code-oss/.devcontainer/`` exists (``devcontainer.json``,
``Dockerfile``, ``post-create.sh``), but it is part of the vendored Code - OSS
fork. It is set up to develop **VS Code itself**, not the Whiteboard
monorepo: it does not install pnpm 11 or run ``pnpm install`` at the
monorepo root. No ``.devcontainer`` exists at the repository root.
``CONTRIBUTING.md`` notes that files under ``code-oss/`` apply to Microsoft's
project.

When to use it
--------------

Do not use the upstream devcontainer for Whiteboard work. If you want
Codespaces or a devcontainer, write a root ``.devcontainer/devcontainer.json``
based on the ``node:24`` image and the steps in :doc:`local`.

Pros and cons
-------------

* Pros: a shared, reproducible editor environment.
* Cons: the same GUI limits as :doc:`docker`. It would be a new artifact to
  maintain.

Verification commands
---------------------

None. There is nothing to verify until a root devcontainer exists.

Failure modes
-------------

Opening the repository in an editor that picks up the nested
``code-oss/.devcontainer`` gives a VS Code build environment, not a
Whiteboard one.
