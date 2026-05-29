"""Appendix case study: plasmonic_geometry."""
from .compute import compute_plasmonic_geometry_analysis
from .figures import render_comprehensive_figure
from .types import PlasmonicGeometryAnalysis

# Re-export core helpers for backward compatibility
from .core import *  # noqa: F403

__all__ = [
    "compute_plasmonic_geometry_analysis",
    "render_comprehensive_figure",
    "PlasmonicGeometryAnalysis",
]
