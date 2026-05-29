"""Appendix case study: detection_limits."""
from .compute import compute_detection_limits_analysis
from .figures import render_comprehensive_figure
from .types import DetectionLimitsAnalysis

# Re-export core helpers for backward compatibility
from .core import *  # noqa: F403
from .noise import *  # noqa: F403

__all__ = [
    "compute_detection_limits_analysis",
    "render_comprehensive_figure",
    "DetectionLimitsAnalysis",
]
