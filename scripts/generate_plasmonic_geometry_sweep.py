#!/usr/bin/env python3
"""Appendix F script: Plasmonic Nano-Geometry using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import sweep_plasmonic_quality


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

    radii = np.linspace(10e-9, 200e-9, 100)
    out = sweep_plasmonic_quality(radii, metal_epsilon_imag=1.0, medium_epsilon_real=1.5)
    q = out['q_factor_proxy']

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(radii * 1e9, q)
    ax.set_xlabel("Radius (nm)")
    ax.set_ylabel("Quality factor (a.u.)")
    ax.set_title("Plasmonic geometry sweep")
    ax.grid(True, alpha=0.3)

    out_png = os.path.join(fig_dir, "plasmonic_geometry_sweep.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    write_caption(os.path.join(fig_dir, "plasmonic_geometry_sweep.caption.txt"), "Proxy Q-factor vs nanoparticle radius for fixed material parameters.")

    np.savez(os.path.join(data_dir, "plasmonic_geometry.npz"), radii=radii, q=q)

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
