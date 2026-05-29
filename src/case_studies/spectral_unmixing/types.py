"""Typed analysis contract for spectral unmixing."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np

@dataclass(frozen=True)
class SpectralUnmixingAnalysis:
    spectral_data: dict[str, Any]
    wavelengths: np.ndarray
    mixed_spectra: np.ndarray
    true_components: np.ndarray
    labels: np.ndarray
    nmf_results: dict[str, np.ndarray]
    vca_results: dict[str, np.ndarray]
    features_all: dict[str, Any]
    classification_results: dict[str, Any]
    nmf_reconstruction: np.ndarray
    vca_reconstruction: np.ndarray
    nmf_mse: float
    vca_mse: float

    def as_dict(self) -> dict[str, object]:
        return {
            "spectral_data": self.spectral_data,
            "wavelengths": self.wavelengths,
            "mixed_spectra": self.mixed_spectra,
            "true_components": self.true_components,
            "labels": self.labels,
            "nmf_results": self.nmf_results,
            "vca_results": self.vca_results,
            "features_all": self.features_all,
            "classification_results": self.classification_results,
            "nmf_reconstruction": self.nmf_reconstruction,
            "vca_reconstruction": self.vca_reconstruction,
            "nmf_mse": self.nmf_mse,
            "vca_mse": self.vca_mse,
        }
