Documentation map
=================

Read the sections in order the first time. Later, jump to the page you need.

1. **Introduction** explains what Whiteboard is, how the repository is laid
   out, and how the project reached its current shape.
2. **DevOps** covers setup, the checks we ran, and each development
   environment.
3. **Entrypoints** follows a command or app launch from the first process to
   the embedded server.
4. **Architecture** explains the core modules, data flow and design choices.
5. **Toolkit** covers the tools that shape everyday work.
6. **Agents** explains how coding agents connect to Whiteboard, including
   the MCP protocol and instance discovery.
7. **Advanced** covers extension points and troubleshooting.

Evidence labels
---------------

Architecture pages label claims with one of these tags wherever a claim
could be ambiguous:

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Label
     - Meaning
   * - **CONFIRMED**
     - Seen directly in current code, or observed by running it during
       verification
   * - **HISTORY**
     - Supported by Git commits (hash or PR number given)
   * - **DOCUMENTED**
     - Stated in project documentation (README, CONTRIBUTING, UPSTREAM,
       package READMEs)
   * - **UPSTREAM**
     - Inherited from an external project, such as Code - OSS, difftastic
       or Electron
   * - **INFERRED**
     - A conclusion drawn from structure, imports, names or binary contents
   * - **UNVERIFIED**
     - The evidence is incomplete. The open question is recorded in
       :doc:`advanced/open_questions`.

Earlier pages use a shorter form, "Confirmed" or "Inferred", with the same
meaning.

.. toctree::
   :maxdepth: 2

   intro/index
   devops/index
   entrypoints/index
   architecture/index
   toolkit/index
   agents/index
   advanced/index
