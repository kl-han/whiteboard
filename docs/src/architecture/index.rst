Architecture
============

These pages explain which components exist, where they come from, how they
are built, how they talk at runtime, and why the design looks the way it
does. Start with :doc:`system_overview` for the one-picture summary.

.. toctree::
   :maxdepth: 2
   :caption: System model

   system_overview
   component_registry
   language_boundaries
   repository_topology
   build_topology
   runtime_topology
   contracts
   external_dependencies

.. toctree::
   :maxdepth: 2
   :caption: Subsystems

   semantic_diff/index
   upstream/index
   feature_flows/index

.. toctree::
   :maxdepth: 2
   :caption: Modules and design

   important_modules
   feature_component_map
   workflow_core_logic
   component_interactions
   descriptive_language
   decisions_and_tradeoffs
   risk_register
