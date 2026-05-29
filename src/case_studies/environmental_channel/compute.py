"""Case study orchestration for environmental_channel."""
from __future__ import annotations

from .core import *
from .types import EnvironmentalChannelAnalysis

def compute_environmental_channel_analysis() -> EnvironmentalChannelAnalysis:
    """Compute transmission and capacity artifacts for clear/humid conditions."""
    wavelengths_um = np.linspace(2.0, 25.0, 200)
    conditions = {
        "clear": {
            "humidity_percent": 30.0,
            "temperature_k": 298.0,
            "pressure_pa": 101325.0,
            "aerosol_visibility_km": 23.0,
        },
        "humid": {
            "humidity_percent": 80.0,
            "temperature_k": 305.0,
            "pressure_pa": 101325.0,
            "aerosol_visibility_km": 15.0,
        },
    }
    transmission_results: Dict[str, Dict[str, np.ndarray]] = {}
    for condition_name, params in conditions.items():
        transmission_results[condition_name] = atmospheric_transmission_comprehensive(
            wavelengths_um, 100.0, **params
        )
    capacity_results: Dict[str, Dict[str, np.ndarray]] = {}
    for condition_name, params in conditions.items():
        env_params = {
            "humidity": params["humidity_percent"],
            "temperature": params["temperature_k"],
            "pressure": params["pressure_pa"],
            "visibility": params["aerosol_visibility_km"],
        }
        capacity_results[condition_name] = channel_capacity_analysis(
            wavelengths_um, 100.0, 0.0, environmental_conditions=env_params
        )
    return EnvironmentalChannelAnalysis(
        wavelengths_um=wavelengths_um,
        transmission_results=transmission_results,
        capacity_results=capacity_results,
    )

