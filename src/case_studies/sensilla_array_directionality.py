"""Appendix A: Sensilla array directionality and beam patterns.

Provides vectorized utilities to compute simple beam patterns from
element positions and scalar gains, estimate array gain, and design
log-periodic arrays. Deterministic and seedless.
"""
from __future__ import annotations

from typing import Dict
import numpy as np


def compute_beam_pattern(
    wavelengths_um: np.ndarray,
    positions_um: np.ndarray,
    gains: np.ndarray,
) -> Dict[str, np.ndarray]:
    """
    Compute a simplified 1D beam pattern over wavelengths.

    Args:
        wavelengths_um: Wavelengths (μm), shape (W,)
        positions_um: Element positions along a line (μm), shape (N,)
        gains: Element scalar gains, shape (N,)

    Returns:
        Dict with fields:
            - 'wavelengths_um': input wavelengths
            - 'pattern': normalized beam pattern vs wavelength (W,)

    Raises:
        ValueError: On shape mismatch or non-positive wavelengths.
    """
    wavelengths_um = np.asarray(wavelengths_um, dtype=float)
    positions_um = np.asarray(positions_um, dtype=float)
    gains = np.asarray(gains, dtype=float)

    if wavelengths_um.ndim != 1 or positions_um.ndim != 1 or gains.ndim != 1:
        raise ValueError("Inputs must be 1D arrays")
    if positions_um.size != gains.size:
        raise ValueError("positions and gains must have same length")
    if np.any(wavelengths_um <= 0):
        raise ValueError("All wavelengths must be positive")

    # Phase k·x with k = 2π/λ and x in same units; convert μm to meters cancels out in ratio
    k = 2.0 * np.pi / wavelengths_um  # (1/μm)
    # Steering assumed broadside; sum fields across elements deterministically
    # Field(λ) = Σ gains_n * exp(i k x_n)
    phases = np.outer(k, positions_um)  # (W,N)
    field = (gains[None, :] * (np.cos(phases) + 1j * np.sin(phases))).sum(axis=1)
    power = np.abs(field) ** 2
    # Normalize to [0,1]
    power_min = power.min()
    power_ptp = power.max() - power_min
    pattern = (power - power_min) / (power_ptp if power_ptp > 0 else 1.0)

    return {'wavelengths_um': wavelengths_um, 'pattern': pattern}


def array_gain(pattern: np.ndarray) -> float:
    """
    Compute a scalar array gain proxy as peak-to-mean power ratio.

    Args:
        pattern: Normalized power pattern (W,) in [0,1]

    Returns:
        Peak-to-mean ratio (unitless).
    """
    pattern = np.asarray(pattern, dtype=float)
    if pattern.size == 0:
        return 0.0
    mean_val = float(np.mean(pattern)) if np.any(pattern) else 0.0
    peak_val = float(np.max(pattern))
    if mean_val == 0.0:
        return np.inf if peak_val > 0 else 0.0
    return peak_val / mean_val


def design_log_periodic_array(
    min_len_um: float, max_len_um: float, tau: float, count: int
) -> np.ndarray:
    """
    Design a 1D log-periodic array of element positions.

    Args:
        min_len_um: Minimum inter-element spacing (μm)
        max_len_um: Maximum aperture length (μm)
        tau: Log-periodic ratio (>1)
        count: Number of elements (>0)

    Returns:
        Positions (μm) as a 1D array of length `count` centered at 0.
    """
    if min_len_um <= 0 or max_len_um <= 0 or tau <= 1.0 or count <= 0:
        raise ValueError("Invalid parameters for log-periodic array design")

    # Generate geometric spacings and cumulative positions
    spacings = min_len_um * (tau ** np.arange(count - 1))  # (count-1,)
    positions = np.concatenate([[0.0], np.cumsum(spacings)])
    # Scale if aperture exceeds max_len_um
    if positions[-1] > max_len_um:
        positions *= (max_len_um / positions[-1])
    # Center
    positions -= np.mean(positions)
    return positions


