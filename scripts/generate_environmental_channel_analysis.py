#!/usr/bin/env python3
"""Generate comprehensive environmental channel analysis."""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import analysis_as_dict, ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script

ensure_src_on_path()
from src.viz.figure_helpers import format_appendix_caption
from src.case_studies.environmental_channel import compute_environmental_channel_analysis, render_comprehensive_figure
from src.viz.figure_helpers import format_display_metric


def main() -> int:
    """Thin orchestrator for environmental channel appendix figure generation."""
    try:
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()

        analysis = compute_environmental_channel_analysis()
        analysis_data = analysis_as_dict(analysis)
        fig, metrics = render_comprehensive_figure(analysis)

        out_png = os.path.join(fig_dir, "environmental_channel_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        caption = format_appendix_caption("fig:app_env_channel", metrics)
        write_figure_bundle_from_script(out_png, caption, label="fig:app_env_channel")

        transmission_results = analysis_data["transmission_results"]
        capacity_results = analysis_data["capacity_results"]
        out_npz = os.path.join(data_dir, "environmental_channel_comprehensive.npz")
        np.savez(
            out_npz,
            wavelengths_um=analysis_data["wavelengths_um"],
            clear_transmission=transmission_results["clear"]["transmission_total"],
            humid_transmission=transmission_results["humid"]["transmission_total"],
            clear_capacity=capacity_results["clear"]["capacity_bps"],
            humid_capacity=capacity_results["humid"]["capacity_bps"],
            clear_snr=capacity_results["clear"]["snr_db"],
            humid_snr=capacity_results["humid"]["snr_db"],
        )

        print(f"Generated: {out_png}")
        print(out_png)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
