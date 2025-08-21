"""Appendix C: Detection limits and operating points."""
from __future__ import annotations

from typing import Dict, Union
import numpy as np


def min_detectable_power(
    temperature_k: float,
    bandwidth_hz: Union[float, np.ndarray],
    snr_min_db: float,
) -> Union[float, np.ndarray]:
    """
    Minimum detectable signal power using thermal noise floor and SNR threshold.
    Supports scalar or array `bandwidth_hz` and returns matching shape.
    """
    k_B = 1.380649e-23
    snr_lin = 10 ** (float(snr_min_db) / 10.0)
    bw = np.asarray(bandwidth_hz, dtype=float)
    pmin = snr_lin * k_B * float(temperature_k) * bw
    return float(pmin) if pmin.ndim == 0 else pmin


def snr_curve(signal_power_w: np.ndarray, noise_temp_k: float, bandwidth_hz: float) -> np.ndarray:
    """SNR vs. signal power, with Johnson–Nyquist noise model."""
    signal_power_w = np.asarray(signal_power_w, dtype=float)
    k_B = 1.380649e-23
    noise = k_B * float(noise_temp_k) * float(bandwidth_hz)
    return signal_power_w / (noise + 1e-30)


def operating_point(capacity_bits_s: float, snr_db: float) -> Dict[str, float]:
    """Bundle operating point parameters deterministically."""
    return {
        'capacity_bits_s': float(capacity_bits_s),
        'snr_db': float(snr_db),
        'snr_linear': float(10 ** (snr_db / 10.0)),
    }


