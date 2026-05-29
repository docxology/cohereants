"""
Case-study modules corresponding to Appendices A–G.

Each appendix exposes ``compute_*`` / ``render_comprehensive_figure`` from its package.
"""

from .active_inference import olfactory_active_inference_step
from .detection_limits import compute_detection_limits_analysis, render_comprehensive_figure as render_detection_limits_figure
from .environmental_channel import (
    atmospheric_transmission_detailed,
    channel_capacity_vs_env,
    compute_environmental_channel_analysis,
    render_comprehensive_figure as render_environmental_channel_figure,
)
from .neural_encoding import (
    compute_neural_encoding_analysis,
    information_rate_time_series,
    rate_coding_metrics,
    render_comprehensive_figure as render_neural_encoding_figure,
)
from .plasmonic_geometry import (
    compute_plasmonic_geometry_analysis,
    render_comprehensive_figure as render_plasmonic_geometry_figure,
    sweep_plasmonic_quality,
)
from .sensilla_array_directionality import (
    array_gain,
    compute_beam_pattern,
    compute_sensilla_array_analysis,
    design_log_periodic_array,
    render_comprehensive_figure as render_sensilla_array_figure,
)
from .spectral_unmixing import (
    compute_spectral_unmixing_analysis,
    lda_baseline,
    nmf_unmix,
    render_comprehensive_figure as render_spectral_unmixing_figure,
)

__all__ = [
    "compute_beam_pattern",
    "array_gain",
    "design_log_periodic_array",
    "atmospheric_transmission_detailed",
    "channel_capacity_vs_env",
    "compute_detection_limits_analysis",
    "render_detection_limits_figure",
    "compute_environmental_channel_analysis",
    "render_environmental_channel_figure",
    "information_rate_time_series",
    "rate_coding_metrics",
    "compute_neural_encoding_analysis",
    "render_neural_encoding_figure",
    "nmf_unmix",
    "lda_baseline",
    "compute_spectral_unmixing_analysis",
    "render_spectral_unmixing_figure",
    "sweep_plasmonic_quality",
    "compute_plasmonic_geometry_analysis",
    "render_plasmonic_geometry_figure",
    "compute_sensilla_array_analysis",
    "render_sensilla_array_figure",
    "olfactory_active_inference_step",
]
