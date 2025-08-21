"""Appendix D: Neural encoding efficiency on time-series."""
from __future__ import annotations

from typing import Dict
import numpy as np


def information_rate_time_series(responses: np.ndarray, dt_s: float, noise_std: float) -> Dict[str, float]:
    """
    Estimate information metrics using a Gaussian channel approximation.
    Deterministic and vectorized.
    """
    x = np.asarray(responses, dtype=float)
    n = x.size
    if n == 0 or dt_s <= 0:
        return {'channel_capacity_bits': 0.0, 'information_rate_bits': 0.0, 'snr': 0.0}
    signal_power = float(np.var(x))
    noise_power = float(noise_std ** 2)
    snr = signal_power / (noise_power + 1e-30)
    capacity = 0.5 * np.log2(1.0 + snr)
    info_rate = capacity * n
    return {'channel_capacity_bits': float(capacity), 'information_rate_bits': float(info_rate), 'snr': float(snr)}


def rate_coding_metrics(responses: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
    """
    Compute simple separability metrics (means/stds) deterministically.
    """
    r = np.asarray(responses, dtype=float)
    y = np.asarray(labels)
    if r.size == 0 or y.size == 0 or r.size != y.size:
        return {'d_prime': 0.0, 'mean_diff': 0.0}
    classes = np.unique(y)
    if classes.size != 2:
        return {'d_prime': 0.0, 'mean_diff': 0.0}
    m0 = float(np.mean(r[y == classes[0]]))
    m1 = float(np.mean(r[y == classes[1]]))
    s0 = float(np.std(r[y == classes[0]]) + 1e-12)
    s1 = float(np.std(r[y == classes[1]]) + 1e-12)
    dprime = (m1 - m0) / np.sqrt(0.5 * (s0 ** 2 + s1 ** 2))
    return {'d_prime': float(dprime), 'mean_diff': float(m1 - m0)}


