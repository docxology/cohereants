"""Appendix C: Detection limits and operating points.

Comprehensive detection theory analysis for IR olfactory systems including
ROC analysis, sensitivity curves, operating regions, and performance optimization.
Models detection under various noise conditions and environmental constraints.
"""
from __future__ import annotations

from typing import Dict, Union, Tuple, Optional
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar


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


def roc_analysis(
    signal_power_w: float,
    noise_power_w: float,
    threshold_range: Optional[np.ndarray] = None,
    n_points: int = 1000
) -> Dict[str, np.ndarray]:
    """
    Receiver Operating Characteristic (ROC) analysis for signal detection.
    
    Args:
        signal_power_w: Signal power in Watts
        noise_power_w: Noise power in Watts  
        threshold_range: Detection threshold range (if None, auto-determined)
        n_points: Number of points for ROC curve
        
    Returns:
        Dict with ROC curve data, AUC, and optimal operating points
    """
    signal_std = np.sqrt(signal_power_w)
    noise_std = np.sqrt(noise_power_w)
    
    # Signal + noise distribution (H1: signal present)
    signal_plus_noise_mean = signal_std
    signal_plus_noise_std = np.sqrt(signal_power_w + noise_power_w)
    
    # Noise only distribution (H0: signal absent)
    noise_only_mean = 0.0
    noise_only_std = noise_std
    
    # Determine threshold range if not provided
    if threshold_range is None:
        # Cover range from -4σ to +4σ of the combined distributions
        min_thresh = min(noise_only_mean - 4*noise_only_std, 
                        signal_plus_noise_mean - 4*signal_plus_noise_std)
        max_thresh = max(noise_only_mean + 4*noise_only_std,
                        signal_plus_noise_mean + 4*signal_plus_noise_std)
        threshold_range = np.linspace(min_thresh, max_thresh, n_points)
    
    # Calculate probability of false alarm (PFA) and probability of detection (PD)
    pfa = []  # P(decide H1 | H0 true) = P(X > threshold | noise only)
    pd = []   # P(decide H1 | H1 true) = P(X > threshold | signal + noise)
    
    for threshold in threshold_range:
        # False alarm probability (Type I error)
        pfa_val = 1 - norm.cdf(threshold, noise_only_mean, noise_only_std)
        pfa.append(pfa_val)
        
        # Detection probability (1 - Type II error)
        pd_val = 1 - norm.cdf(threshold, signal_plus_noise_mean, signal_plus_noise_std)
        pd.append(pd_val)
    
    pfa = np.array(pfa)
    pd = np.array(pd)
    
    # Calculate Area Under Curve (AUC) using trapezoidal rule
    # Sort by PFA for proper integration
    sorted_indices = np.argsort(pfa)
    pfa_sorted = pfa[sorted_indices]
    pd_sorted = pd[sorted_indices]
    auc = np.trapz(pd_sorted, pfa_sorted)
    
    # Find optimal operating point (maximize Youden's J statistic)
    youden_j = pd - pfa
    optimal_idx = np.argmax(youden_j)
    optimal_threshold = threshold_range[optimal_idx]
    optimal_pfa = pfa[optimal_idx]
    optimal_pd = pd[optimal_idx]
    
    # Equal Error Rate (EER) - point where PFA = 1-PD (miss rate)
    miss_rate = 1 - pd
    eer_idx = np.argmin(np.abs(pfa - miss_rate))
    eer_threshold = threshold_range[eer_idx]
    eer_rate = (pfa[eer_idx] + miss_rate[eer_idx]) / 2
    
    return {
        'thresholds': threshold_range,
        'pfa': pfa,
        'pd': pd,
        'auc': auc,
        'optimal_threshold': optimal_threshold,
        'optimal_pfa': optimal_pfa,
        'optimal_pd': optimal_pd,
        'youden_j': youden_j,
        'eer_threshold': eer_threshold,
        'eer_rate': eer_rate,
        'signal_plus_noise_mean': signal_plus_noise_mean,
        'signal_plus_noise_std': signal_plus_noise_std,
        'noise_only_mean': noise_only_mean,
        'noise_only_std': noise_only_std
    }


def detection_performance_vs_snr(
    snr_db_range: np.ndarray,
    pfa_target: float = 1e-3,
    integration_time_s: float = 1.0
) -> Dict[str, np.ndarray]:
    """
    Analyze detection performance vs signal-to-noise ratio.
    
    Args:
        snr_db_range: SNR range in dB
        pfa_target: Target false alarm probability
        integration_time_s: Integration time in seconds
        
    Returns:
        Detection performance metrics vs SNR
    """
    snr_db = np.asarray(snr_db_range, dtype=float)
    snr_linear = 10**(snr_db / 10.0)
    
    # For each SNR, calculate detection probability
    pd_values = []
    threshold_values = []
    
    for snr_lin in snr_linear:
        # Assume unit noise power, signal power = SNR
        signal_power = snr_lin
        noise_power = 1.0
        
        # Calculate threshold for target PFA
        noise_std = np.sqrt(noise_power)
        threshold = noise_std * norm.ppf(1 - pfa_target)
        threshold_values.append(threshold)
        
        # Calculate PD at this threshold
        signal_plus_noise_mean = np.sqrt(signal_power)
        signal_plus_noise_std = np.sqrt(signal_power + noise_power)
        pd = 1 - norm.cdf(threshold, signal_plus_noise_mean, signal_plus_noise_std)
        pd_values.append(pd)
    
    pd_values = np.array(pd_values)
    threshold_values = np.array(threshold_values)
    
    # Calculate minimum detectable signal (MDS) for 90% detection probability
    pd_target = 0.9
    mds_snr_db = []
    for i, pd in enumerate(pd_values):
        if pd >= pd_target:
            mds_snr_db.append(snr_db[i])
            break
    mds_snr_db = mds_snr_db[0] if mds_snr_db else snr_db[-1]
    
    # Calculate processing gain due to integration
    processing_gain_db = 10 * np.log10(integration_time_s)
    effective_snr_db = snr_db + processing_gain_db
    
    return {
        'snr_db': snr_db,
        'snr_linear': snr_linear,
        'pd': pd_values,
        'thresholds': threshold_values,
        'mds_snr_db': mds_snr_db,
        'processing_gain_db': processing_gain_db,
        'effective_snr_db': effective_snr_db,
        'pfa_target': pfa_target
    }


def sensitivity_analysis(
    base_params: Dict[str, float],
    param_ranges: Dict[str, Tuple[float, float]],
    n_points: int = 50
) -> Dict[str, Dict[str, np.ndarray]]:
    """
    Sensitivity analysis of detection performance to parameter variations.
    
    Args:
        base_params: Base parameter values
        param_ranges: Parameter variation ranges
        n_points: Number of points per parameter
        
    Returns:
        Sensitivity analysis results
    """
    results = {}
    
    for param_name, (min_val, max_val) in param_ranges.items():
        param_values = np.linspace(min_val, max_val, n_points)
        sensitivities = []
        
        for param_val in param_values:
            # Create modified parameters
            modified_params = base_params.copy()
            modified_params[param_name] = param_val
            
            # Calculate detection metric (e.g., minimum detectable power)
            if 'temperature_k' in modified_params and 'bandwidth_hz' in modified_params:
                mdp = min_detectable_power(
                    modified_params['temperature_k'],
                    modified_params['bandwidth_hz'],
                    modified_params.get('snr_min_db', 3.0)
                )
                sensitivities.append(float(mdp))
        
        results[param_name] = {
            'parameter_values': param_values,
            'sensitivity_values': np.array(sensitivities),
            'relative_sensitivity': np.array(sensitivities) / sensitivities[len(sensitivities)//2]  # Normalized to midpoint
        }
    
    return results


def operating_regions_analysis(
    power_range_w: np.ndarray,
    temperature_range_k: np.ndarray,
    bandwidth_hz: float = 1e6,
    snr_targets_db: np.ndarray = np.array([0, 3, 6, 10])
) -> Dict[str, np.ndarray]:
    """
    Analyze operating regions in power-temperature space.
    
    Args:
        power_range_w: Signal power range in Watts
        temperature_range_k: Temperature range in Kelvin  
        bandwidth_hz: Signal bandwidth in Hz
        snr_targets_db: Target SNR levels in dB
        
    Returns:
        Operating region boundaries and feasibility maps
    """
    P, T = np.meshgrid(power_range_w, temperature_range_k)
    k_B = 1.380649e-23
    
    # Calculate SNR for each power-temperature combination
    noise_power = k_B * T * bandwidth_hz
    snr_linear = P / noise_power
    snr_db = 10 * np.log10(snr_linear + 1e-30)
    
    # Create feasibility maps for each target SNR
    feasibility_maps = {}
    for target_snr_db in snr_targets_db:
        feasibility_maps[f'snr_{target_snr_db}db'] = snr_db >= target_snr_db
    
    # Calculate minimum power requirements for each temperature
    min_power_requirements = {}
    for target_snr_db in snr_targets_db:
        snr_linear = 10**(target_snr_db / 10.0)
        min_powers = snr_linear * k_B * temperature_range_k * bandwidth_hz
        min_power_requirements[f'snr_{target_snr_db}db'] = min_powers
    
    # Find operating boundaries (contour lines)
    operating_boundaries = {}
    for target_snr_db in snr_targets_db:
        # Find boundary where SNR equals target
        boundary_indices = []
        for i in range(len(temperature_range_k)):
            snr_row = snr_db[i, :]
            crossing_indices = np.where(np.diff(np.sign(snr_row - target_snr_db)))[0]
            if len(crossing_indices) > 0:
                # Linear interpolation for more accurate boundary
                idx = crossing_indices[0]
                if idx < len(power_range_w) - 1:
                    x1, x2 = power_range_w[idx], power_range_w[idx + 1]
                    y1, y2 = snr_row[idx], snr_row[idx + 1]
                    x_boundary = x1 + (target_snr_db - y1) * (x2 - x1) / (y2 - y1)
                    boundary_indices.append((x_boundary, temperature_range_k[i]))
        
        operating_boundaries[f'snr_{target_snr_db}db'] = boundary_indices
    
    return {
        'power_grid_w': P,
        'temperature_grid_k': T,
        'snr_grid_db': snr_db,
        'feasibility_maps': feasibility_maps,
        'min_power_requirements': min_power_requirements,
        'operating_boundaries': operating_boundaries,
        'bandwidth_hz': bandwidth_hz
    }


def noise_floor_analysis(
    frequency_range_hz: np.ndarray,
    temperature_k: float = 300.0,
    include_shot_noise: bool = True,
    include_flicker_noise: bool = True,
    current_a: float = 1e-6
) -> Dict[str, np.ndarray]:
    """
    Analyze noise floor components vs frequency.
    
    Args:
        frequency_range_hz: Frequency range in Hz
        temperature_k: Temperature in Kelvin
        include_shot_noise: Include shot noise contribution
        include_flicker_noise: Include 1/f flicker noise
        current_a: Current in Amperes for shot noise calculation
        
    Returns:
        Noise floor analysis with different noise components
    """
    frequencies = np.asarray(frequency_range_hz, dtype=float)
    
    # Johnson-Nyquist thermal noise (frequency independent)
    k_B = 1.380649e-23
    thermal_noise_density = 4 * k_B * temperature_k  # V²/Hz
    thermal_noise_power = thermal_noise_density * np.ones_like(frequencies)
    
    # Shot noise (frequency independent)
    shot_noise_power = np.zeros_like(frequencies)
    if include_shot_noise:
        q = 1.602176634e-19  # Elementary charge
        shot_noise_density = 2 * q * current_a  # A²/Hz
        shot_noise_power = shot_noise_density * np.ones_like(frequencies)
    
    # Flicker (1/f) noise
    flicker_noise_power = np.zeros_like(frequencies)
    if include_flicker_noise:
        # Typical 1/f noise coefficient (device dependent)
        flicker_coeff = 1e-12  # Empirical coefficient
        flicker_noise_power = flicker_coeff / (frequencies + 1e-6)  # Avoid division by zero
    
    # Total noise
    total_noise_power = thermal_noise_power + shot_noise_power + flicker_noise_power
    
    # Convert to dB scale
    thermal_noise_db = 10 * np.log10(thermal_noise_power + 1e-30)
    shot_noise_db = 10 * np.log10(shot_noise_power + 1e-30)
    flicker_noise_db = 10 * np.log10(flicker_noise_power + 1e-30)
    total_noise_db = 10 * np.log10(total_noise_power)
    
    return {
        'frequencies_hz': frequencies,
        'thermal_noise_power': thermal_noise_power,
        'shot_noise_power': shot_noise_power,
        'flicker_noise_power': flicker_noise_power,
        'total_noise_power': total_noise_power,
        'thermal_noise_db': thermal_noise_db,
        'shot_noise_db': shot_noise_db,
        'flicker_noise_db': flicker_noise_db,
        'total_noise_db': total_noise_db,
        'temperature_k': temperature_k
    }


def detection_range_analysis(
    transmit_power_w: float,
    antenna_gain_db: float,
    frequency_hz: float,
    receiver_sensitivity_dbm: float,
    atmospheric_loss_db_per_km: float = 0.1
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Analyze detection range for IR olfactory communication.
    
    Args:
        transmit_power_w: Transmit power in Watts
        antenna_gain_db: Combined transmit/receive antenna gain in dB
        frequency_hz: Operating frequency in Hz  
        receiver_sensitivity_dbm: Receiver sensitivity in dBm
        atmospheric_loss_db_per_km: Atmospheric loss per km
        
    Returns:
        Range analysis including free space and atmospheric effects
    """
    # Convert power to dBm
    transmit_power_dbm = 10 * np.log10(transmit_power_w * 1000)
    
    # Speed of light
    c = 2.998e8  # m/s
    wavelength_m = c / frequency_hz
    
    # Free space path loss (Friis equation): FSPL = (4πR/λ)²
    # In dB: FSPL_dB = 20*log10(4π) + 20*log10(R) - 20*log10(λ)
    fspl_constant_db = 20 * np.log10(4 * np.pi) - 20 * np.log10(wavelength_m)
    
    # Link budget: Received Power = Transmit Power + Gains - Losses
    # At maximum range: Received Power = Receiver Sensitivity
    # receiver_sensitivity_dbm = transmit_power_dbm + antenna_gain_db - fspl_db - atmospheric_loss_db
    
    # Solve for maximum range without atmospheric loss (free space)
    available_path_loss_db = transmit_power_dbm + antenna_gain_db - receiver_sensitivity_dbm
    range_fspl_db = available_path_loss_db - fspl_constant_db
    max_range_free_space_m = 10**(range_fspl_db / 20)
    
    # Calculate range vs distance including atmospheric loss
    distances_m = np.logspace(0, 6, 1000)  # 1 m to 1000 km
    distances_km = distances_m / 1000
    
    # Path losses
    fspl_db = fspl_constant_db + 20 * np.log10(distances_m)
    atmospheric_loss_db = atmospheric_loss_db_per_km * distances_km
    total_loss_db = fspl_db + atmospheric_loss_db
    
    # Received power
    received_power_dbm = transmit_power_dbm + antenna_gain_db - total_loss_db
    
    # Find maximum range with atmospheric loss
    feasible_indices = received_power_dbm >= receiver_sensitivity_dbm
    if np.any(feasible_indices):
        max_range_atmospheric_m = distances_m[feasible_indices][-1]
    else:
        max_range_atmospheric_m = 0.0
    
    # Calculate range for different receiver sensitivities
    sensitivity_range_dbm = np.arange(-120, -40, 5)  # -120 to -40 dBm
    max_ranges_m = []
    
    for sens_dbm in sensitivity_range_dbm:
        available_loss = transmit_power_dbm + antenna_gain_db - sens_dbm
        # Find range where total loss equals available loss
        loss_differences = np.abs(total_loss_db - available_loss)
        min_idx = np.argmin(loss_differences)
        max_ranges_m.append(distances_m[min_idx])
    
    return {
        'max_range_free_space_m': max_range_free_space_m,
        'max_range_atmospheric_m': max_range_atmospheric_m,
        'distances_m': distances_m,
        'fspl_db': fspl_db,
        'atmospheric_loss_db': atmospheric_loss_db,
        'total_loss_db': total_loss_db,
        'received_power_dbm': received_power_dbm,
        'sensitivity_range_dbm': sensitivity_range_dbm,
        'max_ranges_vs_sensitivity_m': np.array(max_ranges_m),
        'wavelength_m': wavelength_m,
        'link_budget_components': {
            'transmit_power_dbm': transmit_power_dbm,
            'antenna_gain_db': antenna_gain_db,
            'receiver_sensitivity_dbm': receiver_sensitivity_dbm,
            'atmospheric_loss_db_per_km': atmospheric_loss_db_per_km
        }
    }


def optimize_detection_parameters(
    constraints: Dict[str, Tuple[float, float]],
    objectives: Dict[str, float],
    fixed_params: Dict[str, float]
) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Optimize detection system parameters for given constraints and objectives.
    
    Args:
        constraints: Parameter bounds as {param: (min, max)}
        objectives: Target values as {metric: target_value}  
        fixed_params: Fixed parameter values
        
    Returns:
        Optimized parameter values and achieved performance
    """
    def objective_function(params_array):
        """Objective function for optimization."""
        # Map array to parameter dictionary
        param_names = list(constraints.keys())
        params_dict = dict(zip(param_names, params_array))
        params_dict.update(fixed_params)
        
        # Calculate performance metrics
        try:
            if 'temperature_k' in params_dict and 'bandwidth_hz' in params_dict:
                mdp = min_detectable_power(
                    params_dict['temperature_k'],
                    params_dict['bandwidth_hz'],
                    params_dict.get('snr_min_db', 3.0)
                )
                
                # Multi-objective optimization (weighted sum)
                penalty = 0.0
                
                # Minimize minimum detectable power
                if 'mdp_target' in objectives:
                    penalty += abs(mdp - objectives['mdp_target']) / objectives['mdp_target']
                
                # Add other objectives as needed
                if 'power_efficiency' in objectives:
                    power_efficiency = 1.0 / (params_dict.get('current_a', 1e-6) + 1e-12)
                    penalty += abs(power_efficiency - objectives['power_efficiency']) / objectives['power_efficiency']
                
                return penalty
            
        except Exception:
            return 1e6  # Large penalty for invalid parameters
        
        return 1e6
    
    # Set up optimization bounds
    param_names = list(constraints.keys())
    bounds = [constraints[param] for param in param_names]
    
    # Initial guess (midpoint of constraints)
    initial_guess = [(min_val + max_val) / 2 for min_val, max_val in bounds]
    
    # Optimize using scipy
    from scipy.optimize import minimize
    
    result = minimize(
        objective_function,
        initial_guess,
        method='L-BFGS-B',
        bounds=bounds
    )
    
    # Extract optimized parameters
    optimized_params = dict(zip(param_names, result.x))
    optimized_params.update(fixed_params)
    
    # Calculate final performance
    final_performance = {}
    if 'temperature_k' in optimized_params and 'bandwidth_hz' in optimized_params:
        final_mdp = min_detectable_power(
            optimized_params['temperature_k'],
            optimized_params['bandwidth_hz'],
            optimized_params.get('snr_min_db', 3.0)
        )
        final_performance['mdp_optimized'] = float(final_mdp)
    
    return {
        'optimized_parameters': optimized_params,
        'final_performance': final_performance,
        'optimization_success': result.success,
        'optimization_message': result.message,
        'objective_value': result.fun
    }


def operating_point(capacity_bits_s: float, snr_db: float) -> Dict[str, float]:
    """Bundle operating point parameters deterministically. (Legacy function)"""
    return {
        'capacity_bits_s': float(capacity_bits_s),
        'snr_db': float(snr_db),
        'snr_linear': float(10 ** (snr_db / 10.0)),
    }


