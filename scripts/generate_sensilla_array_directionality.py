#!/usr/bin/env python3
"""Appendix A script: Sensilla Array Directionality using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import (
    design_log_periodic_array,
    compute_beam_pattern,
    array_gain,
)


def _setup_paths() -> tuple[str, str]:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fig_dir = os.path.join(repo_root, "output", "figures")
    data_dir = os.path.join(repo_root, "output", "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    return fig_dir, data_dir


essential_caption = "Beam pattern vs wavelength for log-periodic sensilla array; normalized power and array gain."


def main() -> int:
    set_mpl_backend()
    fig_dir, data_dir = setup_paths()

    wavelengths = np.linspace(2.0, 25.0, 300)
    positions = design_log_periodic_array(min_len_um=1.0, max_len_um=200.0, tau=1.2, count=9)
    gains = np.ones_like(positions)
    pattern_out = compute_beam_pattern(wavelengths, positions, gains)
    g = array_gain(pattern_out['pattern'])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pattern_out['wavelengths_um'], pattern_out['pattern'], label=f"Normalized pattern (gain={g:.2f})")
    ax.set_xlabel("Wavelength (μm)")
    ax.set_ylabel("Normalized power")
    ax.set_title("Sensilla Array Directionality")
    ax.grid(True, alpha=0.3)
    ax.legend()

    out_png = os.path.join(fig_dir, "sensilla_array_beam_patterns.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    write_caption(os.path.join(fig_dir, "sensilla_array_beam_patterns.caption.txt"), essential_caption)

    np.savez(
        os.path.join(data_dir, "sensilla_array.npz"),
        wavelengths_um=pattern_out['wavelengths_um'],
        pattern=pattern_out['pattern'],
        positions_um=positions,
        array_gain=g,
    )

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
