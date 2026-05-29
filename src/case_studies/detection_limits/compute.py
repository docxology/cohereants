"""Case study orchestration for detection_limits."""
from __future__ import annotations

from .core import *
from .noise import *
from .types import DetectionLimitsAnalysis

def compute_detection_limits_analysis() -> DetectionLimitsAnalysis:
    """Compute ROC, performance, operating-region, noise, and range artifacts."""
    roc_results: Dict[str, Dict[str, np.ndarray]] = {}
    snr_levels = [0, 3, 6, 10]
    for snr_db in snr_levels:
        signal_power = 10 ** (snr_db / 10.0)
        roc_results[f"snr_{snr_db}db"] = roc_analysis(signal_power, 1.0)

    snr_range_db = np.linspace(-5, 15, 50)
    detection_perf = detection_performance_vs_snr(snr_range_db, pfa_target=1e-3)
    power_range = np.logspace(-15, -8, 50)
    temp_range = np.linspace(250, 400, 50)
    operating_regions = operating_regions_analysis(power_range, temp_range)
    freq_range = np.logspace(3, 8, 100)
    noise_analysis = noise_floor_analysis(freq_range, temperature_k=300.0)
    range_analysis = detection_range_analysis(
        transmit_power_w=1e-6,
        antenna_gain_db=10.0,
        frequency_hz=3e13,
        receiver_sensitivity_dbm=-90.0,
    )
    return DetectionLimitsAnalysis(
        roc_results=roc_results,
        snr_levels=snr_levels,
        detection_perf=detection_perf,
        operating_regions=operating_regions,
        noise_analysis=noise_analysis,
        range_analysis=range_analysis,
    )

