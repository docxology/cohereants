#!/usr/bin/env python3
"""Appendix C script: Detection Limits using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import (
    min_detectable_power,
    snr_curve,
)


def _setup_paths() -> tuple[str, str]:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fig_dir = os.path.join(repo_root, "output", "figures")
    data_dir = os.path.join(repo_root, "output", "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    return fig_dir, data_dir


def main() -> int:
    set_mpl_backend()
    fig_dir, data_dir = setup_paths()

    bandwidth = np.linspace(1e1, 1e4, 200)
    temp = 300.0
    snr_min = 10.0
    pmin = min_detectable_power(temp, bandwidth, snr_min)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(bandwidth, pmin)
    ax.set_xlabel("Bandwidth (Hz)")
    ax.set_ylabel("Min detectable power (W)")
    ax.set_title("Minimum detectable power vs bandwidth")
    ax.grid(True, which="both", alpha=0.3)

    out_png = os.path.join(fig_dir, "detection_limits_operating_points.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    write_caption(os.path.join(fig_dir, "detection_limits_operating_points.caption.txt"), "Minimum detectable power vs bandwidth from Johnson–Nyquist noise and SNR threshold.")

    np.savez(os.path.join(data_dir, "detection_limits.npz"), bandwidth=bandwidth, pmin=pmin)

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
