#!/usr/bin/env python3
"""Appendix D script: Neural Encoding using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import (
    information_rate_time_series,
    rate_coding_metrics,
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

    rng = np.random.default_rng(42)
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 5 * t)
    noise = 0.2 * rng.standard_normal(t.shape)
    resp = signal + noise

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(t, resp, label="Response")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (a.u.)")
    ax.set_title("Neural response surrogate and information metrics")
    ax.grid(True, alpha=0.3)

    out_png = os.path.join(fig_dir, "neural_encoding_information_rate.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    write_caption(os.path.join(fig_dir, "neural_encoding_information_rate.caption.txt"), "Information rate and rate-coding metrics from deterministic time-series.")

    ir = information_rate_time_series(resp, dt_s=t[1]-t[0], noise_std=0.2)
    labels = np.r_[np.zeros(resp.size//2), np.ones(resp.size - resp.size//2)]
    metrics = rate_coding_metrics(resp, labels)

    np.savez(
        os.path.join(data_dir, "neural_encoding.npz"),
        t=t,
        response=resp,
        channel_capacity_bits=ir['channel_capacity_bits'],
        information_rate_bits=ir['information_rate_bits'],
        d_prime=metrics['d_prime'],
        mean_diff=metrics['mean_diff'],
    )

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
