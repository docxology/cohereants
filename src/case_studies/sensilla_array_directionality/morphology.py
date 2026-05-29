"""Appendix A: Sensilla array directionality and beam patterns.

Comprehensive electromagnetic modeling of insect sensilla as antenna arrays,
including multiple geometries, coupling effects, frequency-dependent behavior,
and directional pattern analysis. All implementations are vectorized,
deterministic, and based on established antenna theory.
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Union
import numpy as np

from .core import compute_beam_pattern, mutual_coupling_matrix

def analyze_sensilla_morphology(
    sensilla_lengths_um: np.ndarray, sensilla_diameters_um: np.ndarray, target_wavelengths_um: np.ndarray
) -> Dict[str, np.ndarray]:
    """
    Analyze sensilla dimensions for resonant wavelength matching.

    Args:
        sensilla_lengths_um: Measured sensilla lengths in micrometers
        sensilla_diameters_um: Measured sensilla diameters in micrometers
        target_wavelengths_um: Target IR wavelengths for analysis

    Returns:
        Analysis results including resonance matches and Q factors
    """
    lengths = np.asarray(sensilla_lengths_um, dtype=float)
    diameters = np.asarray(sensilla_diameters_um, dtype=float)
    wavelengths = np.asarray(target_wavelengths_um, dtype=float)

    n_sensilla = len(lengths)
    n_wavelengths = len(wavelengths)

    # Resonant wavelength analysis
    # For quarter-wave resonance: L = λ/4 ⟹ λ = 4L
    quarter_wave_resonances = 4 * lengths
    half_wave_resonances = 2 * lengths

    # Quality factor estimation based on length-to-diameter ratio
    aspect_ratios = lengths / (diameters + 1e-12)
    q_factors = np.clip(aspect_ratios * 10, 1.0, 1000.0)  # Empirical scaling

    # Wavelength matching analysis
    matching_matrix = np.zeros((n_sensilla, n_wavelengths))
    for i, target_wl in enumerate(wavelengths):
        # Match quality based on proximity to resonances
        quarter_match = np.exp(-0.5 * ((quarter_wave_resonances - target_wl) / (0.1 * target_wl)) ** 2)
        half_match = np.exp(-0.5 * ((half_wave_resonances - target_wl) / (0.1 * target_wl)) ** 2)
        matching_matrix[:, i] = np.maximum(quarter_match, half_match)

    # Find best wavelength match for each sensillum
    best_matches = np.argmax(matching_matrix, axis=1)
    match_quality = np.max(matching_matrix, axis=1)

    return {
        "sensilla_lengths_um": lengths,
        "sensilla_diameters_um": diameters,
        "target_wavelengths_um": wavelengths,
        "quarter_wave_resonances_um": quarter_wave_resonances,
        "half_wave_resonances_um": half_wave_resonances,
        "aspect_ratios": aspect_ratios,
        "q_factors": q_factors,
        "wavelength_matching_matrix": matching_matrix,
        "best_wavelength_matches": wavelengths[best_matches],
        "match_quality_scores": match_quality,
    }


def frequency_response_analysis(
    array_geometry: Dict[str, np.ndarray],
    frequency_range_thz: Tuple[float, float],
    n_frequencies: int = 100,
    medium_permittivity: float = 2.5,
) -> Dict[str, np.ndarray]:
    """
    Analyze frequency response characteristics of sensilla array.

    Args:
        array_geometry: Dict with element positions and properties
        frequency_range_thz: Frequency range in THz
        n_frequencies: Number of frequency points
        medium_permittivity: Relative permittivity of surrounding medium

    Returns:
        Frequency response analysis including bandwidth and resonances
    """
    freq_min, freq_max = frequency_range_thz
    frequencies_thz = np.linspace(freq_min, freq_max, n_frequencies)

    # Convert to wavelengths (c = 3e14 μm/s in vacuum)
    c_um_per_s = 2.998e14
    c_medium = c_um_per_s / np.sqrt(medium_permittivity)
    wavelengths_um = c_medium / (frequencies_thz * 1e12)

    positions = array_geometry.get("positions", np.array([[0], [0]]).T)
    n_elements = positions.shape[0]

    # Uniform weighting
    weights = np.ones(n_elements, dtype=complex)

    # Compute gain vs frequency
    gain_db = np.zeros(n_frequencies)
    impedance_real = np.zeros(n_frequencies)
    impedance_imag = np.zeros(n_frequencies)

    for i, wavelength in enumerate(wavelengths_um):
        # Mutual coupling analysis
        Z = mutual_coupling_matrix(positions, wavelength, coupling_strength=0.15)

        # Input impedance (diagonal terms after coupling)
        Z_in = np.mean(np.diag(Z))
        impedance_real[i] = Z_in.real
        impedance_imag[i] = Z_in.imag

        # Gain calculation using simple directivity estimate
        if n_elements > 1:
            array_factor = compute_beam_pattern(
                np.array([wavelength]),
                positions[:, 0] if positions.shape[1] > 0 else positions.flatten(),
                np.abs(weights),
            )["pattern"][0]
            gain_db[i] = 10 * np.log10(max(array_factor, 0.01))
        else:
            gain_db[i] = 0.0

    # Find resonances (peaks in gain, minima in reactive impedance)
    resonance_indices = []
    for i in range(1, len(gain_db) - 1):
        if (
            gain_db[i] > gain_db[i - 1]
            and gain_db[i] > gain_db[i + 1]
            and abs(impedance_imag[i]) < abs(impedance_imag[i - 1])
            and abs(impedance_imag[i]) < abs(impedance_imag[i + 1])
        ):
            resonance_indices.append(i)

    resonance_frequencies = frequencies_thz[resonance_indices] if resonance_indices else np.array([])
    resonance_wavelengths = wavelengths_um[resonance_indices] if resonance_indices else np.array([])

    return {
        "frequencies_thz": frequencies_thz,
        "wavelengths_um": wavelengths_um,
        "gain_db": gain_db,
        "impedance_real": impedance_real,
        "impedance_imag": impedance_imag,
        "resonance_frequencies_thz": resonance_frequencies,
        "resonance_wavelengths_um": resonance_wavelengths,
        "bandwidth_3db_thz": _calculate_bandwidth(frequencies_thz, gain_db),
        "q_factor_avg": _calculate_average_q_factor(frequencies_thz, gain_db, resonance_indices),
    }


def _calculate_bandwidth(frequencies: np.ndarray, gain_db: np.ndarray, threshold_db: float = 3.0) -> float:
    """Calculate 3dB bandwidth from gain curve."""
    max_gain = np.max(gain_db)
    threshold = max_gain - threshold_db

    above_threshold = gain_db >= threshold
    if not np.any(above_threshold):
        return 0.0

    indices = np.where(above_threshold)[0]
    if len(indices) < 2:
        return 0.0

    return frequencies[indices[-1]] - frequencies[indices[0]]


def _calculate_average_q_factor(frequencies: np.ndarray, gain_db: np.ndarray, resonance_indices: List[int]) -> float:
    """Calculate average Q factor from resonance peaks."""
    if not resonance_indices:
        return 0.0

    q_factors = []
    for idx in resonance_indices:
        if idx > 0 and idx < len(frequencies) - 1:
            # Simple Q estimation: f0 / Δf_3dB around resonance
            f0 = frequencies[idx]
            peak_gain = gain_db[idx]

            # Find 3dB points around resonance
            left_3db = idx
            right_3db = idx

            for i in range(idx - 1, -1, -1):
                if gain_db[i] <= peak_gain - 3.0:
                    left_3db = i
                    break

            for i in range(idx + 1, len(gain_db)):
                if gain_db[i] <= peak_gain - 3.0:
                    right_3db = i
                    break

            if right_3db > left_3db:
                delta_f = frequencies[right_3db] - frequencies[left_3db]
                q_factors.append(f0 / delta_f if delta_f > 0 else 0)

    return np.mean(q_factors) if q_factors else 0.0
