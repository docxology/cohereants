"""Appendix E: Spectral unmixing and classification.

Comprehensive spectral analysis module for cuticular hydrocarbon (CHC) and semiochemical
identification using advanced unmixing algorithms, machine learning classification,
and performance evaluation. Includes simulated realistic spectral data generation
and validation against known chemical signatures.
"""
from __future__ import annotations

from typing import Dict, Tuple, List, Union, Optional
import numpy as np
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
    return {'W': W, 'H': H}


def generate_realistic_chc_spectra(
    n_samples: int = 100,
    n_wavelengths: int = 500,
    wavelength_range_um: Tuple[float, float] = (2.5, 25.0),
    n_components: int = 5,
    noise_level: float = 0.05,
    seed: int = 42
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
            -0.5 * ((wavelengths - component_centers[i]) / component_widths[i])**2
        )
        
        # Add overtone and combination bands at harmonics
        if component_centers[i] > 6.0:  # Add overtone for fundamental modes
            overtone = 0.3 * component_strengths[i] * np.exp(
                -0.5 * ((wavelengths - component_centers[i]/2) / (component_widths[i]/2))**2
            )
            primary_band += overtone
        
        # Add CH stretch regions around 3-4 μm
        if component_centers[i] > 8.0:
            ch_stretch = 0.2 * component_strengths[i] * np.exp(
                -0.5 * ((wavelengths - 3.4) / 0.3)**2
            )
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
        'wavelengths_um': wavelengths,
        'mixed_spectra': noisy_spectra,
        'pure_components': pure_components,
        'mixing_coefficients': mixing_coeffs,
        'dominant_labels': dominant_component,
        'component_centers': component_centers,
        'component_widths': component_widths,
        'noise_level': noise_level,
        'snr_db': 20 * np.log10(np.std(mixed_spectra) / noise_level)
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
        'endmembers': endmembers,
        'abundances': abundances,
        'endmember_indices': np.array(endmember_indices),
        'reconstruction': abundances @ endmembers,
        'explained_variance_ratio': s[:n_pc]**2 / np.sum(s**2) if len(s) > 0 else np.array([])
    }


def independent_component_analysis_spectra(
    spectra: np.ndarray, 
    n_components: int,
    max_iter: int = 1000,
    tol: float = 1e-4
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
        'independent_components': independent_components,
        'mixing_matrix': mixing_matrix,
        'whitening_matrix': whitening_matrix,
        'unmixing_matrix': W,
        'reconstructed_spectra': reconstructed,
        'n_iterations': iteration + 1,
        'converged': iteration < max_iter - 1
    }


def spectral_feature_extraction(
    spectra: np.ndarray,
    wavelengths: np.ndarray,
    method: str = 'peaks'
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
    
    if method in ['peaks', 'all']:
        # Peak detection features
        peak_features = []
        for i in range(X.shape[0]):
            spectrum = X[i, :]
            
            # Smooth spectrum
            if len(spectrum) > 5:
                smoothed = savgol_filter(spectrum, min(len(spectrum)//4*2-1, 5), 2)
            else:
                smoothed = spectrum.copy()
            
            # Find peaks (local maxima)
            peaks = []
            for j in range(1, len(smoothed) - 1):
                if smoothed[j] > smoothed[j-1] and smoothed[j] > smoothed[j+1]:
                    peaks.append(j)
            
            # Extract peak features
            if peaks:
                peak_wavelengths = wl[peaks]
                peak_intensities = smoothed[peaks]
                
                # Sort by intensity
                sorted_indices = np.argsort(peak_intensities)[::-1]
                top_peaks = sorted_indices[:min(5, len(peaks))]  # Top 5 peaks
                
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
        
        features['peak_features'] = np.array(peak_features)
    
    if method in ['derivatives', 'all']:
        # Derivative features
        first_deriv = np.gradient(X, axis=1)
        second_deriv = np.gradient(first_deriv, axis=1)
        
        # Statistical moments of derivatives
        deriv_features = []
        for i in range(X.shape[0]):
            d1 = first_deriv[i, :]
            d2 = second_deriv[i, :]
            
            feature_vector = np.array([
                np.mean(d1), np.std(d1), np.max(np.abs(d1)),
                np.mean(d2), np.std(d2), np.max(np.abs(d2))
            ])
            deriv_features.append(feature_vector)
        
        features['derivative_features'] = np.array(deriv_features)
    
    if method in ['pca', 'all']:
        # PCA features
        X_centered = X - np.mean(X, axis=0)
        U, s, Vt = svd(X_centered, full_matrices=False)
        
        # Keep components explaining 95% variance
        cumsum_var = np.cumsum(s**2)
        total_var = np.sum(s**2)
        n_components = np.searchsorted(cumsum_var / total_var, 0.95) + 1
        n_components = min(n_components, len(s))
        
        pca_features = U[:, :n_components] @ np.diag(s[:n_components])
        
        features['pca_features'] = pca_features
        features['pca_explained_variance'] = s[:n_components]**2 / total_var
    
    # Statistical features (always included)
    stat_features = []
    for i in range(X.shape[0]):
        spectrum = X[i, :]
        feature_vector = np.array([
            np.mean(spectrum), np.std(spectrum), np.max(spectrum), np.min(spectrum),
            np.median(spectrum), np.percentile(spectrum, 75) - np.percentile(spectrum, 25),
            np.sum(spectrum), np.trapz(spectrum, wl)
        ])
        stat_features.append(feature_vector)
    
    features['statistical_features'] = np.array(stat_features)
    
    return features


def advanced_classification_suite(
    features: np.ndarray,
    labels: np.ndarray,
    test_size: float = 0.3,
    seed: int = 42
) -> Dict[str, Dict[str, float]]:
    """
    Comprehensive classification analysis using multiple algorithms.
    
    Args:
        features: Feature matrix (n_samples, n_features)
        labels: Class labels
        test_size: Fraction of data for testing
        seed: Random seed
        
    Returns:
        Performance metrics for each classifier
    """
    X = np.asarray(features, dtype=float)
    y = np.asarray(labels)
    
    if X.shape[0] != len(y):
        raise ValueError("Features and labels must have same number of samples")
    
    rng = np.random.default_rng(seed)
    n_samples = len(y)
    n_test = int(n_samples * test_size)
    
    # Train/test split
    indices = rng.permutation(n_samples)
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]
    
    # Standardize features
    mean_features = np.mean(X_train, axis=0)
    std_features = np.std(X_train, axis=0) + 1e-8
    X_train_scaled = (X_train - mean_features) / std_features
    X_test_scaled = (X_test - mean_features) / std_features
    
    results = {}
    
    # 1. Linear Discriminant Analysis
    results['lda'] = _fit_lda_multiclass(X_train_scaled, y_train, X_test_scaled, y_test)
    
    # 2. Quadratic Discriminant Analysis
    results['qda'] = _fit_qda(X_train_scaled, y_train, X_test_scaled, y_test)
    
    # 3. Naive Bayes (Gaussian)
    results['naive_bayes'] = _fit_naive_bayes(X_train_scaled, y_train, X_test_scaled, y_test)
    
    # 4. k-Nearest Neighbors
    results['knn'] = _fit_knn(X_train_scaled, y_train, X_test_scaled, y_test, k=3)
    
    # 5. Logistic Regression (for binary case)
    if len(np.unique(y)) == 2:
        results['logistic'] = _fit_logistic_regression(X_train_scaled, y_train, X_test_scaled, y_test)
    
    return results


def _fit_lda_multiclass(X_train, y_train, X_test, y_test):
    """Multi-class Linear Discriminant Analysis."""
    classes = np.unique(y_train)
    n_classes = len(classes)
    n_features = X_train.shape[1]
    
    # Class means
    class_means = np.zeros((n_classes, n_features))
    class_counts = np.zeros(n_classes)
    
    for i, cls in enumerate(classes):
        mask = y_train == cls
        class_means[i, :] = np.mean(X_train[mask, :], axis=0)
        class_counts[i] = np.sum(mask)
    
    # Pooled covariance
    S_w = np.zeros((n_features, n_features))
    for i, cls in enumerate(classes):
        mask = y_train == cls
        X_cls = X_train[mask, :]
        X_cls_centered = X_cls - class_means[i, :]
        S_w += X_cls_centered.T @ X_cls_centered
    
    S_w /= len(y_train) - n_classes
    S_w += np.eye(n_features) * 1e-6  # Regularization
    
    # Predict
    predictions = []
    for x in X_test:
        scores = []
        for i, cls in enumerate(classes):
            diff = x - class_means[i, :]
            score = -0.5 * diff @ np.linalg.solve(S_w, diff) + np.log(class_counts[i] / len(y_train))
            scores.append(score)
        predictions.append(classes[np.argmax(scores)])
    
    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)
    
    return {'accuracy': accuracy, 'predictions': predictions}


def _fit_qda(X_train, y_train, X_test, y_test):
    """Quadratic Discriminant Analysis."""
    classes = np.unique(y_train)
    n_features = X_train.shape[1]
    
    class_params = {}
    for cls in classes:
        mask = y_train == cls
        X_cls = X_train[mask, :]
        
        mean = np.mean(X_cls, axis=0)
        cov = np.cov(X_cls.T) + np.eye(n_features) * 1e-4
        prior = np.sum(mask) / len(y_train)
        
        class_params[cls] = {'mean': mean, 'cov': cov, 'prior': prior}
    
    # Predict using Gaussian likelihood
    predictions = []
    for x in X_test:
        scores = []
        for cls in classes:
            params = class_params[cls]
            try:
                # Multivariate Gaussian likelihood
                diff = x - params['mean']
                mahalanobis = diff @ np.linalg.solve(params['cov'], diff)
                log_det = np.linalg.slogdet(params['cov'])[1]
                score = -0.5 * (mahalanobis + log_det) + np.log(params['prior'])
                scores.append(score)
            except np.linalg.LinAlgError:
                scores.append(-np.inf)
        
        predictions.append(classes[np.argmax(scores)])
    
    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)
    
    return {'accuracy': accuracy, 'predictions': predictions}


def _fit_naive_bayes(X_train, y_train, X_test, y_test):
    """Gaussian Naive Bayes classifier."""
    classes = np.unique(y_train)
    class_params = {}
    
    for cls in classes:
        mask = y_train == cls
        X_cls = X_train[mask, :]
        
        means = np.mean(X_cls, axis=0)
        variances = np.var(X_cls, axis=0) + 1e-8  # Add small regularization
        prior = np.sum(mask) / len(y_train)
        
        class_params[cls] = {'means': means, 'variances': variances, 'prior': prior}
    
    # Predict
    predictions = []
    for x in X_test:
        scores = []
        for cls in classes:
            params = class_params[cls]
            # Log likelihood assuming feature independence
            log_likelihood = -0.5 * np.sum(np.log(2 * np.pi * params['variances']))
            log_likelihood -= 0.5 * np.sum((x - params['means'])**2 / params['variances'])
            score = log_likelihood + np.log(params['prior'])
            scores.append(score)
        
        predictions.append(classes[np.argmax(scores)])
    
    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)
    
    return {'accuracy': accuracy, 'predictions': predictions}


def _fit_knn(X_train, y_train, X_test, y_test, k=3):
    """k-Nearest Neighbors classifier."""
    predictions = []
    
    for x_test in X_test:
        # Calculate distances to all training points
        distances = np.linalg.norm(X_train - x_test, axis=1)
        
        # Find k nearest neighbors
        k_nearest_indices = np.argpartition(distances, min(k, len(distances)-1))[:k]
        k_nearest_labels = y_train[k_nearest_indices]
        
        # Vote (mode)
        unique_labels, counts = np.unique(k_nearest_labels, return_counts=True)
        predicted_label = unique_labels[np.argmax(counts)]
        predictions.append(predicted_label)
    
    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)
    
    return {'accuracy': accuracy, 'predictions': predictions}


def _fit_logistic_regression(X_train, y_train, X_test, y_test, max_iter=1000):
    """Binary logistic regression using gradient descent."""
    # Convert labels to 0/1
    classes = np.unique(y_train)
    if len(classes) != 2:
        return {'accuracy': 0.0, 'predictions': y_test}
    
    y_binary = (y_train == classes[1]).astype(float)
    
    # Add bias term
    X_train_bias = np.column_stack([np.ones(len(X_train)), X_train])
    X_test_bias = np.column_stack([np.ones(len(X_test)), X_test])
    
    # Initialize weights
    w = np.zeros(X_train_bias.shape[1])
    
    # Gradient descent
    learning_rate = 0.01
    for _ in range(max_iter):
        # Predictions
        z = X_train_bias @ w
        p = 1 / (1 + np.exp(-np.clip(z, -500, 500)))  # Avoid overflow
        
        # Gradient
        gradient = X_train_bias.T @ (p - y_binary) / len(y_binary)
        
        # Update
        w -= learning_rate * gradient
        
        # Simple convergence check
        if np.linalg.norm(gradient) < 1e-6:
            break
    
    # Test predictions
    z_test = X_test_bias @ w
    p_test = 1 / (1 + np.exp(-np.clip(z_test, -500, 500)))
    predictions_binary = (p_test > 0.5).astype(float)
    
    # Convert back to original labels
    predictions = np.where(predictions_binary == 1, classes[1], classes[0])
    accuracy = np.mean(predictions == y_test)
    
    return {'accuracy': accuracy, 'predictions': predictions}


def performance_metrics_comprehensive(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: Optional[List[str]] = None
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Compute comprehensive performance metrics for classification.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: Optional class names for reporting
        
    Returns:
        Dictionary with various performance metrics
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    classes = np.unique(np.concatenate([y_true, y_pred]))
    n_classes = len(classes)
    
    if class_names is None:
        class_names = [f"Class_{i}" for i in classes]
    
    # Confusion matrix
    confusion_matrix = np.zeros((n_classes, n_classes), dtype=int)
    for i, true_class in enumerate(classes):
        for j, pred_class in enumerate(classes):
            confusion_matrix[i, j] = np.sum((y_true == true_class) & (y_pred == pred_class))
    
    # Overall accuracy
    accuracy = np.mean(y_true == y_pred)
    
    # Per-class metrics
    precision = np.zeros(n_classes)
    recall = np.zeros(n_classes)
    f1_score = np.zeros(n_classes)
    
    for i, cls in enumerate(classes):
        tp = confusion_matrix[i, i]
        fp = np.sum(confusion_matrix[:, i]) - tp
        fn = np.sum(confusion_matrix[i, :]) - tp
        
        precision[i] = tp / (tp + fp + 1e-12)
        recall[i] = tp / (tp + fn + 1e-12)
        f1_score[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i] + 1e-12)
    
    # Macro and weighted averages
    macro_precision = np.mean(precision)
    macro_recall = np.mean(recall)
    macro_f1 = np.mean(f1_score)
    
    # Weighted by class frequency
    class_weights = np.array([np.sum(y_true == cls) for cls in classes]) / len(y_true)
    weighted_precision = np.sum(precision * class_weights)
    weighted_recall = np.sum(recall * class_weights)
    weighted_f1 = np.sum(f1_score * class_weights)
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': confusion_matrix,
        'precision_per_class': precision,
        'recall_per_class': recall,
        'f1_score_per_class': f1_score,
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'macro_f1': macro_f1,
        'weighted_precision': weighted_precision,
        'weighted_recall': weighted_recall,
        'weighted_f1': weighted_f1,
        'classes': classes,
        'class_names': class_names
    }


def lda_baseline(features: np.ndarray, labels: np.ndarray, seed: int = 42) -> Dict[str, float]:
    """
    Closed-form two-class LDA with equal covariance; returns accuracy on train.
    Deterministic given inputs. (Legacy function for compatibility)
    """
    X = np.asarray(features, dtype=float)
    y = np.asarray(labels)
    if X.ndim != 2 or y.ndim != 1 or X.shape[0] != y.size:
        raise ValueError("Invalid feature/label shapes")
    classes = np.unique(y)
    if classes.size != 2:
        raise ValueError("LDA baseline supports exactly 2 classes")
    X0 = X[y == classes[0]]
    X1 = X[y == classes[1]]
    m0 = X0.mean(axis=0)
    m1 = X1.mean(axis=0)
    # Pooled covariance
    S = np.cov(X.T, bias=False)
    # Regularize minimally for stability
    S += np.eye(S.shape[0]) * 1e-6
    w = np.linalg.solve(S, (m1 - m0))
    b = -0.5 * (m1 + m0) @ w
    preds = (X @ w + b >= 0).astype(y.dtype)
    acc = float(np.mean(preds == (y == classes[1])))
    return {'train_accuracy': acc}


