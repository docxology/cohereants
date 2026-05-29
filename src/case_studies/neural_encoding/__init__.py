"""Appendix case study: neural_encoding."""
from .compute import compute_neural_encoding_analysis
from .figures import render_comprehensive_figure
from .types import NeuralEncodingAnalysis

# Re-export core helpers for backward compatibility
from .core import *  # noqa: F403
from .population import *  # noqa: F403

__all__ = [
    "compute_neural_encoding_analysis",
    "render_comprehensive_figure",
    "NeuralEncodingAnalysis",
]
