#!/usr/bin/env python3
"""Appendix G script: Active-Inference demo using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_figure_bundle_from_script
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import olfactory_active_inference_step


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

    # Deterministic gradient-following steps toward origin
    steps = 60
    state = {'x': 1.5, 'y': 1.0}
    params = {'step': 0.1, 'gain': 1.0}
    traj = [state.copy()]
    for _ in range(steps):
        state = olfactory_active_inference_step(state, params)
        traj.append(state.copy())
    x = np.array([p['x'] for p in traj])
    y = np.array([p['y'] for p in traj])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, '-o', markersize=3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Active-inference trajectory")
    ax.grid(True, alpha=0.3)

    out_png = os.path.join(fig_dir, "active_inference_trajectory.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    caption = (
        "Deterministic gradient-following trajectory under a simple active-inference step model. "
        "Behavioral demo only; not field data."
    )
    write_figure_bundle_from_script(
        out_png,
        caption,
        label="fig:app_active_inference",
    )

    np.savez(os.path.join(data_dir, "active_inference_demo.npz"), x=x, y=y)

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
