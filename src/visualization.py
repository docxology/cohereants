"""
Backward-compatible shim for visualization APIs.

Canonical implementations live under ``src.viz`` (``advanced``, ``styling``).
"""

import importlib.util

from .viz.advanced import (
    AdvancedVisualizer,
    _plotly_available,
    create_accessible_figure,
    create_publication_figure,
)
from .viz.styling import (
    PlotStyler,
    create_subplots,
    flatten_axes,
    get_colorblind_palette,
    set_plot_style,
)

HAS_SEABORN = importlib.util.find_spec("seaborn") is not None

__all__ = [
    "HAS_SEABORN",
    "AdvancedVisualizer",
    "PlotStyler",
    "_plotly_available",
    "create_accessible_figure",
    "create_publication_figure",
    "create_subplots",
    "flatten_axes",
    "get_colorblind_palette",
    "set_plot_style",
]
