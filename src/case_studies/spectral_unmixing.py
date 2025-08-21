"""Appendix E: Spectral unmixing and simple classification.

Implements deterministic NMF (seeded) and a tiny LDA baseline using
closed-form estimates for two classes.
"""
from __future__ import annotations

from typing import Dict, Tuple
import numpy as np


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


def lda_baseline(features: np.ndarray, labels: np.ndarray, seed: int = 42) -> Dict[str, float]:
    """
    Closed-form two-class LDA with equal covariance; returns accuracy on train.
    Deterministic given inputs.
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


