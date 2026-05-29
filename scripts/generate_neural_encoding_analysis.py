#!/usr/bin/env python3
"""Generate comprehensive neural encoding and temporal dynamics analysis."""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import analysis_as_dict, ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script

ensure_src_on_path()
from src.viz.figure_helpers import format_appendix_caption
from src.case_studies.neural_encoding import compute_neural_encoding_analysis, render_comprehensive_figure


def main() -> int:
    """Thin orchestrator for neural encoding appendix figure generation."""
    try:
        print("Starting neural encoding analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()

        analysis = compute_neural_encoding_analysis()
        analysis_data = analysis_as_dict(analysis)
        fig, metrics = render_comprehensive_figure(analysis)

        out_png = os.path.join(fig_dir, "neural_encoding_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        spike_stats = analysis_data["spike_stats"]
        temporal_results = analysis_data["temporal_results"]

        caption = format_appendix_caption("fig:app_neural_encoding_full", metrics)
        write_figure_bundle_from_script(out_png, caption, label="fig:app_neural_encoding_full")

        out_npz = os.path.join(data_dir, "neural_encoding_comprehensive.npz")
        np.savez(
            out_npz,
            time_axis=analysis_data["time_axis"],
            stimuli=analysis_data["stimuli"],
            stimulus_labels=analysis_data["stimulus_labels"],
            mean_firing_rate_hz=spike_stats["mean_firing_rate_hz"],
            cv_isi=spike_stats["cv_isi"],
            fano_factor=spike_stats["fano_factor"],
            mean_latency_s=temporal_results["mean_latency_s"],
            temporal_precision=metrics["temporal_precision"],
            classification_accuracy=metrics["classification_accuracy"],
            mutual_information_bits=metrics["mutual_information_bits"],
            mean_adaptation_index=metrics["mean_adaptation_index"],
        )

        print(f"Generated: {out_png}")
        print(f"Classification accuracy: {metrics['classification_accuracy']:.1%}")
        print(f"Mutual information: {metrics['mutual_information_bits']:.2f} bits")
        print(out_png)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
