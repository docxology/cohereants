"""Appendix B: Environmental channel modeling.

Deterministic, simplified models for atmospheric transmission with
humidity/temperature/path effects and capacity maps.
"""
from __future__ import annotations

from typing import Dict, Tuple
import numpy as np


def atmospheric_transmission_detailed(
    wavelengths_um: np.ndarray,
    humidity: np.ndarray | float,
    temperature_k: np.ndarray | float,
    path_m: np.ndarray | float,
) -> np.ndarray:
    """
    Compute a simple parametric atmospheric transmission curve.

    Args:
        wavelengths_um: Wavelengths (μm), shape (W,)
        humidity: Relative humidity in [0,1]
        temperature_k: Absolute temperature (K)
        path_m: Path length (m)

    Returns:
        Transmission array in [0,1], shape (W,)
    """
    wl = np.asarray(wavelengths_um, dtype=float)
    if wl.ndim != 1 or np.any(wl <= 0):
        raise ValueError("wavelengths must be 1D positive array")
    humidity = np.clip(np.asarray(humidity, dtype=float), 0.0, 1.0)
    temperature_k = np.asarray(temperature_k, dtype=float)
    path_m = np.asarray(path_m, dtype=float)

    # Baseline windows as in core, modulated by humidity/path
    base = np.ones_like(wl) * 0.1
    base[(wl >= 2) & (wl <= 5)] = 0.8
    base[(wl >= 8) & (wl <= 14)] = 0.9
    base[(wl >= 17) & (wl <= 25)] = 0.7

    # Humidity and path penalties (higher humidity/longer path → lower transmission)
    penalty = np.exp(- (0.5 * humidity + 1e-4 * path_m))
    # Temperature effect: slightly improves in moderate temps; clamp
    temp_factor = 1.0 - 1e-3 * np.abs(300.0 - temperature_k)
    temp_factor = np.clip(temp_factor, 0.9, 1.05)

    # Broadcast factors with wavelength dimension at the end
    # result shape: broadcast(humidity, temperature_k, path_m) + (W,)
    factors = (penalty * temp_factor)[..., None]
    trans = np.clip(factors * base[None, :], 0.0, 1.0)
    # If all inputs were scalars and W==1, return shape (1,) for consistency
    return trans.squeeze() if trans.shape[-1] != 1 else trans[..., 0]


def channel_capacity_vs_env(
    material_refractive_index: float,
    signal_power_w: float,
    bandwidth_hz: float,
    humidity_grid: np.ndarray,
    temperature_grid_k: np.ndarray,
    path_m: float,
) -> Dict[str, np.ndarray]:
    """
    Map Shannon capacity across humidity×temperature grid.

    Uses a simple noise model and transmission attenuation on signal power.
    Deterministic and vectorized.
    """
    h = np.asarray(humidity_grid, dtype=float)
    t = np.asarray(temperature_grid_k, dtype=float)
    if h.ndim != 1 or t.ndim != 1:
        raise ValueError("humidity_grid and temperature_grid_k must be 1D")
    H, T = np.meshgrid(h, t, indexing='ij')

    # Representative wavelength for the band center to evaluate transmission
    wl_center = 10.0  # μm (LWIR)
    trans = atmospheric_transmission_detailed(np.array([wl_center]), H, T, path_m)
    # Broadcast to grid
    trans = trans.reshape(H.shape)

    # Effective signal power after attenuation
    p_sig = np.clip(signal_power_w * trans, 0.0, np.inf)

    # Thermal noise (Johnson–Nyquist): k_B T B, scaled by refractive index
    k_B = 1.380649e-23
    noise = k_B * T * bandwidth_hz * max(material_refractive_index, 1.0)
    snr = p_sig / (noise + 1e-30)
    capacity = bandwidth_hz * np.log2(1.0 + snr)

    return {'humidity': h, 'temperature_k': t, 'capacity_bits_per_s': capacity}


