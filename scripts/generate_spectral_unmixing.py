#!/usr/bin/env python3
"""Generate comprehensive spectral unmixing and classification analysis."""
from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption

ensure_src_on_path()
from src.case_studies.spectral_unmixing import (
    generate_realistic_chc_spectra,
    nmf_unmix,
    vertex_component_analysis,
    spectral_feature_extraction,
    advanced_classification_suite
)


def main() -> int:
    """Generate comprehensive spectral unmixing and classification analysis."""
    try:
        print("🔄 Starting spectral unmixing analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()
        
        # Generate realistic CHC spectral data
        print("📊 Generating realistic CHC spectral data...")
        spectral_data = generate_realistic_chc_spectra(
            n_samples=100, n_wavelengths=250, n_components=4, seed=42
        )
        
        wavelengths = spectral_data['wavelengths_um']
        mixed_spectra = spectral_data['mixed_spectra']
        true_components = spectral_data['pure_components']
        labels = spectral_data['dominant_labels']
        
        print("🧪 Performing unmixing algorithms...")
        # Unmixing algorithms
        nmf_results = nmf_unmix(mixed_spectra, n_components=4, seed=42)
        vca_results = vertex_component_analysis(mixed_spectra, n_components=4)
        
        print("🎯 Extracting features and classification...")
        # Feature extraction and classification
        features_all = spectral_feature_extraction(mixed_spectra, wavelengths, method='all')
        classification_results = advanced_classification_suite(
            features_all['statistical_features'], labels, test_size=0.3, seed=42
        )
        
        # Calculate reconstruction errors
        nmf_reconstruction = nmf_results['W'] @ nmf_results['H']
        vca_reconstruction = vca_results['reconstruction']
        nmf_mse = np.mean((mixed_spectra - nmf_reconstruction)**2)
        vca_mse = np.mean((mixed_spectra - vca_reconstruction)**2)
        
        print("📈 Creating visualization...")
        # Create comprehensive figure
        fig, axes = plt.subplots(3, 4, figsize=(16, 12))
        
        # Mixed spectra examples
        ax = axes[0, 0]
        for i in range(0, min(8, mixed_spectra.shape[0]), 2):
            ax.plot(wavelengths, mixed_spectra[i, :], alpha=0.7)
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Intensity')
        ax.set_title('Mixed Spectra Examples')
        ax.grid(True, alpha=0.3)

        # True components
        ax = axes[0, 1]
        for i in range(true_components.shape[0]):
            ax.plot(wavelengths, true_components[i, :], linewidth=2, label=f'C{i+1}')
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Intensity')
        ax.set_title('True Components')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # NMF components
        ax = axes[0, 2]
        for i in range(nmf_results['H'].shape[0]):
            ax.plot(wavelengths, nmf_results['H'][i, :], linewidth=2, label=f'NMF{i+1}')
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Intensity')
        ax.set_title('NMF Components')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # VCA endmembers
        ax = axes[0, 3]
        for i in range(vca_results['endmembers'].shape[0]):
            ax.plot(wavelengths, vca_results['endmembers'][i, :], linewidth=2, label=f'VCA{i+1}')
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Intensity')
        ax.set_title('VCA Endmembers')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Reconstruction errors
        ax = axes[1, 0]
        methods = ['NMF', 'VCA']
        errors = [nmf_mse, vca_mse]
        bars = ax.bar(methods, errors, color=['blue', 'green'], alpha=0.7)
        ax.set_ylabel('Mean Squared Error')
        ax.set_title('Reconstruction Errors')
        for bar, error in zip(bars, errors):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{error:.4f}', ha='center', va='bottom')

        # Classification results
        ax = axes[1, 1]
        classifiers = list(classification_results.keys())
        accuracies = [classification_results[clf]['accuracy'] for clf in classifiers]
        bars = ax.bar(classifiers, accuracies, color='skyblue', alpha=0.7)
        ax.set_ylabel('Accuracy')
        ax.set_title('Classification Performance')
        ax.tick_params(axis='x', rotation=45)
        for bar, acc in zip(bars, accuracies):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                    f'{acc:.3f}', ha='center', va='bottom', fontsize=8)

        # Mixing coefficients
        ax = axes[1, 2]
        mixing_coeffs = spectral_data['mixing_coefficients']
        im = ax.imshow(mixing_coeffs[:25, :].T, aspect='auto', cmap='viridis')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Component')
        ax.set_title('True Mixing Coefficients')
        plt.colorbar(im, ax=ax, label='Abundance')

        # Feature importance
        ax = axes[1, 3]
        if 'pca_explained_variance' in features_all:
            explained_var = features_all['pca_explained_variance'][:8]
            ax.bar(range(1, len(explained_var)+1), explained_var, alpha=0.7)
            ax.set_xlabel('Principal Component')
            ax.set_ylabel('Explained Variance')
            ax.set_title('PCA Feature Importance')
        ax.grid(True, alpha=0.3)

        # Sample reconstruction comparisons
        for i in range(4):
            ax = axes[2, i]
            sample_idx = i * 20
            if sample_idx < mixed_spectra.shape[0]:
                ax.plot(wavelengths, mixed_spectra[sample_idx, :], 'k-', linewidth=2, label='Original')
                ax.plot(wavelengths, nmf_reconstruction[sample_idx, :], 'b--', linewidth=2, label='NMF')
                ax.plot(wavelengths, vca_reconstruction[sample_idx, :], 'r:', linewidth=2, label='VCA')
                ax.set_xlabel('Wavelength (μm)')
                ax.set_ylabel('Intensity')
                ax.set_title(f'Sample {sample_idx}')
                if i == 0:
                    ax.legend(fontsize=8)
                ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save outputs
        out_png = os.path.join(fig_dir, "spectral_unmixing_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        # Performance metrics
        best_classifier = max(classifiers, key=lambda x: classification_results[x]['accuracy'])
        best_accuracy = classification_results[best_classifier]['accuracy']
        best_unmixing = 'NMF' if nmf_mse < vca_mse else 'VCA'
        best_mse = min(nmf_mse, vca_mse)
        
        caption = f"""Comprehensive spectral unmixing and classification analysis: Analysis of {mixed_spectra.shape[0]} CHC spectra with {true_components.shape[0]} components. {best_unmixing} achieved best reconstruction (MSE: {best_mse:.4f}) while {best_classifier} achieved best classification accuracy ({best_accuracy:.3f}). Analysis includes NMF and VCA unmixing with comprehensive feature extraction and multi-algorithm classification validation."""
        
        write_caption(os.path.join(fig_dir, "spectral_unmixing_comprehensive_analysis.caption.txt"), caption)

        # Save data
        out_npz = os.path.join(data_dir, "spectral_unmixing_comprehensive.npz")
        np.savez(out_npz,
                wavelengths_um=wavelengths,
                mixed_spectra=mixed_spectra,
                true_components=true_components,
                nmf_W=nmf_results['W'],
                nmf_H=nmf_results['H'],
                nmf_mse=nmf_mse,
                vca_endmembers=vca_results['endmembers'],
                vca_abundances=vca_results['abundances'],
                vca_mse=vca_mse,
                classification_accuracies=np.array(accuracies),
                classifier_names=classifiers,
                snr_db=spectral_data['snr_db'])

        print(f"✅ Success! Generated spectral analysis")
        print(f"Generated: {out_png}")
        print(f"Best unmixing: {best_unmixing} (MSE: {best_mse:.4f})")
        print(f"Best classification: {best_classifier} (Accuracy: {best_accuracy:.3f})")
        print(f"SNR: {spectral_data['snr_db']:.1f} dB")
        print(out_png)
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())