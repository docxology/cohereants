#!/usr/bin/env python3
"""Generate comprehensive detection limits and operating regions analysis."""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import analysis_as_dict, ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script

ensure_src_on_path()
from src.case_studies.detection_limits import compute_detection_limits_analysis, render_comprehensive_figure
from src.viz.figure_helpers import format_appendix_caption
from src.visualization import set_plot_style


def main() -> int:
    """Thin orchestrator for detection limits appendix figure generation."""
    try:
        print("Starting detection limits analysis...")
        set_mpl_backend()
        set_plot_style("science")
        fig_dir, data_dir = setup_paths()

        analysis = compute_detection_limits_analysis()
        analysis_data = analysis_as_dict(analysis)
        fig, metrics = render_comprehensive_figure(analysis)

        out_png = os.path.join(fig_dir, "detection_limits_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        caption = format_appendix_caption("fig:app_detection_limits", metrics)
        write_figure_bundle_from_script(out_png, caption, label="fig:app_detection_limits")

        roc_results = analysis_data["roc_results"]
        detection_perf = analysis_data["detection_perf"]
        operating_regions = analysis_data["operating_regions"]
        range_analysis = analysis_data["range_analysis"]
        noise_analysis = analysis_data["noise_analysis"]

        out_npz = os.path.join(data_dir, "detection_limits_comprehensive.npz")
        np.savez(
            out_npz,
            roc_6db_pfa=roc_results["snr_6db"]["pfa"],
            roc_6db_pd=roc_results["snr_6db"]["pd"],
            roc_6db_auc=roc_results["snr_6db"]["auc"],
            snr_db_range=detection_perf["snr_db"],
            detection_probability=detection_perf["pd"],
            mds_snr_db=detection_perf["mds_snr_db"],
            power_grid=operating_regions["power_grid_w"],
            temperature_grid=operating_regions["temperature_grid_k"],
            snr_grid=operating_regions["snr_grid_db"],
            max_range_atmospheric_m=range_analysis["max_range_atmospheric_m"],
            received_power_dbm=range_analysis["received_power_dbm"],
            frequencies_hz=noise_analysis["frequencies_hz"],
            total_noise_db=noise_analysis["total_noise_db"],
        )

        print(f"Generated: {out_png}")
        print(f"Best AUC: {metrics['best_auc']:.3f}")
        print(f"MDS: {metrics['mds_snr_db']:.1f} dB")
        print(f"Max range: {metrics['max_range_km']:.1f} km")
        print("300 DPI appendix figure")
        print(out_png)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
