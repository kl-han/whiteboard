CLI interaction
===============

``whiteboard <command>``, from the shell to the selected Desktop instance.

.. mermaid::

   flowchart TD
       Start["whiteboard args"] --> Built{"running dist/cli.js?"}
       Built -- no (tsx checkout) --> Floor
       Built -- yes --> Skip{"api / mcp / server / instances,<br/>--state-dir, DEV_REVIEW_SERVER_DIR,<br/>or NO_DELEGATE set?"}
       Skip -- yes --> Floor
       Skip -- no --> Sel["select discovery file:<br/>DEV_REVIEW_INSTANCE → default-instance →<br/>only live → stable → legacy server.json"]
       Sel --> Live{"serverPid alive and<br/>cliPath differs from ours?"}
       Live -- yes --> Deleg["spawnSync(cliRuntimePath with ELECTRON_RUN_AS_NODE=1,<br/>[cliPath, ...args])"]
       Live -- no --> Floor["Node ≥ 24 check<br/>(Electron always passes)"]
       Floor --> Runner["runReviewCli(): Commander program 'whiteboard'"]
       Runner --> Hook["preAction: telemetry command start"]
       Hook --> Handler["command handler"]
       Handler --> Conn["connectReviewInstance(): discovery → url + token"]
       Conn --> HTTP["HTTP to /reviews-api"]
       HTTP --> Out["stdout: text or NDJSON (--json)"]

.. list-table::
   :widths: 25 75

   * - Initiating actor
     - A user, an agent skill, a hook or CI
   * - Entrypoint
     - ``packages/review/src/cli.ts`` (delegation bootstrap) →
       ``cli-runner.ts``
   * - Contract
     - The discovery record (``ReviewDesktopDiscoverySchema``, version 3);
       NDJSON events with ``--json``
   * - Persistence
     - Reads ``review-desktop/instances/*.json`` and ``default-instance``
   * - Transitions
     - Node → (optional) Electron-as-Node → HTTP → server
   * - Failure points
     - An old system Node. A shadowing legacy ``review`` on ``PATH``. No
       live instance. The wrong instance selected. An invalid instance key
       (only ``[A-Za-z0-9_.-]`` is allowed).
