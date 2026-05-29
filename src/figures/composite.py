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

def generate_composite_multipanel(figure_dir: str) -> str:
    """Generate composite evidence map across physics, morphology, spectroscopy, and evidence status."""
    from src.core import calculate_atmospheric_transmission
    from src.sensilla import analyze_sensilla_dimensions

    styler = PlotStyler("science")
    colors = get_colorblind_palette(6)

    wavelengths = np.linspace(1, 30, 400)
    transmission = calculate_atmospheric_transmission(wavelengths)

    lengths = np.array([sample[1] for sample in SENSILLA_SAMPLES], dtype=float)
    diameters = np.array([sample[2] for sample in SENSILLA_SAMPLES], dtype=float)
    sens = analyze_sensilla_dimensions(lengths.tolist(), diameters.tolist())
    quarter = sens['optimal_wavelengths_quarter']

    wavenumbers, intensities, _chc_analysis = build_chc_fixture_spectrum()

    fig, axs = styler.create_figure_grid(2, 2, figsize=(15, 11))
    fig.suptitle('CohereAnts Evidence Map: What Is Modeled, Anchored, and Still Untested',
                 fontsize=17, fontweight='bold')

    ax = axs[0, 0]
    ax.plot(wavelengths, transmission, color=colors[0], linewidth=2.8, drawstyle='steps-mid')
    for i, (start, end, label, _) in enumerate(IR_WINDOWS):
        ax.axvspan(start, end, color=colors[(i + 1) % len(colors)], alpha=0.2)
        ax.text((start + end) / 2, 0.08, label, rotation=90, ha='center', va='bottom', fontsize=9)
    ax.set_title('A. Atmospheric opportunity')
    ax.set_xlabel('Wavelength (μm)')
    ax.set_ylabel('Transmission')
    ax.set_xlim(1, 30)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.35)

    ax = axs[0, 1]
    ax.scatter(quarter, lengths, s=115, color=colors[2], edgecolor='black', label='quarter-wave estimate')
    ax.set_xscale('log')
    for start, end, _, _ in IR_WINDOWS:
        ax.axvspan(start, end, color='gray', alpha=0.12)
    ax.set_title('B. Geometry constraint')
    ax.set_xlabel('Modeled quarter-wave wavelength (μm)')
    ax.set_ylabel('Sensillum length (μm)')
    ax.grid(True, alpha=0.35, which='both')
    ax.legend(framealpha=0.9)

    ax = axs[1, 0]
    ax.plot(wavenumbers, intensities, color=colors[3], linewidth=2.8)
    for start, end, label in [
        (1400, 1500, 'C-H bend'),
        (2800, 3000, 'C-H stretch'),
    ]:
        ax.axvspan(start, end, color=colors[1], alpha=0.2)
        ax.text((start + end) / 2, max(intensities) * 0.82, label, ha='center', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))
    ax.set_title('C. Spectral feature extraction')
    ax.set_xlabel('Wavenumber (cm⁻¹)')
    ax.set_ylabel('Absorbance (a.u.)')
    ax.set_xlim(1200, 3400)
    ax.grid(True, alpha=0.35)

    ax = axs[1, 1]
    evidence_labels = ['CHC spectra classify\ncuticular chemistry',
                       'Thermal/IR receptors\nexist in insects',
                       'Fast ORN responses\nare documented',
                       'Direct IR olfaction\nfor semiochemicals']
    evidence_scores = np.array([3, 3, 3, 1], dtype=float)
    evidence_colors = [colors[2], colors[2], colors[2], colors[5]]
    ax.barh(evidence_labels, evidence_scores, color=evidence_colors, edgecolor='black')
    ax.set_xlim(0, 3.4)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['open test', 'supporting analogy', 'direct anchor'])
    ax.set_title('D. Evidence status')
    ax.grid(True, axis='x', alpha=0.35)
    for i, score in enumerate(evidence_scores):
        text = 'untested in this system' if score == 1 else 'literature anchored'
        if score >= 3:
            ax.text(score - 0.08, i, text, va='center', ha='right', fontsize=9, color='white')
        else:
            ax.text(score + 0.08, i, text, va='center', ha='left', fontsize=9)

    for letter, panel in zip("ABCD", axs.flat):
        add_panel_letter(panel, letter)

    plt.tight_layout(rect=(0, 0, 1, 0.96))

    out_path = Path(figure_dir) / 'composite_cross_domain_overview.png'
    fig.savefig(out_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    caption = f"""Cross-domain evidence map for the CohereAnts IR/semiochemical hypothesis.

Methodology: Four panels combine:
• Atmospheric transmission modeling (src.core.calculate_atmospheric_transmission)
• Representative sensilla wavelength estimates (src.sensilla.analyze_sensilla_dimensions)
• CHC fixture spectrum analyzed via analyze_chc_spectra()
• An evidence ladder separating direct anchors from open experimental tests

Model summary:
• Atmospheric model windows: 2-5 μm, 8-14 μm, and lower-confidence 17-25 μm.
• Representative quarter-wave estimate mean: {np.mean(quarter):.1f} μm.
• CHC bands shown: C-H bend near 1465 cm⁻¹ and C-H stretch near 2800-3000 cm⁻¹.

Interpretation: The figure is a hypothesis map. It shows physical and biological constraints that make the question
testable, while marking direct semiochemical IR olfaction as unproven."""

    save_figure_bundle(
        out_path,
        caption,
        label="fig:composite_cross_domain_overview",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES["fig:composite_cross_domain_overview"],
        alt_text=FIGURE_ALT_TEXT["fig:composite_cross_domain_overview"],
    )
    return str(out_path)


