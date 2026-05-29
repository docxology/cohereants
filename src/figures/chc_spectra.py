from __future__ import annotations

import os
import time
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from src.figure_artifacts import save_figure_bundle
from src.figure_registry_builder import build_figure_registry
from src.manuscript_fixtures import BIOMIMETIC_IR_BAND_UM, IR_WINDOWS, SENSILLA_SAMPLES
from src.viz.figure_helpers import (
    FIGURE_ALT_TEXT,
    FIGURE_CLAIM_BOUNDARIES,
    add_panel_letter,
    add_source_badge,
    build_chc_fixture_spectrum,
    build_response_time_series,
    empirical_axes_panel_data,
)
from src.viz.styling import PlotStyler, get_colorblind_palette

def generate_chc_spectra_example(figure_dir: str, data_dir: str) -> str:
    """Generate CHC infrared spectrum figure grounded in analyze_chc_spectra()."""
    from src.visualization import set_plot_style, get_colorblind_palette

    set_plot_style('science')
    wavenumbers, intensities, analysis = build_chc_fixture_spectrum()
    colors = get_colorblind_palette(6)

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(wavenumbers, intensities, color=colors[0], linewidth=3, label='CHC fixture spectrum')

    peak_wavenumbers = analysis.get("peak_wavenumbers", np.array([]))
    for i, peak in enumerate(np.asarray(peak_wavenumbers)[:4]):
        idx = int(np.abs(wavenumbers - peak).argmin())
        ax.plot(wavenumbers[idx], intensities[idx], 'o', color=colors[(i + 1) % len(colors)], markersize=10,
                markeredgecolor='black', markeredgewidth=2)
        ax.annotate(f"{int(wavenumbers[idx])} cm⁻¹",
                   (wavenumbers[idx], intensities[idx]), textcoords="offset points", xytext=(0, 15),
                   ha='center', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

    ax.set_xlabel('Wavenumber (cm⁻¹)', fontweight='bold', fontsize=14)
    ax.set_ylabel('Absorbance (a.u.)', fontweight='bold', fontsize=14)
    ax.set_title('CHC Infrared Spectrum Fixture\nAnalyzed via src.spectroscopy.analyze_chc_spectra()',
                fontweight='bold', fontsize=16, pad=20)

    for start, end, color, label in [
        (2800, 3000, colors[1], 'C-H Stretch'),
        (1400, 1500, colors[2], 'C-H Bend'),
    ]:
        ax.axvspan(start, end, alpha=0.25, color=color, linewidth=0)
        ax.text((start + end) / 2, max(intensities) * 0.9, label, ha='center', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

    ax.grid(True, alpha=0.4, linewidth=1.0)
    ax.set_xlim(1200, 3400)
    ax.set_ylim(0, max(intensities) * 1.1)
    add_panel_letter(ax, "A")
    add_source_badge(ax, "Source: Model fixture + analyze_chc_spectra()")
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)

    figure_path = Path(figure_dir) / "chc_spectra_example.png"
    fig.savefig(figure_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    n_peaks = len(peak_wavenumbers)
    caption = f"""Cuticular-hydrocarbon (CHC) infrared spectrum fixture analyzed with src.spectroscopy.analyze_chc_spectra().

Methodology: Deterministic synthetic spectrum passed through the production CHC analyzer ({n_peaks} detected peaks).
The output is a reproducible model fixture for manuscript figures, not a measured ant spectrum.

Bounded interpretation:
• CHC molecules form the primary component of insect cuticles
• FTIR/ATR spectra can classify insect cuticular chemistry in empirical studies
• The figure supports spectral feature extraction and hypothesis generation
• It does not establish that insects directly read these IR absorbance bands as olfactory signals

Literature anchors: CHC biology from Blomquist and Ginzel 2021; ATR-FTIR classification evidence from Durak et al. 2022."""

    save_figure_bundle(
        figure_path,
        caption,
        label="fig:chc_spectra_example",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES["fig:chc_spectra_example"],
        alt_text=FIGURE_ALT_TEXT["fig:chc_spectra_example"],
        npz_path=Path(data_dir) / "chc_spectra.npz",
        npz_payload={
            "wavenumbers": wavenumbers,
            "intensities": intensities,
            "peak_wavenumbers": np.asarray(peak_wavenumbers),
            "ch_stretch_region": np.array([2800, 3000]),
            "ch_bend_region": np.array([1400, 1500]),
        },
    )
    return str(figure_path)


