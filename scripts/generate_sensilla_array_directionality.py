#!/usr/bin/env python3
"""Generate comprehensive sensilla array directionality analysis."""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import analysis_as_dict, ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script

ensure_src_on_path()
from src.viz.figure_helpers import format_appendix_caption
from src.case_studies.sensilla_array_directionality import (
    compute_sensilla_array_analysis,
    render_comprehensive_figure,
)


def main() -> int:
    """Thin orchestrator for sensilla array appendix figure generation."""
    try:
        print("Starting sensilla array analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()

        analysis = compute_sensilla_array_analysis()
        analysis_data = analysis_as_dict(analysis)
        fig, metrics = render_comprehensive_figure(analysis)

        out_png = os.path.join(fig_dir, "sensilla_array_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        morphology_analysis = analysis_data["morphology_analysis"]
        freq_response = analysis_data["freq_response"]
        n_sensilla = int(metrics["n_sensilla"])

        caption = format_appendix_caption("fig:app_sensilla_beam", metrics)
        write_figure_bundle_from_script(out_png, caption, label="fig:app_sensilla_beam")

        out_npz = os.path.join(data_dir, "sensilla_array_comprehensive.npz")
        np.savez(
            out_npz,
            log_positions=analysis_data["log_positions"],
            circular_positions=analysis_data["circ_positions"],
            wavelengths=analysis_data["wavelengths"],
            log_pattern=analysis_data["log_pattern"]["pattern"],
            log_gain=metrics["log_gain"],
            sensilla_lengths=morphology_analysis["sensilla_lengths_um"],
            sensilla_diameters=morphology_analysis["sensilla_diameters_um"],
            wavelength_matching_matrix=morphology_analysis["wavelength_matching_matrix"],
            best_wavelength_matches=morphology_analysis["best_wavelength_matches"],
            match_quality_scores=morphology_analysis["match_quality_scores"],
            q_factors=morphology_analysis["q_factors"],
            frequencies_thz=freq_response["frequencies_thz"],
            gain_db=freq_response["gain_db"],
            impedance_real=freq_response["impedance_real"],
            impedance_imag=freq_response["impedance_imag"],
            resonance_frequencies=freq_response["resonance_frequencies_thz"],
            bandwidth_3db=freq_response["bandwidth_3db_thz"],
            angles=analysis_data["angles"],
            dipole_pattern=analysis_data["dipole_pattern"],
            monopole_pattern=analysis_data["monopole_pattern"],
            patch_pattern=analysis_data["patch_pattern"],
            coupling_matrix_magnitude=np.abs(analysis_data["coupling_matrix"]),
        )

        print(f"Generated: {out_png}")
        print(f"Generated: {out_npz}")
        print(f"Log-periodic array gain: {metrics['log_gain']:.2f}")
        print(f"Circular array elements: {int(metrics['n_circular_elements'])}")
        print(f"Frequency bandwidth: {metrics['bandwidth_3db_thz']:.1f} THz")
        print(f"Average Q factor: {metrics['q_factor_avg']:.1f}")
        print(f"Morphology correlation: {metrics['morph_correlation']:.3f}")
        print(out_png)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
