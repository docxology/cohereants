"""Spectral unmixing analysis orchestration."""

from __future__ import annotations

import numpy as np

from .classifiers import advanced_classification_suite
from .core import generate_realistic_chc_spectra, nmf_unmix, vertex_component_analysis
from .features import spectral_feature_extraction
from .types import SpectralUnmixingAnalysis

def compute_spectral_unmixing_analysis(seed: int = 42) -> SpectralUnmixingAnalysis:
    """Compute CHC spectral unmixing, features, and classification artifacts."""
    spectral_data = generate_realistic_chc_spectra(
        n_samples=100, n_wavelengths=250, n_components=4, seed=seed
    )
    wavelengths = spectral_data["wavelengths_um"]
    mixed_spectra = spectral_data["mixed_spectra"]
    true_components = spectral_data["pure_components"]
    labels = spectral_data["dominant_labels"]

    nmf_results = nmf_unmix(mixed_spectra, n_components=4, seed=seed)
    vca_results = vertex_component_analysis(mixed_spectra, n_components=4)
    features_all = spectral_feature_extraction(mixed_spectra, wavelengths, method="all")
    classification_results = advanced_classification_suite(
        features_all["statistical_features"], labels, test_size=0.3, seed=seed
    )

    nmf_reconstruction = nmf_results["W"] @ nmf_results["H"]
    vca_reconstruction = vca_results["reconstruction"]
    nmf_mse = float(np.mean((mixed_spectra - nmf_reconstruction) ** 2))
    vca_mse = float(np.mean((mixed_spectra - vca_reconstruction) ** 2))

    return SpectralUnmixingAnalysis(
        spectral_data=spectral_data,
        wavelengths=wavelengths,
        mixed_spectra=mixed_spectra,
        true_components=true_components,
        labels=labels,
        nmf_results=nmf_results,
        vca_results=vca_results,
        features_all=features_all,
        classification_results=classification_results,
        nmf_reconstruction=nmf_reconstruction,
        vca_reconstruction=vca_reconstruction,
        nmf_mse=nmf_mse,
        vca_mse=vca_mse,
    )
