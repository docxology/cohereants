"""
Case-study modules corresponding to Appendices A–G.

Modules:
- sensilla_array_directionality: Array beam patterns and gains
- environmental_channel: Detailed atmospheric channel models
- detection_limits: Minimum detectable power and operating points
- neural_encoding: Information rate and rate coding metrics
- spectral_unmixing: NMF unmixing and simple classification
- plasmonic_geometry: Plasmonic resonance and Q sweeps
- active_inference: Minimal active-inference step demo
"""

from .sensilla_array_directionality import (
    compute_beam_pattern,
    array_gain,
    design_log_periodic_array,
)

from .environmental_channel import (
    atmospheric_transmission_detailed,
    channel_capacity_vs_env,
)

from .detection_limits import (
    min_detectable_power,
    snr_curve,
    operating_point,
)

from .neural_encoding import (
    information_rate_time_series,
    rate_coding_metrics,
)

from .spectral_unmixing import (
    nmf_unmix,
    lda_baseline,
)

from .plasmonic_geometry import (
    sweep_plasmonic_quality,
)

from .active_inference import (
    olfactory_active_inference_step,
)

__all__ = [
    # A
    'compute_beam_pattern', 'array_gain', 'design_log_periodic_array',
    # B
    'atmospheric_transmission_detailed', 'channel_capacity_vs_env',
    # C
    'min_detectable_power', 'snr_curve', 'operating_point',
    # D
    'information_rate_time_series', 'rate_coding_metrics',
    # E
    'nmf_unmix', 'lda_baseline',
    # F
    'sweep_plasmonic_quality',
    # G
    'olfactory_active_inference_step',
]


