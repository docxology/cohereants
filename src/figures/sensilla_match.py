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

def generate_sensilla_wavelength_matching(figure_dir: str, data_dir: str) -> str:
    """Generate source-bounded sensilla dimensions vs modeled wavelength matching."""
    from src.sensilla import analyze_sensilla_dimensions
    from src.visualization import set_plot_style, get_colorblind_palette

    set_plot_style('science')

    sample_classes = np.array([sample[0] for sample in SENSILLA_SAMPLES])
    lengths = np.array([sample[1] for sample in SENSILLA_SAMPLES], dtype=float)
    diameters = np.array([sample[2] for sample in SENSILLA_SAMPLES], dtype=float)
    analysis = analyze_sensilla_dimensions(lengths, diameters)

    colors = get_colorblind_palette(6)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    class_names = list(dict.fromkeys(sample_classes.tolist()))
    class_markers = {"coeloconica": "o", "basiconica": "s", "trichodea": "^"}
    for i, class_name in enumerate(class_names):
        mask = sample_classes == class_name
        ax1.scatter(
            diameters[mask],
            lengths[mask],
            s=150,
            alpha=0.9,
            color=colors[i],
            edgecolors='black',
            linewidth=1.5,
            marker=class_markers.get(class_name, "o"),
            label=class_name,
        )

    z = np.polyfit(diameters, lengths, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(min(diameters), max(diameters), 100)
    r_squared = float(np.corrcoef(diameters, lengths)[0, 1] ** 2)
    ax1.plot(
        x_trend,
        p(x_trend),
        '--',
        color='black',
        linewidth=2,
        alpha=0.7,
        label=f"sample trend, R²={r_squared:.2f}",
    )

    ax1.set_xlabel('Diameter (μm)', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Length (μm)', fontweight='bold', fontsize=14)
    ax1.set_title('Representative Sensilla Dimensions\nInput Ranges for Antenna-Style Model',
                 fontweight='bold', fontsize=15, pad=15)
    ax1.grid(True, alpha=0.4, linewidth=1.0)
    ax1.set_xlim(0, 7)
    ax1.set_ylim(0, 165)
    ax1.legend(fontsize=11, framealpha=0.9)

    quarter_data = analysis['optimal_wavelengths_quarter']
    half_data = analysis['optimal_wavelengths_half']

    def in_any_window(values: np.ndarray) -> np.ndarray:
        mask = np.zeros_like(values, dtype=bool)
        for start, end, _, _ in IR_WINDOWS:
            mask |= (values >= start) & (values <= end)
        return mask

    quarter_overlap = in_any_window(quarter_data)
    half_overlap = in_any_window(half_data)

    for i, (start, end, label, _) in enumerate(IR_WINDOWS):
        ax2.axvspan(start, end, color=colors[(i + 1) % len(colors)], alpha=0.18)
        ax2.text((start + end) / 2, 1.38, label, ha='center', va='center', fontsize=9, rotation=90)

    y_quarter = np.full_like(quarter_data, 0.35, dtype=float)
    y_half = np.full_like(half_data, 0.95, dtype=float)
    ax2.scatter(
        quarter_data,
        y_quarter,
        s=120,
        color=np.where(quarter_overlap, colors[2], '#bbbbbb'),
        edgecolors='black',
        linewidth=1,
        label='quarter-wave estimate',
    )
    ax2.scatter(
        half_data,
        y_half,
        s=120,
        marker='D',
        color=np.where(half_overlap, colors[3], '#dddddd'),
        edgecolors='black',
        linewidth=1,
        label='half-wave estimate',
    )
    for wl, label in zip(quarter_data, sample_classes):
        ax2.annotate(label[:4], (wl, 0.35), xytext=(0, -18), textcoords='offset points',
                     ha='center', fontsize=8)
    for wl, label in zip(half_data, sample_classes):
        ax2.annotate(label[:4], (wl, 0.95), xytext=(0, 12), textcoords='offset points',
                     ha='center', fontsize=8)

    ax2.set_xscale('log')
    ax2.set_xlim(2, 700)
    ax2.set_ylim(0, 1.55)
    ax2.set_yticks([0.35, 0.95])
    ax2.set_yticklabels(['quarter λ', 'half λ'])
    ax2.set_xlabel('Modeled Wavelength (μm, log scale)', fontweight='bold', fontsize=14)
    ax2.set_title('Modeled Resonance Estimates vs Atmospheric Windows',
                 fontweight='bold', fontsize=15, pad=15)
    ax2.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax2.grid(True, alpha=0.4, linewidth=1.0)

    stats_text = (
        f"n={len(lengths)} representative inputs\n"
        f"quarter-window overlap: {int(np.sum(quarter_overlap))}/{len(quarter_data)}\n"
        f"half-window overlap: {int(np.sum(half_overlap))}/{len(half_data)}\n"
        f"quarter mean: {np.mean(quarter_data):.1f} μm\n"
        f"half mean: {np.mean(half_data):.1f} μm"
    )
    ax2.text(0.02, 0.08, stats_text, transform=ax2.transAxes,
             fontsize=10, verticalalignment='bottom',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
    add_panel_letter(ax1, "A")
    add_panel_letter(ax2, "B")
    add_source_badge(ax1, "Source: Literature morphometry inputs")
    add_source_badge(ax2, "Source: Model resonance estimates")

    plt.tight_layout()

    figure_path = Path(figure_dir) / "sensilla_wavelength_matching.png"
    fig.savefig(figure_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    caption = f"""Sensilla wavelength-matching analysis using representative morphometric inputs.

Methodology: Computed with src.sensilla.analyze_sensilla_dimensions() on representative coeloconica, basiconica,
and trichodea length/diameter inputs. Quarter- and half-wave estimates are model probes, not measured insect IR
receptor tuning curves.

Model summary:
• Input length range: {np.min(lengths):.1f}-{np.max(lengths):.1f} μm; diameter range: {np.min(diameters):.1f}-{np.max(diameters):.1f} μm.
• Quarter-wave mean: {np.mean(quarter_data):.1f} μm; overlap with modeled atmospheric windows: {int(np.sum(quarter_overlap))}/{len(quarter_data)}.
• Half-wave mean: {np.mean(half_data):.1f} μm; overlap with modeled atmospheric windows: {int(np.sum(half_overlap))}/{len(half_data)}.
• The broad spread shows why wavelength matching is a falsifiable constraint rather than a proof of IR olfaction.

Literature anchors: ant sensilla morphometrics and taxonomy from Liu et al. 2021; thermo-sensitive sensilla from
Ruchty et al. 2009; biomimetic IR-receptor modeling from Siebke et al. 2014."""

    save_figure_bundle(
        figure_path,
        caption,
        label="fig:sensilla_wavelength_matching",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES["fig:sensilla_wavelength_matching"],
        alt_text=FIGURE_ALT_TEXT["fig:sensilla_wavelength_matching"],
        npz_path=Path(data_dir) / "sensilla_data.npz",
        npz_payload={
            "lengths": lengths,
            "diameters": diameters,
            "sample_classes": sample_classes,
            "quarter_wavelengths": analysis['optimal_wavelengths_quarter'],
            "half_wavelengths": analysis['optimal_wavelengths_half'],
            "quarter_window_overlap": quarter_overlap,
            "half_window_overlap": half_overlap,
        },
    )
    return str(figure_path)


