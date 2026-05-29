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

def generate_response_time_comparison(figure_dir: str, data_dir: str) -> str:
    """Generate response-time constraint map from fixture-backed core calculations."""
    PlotStyler("science")
    modalities, response_times, source_status, is_model_target, improvement_factors = build_response_time_series()
    colors = get_colorblind_palette(len(modalities))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    bar_colors = [colors[i % len(colors)] for i in range(len(modalities))]
    bars = ax1.bar(modalities, response_times, color=bar_colors, alpha=0.9, edgecolor='black', linewidth=1.5)
    for bar, model_only in zip(bars, is_model_target):
        if model_only:
            bar.set_hatch('//')

    for bar, latency, status in zip(bars, response_times, source_status):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.28, f'{latency:.2g} ms',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
        ax1.text(bar.get_x() + bar.get_width() / 2., 0.15, status, rotation=90,
                 ha='center', va='bottom', fontsize=8,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

    ax1.set_ylabel('Response Time (ms)', fontweight='bold', fontsize=14)
    ax1.set_title('Response-Time Constraint Map\nObserved Anchors vs Model Target', fontweight='bold', fontsize=15, pad=15)
    ax1.grid(True, alpha=0.4, axis='y', linewidth=1.0)
    ax1.set_ylim(0, max(response_times) * 1.3)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=12, fontweight='bold')
    add_panel_letter(ax1, "A")
    add_source_badge(ax1, "Source: Literature anchors + model target")

    x_positions = np.arange(len(modalities))
    bars2 = ax2.bar(x_positions, response_times, color=bar_colors, alpha=0.9, edgecolor='black', linewidth=1.5)
    for bar, model_only in zip(bars2, is_model_target):
        if model_only:
            bar.set_hatch('//')
    ax2.set_yscale('log')
    ax2.set_ylabel('Response Time (ms, log scale)', fontweight='bold', fontsize=14)
    ax2.set_title('Log-Scale Response Time Comparison\nHighlighting Dynamic Range', fontweight='bold', fontsize=15, pad=15)
    for i, (latency, color) in enumerate(zip(response_times, bar_colors)):
        label_y = latency * 1.2 if latency < 8 else latency * 0.8
        label_va = 'bottom' if latency < 8 else 'top'
        ax2.text(i, label_y, f'{latency:.2g} ms', ha='center', va=label_va,
                 fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.8))
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(modalities, rotation=45, ha='right', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.4, which='both', linewidth=1.0)
    for t in (0.1, 1, 10):
        ax2.axhline(y=t, color='red', linestyle='--', alpha=0.7, linewidth=1)
    add_panel_letter(ax2, "B")

    plt.tight_layout()
    figure_path = Path(figure_dir) / "response_time_comparison.png"
    fig.savefig(figure_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    imp_low = float(np.min(improvement_factors))
    imp_high = float(np.max(improvement_factors))
    caption = f"""Response-time constraint map for evaluating any proposed infrared olfactory stage.

Methodology: Built via src.viz.figure_helpers.build_response_time_series() using calculate_response_time_improvement()
on slow-comparator, ORN-anchor, and model-target latencies. Hatched bars are model targets, not measurements.

Interpretation:
• Insect ORN responses can already occur on a few-millisecond scale.
• Visual and auditory benchmarks show faster channels exist but do not prove IR olfaction.
• Model improvement factors span {imp_low:.1f}–{imp_high:.1f}× relative to slow-comparator terms.
• Any future experiment should report stimulus onset, radiant/chemical control, and latency separately.

Literature anchors: rapid insect ORN timing from Egea-Weiss et al. 2018 and Gorur-Shandilya et al. 2017; thermal/IR
behavioral context from Chandel et al. 2024."""

    save_figure_bundle(
        figure_path,
        caption,
        label="fig:response_time_comparison",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES["fig:response_time_comparison"],
        alt_text=FIGURE_ALT_TEXT["fig:response_time_comparison"],
        npz_path=Path(data_dir) / "response_time_comparison.npz",
        npz_payload={
            "modalities": np.array(modalities),
            "response_times": response_times,
            "source_status": np.array(source_status),
            "is_model_target": is_model_target,
            "improvement_factors": improvement_factors,
        },
    )
    return str(figure_path)


