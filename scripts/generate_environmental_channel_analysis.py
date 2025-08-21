#!/usr/bin/env python3
"""Appendix B script: Environmental Channel using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import (
    atmospheric_transmission_detailed,
    channel_capacity_vs_env,
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

    humidity = np.linspace(0.2, 0.9, 60)
    temperature = np.linspace(280.0, 320.0, 60)
    cap = channel_capacity_vs_env(
        material_refractive_index=1.5,
        signal_power_w=1e-6,
        bandwidth_hz=1e6,
        humidity_grid=humidity,
        temperature_grid_k=temperature,
        path_m=100.0,
    )
    capacity = cap['capacity_bits_per_s']

    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(capacity, origin="lower", aspect="auto", extent=[humidity.min(), humidity.max(), temperature.min(), temperature.max()], cmap="viridis")
    ax.set_xlabel("Humidity (fraction)")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Channel capacity vs environment")
    fig.colorbar(im, ax=ax, label="Capacity (a.u.)")

    out_png = os.path.join(fig_dir, "environmental_channel_capacity.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    write_caption(os.path.join(fig_dir, "environmental_channel_capacity.caption.txt"), "Shannon capacity (bits/s) across humidity and temperature with simple transmission/noise model.")

    np.savez(
        os.path.join(data_dir, "environmental_channel.npz"),
        humidity=humidity,
        temperature_k=temperature,
        capacity_bits_per_s=capacity,
    )

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
