"""Classification helpers for spectral unmixing."""

from __future__ import annotations

from typing import Dict
import numpy as np

def advanced_classification_suite(
    features: np.ndarray, labels: np.ndarray, test_size: float = 0.3, seed: int = 42
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
    results["lda"] = _fit_lda_multiclass(X_train_scaled, y_train, X_test_scaled, y_test)

    # 2. Quadratic Discriminant Analysis
    results["qda"] = _fit_qda(X_train_scaled, y_train, X_test_scaled, y_test)

    # 3. Naive Bayes (Gaussian)
    results["naive_bayes"] = _fit_naive_bayes(X_train_scaled, y_train, X_test_scaled, y_test)

    # 4. k-Nearest Neighbors
    results["knn"] = _fit_knn(X_train_scaled, y_train, X_test_scaled, y_test, k=3)

    # 5. Logistic Regression (for binary case)
    if len(np.unique(y)) == 2:
        results["logistic"] = _fit_logistic_regression(X_train_scaled, y_train, X_test_scaled, y_test)

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

    return {"accuracy": accuracy, "predictions": predictions}


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

        class_params[cls] = {"mean": mean, "cov": cov, "prior": prior}

    # Predict using Gaussian likelihood
    predictions = []
    for x in X_test:
        scores = []
        for cls in classes:
            params = class_params[cls]
            try:
                # Multivariate Gaussian likelihood
                diff = x - params["mean"]
                mahalanobis = diff @ np.linalg.solve(params["cov"], diff)
                log_det = np.linalg.slogdet(params["cov"])[1]
                score = -0.5 * (mahalanobis + log_det) + np.log(params["prior"])
                scores.append(score)
            except np.linalg.LinAlgError:
                scores.append(-np.inf)

        predictions.append(classes[np.argmax(scores)])

    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)

    return {"accuracy": accuracy, "predictions": predictions}


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

        class_params[cls] = {"means": means, "variances": variances, "prior": prior}

    # Predict
    predictions = []
    for x in X_test:
        scores = []
        for cls in classes:
            params = class_params[cls]
            # Log likelihood assuming feature independence
            log_likelihood = -0.5 * np.sum(np.log(2 * np.pi * params["variances"]))
            log_likelihood -= 0.5 * np.sum((x - params["means"]) ** 2 / params["variances"])
            score = log_likelihood + np.log(params["prior"])
            scores.append(score)

        predictions.append(classes[np.argmax(scores)])

    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)

    return {"accuracy": accuracy, "predictions": predictions}


def _fit_knn(X_train, y_train, X_test, y_test, k=3):
    """k-Nearest Neighbors classifier."""
    predictions = []

    for x_test in X_test:
        # Calculate distances to all training points
        distances = np.linalg.norm(X_train - x_test, axis=1)

        # Find k nearest neighbors
        k_nearest_indices = np.argpartition(distances, min(k, len(distances) - 1))[:k]
        k_nearest_labels = y_train[k_nearest_indices]

        # Vote (mode)
        unique_labels, counts = np.unique(k_nearest_labels, return_counts=True)
        predicted_label = unique_labels[np.argmax(counts)]
        predictions.append(predicted_label)

    predictions = np.array(predictions)
    accuracy = np.mean(predictions == y_test)

    return {"accuracy": accuracy, "predictions": predictions}


def _fit_logistic_regression(X_train, y_train, X_test, y_test, max_iter=1000):
    """Binary logistic regression using gradient descent."""
    # Convert labels to 0/1
    classes = np.unique(y_train)
    if len(classes) != 2:
        return {"accuracy": 0.0, "predictions": y_test}

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

    return {"accuracy": accuracy, "predictions": predictions}


def performance_metrics_comprehensive(
    y_true: np.ndarray, y_pred: np.ndarray, class_names: Optional[List[str]] = None
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
        "accuracy": accuracy,
        "confusion_matrix": confusion_matrix,
        "precision_per_class": precision,
        "recall_per_class": recall,
        "f1_score_per_class": f1_score,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "weighted_precision": weighted_precision,
        "weighted_recall": weighted_recall,
        "weighted_f1": weighted_f1,
        "classes": classes,
        "class_names": class_names,
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
    return {"train_accuracy": acc}
