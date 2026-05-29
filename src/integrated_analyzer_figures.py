"""IntegratedAnalyzer figure builders (matplotlib only)."""
from __future__ import annotations

from typing import Dict, Optional

import matplotlib.pyplot as plt
import numpy as np

from src.viz.panels import plot_receptor_specificity_curve
from src.viz.styling import PlotStyler, get_colorblind_palette
from src.viz.warnings_util import suppress_plot_warnings


def generate_integrated_visualization(analyzer, analysis_results: Optional[Dict] = None):
    """
    Generate comprehensive integrated analysis visualization.

    Args:
        analyzer: IntegratedAnalyzer instance (unused; kept for API symmetry)
        analysis_results: Optional analysis results to visualize

    Returns:
        Matplotlib figure with integrated visualization
    """
    with suppress_plot_warnings():
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle("Integrated Olfactory System Analysis", fontsize=16, fontweight="bold")
        styler = PlotStyler("science")
        colors = get_colorblind_palette(6)

        if analysis_results:
            # Plot 1: Molecular information content
            if "fermi_analysis" in analysis_results and "molecular" in analysis_results["fermi_analysis"]:
                molecular_data = analysis_results["fermi_analysis"]["molecular"]
                labels = ["Translational", "Rotational", "Vibrational"]
                values = [
                    molecular_data.get("translational_bits", 0),
                    molecular_data.get("rotational_bits", 0),
                    molecular_data.get("vibrational_bits", 0),
                ]

                axes[0, 0].bar(labels, values, color=colors[:3])
                styler.format_axes(
                    axes[0, 0],
                    ylabel="Bits",
                    title="Molecular Information Content",
                    legend=False,
                )
                axes[0, 0].tick_params(axis="x", rotation=45)

            # Plot 2: Neural efficiency
            if "fermi_analysis" in analysis_results and "neural" in analysis_results["fermi_analysis"]:
                neural_data = analysis_results["fermi_analysis"]["neural"]
                metrics = ["Encoding Efficiency", "Channel Capacity", "Information Rate"]
                values = [
                    neural_data.get("encoding_efficiency_bits_per_energy", 0),
                    neural_data.get("channel_capacity_bits", 0),
                    neural_data.get("information_rate_bits", 0),
                ]

                axes[0, 1].bar(metrics, values, color=colors[3:6])
                styler.format_axes(
                    axes[0, 1],
                    ylabel="Value",
                    title="Neural Encoding Performance",
                    legend=False,
                )
                axes[0, 1].tick_params(axis="x", rotation=45)

            # Plot 3: Metamaterial properties
            if (
                "metamaterial_analysis" in analysis_results
                and "dielectric" in analysis_results["metamaterial_analysis"]
            ):
                dielectric_data = analysis_results["metamaterial_analysis"]["dielectric"]
                refractive_indices = dielectric_data.get("refractive_index", [])

                if refractive_indices is not None and len(refractive_indices) > 0:
                    axes[1, 0].hist(
                        refractive_indices,
                        bins=10,
                        alpha=0.7,
                        color=colors[0],
                        edgecolor="black",
                    )
                    styler.format_axes(
                        axes[1, 0],
                        xlabel="Refractive Index",
                        ylabel="Frequency",
                        title="Dielectric Refractive Index Distribution",
                        legend=False,
                    )

            # Plot 4: Information capacity
            if (
                "metamaterial_analysis" in analysis_results
                and "information_capacity" in analysis_results["metamaterial_analysis"]
            ):
                info_data = analysis_results["metamaterial_analysis"]["information_capacity"]
                capacity = info_data.get("channel_capacity_bits_per_sec", 0)
                efficiency = info_data.get("spectral_efficiency", 0)

                axes[1, 1].bar(
                    ["Channel Capacity", "Spectral Efficiency"],
                    [capacity, efficiency * 100],
                    color=[colors[1], colors[2]],
                )
                styler.format_axes(
                    axes[1, 1],
                    ylabel="Value",
                    title="Information Capacity Performance",
                    legend=False,
                )
                axes[1, 1].tick_params(axis="x", rotation=45)

        plt.tight_layout()
    return fig


def create_integrated_visualization_figures(analyzer, analysis_results: Dict):
    """
    Create comprehensive visualization figures for the analysis.

    Args:
        analyzer: IntegratedAnalyzer instance
        analysis_results: Output from analyze_olfactory_system

    Returns:
        Dictionary with matplotlib figures
    """
    with suppress_plot_warnings():
        figures = {}
        styler = PlotStyler("science")
        colors = get_colorblind_palette(8)

        # Figure 1: Information content breakdown
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Molecular information breakdown
        fermi = analysis_results["fermi_analysis"]
        molecular_labels = ["Translational", "Rotational", "Vibrational"]
        molecular_values = np.array(
            [
                fermi["molecular"]["translational_bits"],
                fermi["molecular"]["rotational_bits"],
                fermi["molecular"]["vibrational_bits"],
            ],
            dtype=float,
        )

        molecular_values = np.clip(molecular_values, 0.0, None)
        if np.sum(molecular_values) == 0:
            molecular_values = np.ones_like(molecular_values) * 1e-6

        ax1.pie(molecular_values, labels=molecular_labels, autopct="%1.1f%%", colors=colors[:3])
        ax1.set_title("Molecular Information Content Distribution")

        plot_receptor_specificity_curve(ax2, fermi["receptor"], styler=styler, color=colors[0])

        figures["information_breakdown"] = fig1

        # Figure 2: Meta-material properties
        fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 6))

        metamaterial = analysis_results["metamaterial_analysis"]
        frequency_thz = metamaterial["dielectric"]["frequency"] / 1e12

        ax3.plot(
            frequency_thz,
            metamaterial["dielectric"]["epsilon_real"],
            color=colors[0],
            label="Real",
            linewidth=2,
        )
        ax3.plot(
            frequency_thz,
            metamaterial["dielectric"]["epsilon_imag"],
            color=colors[1],
            linestyle="--",
            label="Imaginary",
            linewidth=2,
        )
        styler.format_axes(
            ax3,
            xlabel="Frequency (THz)",
            ylabel="Dielectric Constant",
            title="Dielectric Response vs Frequency",
        )
        ax3.set_xscale("log")

        ax4.plot(frequency_thz, metamaterial["dielectric"]["refractive_index"], color=colors[2], linewidth=2)
        styler.format_axes(
            ax4,
            xlabel="Frequency (THz)",
            ylabel="Refractive Index",
            title="Refractive Index vs Frequency",
            legend=False,
        )
        ax4.set_xscale("log")

        figures["metamaterial_properties"] = fig2

        # Figure 3: System performance overview
        fig3, ax5 = plt.subplots(1, 1, figsize=(10, 6))

        performance_metrics = analyzer.calculate_system_performance_metrics(analysis_results)
        metric_names = ["Info Processing", "Material Performance", "System Efficiency"]
        metric_values = [
            performance_metrics["information_processing_score"],
            performance_metrics["material_performance_score"],
            performance_metrics["system_efficiency"],
        ]

        normalized_values = np.array(metric_values) / np.max(metric_values)

        bars = ax5.bar(metric_names, normalized_values, color=colors[:3], alpha=0.7)
        styler.format_axes(
            ax5,
            ylabel="Normalized Performance Score",
            title="Integrated System Performance Overview",
            legend=False,
        )
        ax5.set_ylim(0, 1.1)

        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax5.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.01,
                f"{value:.2e}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        figures["system_performance"] = fig3

    return figures


def save_integrated_analysis_figures(figures: Dict[str, plt.Figure], output_dir: str = "output/figures"):
    """
    Save all analysis figures to the output directory.

    Args:
        figures: Dictionary of matplotlib figures
        output_dir: Output directory path
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    for name, fig in figures.items():
        filename = f"{output_dir}/integrated_analysis_{name}.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        print(f"Saved figure: {filename}")

    plt.close("all")
