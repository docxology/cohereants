"""Integrated analysis figure builders for CohereAnts."""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.config import set_random_seed
from src.figure_artifacts import save_figure_bundle
from src.figure_registry_builder import build_figure_registry
from src.integrated_analysis import IntegratedAnalyzer
from src.integrated_figures_panels import (
    create_composite_summary_figure,
    create_cross_domain_synthesis_figure,
    create_information_analysis_figure,
    create_metamaterial_properties_figure,
    create_system_performance_figure,
)
from src.manuscript_fixtures import default_olfactory_fixtures
from src.visualization import AdvancedVisualizer, get_colorblind_palette, set_plot_style
from src.viz.figure_helpers import FIGURE_ALT_TEXT, FIGURE_CLAIM_BOUNDARIES

__all__ = [
    "create_comprehensive_analysis_figures",
    "create_information_analysis_figure",
    "create_metamaterial_properties_figure",
    "create_system_performance_figure",
    "create_cross_domain_synthesis_figure",
    "create_composite_summary_figure",
    "generate_integrated_analysis_figures",
]


def _sample_analysis_inputs() -> tuple[dict, dict, dict]:
    return default_olfactory_fixtures()


def create_comprehensive_analysis_figures():
    """
    Create comprehensive analysis figures for the manuscript.

    Returns:
        Dictionary of matplotlib figures
    """
    print("Creating comprehensive integrated analysis figures...")

    integrated_analyzer = IntegratedAnalyzer()
    set_random_seed(42)
    set_plot_style("science")
    get_colorblind_palette(8)

    odorant_properties, receptor_properties, environmental_conditions = _sample_analysis_inputs()

    analysis_results = integrated_analyzer.analyze_olfactory_system(
        odorant_properties, receptor_properties, environmental_conditions
    )

    performance_metrics = integrated_analyzer.calculate_system_performance_metrics(analysis_results)

    figures = {}

    figures["information_analysis"] = create_information_analysis_figure(analysis_results, performance_metrics)
    figures["metamaterial_properties"] = create_metamaterial_properties_figure(analysis_results)
    figures["system_performance"] = create_system_performance_figure(performance_metrics)
    figures["cross_domain_synthesis"] = create_cross_domain_synthesis_figure(analysis_results)

    return figures


_INTEGRATED_LABELS = {
    "information_analysis": "fig:integrated_info",
    "metamaterial_properties": "fig:integrated_metamaterial",
    "cross_domain_synthesis": "fig:integrated_classification",
}

_INTEGRATED_CAPTIONS = {
    "information_analysis": (
        "Integrated information analysis combining Fermi estimation with neural encoding models. "
        "Bounds sensor information throughput; does not establish biological IR olfaction."
    ),
    "metamaterial_properties": (
        "Meta-material dielectric and plasmonic response sweep for biomimetic IR sensor design. "
        "Model output only."
    ),
    "system_performance": (
        "System performance metrics across information, material, and efficiency domains. "
        "Engineering bounds for protocol design."
    ),
    "cross_domain_synthesis": (
        "Cross-domain synthesis linking atmospheric, sensor, and information-theory assumptions. "
        "Panel D shows unitless model sensitivity demo values, not predictive accuracy on live specimens."
    ),
}


def generate_integrated_analysis_figures(project_root: Path | None = None) -> list[Path]:
    """Generate integrated analysis figures, captions, data, and refresh registry."""
    os.environ.setdefault("MPLBACKEND", "Agg")
    root = project_root or Path(__file__).resolve().parent.parent
    figure_dir = root / "output" / "figures"
    data_dir = root / "output" / "data"
    figure_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    try:
        set_random_seed(42)
        set_plot_style("science")
    except Exception:
        np.random.seed(42)

    figures = create_comprehensive_analysis_figures()
    visualizer = AdvancedVisualizer(style="science")
    paths: list[Path] = []

    for name, fig in figures.items():
        filename = figure_dir / f"integrated_analysis_{name}.png"
        visualizer.save_figure(fig, str(filename), dpi=600, enhance_for_accessibility=True)
        paths.append(filename)
        label = _INTEGRATED_LABELS.get(name, f"fig:integrated_{name}")
        caption_body = _INTEGRATED_CAPTIONS.get(name, name)
        save_figure_bundle(
            filename,
            caption_body,
            label=label,
            claim_boundary=FIGURE_CLAIM_BOUNDARIES.get(label, FIGURE_CLAIM_BOUNDARIES["fig:integrated_info"]),
            alt_text=FIGURE_ALT_TEXT.get(label, caption_body.split(".")[0]),
        )

    plt.close("all")

    integrated_analyzer = IntegratedAnalyzer()
    odorant_properties, receptor_properties, environmental_conditions = _sample_analysis_inputs()
    analysis_results = integrated_analyzer.analyze_olfactory_system(
        odorant_properties, receptor_properties, environmental_conditions
    )
    performance_metrics = integrated_analyzer.calculate_system_performance_metrics(analysis_results)
    report = integrated_analyzer.generate_comprehensive_report(analysis_results)
    (figure_dir / "integrated_analysis_report.txt").write_text(report, encoding="utf-8")

    dielec = analysis_results["metamaterial_analysis"]["dielectric"]
    plasm = analysis_results["metamaterial_analysis"]["plasmonic"]
    info_cap = analysis_results["metamaterial_analysis"]["information_capacity"]
    np.savez(
        data_dir / "integrated_analysis.npz",
        frequency=dielec.get("frequency"),
        epsilon_real=dielec.get("epsilon_real"),
        epsilon_imag=dielec.get("epsilon_imag"),
        refractive_index=dielec.get("refractive_index"),
        absorption_coefficient=dielec.get("absorption_coefficient"),
        plasmonic_resonance_frequency_hz=plasm.get("resonance_frequency_hz"),
        plasmonic_resonance_wavelength_m=plasm.get("resonance_wavelength_m"),
        plasmonic_quality_factor=plasm.get("quality_factor"),
        plasmonic_field_enhancement=plasm.get("field_enhancement"),
        channel_capacity_bits_per_sec=info_cap.get("channel_capacity_bits_per_sec"),
        info_signal_to_noise_ratio=info_cap.get("signal_to_noise_ratio"),
        information_density_bits_per_joule_meter=info_cap.get("information_density_bits_per_joule_meter"),
        quantum_limit_bits_per_sec=info_cap.get("quantum_limit_bits_per_sec"),
        information_processing_score=performance_metrics["information_processing_score"],
        material_performance_score=performance_metrics["material_performance_score"],
        system_efficiency=performance_metrics["system_efficiency"],
        total_information_content_bits=performance_metrics["total_information_content_bits"],
        receptor_specificity_index=performance_metrics["receptor_specificity_index"],
        neural_encoding_efficiency=performance_metrics["neural_encoding_efficiency"],
        average_refractive_index=performance_metrics["average_refractive_index"],
        plasmonic_quality_factor_pm=performance_metrics["plasmonic_quality_factor"],
        information_capacity_bits_per_sec_pm=performance_metrics["information_capacity_bits_per_sec"],
    )

    summary_fig = create_composite_summary_figure(analysis_results, performance_metrics)
    summary_path = figure_dir / "integrated_analysis_summary.png"
    visualizer.save_figure(summary_fig, str(summary_path), dpi=600, enhance_for_accessibility=True)
    summary_caption = (
        "Composite summary of dielectric response and normalized performance metrics for sensor bounds."
    )
    save_figure_bundle(
        summary_path,
        summary_caption,
        label="fig:integrated_summary",
        claim_boundary=FIGURE_CLAIM_BOUNDARIES.get("fig:integrated_summary", FIGURE_CLAIM_BOUNDARIES["fig:integrated_info"]),
        alt_text=FIGURE_ALT_TEXT.get("fig:integrated_summary", summary_caption),
    )
    plt.close(summary_fig)
    paths.append(summary_path)

    build_figure_registry(root)
    return paths
