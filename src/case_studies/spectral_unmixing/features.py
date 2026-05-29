"""Spectral feature extraction."""

from __future__ import annotations

from typing import Dict
import numpy as np
from scipy.linalg import svd
from scipy.signal import savgol_filter

from .core import _trapezoid


def spectral_feature_extraction(
    spectra: np.ndarray, wavelengths: np.ndarray, method: str = "peaks"
) -> Dict[str, np.ndarray]:
    """
    Extract discriminative features from spectral data.

    Args:
        spectra: Spectral data (n_samples, n_wavelengths)
        wavelengths: Wavelength vector
        method: Feature extraction method ('peaks', 'derivatives', 'pca', 'all')

    Returns:
        Dictionary with extracted features and metadata
    """
    X = np.asarray(spectra, dtype=float)
    wl = np.asarray(wavelengths, dtype=float)

    features = {}

    if method in ["peaks", "all"]:
        # Peak detection features
        peak_features = []
        for i in range(X.shape[0]):
            spectrum = X[i, :]

            # Smooth spectrum
            if len(spectrum) > 5:
                smoothed = savgol_filter(spectrum, min(len(spectrum) // 4 * 2 - 1, 5), 2)
            else:
                smoothed = spectrum.copy()

            # Find peaks (local maxima)
            peaks = []
            for j in range(1, len(smoothed) - 1):
                if smoothed[j] > smoothed[j - 1] and smoothed[j] > smoothed[j + 1]:
                    peaks.append(j)

            # Extract peak features
            if peaks:
                peak_wavelengths = wl[peaks]
                peak_intensities = smoothed[peaks]

                # Sort by intensity
                sorted_indices = np.argsort(peak_intensities)[::-1]
                top_peaks = sorted_indices[: min(5, len(peaks))]  # Top 5 peaks

                peak_wl_features = peak_wavelengths[top_peaks]
                peak_int_features = peak_intensities[top_peaks]

                # Pad to fixed length
                padded_wl = np.zeros(5)
                padded_int = np.zeros(5)
                n_peaks = len(top_peaks)
                padded_wl[:n_peaks] = peak_wl_features
                padded_int[:n_peaks] = peak_int_features

                feature_vector = np.concatenate([padded_wl, padded_int])
            else:
                feature_vector = np.zeros(10)  # 5 wavelengths + 5 intensities

            peak_features.append(feature_vector)

        features["peak_features"] = np.array(peak_features)

    if method in ["derivatives", "all"]:
        # Derivative features
        first_deriv = np.gradient(X, axis=1)
        second_deriv = np.gradient(first_deriv, axis=1)

        # Statistical moments of derivatives
        deriv_features = []
        for i in range(X.shape[0]):
            d1 = first_deriv[i, :]
            d2 = second_deriv[i, :]

            feature_vector = np.array(
                [np.mean(d1), np.std(d1), np.max(np.abs(d1)), np.mean(d2), np.std(d2), np.max(np.abs(d2))]
            )
            deriv_features.append(feature_vector)

        features["derivative_features"] = np.array(deriv_features)

    if method in ["pca", "all"]:
        # PCA features
        X_centered = X - np.mean(X, axis=0)
        U, s, Vt = svd(X_centered, full_matrices=False)

        # Keep components explaining 95% variance
        cumsum_var = np.cumsum(s**2)
        total_var = np.sum(s**2)
        n_components = np.searchsorted(cumsum_var / total_var, 0.95) + 1
        n_components = min(n_components, len(s))

        pca_features = U[:, :n_components] @ np.diag(s[:n_components])

        features["pca_features"] = pca_features
        features["pca_explained_variance"] = s[:n_components] ** 2 / total_var

    # Statistical features (always included)
    stat_features = []
    for i in range(X.shape[0]):
        spectrum = X[i, :]
        feature_vector = np.array(
            [
                np.mean(spectrum),
                np.std(spectrum),
                np.max(spectrum),
                np.min(spectrum),
                np.median(spectrum),
                np.percentile(spectrum, 75) - np.percentile(spectrum, 25),
                np.sum(spectrum),
                _trapezoid(spectrum, wl),
            ]
        )
        stat_features.append(feature_vector)

    features["statistical_features"] = np.array(stat_features)

    return features
