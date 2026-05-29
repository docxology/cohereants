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

def generate_empirical_ir_axes(figure_dir: str, data_dir: str) -> str:
    """Generate three-axis empirical IR evidence schematic for §07."""
    from src.visualization import set_plot_style, get_colorblind_palette

    set_plot_style('science')
    colors = get_colorblind_palette(3)
    panel_data = empirical_axes_panel_data()

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    fig.suptitle(
        'Empirical IR Biology: Three Functional Axes (Literature Synthesis)',
        fontsize=16,
        fontweight='bold',
    )

    active = panel_data["active"]
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title(active["title"], fontweight='bold', fontsize=13)
    band = active["band_um"]
    thresh = active["threshold_mw_cm2"]
    ax.text(
        5,
        8.2,
        "Taxa: " + ", ".join(active["taxa"]),
        ha='center',
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[0], alpha=0.35),
    )
    ax.axhspan(3, 5, xmin=0.1, xmax=0.9, color=colors[0], alpha=0.25)
    ax.text(5, 4.5, f"Band {band[0]}–{band[1]} µm", ha='center', fontsize=11, fontweight='bold')
    ax.text(5, 3.2, f"Threshold {thresh[0]}–{thresh[1]} mW/cm²", ha='center', fontsize=10)
    ax.text(5, 1.5, f"Fire blackbody peak ~{active['peak_um']} µm", ha='center', fontsize=9)
    add_panel_letter(ax, "A")
    add_source_badge(ax, "Source: Literature synthesis")

    passive = panel_data["passive"]
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title(passive["title"], fontweight='bold', fontsize=13)
    ax.text(
        5,
        8.2,
        "Taxa: " + ", ".join(passive["taxa"]),
        ha='center',
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[1], alpha=0.35),
    )
    ax.text(5, 5.5, "Cuticle emissivity / thermosensory\nwarm-cell combinatorial coding", ha='center', fontsize=10)
    ax.text(5, 2.5, f"Skin-temperature peak ~{passive['peak_um']} µm", ha='center', fontsize=10)
    add_panel_letter(ax, "B")
    add_source_badge(ax, "Source: Literature synthesis")

    applied = panel_data["applied"]
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title(applied["title"], fontweight='bold', fontsize=13)
    ax.text(
        5,
        8.2,
        "Methods: " + ", ".join(applied["taxa"]),
        ha='center',
        fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[2], alpha=0.35),
    )
    ax.text(5, 5.0, "Human-applied IR spectroscopy\nand remote monitoring", ha='center', fontsize=10)
    ax.text(5, 2.0, "Species discrimination ≠\nin vivo semiochemical IR sensing", ha='center', fontsize=10)
    add_panel_letter(ax, "C")
    add_source_badge(ax, "Source: Applied IR literature")

    plt.tight_layout(rect=(0, 0, 1, 0.92))
    out_path = Path(figure_dir) / "empirical_ir_axes.png"
    fig.savefig(out_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    caption = """Three-axis schematic of insect IR biology synthesized from §07 empirical studies.

Methodology: Panel layout derived from manuscript fixtures (biomimetic band, threshold range, blackbody peaks) and
the comparative taxon table. This is a literature synthesis figure, not new empirical measurement.

Interpretation:
• Active photomechanic organs anchor biomimetic sensor bands but do not prove semiochemical IR olfaction.
• Passive cuticle and thermosensory pathways shape background IR and host-finding context.
• Applied spectroscopy validates discriminative IR structure in insect bodies without demonstrating in vivo IR olfaction."""

    save_figure_bundle(
        out_path,
        caption,
        label="fig:empirical_ir_axes",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES["fig:empirical_ir_axes"],
        alt_text=FIGURE_ALT_TEXT["fig:empirical_ir_axes"],
    )
    return str(out_path)


