Instance discovery
==================

Several Desktops (stable, preview, dev builds) can share one
``DEV_REVIEW_HOME`` (#511). Discovery decides which one a CLI or MCP call
reaches.

Files
-----

.. list-table::
   :widths: 40 60

   * - ``$DEV_REVIEW_HOME/review-desktop/instances/<key>.json``
     - Discovery record written by each Desktop server (private, atomic)
   * - ``$DEV_REVIEW_HOME/review-desktop/default-instance``
     - The machine default, set by ``whiteboard instances use <key>``
   * - ``$DEV_REVIEW_HOME/review-desktop/server.json``
     - Legacy record from Desktops that predate instances (acts as
       ``stable``)
   * - ``<state-dir>/review-server``
     - Headless discovery (``server-discovery.ts``)

Record schema (``ReviewDesktopDiscoverySchema``, version 3)
-----------------------------------------------------------

``version`` (must be 3), ``instanceId``, ``url`` (loopback origin only),
``appPid``, ``serverPid``, ``token``, ``startedAt``; optional ``cliPath``,
``cliVersion``, ``cliRuntimePath``, ``key``, ``channel`` (``stable``,
``preview`` or ``dev``), ``checkout``, ``appPath`` and ``appVersion``.
Unknown keys are tolerated, so additive fields need no version bump.

Selection algorithm
-------------------

.. mermaid::

   flowchart TD
       A{"DEV_REVIEW_SERVER_DIR or --state-dir?"} -- yes --> H["headless server in that dir<br/>(no Desktop discovery)"]
       A -- no --> B{"DEV_REVIEW_INSTANCE set?"}
       B -- yes --> K["that key"]
       B -- no --> C{"default-instance file?"}
       C -- yes --> K
       C -- no --> D{"exactly one live record?"}
       D -- yes --> L["that record"]
       D -- no --> S["stable.json, else legacy server.json"]
       K --> V{"key matches ^[A-Za-z0-9_.-]+$ and record live (serverPid alive)?"}
       L --> OK["connect: url + token"]
       S --> V
       V -- yes --> OK
       V -- no --> ERR["unavailable: error names the problem<br/>(MCP: degraded mode)"]

"Live" means ``process.kill(serverPid, 0)`` succeeds, or fails with
``EPERM``. The CLI bootstrap (``cli.ts`` ``selectedDiscoveryFile``) keeps a
copy of this logic "in step with ``selectReviewInstance``" because it runs
before the Node version check. That is a duplication risk (see
:doc:`../architecture/risk_register`, R13).

Commands
--------

* ``whiteboard instances [--json]`` lists key, channel, state
  (running/stopped), version, url, checkout, selected and default.
* ``whiteboard instances use <key>`` and ``instances clear``.
* ``whiteboard_status`` (MCP) names the instance the session talks to.
