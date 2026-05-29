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

def generate_atmospheric_transmission_plot(figure_dir: str, data_dir: str) -> str:
    """Generate atmospheric transmission plot with explicit model boundaries."""
    from src.core import calculate_atmospheric_transmission

    PlotStyler("science")
    colors = get_colorblind_palette(5)

    wavelengths = np.linspace(1, 30, 1000)
    transmission = calculate_atmospheric_transmission(wavelengths)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(
        wavelengths,
        transmission,
        color=colors[0],
        linewidth=3,
        drawstyle="steps-mid",
        label='Coarse transmission model',
    )

    for i, (start, end, label, confidence) in enumerate(IR_WINDOWS):
        color = colors[(i + 1) % len(colors)]
        ax.axvspan(start, end, alpha=0.24, color=color, linewidth=0)
        center = (start + end) / 2
        window_mask = (wavelengths >= start) & (wavelengths <= end)
        window_mean = float(np.mean(transmission[window_mask]))
        ax.plot(center, window_mean, 'o', color=color, markersize=9, markeredgecolor='black')
        ax.annotate(
            f"{label}\nmean T={window_mean:.2f}\n{confidence}",
            (center, window_mean),
            xytext=(0, 26),
            textcoords='offset points',
            ha='center',
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.92),
        )

    bio_start, bio_end = BIOMIMETIC_IR_BAND_UM
    ax.axvspan(bio_start, bio_end, alpha=0.15, color=colors[4], linewidth=1.5, linestyle='--')
    ax.text(
        (bio_start + bio_end) / 2,
        1.02,
        f"Biomimetic band\n{bio_start}–{bio_end} µm",
        ha='center',
        fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9),
    )
    add_panel_letter(ax, "A")
    add_source_badge(ax, "Source: Model fixture (src.core)")

    ax.set_xlabel('Wavelength (μm)', fontweight='bold', fontsize=14)
    ax.set_ylabel('Atmospheric Transmission', fontweight='bold', fontsize=14)
    ax.set_title('Atmospheric Infrared Windows Used by the Model',
                 fontweight='bold', fontsize=16, pad=20)

    ax.grid(True, alpha=0.4, linewidth=1.0, color='gray')
    ax.set_ylim(0, 1.1)
    ax.set_xlim(1, 30)
    ax.legend(loc='lower right', fontsize=12, framealpha=0.9)

    def wavelength_to_wavenumber(x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        return 10000.0 / np.maximum(x, 1e-9)

    def wavenumber_to_wavelength(x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        return 10000.0 / np.maximum(x, 1e-9)

    secax = ax.secondary_xaxis('top', functions=(wavelength_to_wavenumber, wavenumber_to_wavelength))
    secax.set_xlabel('Wavenumber (cm⁻¹)', fontweight='bold', fontsize=12)

    ax.text(
        0.02,
        0.04,
        'Model scope: window-level transmission from src.core; use HITRAN-style\n'
        'line data for quantitative range claims. Figure marks physical opportunity,\n'
        'not demonstrated insect communication distance.',
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9),
    )

    figure_path = Path(figure_dir) / "atmospheric_transmission.png"
    fig.savefig(figure_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    caption = """Atmospheric transmission window analysis for the CohereAnts model.

Methodology: Computed using src.core.calculate_atmospheric_transmission() across 1-30 μm. The function is a coarse
window-level model, not a line-by-line radiative-transfer calculation.

Interpretation:
• 2-5 μm and 8-14 μm are the principal modeled transmission opportunities.
• 17-25 μm is retained as a lower-confidence sensitivity band and should not carry strong range claims.
• Window overlap is a necessary physical condition for any IR semiochemical hypothesis, not evidence that insects use
  these wavelengths for distant chemical communication.

Literature anchors: HITRAN2020 atmospheric line data; insect IR and thermal-receptor literature cited in the manuscript."""

    figure_path = Path(figure_dir) / "atmospheric_transmission.png"
    save_figure_bundle(
        figure_path,
        caption,
        label="fig:atmospheric_transmission",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES["fig:atmospheric_transmission"],
        alt_text=FIGURE_ALT_TEXT["fig:atmospheric_transmission"],
        npz_path=Path(data_dir) / "atmospheric_transmission.npz",
        npz_payload={
            "wavelengths": wavelengths,
            "transmission": transmission,
            "ir_windows": np.array([[start, end] for start, end, _, _ in IR_WINDOWS]),
            "biomimetic_band_um": np.array(BIOMIMETIC_IR_BAND_UM),
        },
    )
    return str(figure_path)


