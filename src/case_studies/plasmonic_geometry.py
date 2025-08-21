"""Appendix F: Plasmonic nano-geometry sweep."""
from __future__ import annotations

from typing import Dict
import numpy as np


def sweep_plasmonic_quality(
    radii_m: np.ndarray,
    metal_epsilon_imag: float,
    medium_epsilon_real: float,
) -> Dict[str, np.ndarray]:
    """
    Sweep Q factor with a simple inverse-loss proxy across radii.
    """
    r = np.asarray(radii_m, dtype=float)
    if r.ndim != 1 or np.any(r <= 0):
        raise ValueError("radii_m must be positive 1D array")
    eps_i = abs(float(metal_epsilon_imag)) + 1e-12
    eps_m = max(float(medium_epsilon_real), 1e-12)
    # Proxy Q grows with radius to a saturation, inversely with loss
    q = (1.0 - np.exp(-r / (r.max() + 1e-30))) * (2.0 * eps_m / eps_i)
    return {'radii_m': r, 'q_factor_proxy': q}


