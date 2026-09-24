Development environments
========================

The repository supports **local development** directly. It contains no
Docker, devcontainer, Nix or remote-VM configuration of its own. The only
``.devcontainer`` directory is inside the vendored Code - OSS tree and
belongs to Microsoft's VS Code project. Each page below records what we
checked.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Environment
     - Status
     - Evidence
   * - Local
     - Supported
     - ``CONTRIBUTING.md``, ``apps/review-desktop/README.md``, root ``package.json``
   * - Docker
     - Not provided
     - No ``Dockerfile`` or compose file outside ``apps/review-desktop/code-oss/``
   * - Devcontainer
     - Not provided (upstream-only)
     - ``apps/review-desktop/code-oss/.devcontainer/`` is VS Code's own
   * - Nix
     - Not provided
     - No ``flake.nix``, ``shell.nix`` or ``default.nix``
   * - Remote VM / CI runner
     - Used by CI; not documented for developers
     - ``.github/workflows/*.yml`` run on ``ubuntu-latest``,
       ``review_big_boy`` and ``macos-15-xlarge``

.. toctree::
   :maxdepth: 1

   local
   docker
   devcontainer
   nix
   remote_vm
