#!/usr/bin/env python3
"""Generate comprehensive plasmonic nanoparticle analysis."""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import analysis_as_dict, ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script

ensure_src_on_path()
from src.viz.figure_helpers import format_appendix_caption
from src.case_studies.plasmonic_geometry import compute_plasmonic_geometry_analysis, render_comprehensive_figure


def main() -> int:
    """Thin orchestrator for plasmonic geometry appendix figure generation."""
    try:
        print("Starting plasmonic geometry analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()

        analysis = compute_plasmonic_geometry_analysis()
        analysis_data = analysis_as_dict(analysis)
        fig, metrics = render_comprehensive_figure(analysis)

        out_png = os.path.join(fig_dir, "plasmonic_geometry_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        sweep_gold = analysis_data["sweep_gold"]
        sweep_silver = analysis_data["sweep_silver"]
        optimized_geometries = analysis_data["optimized_geometries"]
        gold_opt_sizes = [opt["optimal_size_nm"] for opt in optimized_geometries["gold"]]
        gold_opt_enhancements = [opt["max_enhancement"] for opt in optimized_geometries["gold"]]
        silver_opt_sizes = [opt["optimal_size_nm"] for opt in optimized_geometries["silver"]]
        silver_opt_enhancements = [opt["max_enhancement"] for opt in optimized_geometries["silver"]]
        field_dist = analysis_data["field_dist"]
        coupling_analysis = analysis_data["coupling_analysis"]

        caption = format_appendix_caption("fig:app_plasmonic_sweep", metrics)
        write_figure_bundle_from_script(out_png, caption, label="fig:app_plasmonic_sweep")

        out_npz = os.path.join(data_dir, "plasmonic_geometry_comprehensive.npz")
        np.savez(
            out_npz,
            radii_nm=analysis_data["radii_nm"],
            wavelengths_um=analysis_data["wavelengths_um"],
            ir_wavelengths=analysis_data["ir_wavelengths"],
            gold_q_factors_2d=sweep_gold["q_factors_2d"],
            gold_enhancements_2d=sweep_gold["enhancements_2d"],
            gold_resonance_wavelengths=sweep_gold["resonance_wavelengths"],
            gold_max_enhancements=sweep_gold["max_enhancements"],
            silver_q_factors_2d=sweep_silver["q_factors_2d"],
            silver_enhancements_2d=sweep_silver["enhancements_2d"],
            silver_resonance_wavelengths=sweep_silver["resonance_wavelengths"],
            silver_max_enhancements=sweep_silver["max_enhancements"],
            gold_permittivity=analysis_data["gold_epsilon"],
            silver_permittivity=analysis_data["silver_epsilon"],
            gold_optimal_sizes=gold_opt_sizes,
            gold_optimal_enhancements=gold_opt_enhancements,
            silver_optimal_sizes=silver_opt_sizes,
            silver_optimal_enhancements=silver_opt_enhancements,
            coupling_positions=analysis_data["positions_nm"],
            coupling_enhancement_ratios=coupling_analysis["enhancement_ratio"],
            coupling_strength=coupling_analysis["coupling_strength"],
            field_x_nm=field_dist["x_nm"],
            field_y_nm=field_dist["y_nm"],
            field_intensity=field_dist["intensity"],
            field_max_enhancement=field_dist["max_enhancement"],
        )

        print(f"Generated: {out_png}")
        print(f"Generated: {out_npz}")
        print(f"Gold max enhancement: {metrics['max_gold_enhancement']:.0f}×")
        print(f"Silver max enhancement: {metrics['max_silver_enhancement']:.0f}×")
        print(f"Coupling enhancement: {metrics['avg_coupling_enhancement']:.1f}× average")
        print(f"Near-field peak: {metrics['field_max_enhancement']:.0f}×")
        print(f"Optimal radius range: {metrics['min_gold_opt_size']:.1f}-{metrics['max_gold_opt_size']:.1f} nm")
        print(out_png)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
