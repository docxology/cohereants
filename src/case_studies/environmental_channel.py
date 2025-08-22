"""Appendix B: Environmental channel modeling.

Comprehensive atmospheric transmission modeling for infrared olfactory communication,
including detailed physical effects, channel capacity analysis, and environmental
optimization. Models molecular absorption, scattering, and thermal effects.
"""
from __future__ import annotations

from typing import Dict, Tuple, Union, List
import numpy as np
from scipy.interpolate import interp1d


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


def molecular_absorption_cross_section(
    wavelengths_um: np.ndarray,
    molecule: str = 'H2O',
    temperature_k: float = 298.0,
    pressure_pa: float = 101325.0
) -> np.ndarray:
    """
    Calculate molecular absorption cross-sections for atmospheric constituents.
    
    Args:
        wavelengths_um: Wavelengths in micrometers
        molecule: Molecule type ('H2O', 'CO2', 'O2', 'N2', 'CH4')
        temperature_k: Temperature in Kelvin
        pressure_pa: Pressure in Pascals
        
    Returns:
        Absorption cross-section in cm²/molecule
    """
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    
    # Simplified absorption line parameters (representative values)
    absorption_params = {
        'H2O': {
            'line_centers': [1.38, 1.87, 2.7, 6.3, 20.0],  # μm
            'line_strengths': [1e-20, 5e-21, 2e-20, 1e-19, 3e-20],  # cm²/molecule
            'line_widths': [0.1, 0.15, 0.2, 0.5, 1.0]  # μm
        },
        'CO2': {
            'line_centers': [2.0, 2.7, 4.3, 15.0],
            'line_strengths': [3e-21, 1e-21, 2e-20, 1e-20],
            'line_widths': [0.05, 0.1, 0.2, 0.8]
        },
        'CH4': {
            'line_centers': [3.3, 7.7],
            'line_strengths': [1e-20, 5e-21],
            'line_widths': [0.2, 0.3]
        }
    }
    
    if molecule not in absorption_params:
        return np.zeros_like(wavelengths)
    
    params = absorption_params[molecule]
    cross_section = np.zeros_like(wavelengths)
    
    # Temperature scaling factor (simplified)
    T_ref = 296.0  # Reference temperature
    temp_factor = (T_ref / temperature_k) ** 0.5
    
    # Pressure broadening (simplified)
    pressure_factor = pressure_pa / 101325.0
    
    for center, strength, width in zip(params['line_centers'], 
                                      params['line_strengths'], 
                                      params['line_widths']):
        # Lorentzian absorption line shape
        effective_width = width * pressure_factor
        line_shape = effective_width / (np.pi * ((wavelengths - center)**2 + effective_width**2))
        cross_section += strength * temp_factor * line_shape
    
    return cross_section


def rayleigh_scattering_coefficient(
    wavelengths_um: np.ndarray,
    pressure_pa: float = 101325.0,
    temperature_k: float = 298.0
) -> np.ndarray:
    """
    Calculate Rayleigh scattering coefficient for dry air.
    
    Args:
        wavelengths_um: Wavelengths in micrometers
        pressure_pa: Pressure in Pascals
        temperature_k: Temperature in Kelvin
        
    Returns:
        Scattering coefficient in m⁻¹
    """
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    
    # Standard conditions
    P_0 = 101325.0  # Pa
    T_0 = 288.15    # K
    
    # Refractive index of dry air (Ciddor formula, simplified)
    n_minus_1 = 2.875e-4 * (pressure_pa / P_0) * (T_0 / temperature_k)
    
    # Rayleigh scattering cross-section 
    # σ = (8π³/3) * (n²-1)² / (N λ⁴)
    # where N is number density
    
    # Number density of air molecules
    k_B = 1.380649e-23
    N = pressure_pa / (k_B * temperature_k)  # molecules/m³
    
    # Scattering coefficient
    lambda_m = wavelengths * 1e-6  # Convert μm to m
    scattering_coeff = (8 * np.pi**3 / 3) * (n_minus_1**2) / (N * lambda_m**4) * N
    
    return scattering_coeff * 1e6  # Convert m⁻¹ to μm⁻¹ for consistency


def atmospheric_transmission_comprehensive(
    wavelengths_um: np.ndarray,
    path_length_m: float,
    humidity_percent: float = 50.0,
    temperature_k: float = 298.0,
    pressure_pa: float = 101325.0,
    aerosol_visibility_km: float = 23.0
) -> Dict[str, np.ndarray]:
    """
    Comprehensive atmospheric transmission model with multiple physical effects.
    
    Args:
        wavelengths_um: Wavelengths in micrometers
        path_length_m: Propagation path length in meters
        humidity_percent: Relative humidity (0-100%)
        temperature_k: Temperature in Kelvin
        pressure_pa: Atmospheric pressure in Pascals
        aerosol_visibility_km: Meteorological visibility in kilometers
        
    Returns:
        Dict with transmission coefficients and individual loss components
    """
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    humidity_fraction = humidity_percent / 100.0
    
    # 1. Molecular absorption
    h2o_concentration = humidity_fraction * 2.3e22  # molecules/m³ (approximate)
    co2_concentration = 1.0e22  # molecules/m³ (approximate for 400 ppm)
    
    h2o_cross_section = molecular_absorption_cross_section(wavelengths, 'H2O', temperature_k, pressure_pa)
    co2_cross_section = molecular_absorption_cross_section(wavelengths, 'CO2', temperature_k, pressure_pa)
    
    # Absorption coefficients (Beer-Lambert law)
    alpha_h2o = h2o_cross_section * h2o_concentration * 1e-4  # Convert cm² to m²
    alpha_co2 = co2_cross_section * co2_concentration * 1e-4
    alpha_molecular = alpha_h2o + alpha_co2
    
    # 2. Rayleigh scattering
    alpha_rayleigh = rayleigh_scattering_coefficient(wavelengths, pressure_pa, temperature_k)
    
    # 3. Aerosol extinction (simplified Koschmieder relation)
    alpha_aerosol = 3.912 / (aerosol_visibility_km * 1000)  # m⁻¹, approximately wavelength independent
    
    # 4. Total attenuation coefficient
    alpha_total = alpha_molecular + alpha_rayleigh + alpha_aerosol
    
    # 5. Transmission (Beer-Lambert law)
    transmission = np.exp(-alpha_total * path_length_m)
    
    # 6. Individual transmission components
    transmission_molecular = np.exp(-alpha_molecular * path_length_m)
    transmission_rayleigh = np.exp(-alpha_rayleigh * path_length_m)
    transmission_aerosol = np.exp(-alpha_aerosol * path_length_m)
    
    return {
        'wavelengths_um': wavelengths,
        'transmission_total': transmission,
        'transmission_molecular': transmission_molecular,
        'transmission_rayleigh': transmission_rayleigh,
        'transmission_aerosol': transmission_aerosol,
        'alpha_molecular': alpha_molecular,
        'alpha_rayleigh': alpha_rayleigh,
        'alpha_aerosol': alpha_aerosol,
        'alpha_total': alpha_total
    }


def channel_capacity_analysis(
    wavelengths_um: np.ndarray,
    path_length_m: float,
    signal_power_dbm: float,
    noise_temperature_k: float = 290.0,
    bandwidth_hz: float = 1e9,
    environmental_conditions: Dict[str, float] = None
) -> Dict[str, Union[np.ndarray, float]]:
    """
    Analyze communication channel capacity under atmospheric conditions.
    
    Args:
        wavelengths_um: Operating wavelengths in micrometers
        path_length_m: Communication range in meters
        signal_power_dbm: Transmit power in dBm
        noise_temperature_k: System noise temperature in Kelvin
        bandwidth_hz: Signal bandwidth in Hz
        environmental_conditions: Dict with 'humidity', 'temperature', 'pressure', 'visibility'
        
    Returns:
        Channel capacity analysis results
    """
    if environmental_conditions is None:
        environmental_conditions = {
            'humidity': 50.0, 'temperature': 298.0, 
            'pressure': 101325.0, 'visibility': 23.0
        }
    
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    
    # Calculate atmospheric transmission - map parameter names
    env_params_mapped = {
        'humidity_percent': environmental_conditions.get('humidity', 50.0),
        'temperature_k': environmental_conditions.get('temperature', 298.0),
        'pressure_pa': environmental_conditions.get('pressure', 101325.0),
        'aerosol_visibility_km': environmental_conditions.get('visibility', 23.0)
    }
    transmission_result = atmospheric_transmission_comprehensive(
        wavelengths, path_length_m, **env_params_mapped
    )
    transmission = transmission_result['transmission_total']
    
    # Convert transmit power from dBm to Watts
    signal_power_w = 10**((signal_power_dbm - 30) / 10)
    
    # Received signal power after atmospheric attenuation
    received_power_w = signal_power_w * transmission
    
    # Thermal noise power
    k_B = 1.380649e-23
    noise_power_w = k_B * noise_temperature_k * bandwidth_hz
    
    # Signal-to-noise ratio
    snr_linear = received_power_w / noise_power_w
    snr_db = 10 * np.log10(snr_linear + 1e-30)
    
    # Channel capacity (Shannon limit)
    capacity_bps = bandwidth_hz * np.log2(1 + snr_linear)
    
    # Path loss in dB
    path_loss_db = -10 * np.log10(transmission + 1e-30)
    
    # Free space path loss for comparison
    free_space_loss_db = 20 * np.log10(4 * np.pi * path_length_m / (wavelengths * 1e-6))
    
    # Atmospheric excess loss
    atmospheric_excess_db = path_loss_db - free_space_loss_db
    
    return {
        'wavelengths_um': wavelengths,
        'transmission': transmission,
        'received_power_w': received_power_w,
        'snr_linear': snr_linear,
        'snr_db': snr_db,
        'capacity_bps': capacity_bps,
        'path_loss_db': path_loss_db,
        'free_space_loss_db': free_space_loss_db,
        'atmospheric_excess_db': atmospheric_excess_db,
        'noise_power_w': noise_power_w
    }


def optimize_wavelength_for_range(
    target_range_m: float,
    min_capacity_bps: float,
    wavelength_range_um: Tuple[float, float] = (2.0, 25.0),
    environmental_conditions: Dict[str, float] = None,
    signal_power_dbm: float = 0.0
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Find optimal wavelengths for target communication range and capacity.
    
    Args:
        target_range_m: Target communication range in meters
        min_capacity_bps: Minimum required channel capacity in bits/second
        wavelength_range_um: Wavelength search range in micrometers
        environmental_conditions: Environmental parameters
        signal_power_dbm: Available transmit power in dBm
        
    Returns:
        Optimization results with optimal wavelengths and performance metrics
    """
    if environmental_conditions is None:
        environmental_conditions = {
            'humidity': 50.0, 'temperature': 298.0,
            'pressure': 101325.0, 'visibility': 23.0
        }
    
    # Create wavelength grid for optimization
    wavelengths = np.linspace(wavelength_range_um[0], wavelength_range_um[1], 500)
    
    # Analyze channel capacity across wavelength range
    capacity_analysis = channel_capacity_analysis(
        wavelengths, target_range_m, signal_power_dbm, 
        environmental_conditions=environmental_conditions
    )
    
    # Find wavelengths meeting capacity requirement
    suitable_wavelengths = wavelengths[capacity_analysis['capacity_bps'] >= min_capacity_bps]
    
    if len(suitable_wavelengths) == 0:
        optimal_wavelength = wavelengths[np.argmax(capacity_analysis['capacity_bps'])]
        max_achievable_capacity = np.max(capacity_analysis['capacity_bps'])
        feasible = False
    else:
        # Choose wavelength with best transmission among suitable ones
        suitable_indices = capacity_analysis['capacity_bps'] >= min_capacity_bps
        suitable_transmissions = capacity_analysis['transmission'][suitable_indices]
        best_idx = np.argmax(suitable_transmissions)
        optimal_wavelength = suitable_wavelengths[best_idx]
        max_achievable_capacity = capacity_analysis['capacity_bps'][suitable_indices][best_idx]
        feasible = True
    
    # Calculate performance at optimal wavelength
    optimal_idx = np.argmin(np.abs(wavelengths - optimal_wavelength))
    optimal_performance = {
        'transmission': capacity_analysis['transmission'][optimal_idx],
        'snr_db': capacity_analysis['snr_db'][optimal_idx],
        'capacity_bps': capacity_analysis['capacity_bps'][optimal_idx],
        'path_loss_db': capacity_analysis['path_loss_db'][optimal_idx]
    }
    
    return {
        'optimal_wavelength_um': optimal_wavelength,
        'feasible': feasible,
        'max_achievable_capacity_bps': max_achievable_capacity,
        'suitable_wavelengths_um': suitable_wavelengths,
        'optimal_performance': optimal_performance,
        'full_analysis': capacity_analysis
    }


def environmental_sensitivity_analysis(
    wavelength_um: float,
    path_length_m: float,
    parameter_ranges: Dict[str, Tuple[float, float]],
    n_points: int = 20
) -> Dict[str, Dict[str, np.ndarray]]:
    """
    Analyze sensitivity of transmission to environmental parameters.
    
    Args:
        wavelength_um: Operating wavelength in micrometers
        path_length_m: Path length in meters
        parameter_ranges: Dict with ranges for 'humidity', 'temperature', 'pressure', 'visibility'
        n_points: Number of points per parameter
        
    Returns:
        Sensitivity analysis results for each parameter
    """
    base_conditions = {
        'humidity': 50.0, 'temperature': 298.0,
        'pressure': 101325.0, 'visibility': 23.0
    }
    
    results = {}
    
    for param_name, (min_val, max_val) in parameter_ranges.items():
        param_values = np.linspace(min_val, max_val, n_points)
        transmissions = []
        capacities = []
        snr_values = []
        
        for param_val in param_values:
            conditions = base_conditions.copy()
            conditions[param_name] = param_val
            
            # Calculate transmission - map parameter names
            env_params_mapped = {
                'humidity_percent': conditions.get('humidity', 50.0),
                'temperature_k': conditions.get('temperature', 298.0),
                'pressure_pa': conditions.get('pressure', 101325.0),
                'aerosol_visibility_km': conditions.get('visibility', 23.0)
            }
            trans_result = atmospheric_transmission_comprehensive(
                np.array([wavelength_um]), path_length_m, **env_params_mapped
            )
            transmission = trans_result['transmission_total'][0]
            
            # Calculate capacity
            cap_result = channel_capacity_analysis(
                np.array([wavelength_um]), path_length_m, 0.0,  # 0 dBm
                environmental_conditions=conditions
            )
            capacity = cap_result['capacity_bps'][0]
            snr = cap_result['snr_db'][0]
            
            transmissions.append(transmission)
            capacities.append(capacity)
            snr_values.append(snr)
        
        results[param_name] = {
            'parameter_values': param_values,
            'transmission': np.array(transmissions),
            'capacity_bps': np.array(capacities),
            'snr_db': np.array(snr_values)
        }
    
    return results


def channel_capacity_vs_env(
    material_refractive_index: float,
    signal_power_w: float,
    bandwidth_hz: float,
    humidity_grid: np.ndarray,
    temperature_grid_k: np.ndarray,
    path_m: float,
) -> Dict[str, np.ndarray]:
    """
    Map Shannon capacity across humidity×temperature grid (legacy function).
    
    Enhanced version using comprehensive atmospheric modeling.
    """
    h = np.asarray(humidity_grid, dtype=float)
    t = np.asarray(temperature_grid_k, dtype=float)
    if h.ndim != 1 or t.ndim != 1:
        raise ValueError("humidity_grid and temperature_grid_k must be 1D")
    
    H, T = np.meshgrid(h, t, indexing='ij')
    
    # Use comprehensive model for transmission
    wavelength_um = 10.0  # Representative LWIR wavelength
    capacity_grid = np.zeros_like(H)
    
    for i in range(len(h)):
        for j in range(len(t)):
            conditions = {
                'humidity': h[i], 'temperature': t[j],
                'pressure': 101325.0, 'visibility': 23.0
            }
            
            # Convert power to dBm
            signal_power_dbm = 10 * np.log10(signal_power_w * 1000) if signal_power_w > 0 else -30
            
            cap_result = channel_capacity_analysis(
                np.array([wavelength_um]), path_m, signal_power_dbm,
                bandwidth_hz=bandwidth_hz, environmental_conditions=conditions
            )
            capacity_grid[i, j] = cap_result['capacity_bps'][0]
    
    return {'humidity': h, 'temperature_k': t, 'capacity_bits_per_s': capacity_grid}


