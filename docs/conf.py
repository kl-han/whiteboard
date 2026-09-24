"""Sphinx configuration for the Whiteboard developer documentation.

Build from the repository root:

    python3 -m pip install -r docs/requirements.txt
    sphinx-build -b html docs docs/_build/html

Optional extensions degrade gracefully: without sphinx-rtd-theme the build uses
the built-in alabaster theme, and without sphinxcontrib-mermaid every
``.. mermaid::`` block renders as its Mermaid source in a literal block.
"""

from __future__ import annotations

import importlib.util

from docutils import nodes
from docutils.parsers.rst import Directive

project = "Whiteboard"
author = "dev.fast and Whiteboard contributors"
copyright = "2026, dev.fast and Whiteboard contributors"

root_doc = "index"
source_suffix = {".rst": "restructuredtext"}

# docs/ also holds the product's Markdown pages (privacy.md, telemetry.md) and
# README images. They are linked from these pages, not built by Sphinx.
exclude_patterns = ["_build", "assets", "*.md", "requirements.txt"]

extensions: list[str] = []


def _available(module: str) -> bool:
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


HAS_MERMAID = _available("sphinxcontrib.mermaid")
HAS_RTD_THEME = _available("sphinx_rtd_theme")

if HAS_MERMAID:
    extensions.append("sphinxcontrib.mermaid")

# myst-parser is loaded so contributors can add Markdown pages later. It is not
# required for the reStructuredText pages that ship today.
if _available("myst_parser"):
    extensions.append("myst_parser")
    myst_enable_extensions = ["colon_fence"]

html_theme = "sphinx_rtd_theme" if HAS_RTD_THEME else "alabaster"
html_title = "Whiteboard developer documentation"
html_theme_options = (
    {"navigation_depth": 4, "collapse_navigation": False}
    if HAS_RTD_THEME
    else {}
)

# Mermaid renders in the browser from a CDN copy of mermaid.js.
mermaid_init_config = {"startOnLoad": True, "securityLevel": "strict"}


class _MermaidSourceFallback(Directive):
    """Stand-in for ``.. mermaid::`` when sphinxcontrib-mermaid is missing."""

    has_content = True
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {"caption": str, "align": str, "zoom": bool}

    def run(self):
        note = nodes.note()
        note += nodes.paragraph(
            text=(
                "Mermaid diagram (source shown because sphinxcontrib-mermaid "
                "is not installed; run "
                "`python3 -m pip install -r docs/requirements.txt`)."
            )
        )
        source = "\n".join(self.content)
        return [note, nodes.literal_block(source, source)]


def setup(app):
    if not HAS_MERMAID:
        app.add_directive("mermaid", _MermaidSourceFallback)
