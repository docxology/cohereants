#!/usr/bin/env python3
"""Generate comprehensive spectral unmixing and classification analysis."""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script

ensure_src_on_path()
from src.case_studies.spectral_unmixing import compute_spectral_unmixing_analysis, render_comprehensive_figure
from src.viz.figure_helpers import format_appendix_caption


def main() -> int:
    """Thin orchestrator for spectral unmixing appendix figure generation."""
    try:
        print("Starting spectral unmixing analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()

        analysis = compute_spectral_unmixing_analysis()
        analysis_data = analysis.as_dict() if hasattr(analysis, "as_dict") else analysis
        fig, metrics = render_comprehensive_figure(analysis)

        out_png = os.path.join(fig_dir, "spectral_unmixing_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        mixed_spectra = analysis_data["mixed_spectra"]
        true_components = analysis_data["true_components"]
        nmf_results = analysis_data["nmf_results"]
        vca_results = analysis_data["vca_results"]
        classification_results = analysis_data["classification_results"]
        classifiers = list(classification_results.keys())
        accuracies = [classification_results[clf]["accuracy"] for clf in classifiers]

        caption = format_appendix_caption(
            "fig:app_spectral_unmixing",
            metrics,
            n_spectra=mixed_spectra.shape[0],
            n_components=true_components.shape[0],
        )
        write_figure_bundle_from_script(out_png, caption, label="fig:app_spectral_unmixing")

        out_npz = os.path.join(data_dir, "spectral_unmixing_comprehensive.npz")
        np.savez(
            out_npz,
            wavelengths_um=analysis_data["wavelengths"],
            mixed_spectra=mixed_spectra,
            true_components=true_components,
            nmf_W=nmf_results["W"],
            nmf_H=nmf_results["H"],
            nmf_mse=analysis_data["nmf_mse"],
            vca_endmembers=vca_results["endmembers"],
            vca_abundances=vca_results["abundances"],
            vca_mse=analysis_data["vca_mse"],
            classification_accuracies=np.array(accuracies),
            classifier_names=classifiers,
            snr_db=metrics["snr_db"],
        )

        print(f"Generated: {out_png}")
        print(f"Best unmixing: {metrics['best_unmixing']} (MSE: {metrics['best_mse']:.4f})")
        print(f"Best classification: {metrics['best_classifier']} (Accuracy: {metrics['best_accuracy']:.3f})")
        print(f"SNR: {metrics['snr_db']:.1f} dB")
        print(out_png)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
