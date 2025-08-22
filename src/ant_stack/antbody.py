"""
Ant Stack - AntBody layer components.

Implements sensilla morphology utilities and atmospheric spectroscopy accessors using
existing, tested src utilities to preserve thin orchestrator constraints.
"""

from typing import Dict, Tuple, Optional
import numpy as np

from src.sensilla import analyze_sensilla_dimensions
from src.core import calculate_atmospheric_transmission


class AntBodySensilla:
    """
    Sensilla configuration using cohereAnts morphology analysis.

    Args:
        lengths: array of sensilla lengths (μm)
        diameters: array of sensilla diameters (μm)
    """

    def __init__(self, lengths: np.ndarray, diameters: np.ndarray):
        self.lengths = np.asarray(lengths, dtype=float)
        self.diameters = np.asarray(diameters, dtype=float)

        analysis = analyze_sensilla_dimensions(self.lengths.tolist(), self.diameters.tolist())
        self.optimal_wavelengths_quarter = analysis["optimal_wavelengths_quarter"]
        self.optimal_wavelengths_half = analysis["optimal_wavelengths_half"]
        self.aspect_ratios = analysis["aspect_ratios"]

    def get_statistics(self) -> Dict[str, float]:
        return {
            "mean_length": float(np.mean(self.lengths)) if self.lengths.size else 0.0,
            "mean_diameter": float(np.mean(self.diameters)) if self.diameters.size else 0.0,
            "mean_aspect_ratio": float(np.mean(self.aspect_ratios)) if self.aspect_ratios.size else 0.0,
        }

    def get_resonant_wavelengths(self) -> Dict[str, np.ndarray]:
        """
        Access quarter-/half-wavelength predictions derived from analysis.

        Returns:
            Dictionary with numpy arrays for 'quarter' and 'half' resonance wavelengths (μm).
        """
        return {
            'quarter': self.optimal_wavelengths_quarter.copy(),
            'half': self.optimal_wavelengths_half.copy(),
        }


class AntBodySpectroscopy:
    """
    Atmospheric transmission access aligned with core calculations.

    Args:
        spectral_resolution: wavelength resolution in μm
    """

    def __init__(self, spectral_resolution: float = 0.01):
        if spectral_resolution <= 0:
            raise ValueError("spectral_resolution must be positive")
        self.spectral_resolution = float(spectral_resolution)

    def get_transmission(self, wavelength: float, distance: Optional[float] = None) -> float:
        """
        Return modeled atmospheric transmission for a single wavelength (μm).
        """
        return float(calculate_atmospheric_transmission(float(wavelength), distance))


