"""
Ant Stack - AntBrain layer components.

Implements a simple vibrationally tuned glomeruli circuit and a high-level
olfactory processing pipeline stub with clear I/O contracts.
"""

from typing import Optional
import numpy as np


class VibrationalGlomeruliCircuit:
    """
    Bank of resonant channels tuned across 2–25 μm.

    Args:
        num_channels: number of channels spanning the wavelength range
        q_factor: channel quality factor scaling response sharpness
    """

    def __init__(self, num_channels: int = 50, q_factor: float = 100.0):
        if num_channels <= 0:
            raise ValueError("num_channels must be positive")
        if q_factor <= 0:
            raise ValueError("q_factor must be positive")
        self.num_channels = int(num_channels)
        self.q_factor = float(q_factor)
        self.frequency_tuning = np.linspace(2.0, 25.0, self.num_channels)

    def _gaussian_coupling(self, wavelengths: np.ndarray, center: float, width: float) -> np.ndarray:
        return np.exp(-0.5 * ((wavelengths - center) / width) ** 2)

    def process_spectral_input(self, wavelengths: np.ndarray, intensities: np.ndarray) -> np.ndarray:
        """
        Compute channel responses to a spectrum (wavelengths μm, intensities arbitrary units).
        Returns an array of shape (num_channels,).
        """
        wavelengths = np.asarray(wavelengths, dtype=float)
        intensities = np.asarray(intensities, dtype=float)
        if wavelengths.shape != intensities.shape:
            raise ValueError("wavelengths and intensities must have the same shape")
        if wavelengths.ndim != 1:
            raise ValueError("Inputs must be 1D arrays")

        responses = np.zeros(self.num_channels, dtype=float)
        # Width heuristic inversely related to Q and center frequency scale
        for i, center in enumerate(self.frequency_tuning):
            width = max(0.2, center / self.q_factor)
            coupling = self._gaussian_coupling(wavelengths, center, width)
            responses[i] = float(np.trapz(coupling * intensities, wavelengths))
        return responses

    def get_channel_centers(self) -> np.ndarray:
        """
        Return the center wavelengths (μm) for each resonant channel.
        """
        return self.frequency_tuning.copy()

    def get_effective_bandwidths(self) -> np.ndarray:
        """
        Return approximate bandwidths per channel from Q heuristic.
        """
        return np.maximum(0.2, self.frequency_tuning / self.q_factor)


class AntBrainOlfaction:
    """
    High-level olfactory pipeline stub with AL→MB→CX placeholders.

    Args:
        neuron_count: approximate neuron budget for documentation
        num_channels: number of vibrational channels in AL
    """

    def __init__(self, neuron_count: int = 100000, num_channels: int = 50):
        if neuron_count <= 0:
            raise ValueError("neuron_count must be positive")
        self.neuron_count = int(neuron_count)
        self.al = VibrationalGlomeruliCircuit(num_channels=num_channels)
        # Placeholders for MB and CX layers
        self.mb: Optional[object] = object()
        self.cx: Optional[object] = object()

    def summarize_channels(self) -> dict:
        """
        Provide a summary of AL channel centers and bandwidths for diagnostics.
        """
        centers = self.al.get_channel_centers()
        widths = self.al.get_effective_bandwidths()
        return {
            'num_channels': int(self.al.num_channels),
            'centers_um_min': float(centers.min()),
            'centers_um_max': float(centers.max()),
            'median_bandwidth_um': float(np.median(widths))
        }


