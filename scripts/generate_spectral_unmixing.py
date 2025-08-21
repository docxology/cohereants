#!/usr/bin/env python3
"""Appendix E script: Spectral Unmixing using src.case_studies."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption
import numpy as np
import matplotlib.pyplot as plt
ensure_src_on_path()
from src.case_studies import (
    nmf_unmix,
    lda_baseline,
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
    w = np.linspace(2, 5, 300)
    comp1 = np.exp(-((w - 3.0) / 0.2) ** 2)
    comp2 = 0.7 * np.exp(-((w - 4.0) / 0.25) ** 2)
    mix = comp1 + comp2 + 0.05 * rng.standard_normal(w.shape)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(w, mix, label="Mixture")
    ax.plot(w, comp1, '--', label="Comp 1")
    ax.plot(w, comp2, '--', label="Comp 2")
    ax.set_xlabel("Wavelength (μm)")
    ax.set_ylabel("Absorbance (a.u.)")
    ax.set_title("Spectral unmixing and baseline classification")
    ax.legend()
    ax.grid(True, alpha=0.3)

    out_png = os.path.join(fig_dir, "spectral_unmixing_components.png")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    write_caption(os.path.join(fig_dir, "spectral_unmixing_components.caption.txt"), "NMF-unmixed components and reconstruction; simple two-class LDA baseline accuracy.")

    nmf = nmf_unmix(mix.reshape(1, -1), n_components=2, seed=42)
    # Toy LDA on synthetic features
    feats = np.vstack([np.c_[comp1[:100], comp2[:100]], np.c_[comp1[100:200], comp2[100:200]]])
    labs = np.r_[np.zeros(100), np.ones(100)]
    lda = lda_baseline(feats, labs, seed=42)
    np.savez(
        os.path.join(data_dir, "spectral_unmixing.npz"),
        wavelength=w,
        comp1=comp1,
        comp2=comp2,
        mix=mix,
        W=nmf['W'],
        H=nmf['H'],
        lda_train_accuracy=lda['train_accuracy'],
    )

    print(out_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
