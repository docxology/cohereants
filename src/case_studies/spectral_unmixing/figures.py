"""Appendix figure rendering for spectral_unmixing."""

from __future__ import annotations

from typing import Mapping

import matplotlib.pyplot as plt

from src.viz.warnings_util import suppress_plot_warnings


def render_comprehensive_figure(analysis: Mapping[str, object]) -> tuple[object, dict[str, float]]:
    """Render comprehensive appendix figure and return summary metrics."""
    data = analysis.as_dict() if hasattr(analysis, "as_dict") else analysis
    with suppress_plot_warnings():
        import matplotlib.pyplot as plt

        wavelengths = data["wavelengths"]
        mixed_spectra = data["mixed_spectra"]
        true_components = data["true_components"]
        nmf_results = data["nmf_results"]
        vca_results = data["vca_results"]
        features_all = data["features_all"]
        classification_results = data["classification_results"]
        nmf_reconstruction = data["nmf_reconstruction"]
        vca_reconstruction = data["vca_reconstruction"]
        nmf_mse = float(data["nmf_mse"])
        vca_mse = float(data["vca_mse"])
        spectral_data = data["spectral_data"]

        fig, axes = plt.subplots(3, 4, figsize=(16, 12))

        ax = axes[0, 0]
        for i in range(0, min(8, mixed_spectra.shape[0]), 2):
            ax.plot(wavelengths, mixed_spectra[i, :], alpha=0.7)
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Intensity")
        ax.set_title("Mixed Spectra Examples")
        ax.grid(True, alpha=0.3)

        ax = axes[0, 1]
        for i in range(true_components.shape[0]):
            ax.plot(wavelengths, true_components[i, :], linewidth=2, label=f"C{i + 1}")
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Intensity")
        ax.set_title("True Components")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[0, 2]
        for i in range(nmf_results["H"].shape[0]):
            ax.plot(wavelengths, nmf_results["H"][i, :], linewidth=2, label=f"NMF{i + 1}")
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Intensity")
        ax.set_title("NMF Components")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[0, 3]
        for i in range(vca_results["endmembers"].shape[0]):
            ax.plot(wavelengths, vca_results["endmembers"][i, :], linewidth=2, label=f"VCA{i + 1}")
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Intensity")
        ax.set_title("VCA Endmembers")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[1, 0]
        methods = ["NMF", "VCA"]
        errors = [nmf_mse, vca_mse]
        bars = ax.bar(methods, errors, color=["blue", "green"], alpha=0.7)
        ax.set_ylabel("Mean Squared Error")
        ax.set_title("Reconstruction Errors")
        for bar, error in zip(bars, errors):
            ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height(), f"{error:.4f}", ha="center", va="bottom")

        ax = axes[1, 1]
        classifiers = list(classification_results.keys())
        accuracies = [classification_results[clf]["accuracy"] for clf in classifiers]
        bars = ax.bar(classifiers, accuracies, color="skyblue", alpha=0.7)
        ax.set_ylabel("Accuracy")
        ax.set_title("Classification Performance")
        ax.tick_params(axis="x", rotation=45)
        for bar, acc in zip(bars, accuracies):
            ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 0.01, f"{acc:.3f}", ha="center", va="bottom", fontsize=8)

        ax = axes[1, 2]
        mixing_coeffs = spectral_data["mixing_coefficients"]
        im = ax.imshow(mixing_coeffs[:25, :].T, aspect="auto", cmap="viridis")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Component")
        ax.set_title("True Mixing Coefficients")
        plt.colorbar(im, ax=ax, label="Abundance")

        ax = axes[1, 3]
        if "pca_explained_variance" in features_all:
            explained_var = features_all["pca_explained_variance"][:8]
            ax.bar(range(1, len(explained_var) + 1), explained_var, alpha=0.7)
            ax.set_xlabel("Principal Component")
            ax.set_ylabel("Explained Variance")
            ax.set_title("PCA Feature Importance")
        ax.grid(True, alpha=0.3)

        for i in range(4):
            ax = axes[2, i]
            sample_idx = i * 20
            if sample_idx < mixed_spectra.shape[0]:
                ax.plot(wavelengths, mixed_spectra[sample_idx, :], "k-", linewidth=2, label="Original")
                ax.plot(wavelengths, nmf_reconstruction[sample_idx, :], "b--", linewidth=2, label="NMF")
                ax.plot(wavelengths, vca_reconstruction[sample_idx, :], "r:", linewidth=2, label="VCA")
                ax.set_xlabel("Wavelength (μm)")
                ax.set_ylabel("Intensity")
                ax.set_title(f"Sample {sample_idx}")
                if i == 0:
                    ax.legend(fontsize=8)
                ax.grid(True, alpha=0.3)

        plt.tight_layout()

        best_classifier = max(classifiers, key=lambda x: classification_results[x]["accuracy"])
        best_accuracy = float(classification_results[best_classifier]["accuracy"])
        best_unmixing = "NMF" if nmf_mse < vca_mse else "VCA"
        best_mse = float(min(nmf_mse, vca_mse))
        metrics = {
            "best_accuracy": best_accuracy,
            "best_mse": best_mse,
            "best_classifier": best_classifier,
            "best_unmixing": best_unmixing,
            "snr_db": float(spectral_data["snr_db"]),
        }
        return fig, metrics

