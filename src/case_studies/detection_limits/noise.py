"""Appendix C: Detection limits and operating points.

Comprehensive detection theory analysis for IR olfactory systems including
ROC analysis, sensitivity curves, operating regions, and performance optimization.
Models detection under various noise conditions and environmental constraints.
"""

from __future__ import annotations

from typing import Dict, Union, Tuple, Optional
import numpy as np

# numpy>=2.0 renamed ``np.trapz`` to ``np.trapezoid``; bind whichever this numpy
# provides so the module works on both numpy 1.x and 2.x.
_trapezoid = getattr(np, "trapezoid", None) or getattr(np, "trapz")
from scipy.stats import norm

from .core import min_detectable_power

def noise_floor_analysis(
    frequency_range_hz: np.ndarray,
    temperature_k: float = 300.0,
    include_shot_noise: bool = True,
    include_flicker_noise: bool = True,
    current_a: float = 1e-6,
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
        "frequencies_hz": frequencies,
        "thermal_noise_power": thermal_noise_power,
        "shot_noise_power": shot_noise_power,
        "flicker_noise_power": flicker_noise_power,
        "total_noise_power": total_noise_power,
        "thermal_noise_db": thermal_noise_db,
        "shot_noise_db": shot_noise_db,
        "flicker_noise_db": flicker_noise_db,
        "total_noise_db": total_noise_db,
        "temperature_k": temperature_k,
    }


def detection_range_analysis(
    transmit_power_w: float,
    antenna_gain_db: float,
    frequency_hz: float,
    receiver_sensitivity_dbm: float,
    atmospheric_loss_db_per_km: float = 0.1,
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
    max_range_free_space_m = 10 ** (range_fspl_db / 20)

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
        "max_range_free_space_m": max_range_free_space_m,
        "max_range_atmospheric_m": max_range_atmospheric_m,
        "distances_m": distances_m,
        "fspl_db": fspl_db,
        "atmospheric_loss_db": atmospheric_loss_db,
        "total_loss_db": total_loss_db,
        "received_power_dbm": received_power_dbm,
        "sensitivity_range_dbm": sensitivity_range_dbm,
        "max_ranges_vs_sensitivity_m": np.array(max_ranges_m),
        "wavelength_m": wavelength_m,
        "link_budget_components": {
            "transmit_power_dbm": transmit_power_dbm,
            "antenna_gain_db": antenna_gain_db,
            "receiver_sensitivity_dbm": receiver_sensitivity_dbm,
            "atmospheric_loss_db_per_km": atmospheric_loss_db_per_km,
        },
    }


def optimize_detection_parameters(
    constraints: Dict[str, Tuple[float, float]], objectives: Dict[str, float], fixed_params: Dict[str, float]
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
            if "temperature_k" in params_dict and "bandwidth_hz" in params_dict:
                mdp = min_detectable_power(
                    params_dict["temperature_k"], params_dict["bandwidth_hz"], params_dict.get("snr_min_db", 3.0)
                )

                # Multi-objective optimization (weighted sum)
                penalty = 0.0

                # Minimize minimum detectable power
                if "mdp_target" in objectives:
                    penalty += abs(mdp - objectives["mdp_target"]) / objectives["mdp_target"]

                # Add other objectives as needed
                if "power_efficiency" in objectives:
                    power_efficiency = 1.0 / (params_dict.get("current_a", 1e-6) + 1e-12)
                    penalty += abs(power_efficiency - objectives["power_efficiency"]) / objectives["power_efficiency"]

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

    result = minimize(objective_function, initial_guess, method="L-BFGS-B", bounds=bounds)

    # Extract optimized parameters
    optimized_params = dict(zip(param_names, result.x))
    optimized_params.update(fixed_params)

    # Calculate final performance
    final_performance = {}
    if "temperature_k" in optimized_params and "bandwidth_hz" in optimized_params:
        final_mdp = min_detectable_power(
            optimized_params["temperature_k"], optimized_params["bandwidth_hz"], optimized_params.get("snr_min_db", 3.0)
        )
        final_performance["mdp_optimized"] = float(final_mdp)

    return {
        "optimized_parameters": optimized_params,
        "final_performance": final_performance,
        "optimization_success": result.success,
        "optimization_message": result.message,
        "objective_value": result.fun,
    }


def operating_point(capacity_bits_s: float, snr_db: float) -> Dict[str, float]:
    """Bundle operating point parameters deterministically. (Legacy function)"""
    return {
        "capacity_bits_s": float(capacity_bits_s),
        "snr_db": float(snr_db),
        "snr_linear": float(10 ** (snr_db / 10.0)),
    }
