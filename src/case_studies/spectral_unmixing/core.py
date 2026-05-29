"""Spectral unmixing core algorithms."""

from __future__ import annotations

from typing import Dict, Tuple, List, Union, Optional
import numpy as np

_trapezoid = getattr(np, "trapezoid", None) or getattr(np, "trapz")
from scipy.linalg import svd
from scipy.signal import savgol_filter

def nmf_unmix(spectra: np.ndarray, n_components: int, seed: int = 42) -> Dict[str, np.ndarray]:
    """
    Deterministic, simple NMF via multiplicative updates.
    """
    X = np.clip(np.asarray(spectra, dtype=float), 0.0, np.inf)
    if X.ndim != 2 or n_components <= 0:
        raise ValueError("spectra must be 2D and n_components > 0")
    rng = np.random.default_rng(seed)
    m, n = X.shape
    W = rng.random((m, n_components))
    H = rng.random((n_components, n))
    for _ in range(200):
        WH = W @ H + 1e-12
        H *= (W.T @ (X / WH)) / (W.T @ np.ones_like(X) + 1e-12)
        WH = W @ H + 1e-12
        W *= ((X / WH) @ H.T) / (np.ones_like(X) @ H.T + 1e-12)
    return {"W": W, "H": H}


def generate_realistic_chc_spectra(
    n_samples: int = 100,
    n_wavelengths: int = 500,
    wavelength_range_um: Tuple[float, float] = (2.5, 25.0),
    n_components: int = 5,
    noise_level: float = 0.05,
    seed: int = 42,
) -> Dict[str, np.ndarray]:
    """
    Generate realistic CHC spectral data with known ground truth components.

    Args:
        n_samples: Number of spectral samples to generate
        n_wavelengths: Number of wavelength points
        wavelength_range_um: Wavelength range in micrometers
        n_components: Number of pure component spectra
        noise_level: Additive noise standard deviation
        seed: Random seed for reproducibility

    Returns:
        Dict with synthetic spectra, true components, mixing coefficients, and metadata
    """
    rng = np.random.default_rng(seed)
    wavelengths = np.linspace(wavelength_range_um[0], wavelength_range_um[1], n_wavelengths)

    # Create realistic CHC spectral signatures based on known IR bands
    component_centers = rng.uniform(3.0, 20.0, n_components)  # μm
    component_widths = rng.uniform(0.5, 2.0, n_components)
    component_strengths = rng.uniform(0.3, 1.0, n_components)

    # Generate pure component spectra with realistic line shapes
    pure_components = np.zeros((n_components, n_wavelengths))
    for i in range(n_components):
        # Primary absorption band
        primary_band = component_strengths[i] * np.exp(
            -0.5 * ((wavelengths - component_centers[i]) / component_widths[i]) ** 2
        )

        # Add overtone and combination bands at harmonics
        if component_centers[i] > 6.0:  # Add overtone for fundamental modes
            overtone = (
                0.3
                * component_strengths[i]
                * np.exp(-0.5 * ((wavelengths - component_centers[i] / 2) / (component_widths[i] / 2)) ** 2)
            )
            primary_band += overtone

        # Add CH stretch regions around 3-4 μm
        if component_centers[i] > 8.0:
            ch_stretch = 0.2 * component_strengths[i] * np.exp(-0.5 * ((wavelengths - 3.4) / 0.3) ** 2)
            primary_band += ch_stretch

        pure_components[i, :] = primary_band

    # Generate mixing coefficients (concentrations)
    # Use Dirichlet distribution to ensure realistic mixing
    mixing_coeffs = rng.dirichlet(np.ones(n_components), n_samples)

    # Create mixed spectra
    mixed_spectra = mixing_coeffs @ pure_components

    # Add realistic noise
    noise = rng.normal(0, noise_level, mixed_spectra.shape)
    noisy_spectra = np.clip(mixed_spectra + noise, 0, None)

    # Create component labels for classification
    dominant_component = np.argmax(mixing_coeffs, axis=1)

    return {
        "wavelengths_um": wavelengths,
        "mixed_spectra": noisy_spectra,
        "pure_components": pure_components,
        "mixing_coefficients": mixing_coeffs,
        "dominant_labels": dominant_component,
        "component_centers": component_centers,
        "component_widths": component_widths,
        "noise_level": noise_level,
        "snr_db": 20 * np.log10(np.std(mixed_spectra) / noise_level),
    }


def vertex_component_analysis(spectra: np.ndarray, n_components: int) -> Dict[str, np.ndarray]:
    """
    Vertex Component Analysis (VCA) for endmember extraction.

    Finds the most pure pixels/spectra by projecting onto a simplex.
    More robust than NMF for spectral unmixing applications.
    """
    X = np.asarray(spectra, dtype=float)
    if X.ndim != 2:
        raise ValueError("Spectra must be 2D array")

    n_samples, n_bands = X.shape
    if n_components >= n_samples:
        raise ValueError("n_components must be less than n_samples")

    # Step 1: Dimensionality reduction via PCA
    X_centered = X - np.mean(X, axis=0)
    U, s, Vt = svd(X_centered, full_matrices=False)

    # Keep components that explain variance
    n_pc = min(n_components, len(s))
    Y = U[:, :n_pc] @ np.diag(s[:n_pc])

    # Step 2: Projection onto probability simplex
    # Add small regularization
    Y_proj = Y + 1e-6

    # Step 3: Vertex finding using iterative projection
    endmember_indices = []
    remaining_indices = list(range(n_samples))

    # Initialize with maximum norm point
    norms = np.linalg.norm(Y_proj, axis=1)
    first_vertex = np.argmax(norms)
    endmember_indices.append(first_vertex)
    remaining_indices.remove(first_vertex)

    # Iteratively find vertices
    for _ in range(n_components - 1):
        if not remaining_indices:
            break

        # Project remaining points away from current endmembers
        projections = []

        for idx in remaining_indices:
            point = Y_proj[idx, :]
            # Distance to convex hull of current endmembers
            distances = []
            for em_idx in endmember_indices:
                em_point = Y_proj[em_idx, :]
                distances.append(np.linalg.norm(point - em_point))
            min_distance = np.min(distances)
            projections.append(min_distance)

        # Select point with maximum distance to current endmembers
        max_proj_idx = np.argmax(projections)
        next_vertex = remaining_indices[max_proj_idx]
        endmember_indices.append(next_vertex)
        remaining_indices.remove(next_vertex)

    # Extract endmember spectra
    endmembers = X[endmember_indices, :]

    # Compute abundances using least squares
    abundances = np.zeros((n_samples, n_components))
    for i in range(n_samples):
        # Non-negative least squares with sum-to-one constraint
        spectrum = X[i, :]
        try:
            # Simple approach: solve with regularization
            A = np.vstack([endmembers.T, np.ones(n_components)])
            b = np.hstack([spectrum, 1.0])
            result = np.linalg.lstsq(A, b, rcond=None)
            abundances[i, :] = np.clip(result[0], 0, None)
            abundances[i, :] /= np.sum(abundances[i, :]) + 1e-12
        except np.linalg.LinAlgError:
            # Fallback: uniform mixing
            abundances[i, :] = 1.0 / n_components

    return {
        "endmembers": endmembers,
        "abundances": abundances,
        "endmember_indices": np.array(endmember_indices),
        "reconstruction": abundances @ endmembers,
        "explained_variance_ratio": s[:n_pc] ** 2 / np.sum(s**2) if len(s) > 0 else np.array([]),
    }


def independent_component_analysis_spectra(
    spectra: np.ndarray, n_components: int, max_iter: int = 1000, tol: float = 1e-4
) -> Dict[str, np.ndarray]:
    """
    Independent Component Analysis (ICA) for blind source separation of spectra.

    Uses FastICA algorithm with spectral data preprocessing.
    """
    X = np.asarray(spectra, dtype=float)
    if X.ndim != 2:
        raise ValueError("Spectra must be 2D array")

    n_samples, n_bands = X.shape
    n_components = min(n_components, n_samples, n_bands)

    # Center and whiten the data
    X_centered = X - np.mean(X, axis=0)

    # PCA whitening
    U, s, Vt = svd(X_centered, full_matrices=False)
    # Keep only the first n_components
    s_trunc = s[:n_components]
    Vt_trunc = Vt[:n_components, :]

    # Whitening matrix
    whitening_matrix = np.diag(1.0 / np.sqrt(s_trunc + 1e-12)) @ Vt_trunc
    X_whitened = X_centered @ whitening_matrix.T

    # FastICA iteration
    W = np.random.RandomState(42).normal(size=(n_components, n_components))
    W = np.linalg.qr(W)[0]  # Orthogonalize

    for iteration in range(max_iter):
        W_old = W.copy()

        # FastICA update with tanh nonlinearity
        Y = X_whitened @ W.T
        g_Y = np.tanh(Y)
        g_prime_Y = 1 - g_Y**2

        W_new = (1.0 / n_samples) * (X_whitened.T @ g_Y) - np.mean(g_prime_Y, axis=0)[:, None] * W

        # Gram-Schmidt orthogonalization
        for i in range(n_components):
            for j in range(i):
                W_new[i, :] -= np.dot(W_new[i, :], W_new[j, :]) * W_new[j, :]
            W_new[i, :] /= np.linalg.norm(W_new[i, :]) + 1e-12

        W = W_new

        # Check convergence
        if np.max(np.abs(np.abs(np.diag(W @ W_old.T)) - 1)) < tol:
            break

    # Compute independent components
    independent_components = X_whitened @ W.T

    # Mixing matrix
    mixing_matrix = np.linalg.pinv(W @ whitening_matrix)

    # Reconstruct spectra
    reconstructed = independent_components @ W @ whitening_matrix
    reconstructed += np.mean(X, axis=0)[None, :]

    return {
        "independent_components": independent_components,
        "mixing_matrix": mixing_matrix,
        "whitening_matrix": whitening_matrix,
        "unmixing_matrix": W,
        "reconstructed_spectra": reconstructed,
        "n_iterations": iteration + 1,
        "converged": iteration < max_iter - 1,
    }
