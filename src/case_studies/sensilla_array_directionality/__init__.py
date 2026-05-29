"""Appendix case study: sensilla_array_directionality."""
from .compute import compute_sensilla_array_analysis
from .figures import render_comprehensive_figure
from .types import SensillaArrayDirectionalityAnalysis

# Re-export core helpers for backward compatibility
from .core import *  # noqa: F403
from .morphology import *  # noqa: F403

__all__ = [
    "compute_sensilla_array_analysis",
    "render_comprehensive_figure",
    "SensillaArrayDirectionalityAnalysis",
]
