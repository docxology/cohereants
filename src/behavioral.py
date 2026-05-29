"""
Behavioral response analysis functions.

Statistical computation lives in ``behavioral_stats``; plotting in ``viz.behavioral_plots``.
This module re-exports the public API for backward compatibility.
"""

from .behavioral_stats import (
    BehavioralAnalyzer,
    BehavioralData,
    StatisticalAnalyzer,
    analyze_behavioral_response,
    calculate_power_analysis,
    calculate_response_statistics,
)
from .viz.behavioral_plots import generate_behavioral_plots

__all__ = [
    "BehavioralData",
    "StatisticalAnalyzer",
    "BehavioralAnalyzer",
    "analyze_behavioral_response",
    "calculate_power_analysis",
    "calculate_response_statistics",
    "generate_behavioral_plots",
]
