"""Appendix case study: environmental_channel."""
from .compute import compute_environmental_channel_analysis
from .figures import render_comprehensive_figure
from .types import EnvironmentalChannelAnalysis

# Re-export core helpers for backward compatibility
from .core import *  # noqa: F403

__all__ = [
    "compute_environmental_channel_analysis",
    "render_comprehensive_figure",
    "EnvironmentalChannelAnalysis",
]
