"""Appendix A: Sensilla array directionality and beam patterns.

Comprehensive electromagnetic modeling of insect sensilla as antenna arrays,
including multiple geometries, coupling effects, frequency-dependent behavior,
and directional pattern analysis. All implementations are vectorized,
deterministic, and based on established antenna theory.
"""
from __future__ import annotations

from typing import Dict, List, Tuple, Union
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


def design_circular_array(radius_um: float, count: int, phase_center: bool = True) -> Dict[str, np.ndarray]:
    """
    Design a circular antenna array representing sensilla on insect antennae.
    
    Args:
        radius_um: Array radius in micrometers
        count: Number of sensilla elements
        phase_center: If True, add central element at origin
        
    Returns:
        Dict with 'x_positions', 'y_positions' in μm, and 'angles' in radians
    """
    if radius_um <= 0 or count <= 0:
        raise ValueError("Invalid parameters: radius and count must be positive")
    
    # Angular positions for perimeter elements
    angles = np.linspace(0, 2*np.pi, count, endpoint=False)
    x_pos = radius_um * np.cos(angles)
    y_pos = radius_um * np.sin(angles)
    
    if phase_center:
        # Add central element
        x_pos = np.concatenate([[0.0], x_pos])
        y_pos = np.concatenate([[0.0], y_pos])
        angles = np.concatenate([[0.0], angles])
    
    return {'x_positions': x_pos, 'y_positions': y_pos, 'angles': angles}


def sensilla_element_pattern(
    theta_deg: np.ndarray, 
    length_um: float, 
    wavelength_um: float,
    element_type: str = 'dipole'
) -> np.ndarray:
    """
    Individual sensillum radiation pattern as function of observation angle.
    
    Args:
        theta_deg: Observation angles in degrees (0° = along antenna axis)
        length_um: Sensillum length in micrometers  
        wavelength_um: Operating wavelength in micrometers
        element_type: 'dipole', 'monopole', or 'patch'
        
    Returns:
        Normalized power pattern (linear scale)
    """
    theta = np.asarray(theta_deg, dtype=float)
    if np.any((theta < 0) | (theta > 180)):
        raise ValueError("Angles must be in range [0, 180] degrees")
    
    theta_rad = np.deg2rad(theta)
    k = 2*np.pi / wavelength_um
    beta = k * length_um
    
    if element_type == 'dipole':
        # Short dipole pattern with length correction
        pattern = (np.sin(theta_rad))**2 * np.sinc(beta * np.cos(theta_rad) / (2*np.pi))**2
    elif element_type == 'monopole':  
        # Half-space monopole pattern
        pattern = np.where(theta_rad <= np.pi/2, 
                          (np.sin(theta_rad))**2, 0.0)
    elif element_type == 'patch':
        # Approximate patch antenna pattern (more directional)
        pattern = (np.cos(theta_rad))**2 * np.where(theta_rad <= np.pi/2, 1.0, 0.0)
    else:
        raise ValueError(f"Unknown element type: {element_type}")
    
    # Normalize to peak value
    pattern_max = np.max(pattern)
    return pattern / pattern_max if pattern_max > 0 else pattern


def mutual_coupling_matrix(
    positions: Union[np.ndarray, List[List[float]]],
    wavelength_um: float,
    coupling_strength: float = 0.1
) -> np.ndarray:
    """
    Compute mutual coupling matrix between antenna elements.
    
    Args:
        positions: Element positions, shape (N, 2) or (N, 3) 
        wavelength_um: Operating wavelength in micrometers
        coupling_strength: Coupling coefficient (0 = no coupling, 1 = maximum)
        
    Returns:
        Coupling matrix Z of shape (N, N), complex valued
    """
    pos = np.asarray(positions, dtype=float)
    if pos.ndim == 1:
        # Convert 1D positions to 2D
        pos = np.column_stack([pos, np.zeros_like(pos)])
    elif pos.ndim != 2:
        raise ValueError("Positions must be 1D or 2D array")
    
    n_elements = pos.shape[0]
    k = 2*np.pi / wavelength_um
    
    # Distance matrix between all element pairs
    dx = pos[:, 0, None] - pos[:, 0, None].T  # (N, N)
    dy = pos[:, 1, None] - pos[:, 1, None].T if pos.shape[1] > 1 else np.zeros((n_elements, n_elements))
    distances = np.sqrt(dx**2 + dy**2)
    
    # Avoid division by zero on diagonal
    distances[np.diag_indices(n_elements)] = 1e-12
    
    # Coupling matrix using simplified mutual impedance model
    Z = np.eye(n_elements, dtype=complex)  # Self-impedance = 1
    
    # Off-diagonal mutual coupling terms
    coupling = coupling_strength * np.exp(-1j * k * distances) / (1 + k * distances)
    Z += coupling * (1 - np.eye(n_elements))
    
    return Z


def array_pattern_2d(
    wavelengths_um: np.ndarray,
    positions: Union[np.ndarray, List[List[float]]],
    weights: np.ndarray,
    theta_range_deg: Tuple[float, float] = (0, 180),
    phi_range_deg: Tuple[float, float] = (0, 360),
    resolution_deg: float = 2.0,
    include_coupling: bool = True
) -> Dict[str, Union[np.ndarray, float]]:
    """
    Compute 2D radiation pattern for sensilla array across frequency range.
    
    Args:
        wavelengths_um: Operating wavelengths in micrometers
        positions: Element positions (N, 2) or (N, 3) in μm
        weights: Complex weights for each element (N,) 
        theta_range_deg: Elevation angle range (degrees)
        phi_range_deg: Azimuth angle range (degrees)
        resolution_deg: Angular resolution in degrees
        include_coupling: Whether to include mutual coupling effects
        
    Returns:
        Dict containing pattern data and metadata
    """
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    pos = np.asarray(positions, dtype=float) 
    weights = np.asarray(weights, dtype=complex)
    
    if pos.ndim == 1:
        pos = np.column_stack([pos, np.zeros_like(pos)])
    
    n_elements = pos.shape[0]
    if weights.size != n_elements:
        raise ValueError("Weights array size must match number of elements")
    
    # Angular grids
    theta_deg = np.arange(theta_range_deg[0], theta_range_deg[1] + resolution_deg, resolution_deg)
    phi_deg = np.arange(phi_range_deg[0], phi_range_deg[1] + resolution_deg, resolution_deg) 
    THETA, PHI = np.meshgrid(theta_deg, phi_deg, indexing='ij')
    
    n_freq = len(wavelengths)
    n_theta = len(theta_deg)
    n_phi = len(phi_deg)
    
    # Output arrays
    patterns = np.zeros((n_freq, n_theta, n_phi), dtype=float)
    directivity = np.zeros(n_freq)
    gain_db = np.zeros(n_freq)
    
    for freq_idx, wavelength in enumerate(wavelengths):
        k = 2*np.pi / wavelength
        
        # Include mutual coupling if requested
        if include_coupling:
            Z = mutual_coupling_matrix(pos, wavelength)
            # Solve for actual currents: Z * I = V (with V = weights)
            try:
                currents = np.linalg.solve(Z, weights)
            except np.linalg.LinAlgError:
                currents = weights  # Fallback to no coupling
        else:
            currents = weights
        
        # Compute array factor
        pattern_2d = np.zeros((n_theta, n_phi))
        
        for t_idx, theta in enumerate(np.deg2rad(theta_deg)):
            for p_idx, phi in enumerate(np.deg2rad(phi_deg)):
                # Direction vector
                u_x = np.sin(theta) * np.cos(phi)
                u_y = np.sin(theta) * np.sin(phi)
                
                # Phase shifts for each element
                phases = k * (pos[:, 0] * u_x + pos[:, 1] * u_y)
                
                # Array factor with element patterns
                element_pattern = sensilla_element_pattern(np.rad2deg([theta]), 
                                                         wavelength/4, wavelength)[0]
                
                array_factor = np.sum(currents * np.exp(1j * phases))
                pattern_2d[t_idx, p_idx] = element_pattern * np.abs(array_factor)**2
        
        patterns[freq_idx] = pattern_2d
        
        # Calculate directivity (peak/average power)
        if np.max(pattern_2d) > 0:
            directivity[freq_idx] = np.max(pattern_2d) / np.mean(pattern_2d)
            gain_db[freq_idx] = 10 * np.log10(directivity[freq_idx])
        
    return {
        'wavelengths_um': wavelengths,
        'theta_deg': theta_deg,
        'phi_deg': phi_deg,
        'patterns': patterns,
        'directivity': directivity, 
        'gain_db': gain_db,
        'positions': pos,
        'currents_used': currents if include_coupling else weights
    }


def analyze_sensilla_morphology(
    sensilla_lengths_um: np.ndarray,
    sensilla_diameters_um: np.ndarray,
    target_wavelengths_um: np.ndarray
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
        quarter_match = np.exp(-0.5 * ((quarter_wave_resonances - target_wl) / (0.1 * target_wl))**2)
        half_match = np.exp(-0.5 * ((half_wave_resonances - target_wl) / (0.1 * target_wl))**2)
        matching_matrix[:, i] = np.maximum(quarter_match, half_match)
    
    # Find best wavelength match for each sensillum
    best_matches = np.argmax(matching_matrix, axis=1)
    match_quality = np.max(matching_matrix, axis=1)
    
    return {
        'sensilla_lengths_um': lengths,
        'sensilla_diameters_um': diameters,
        'target_wavelengths_um': wavelengths,
        'quarter_wave_resonances_um': quarter_wave_resonances,
        'half_wave_resonances_um': half_wave_resonances,
        'aspect_ratios': aspect_ratios,
        'q_factors': q_factors,
        'wavelength_matching_matrix': matching_matrix,
        'best_wavelength_matches': wavelengths[best_matches],
        'match_quality_scores': match_quality
    }


def frequency_response_analysis(
    array_geometry: Dict[str, np.ndarray],
    frequency_range_thz: Tuple[float, float],
    n_frequencies: int = 100,
    medium_permittivity: float = 2.5
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
    
    positions = array_geometry.get('positions', np.array([[0], [0]]).T)
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
                np.abs(weights)
            )['pattern'][0]
            gain_db[i] = 10 * np.log10(max(array_factor, 0.01))
        else:
            gain_db[i] = 0.0
    
    # Find resonances (peaks in gain, minima in reactive impedance)
    resonance_indices = []
    for i in range(1, len(gain_db) - 1):
        if (gain_db[i] > gain_db[i-1] and gain_db[i] > gain_db[i+1] and 
            abs(impedance_imag[i]) < abs(impedance_imag[i-1]) and 
            abs(impedance_imag[i]) < abs(impedance_imag[i+1])):
            resonance_indices.append(i)
    
    resonance_frequencies = frequencies_thz[resonance_indices] if resonance_indices else np.array([])
    resonance_wavelengths = wavelengths_um[resonance_indices] if resonance_indices else np.array([])
    
    return {
        'frequencies_thz': frequencies_thz,
        'wavelengths_um': wavelengths_um,
        'gain_db': gain_db,
        'impedance_real': impedance_real,
        'impedance_imag': impedance_imag,
        'resonance_frequencies_thz': resonance_frequencies,
        'resonance_wavelengths_um': resonance_wavelengths,
        'bandwidth_3db_thz': _calculate_bandwidth(frequencies_thz, gain_db),
        'q_factor_avg': _calculate_average_q_factor(frequencies_thz, gain_db, resonance_indices)
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


def _calculate_average_q_factor(frequencies: np.ndarray, gain_db: np.ndarray, 
                              resonance_indices: List[int]) -> float:
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


