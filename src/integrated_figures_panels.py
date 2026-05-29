"""Panel builders for integrated analysis manuscript figures."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from src.visualization import AdvancedVisualizer, get_colorblind_palette
from src.viz.panels import plot_receptor_specificity_curve
from src.viz.styling import PlotStyler


def create_information_analysis_figure(analysis_results, performance_metrics):
    """
    Create comprehensive information analysis figure.

    Args:
        analysis_results: Results from integrated analysis
        performance_metrics: System performance metrics

    Returns:
        Matplotlib figure
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Comprehensive Information Analysis: Fermi Estimation Framework", fontsize=16, fontweight="bold")
    styler = PlotStyler("science")

    fermi = analysis_results["fermi_analysis"]

    molecular_labels = ["Translational", "Rotational", "Vibrational"]
    molecular_values = [
        fermi["molecular"]["translational_bits"],
        fermi["molecular"]["rotational_bits"],
        fermi["molecular"]["vibrational_bits"],
    ]

    molecular_values = np.array(molecular_values)
    if np.any(molecular_values < 0):
        molecular_values = molecular_values - np.min(molecular_values) + 0.1

    colors = get_colorblind_palette(len(molecular_labels))
    ax1.pie(molecular_values, labels=molecular_labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax1.set_title("Molecular Information Content Distribution", fontweight="bold")

    plot_receptor_specificity_curve(ax2, fermi["receptor"], styler=styler)
    ax2.set_ylim(0.4, 0.9)

    response_amplitudes = np.linspace(0.5, 1.5, 100)
    encoding_efficiency = fermi["neural"]["encoding_efficiency_bits_per_energy"]

    ax3.hist(response_amplitudes, bins=20, alpha=0.7, color="green", edgecolor="black")
    ax3.axvline(
        np.mean(response_amplitudes),
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {np.mean(response_amplitudes):.2f}",
    )
    ax3.set_xlabel("Response Amplitude", fontweight="bold")
    ax3.set_ylabel("Frequency", fontweight="bold")
    ax3.set_title(
        f"Neural Response Distribution\n(Encoding Efficiency: {encoding_efficiency:.4f} bits/energy)",
        fontweight="bold",
    )
    ax3.legend()

    env_labels = ["Temperature", "Humidity", "Pressure"]
    env_values = [
        fermi["environmental"]["temperature_bits"],
        fermi["environmental"]["humidity_bits"],
        fermi["environmental"]["pressure_bits"],
    ]

    bars = ax4.bar(env_labels, env_values, color=get_colorblind_palette(3), alpha=0.8)
    ax4.set_ylabel("Information Content (bits)", fontweight="bold")
    ax4.set_title("Environmental Information Content", fontweight="bold")
    ax4.grid(True, alpha=0.3, axis="y")

    for bar, value in zip(bars, env_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width() / 2.0, height + 0.1, f"{value:.2f}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    return fig


def create_metamaterial_properties_figure(analysis_results):
    """
    Create meta-material properties and response figure.

    Args:
        analysis_results: Results from integrated analysis

    Returns:
        Matplotlib figure
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Meta-Material Properties and Electromagnetic Response", fontsize=16, fontweight="bold")

    metamaterial = analysis_results["metamaterial_analysis"]
    frequency_thz = metamaterial["dielectric"]["frequency"] / 1e12

    ax1.plot(frequency_thz, metamaterial["dielectric"]["epsilon_real"], "b-", label="Real Part", linewidth=2)
    ax1.plot(frequency_thz, metamaterial["dielectric"]["epsilon_imag"], "r--", label="Imaginary Part", linewidth=2)
    ax1.set_xlabel("Frequency (THz)", fontweight="bold")
    ax1.set_ylabel("Dielectric Constant", fontweight="bold")
    ax1.set_title("Dielectric Response vs Frequency", fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    try:
        ax1.set_xscale("log")
    except Exception:
        pass

    ax2_twin = ax2.twinx()

    line1 = ax2.plot(frequency_thz, metamaterial["dielectric"]["refractive_index"], "g-", linewidth=2, label="Refractive Index")
    line2 = ax2_twin.plot(
        frequency_thz,
        metamaterial["dielectric"]["absorption_coefficient"],
        "m--",
        linewidth=2,
        label="Absorption Coefficient",
    )

    ax2.set_xlabel("Frequency (THz)", fontweight="bold")
    ax2.set_ylabel("Refractive Index", fontweight="bold", color="green")
    ax2_twin.set_ylabel("Absorption Coefficient (m⁻¹)", fontweight="bold", color="magenta")
    ax2.set_title("Optical Properties vs Frequency", fontweight="bold")
    ax2.grid(True, alpha=0.3)
    try:
        ax2.set_xscale("log")
    except Exception:
        pass

    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax2.legend(lines, labels, loc="upper right")

    plasmonic = metamaterial["plasmonic"]

    resonance_freq = plasmonic["resonance_frequency_hz"] / 1e12
    quality_factor = plasmonic["quality_factor"]
    field_enhancement = plasmonic["field_enhancement"]

    freq_range = np.linspace(resonance_freq * 0.5, resonance_freq * 1.5, 100)
    resonance_response = 1 / (1 + ((freq_range - resonance_freq) / (resonance_freq / (2 * quality_factor))) ** 2)

    ax3.plot(freq_range, resonance_response, "b-", linewidth=2)
    ax3.axvline(resonance_freq, color="red", linestyle="--", linewidth=2, label=f"Resonance: {resonance_freq:.2f} THz")
    ax3.set_xlabel("Frequency (THz)", fontweight="bold")
    ax3.set_ylabel("Normalized Response", fontweight="bold")
    ax3.set_title(
        f"Plasmonic Resonance Response\n(Q = {quality_factor:.1f}, Enhancement = {field_enhancement:.2f})",
        fontweight="bold",
    )
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    info_capacity = metamaterial["information_capacity"]

    capacity_metrics = ["Channel Capacity", "Signal/Noise", "Info Density", "Quantum Limit"]
    capacity_values = [
        np.log10(info_capacity["channel_capacity_bits_per_sec"] + 1),
        np.log10(info_capacity["signal_to_noise_ratio"] + 1),
        np.log10(info_capacity["information_density_bits_per_joule_meter"] + 1),
        np.log10(info_capacity["quantum_limit_bits_per_sec"] + 1),
    ]

    palette = get_colorblind_palette(4)
    bars = ax4.bar(capacity_metrics, capacity_values, color=palette)
    ax4.set_ylabel("Log10(Value + 1)", fontweight="bold")
    ax4.set_title("Information Capacity Metrics", fontweight="bold")
    ax4.grid(True, alpha=0.3, axis="y")
    ax4.tick_params(axis="x", rotation=45)

    for bar, value in zip(bars, capacity_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01, f"{value:.2f}", ha="center", va="bottom", fontweight="bold")

    try:
        out_dir = os.path.join("output", "figures")
        os.makedirs(out_dir, exist_ok=True)
        caption_file = os.path.join(out_dir, "metamaterial_properties.caption.txt")
        with open(caption_file, "w", encoding="utf-8") as cf:
            cf.write(
                "Meta-material dielectric and plasmonic response computed from MetaMaterialAnalyzer outputs. "
                "Shows epsilon real/imag, refractive index, absorption, resonance Q and field enhancement. "
                "Values are example outputs from integrated analysis.\n"
            )
    except Exception:
        pass

    plt.tight_layout()
    return fig


def create_system_performance_figure(performance_metrics):
    """
    Create system performance and efficiency figure.

    Args:
        performance_metrics: System performance metrics

    Returns:
        Matplotlib figure
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Integrated System Performance and Efficiency Analysis", fontsize=16, fontweight="bold")

    metric_names = ["Information\nProcessing", "Material\nPerformance", "System\nEfficiency"]
    metric_values = [
        performance_metrics["information_processing_score"],
        performance_metrics["material_performance_score"],
        performance_metrics["system_efficiency"],
    ]

    normalized_values = np.array(metric_values) / np.max(metric_values)

    palette = get_colorblind_palette(3)
    bars = ax1.bar(metric_names, normalized_values, color=palette, alpha=0.8)
    ax1.set_ylabel("Normalized Performance Score", fontweight="bold")
    ax1.set_title("System Performance Overview", fontweight="bold")
    ax1.set_ylim(0, 1.1)

    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.01,
            f"{value:.2e}",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=9,
        )

    info_components = ["Total Info", "Receptor Spec", "Neural Eff"]
    info_values = [
        performance_metrics["total_information_content_bits"],
        performance_metrics["receptor_specificity_index"],
        performance_metrics["neural_encoding_efficiency"],
    ]

    info_normalized = np.array(info_values) / np.max(info_values)

    ax2.bar(info_components, info_normalized, color=get_colorblind_palette(3), alpha=0.8)
    ax2.set_ylabel("Normalized Value", fontweight="bold")
    ax2.set_title("Information Processing Components", fontweight="bold")
    ax2.set_ylim(0, 1.1)

    material_components = ["Refractive\nIndex", "Plasmonic\nQuality", "Info\nCapacity"]
    material_values = [
        performance_metrics["average_refractive_index"],
        performance_metrics["plasmonic_quality_factor"],
        np.log10(performance_metrics["information_capacity_bits_per_sec"] + 1),
    ]

    material_normalized = np.array(material_values) / np.max(material_values)

    ax3.bar(material_components, material_normalized, color=get_colorblind_palette(3), alpha=0.8)
    ax3.set_ylabel("Normalized Value", fontweight="bold")
    ax3.set_title("Material Performance Components", fontweight="bold")
    ax3.set_ylim(0, 1.1)

    categories = ["Info Processing", "Material Perf", "System Eff", "Receptor Spec", "Neural Eff"]
    values = [
        performance_metrics["information_processing_score"] / 1e6,
        performance_metrics["material_performance_score"] / 1e6,
        performance_metrics["system_efficiency"] / 1e6,
        performance_metrics["receptor_specificity_index"],
        performance_metrics["neural_encoding_efficiency"] * 1e3,
    ]

    values_normalized = np.array(values) / np.max(values)

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values_normalized = np.concatenate((values_normalized, [values_normalized[0]]))
    angles += angles[:1]

    ax4.plot(angles, values_normalized, "o-", linewidth=2, color=get_colorblind_palette(1)[0])
    ax4.fill(angles, values_normalized, alpha=0.25, color=get_colorblind_palette(1)[0])
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(categories)
    ax4.set_ylim(0, 1)
    ax4.set_title("System Efficiency Radar Chart", fontweight="bold")
    ax4.grid(True)

    plt.tight_layout()
    return fig


def create_cross_domain_synthesis_figure(analysis_results):
    """
    Create cross-domain synthesis figure.

    Args:
        analysis_results: Results from integrated analysis

    Returns:
        Matplotlib figure
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Cross-Domain Synthesis: Fermi Estimation + Meta-Material Framework", fontsize=16, fontweight="bold")

    fermi = analysis_results["fermi_analysis"]
    metamaterial = analysis_results["metamaterial_analysis"]

    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis("off")

    ax1.add_patch(Rectangle((1, 7), 2, 1.5, facecolor="lightblue", edgecolor="navy", linewidth=2))
    ax1.add_patch(Rectangle((4, 7), 2, 1.5, facecolor="lightgreen", edgecolor="darkgreen", linewidth=2))
    ax1.add_patch(Rectangle((7, 7), 2, 1.5, facecolor="lightcoral", edgecolor="red", linewidth=2))

    ax1.add_patch(Rectangle((1, 4), 2, 1.5, facecolor="lightyellow", edgecolor="orange", linewidth=2))
    ax1.add_patch(Rectangle((4, 4), 2, 1.5, facecolor="lightpink", edgecolor="purple", linewidth=2))
    ax1.add_patch(Rectangle((7, 4), 2, 1.5, facecolor="lightcyan", edgecolor="teal", linewidth=2))

    ax1.add_patch(Rectangle((1, 1), 2, 1.5, facecolor="lightgray", edgecolor="black", linewidth=2))
    ax1.add_patch(Rectangle((4, 1), 2, 1.5, facecolor="lightsteelblue", edgecolor="steelblue", linewidth=2))
    ax1.add_patch(Rectangle((7, 1), 2, 1.5, facecolor="lightgoldenrodyellow", edgecolor="goldenrod", linewidth=2))

    ax1.text(2, 7.75, "Molecular\nInfo", ha="center", va="center", fontweight="bold")
    ax1.text(5, 7.75, "Receptor\nSpecificity", ha="center", va="center", fontweight="bold")
    ax1.text(8, 7.75, "Neural\nEncoding", ha="center", va="center", fontweight="bold")

    ax1.text(2, 4.75, "Dielectric\nResponse", ha="center", va="center", fontweight="bold")
    ax1.text(5, 4.75, "Plasmonic\nResonance", ha="center", va="center", fontweight="bold")
    ax1.text(8, 4.75, "Info\nCapacity", ha="center", va="center", fontweight="bold")

    ax1.text(2, 1.75, "Environmental\nFactors", ha="center", va="center", fontweight="bold")
    ax1.text(5, 1.75, "Quantum\nCoupling", ha="center", va="center", fontweight="bold")
    ax1.text(8, 1.75, "System\nIntegration", ha="center", va="center", fontweight="bold")

    for i in range(3):
        for _j in range(2):
            ax1.arrow(2 + i * 3, 6.5, 0, -1, head_width=0.2, head_length=0.2, fc="black", ec="black")
            ax1.arrow(2 + i * 3, 3.5, 0, -1, head_width=0.2, head_length=0.2, fc="black", ec="black")

    ax1.set_title("Information Flow Architecture", fontweight="bold")

    synthesis_metrics = ["Molecular", "Receptor", "Neural", "Environmental", "Dielectric", "Plasmonic"]
    synthesis_values = [
        fermi["molecular"]["total_bits"],
        fermi["receptor"]["specificity_index"],
        fermi["neural"]["encoding_efficiency_bits_per_energy"],
        fermi["environmental"]["total_environmental_bits"],
        np.mean(metamaterial["dielectric"]["refractive_index"]),
        metamaterial["plasmonic"]["quality_factor"],
    ]

    synthesis_normalized = np.array(synthesis_values) / np.max(synthesis_values)

    palette = get_colorblind_palette(len(synthesis_metrics))
    ax2.bar(synthesis_metrics, synthesis_normalized, color=palette)
    ax2.set_ylabel("Normalized Value", fontweight="bold")
    ax2.set_title("Cross-Domain Metric Synthesis", fontweight="bold")
    ax2.tick_params(axis="x", rotation=45)
    ax2.set_ylim(0, 1.1)

    fermi_efficiency = np.mean(
        [
            fermi["molecular"]["total_bits"] / 100,
            fermi["receptor"]["specificity_index"],
            fermi["neural"]["encoding_efficiency_bits_per_energy"] * 1000,
            fermi["environmental"]["total_environmental_bits"] / 10,
        ]
    )

    metamaterial_efficiency = np.mean(
        [
            np.mean(metamaterial["dielectric"]["refractive_index"]) / 2,
            metamaterial["plasmonic"]["quality_factor"] / 10,
            np.log10(metamaterial["information_capacity"]["channel_capacity_bits_per_sec"] + 1) / 10,
        ]
    )

    integration_efficiency = (fermi_efficiency + metamaterial_efficiency) / 2

    efficiency_data = [fermi_efficiency, metamaterial_efficiency, integration_efficiency]
    efficiency_labels = ["Fermi\nFramework", "Meta-Material\nFramework", "Integrated\nEfficiency"]

    palette = get_colorblind_palette(3)
    bars = ax3.bar(efficiency_labels, efficiency_data, color=palette, alpha=0.8)
    ax3.set_ylabel("Efficiency Score", fontweight="bold")
    ax3.set_title("Framework Integration Efficiency", fontweight="bold")
    ax3.set_ylim(0, max(efficiency_data) * 1.1)

    for bar, value in zip(bars, efficiency_data):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01, f"{value:.3f}", ha="center", va="bottom", fontweight="bold")

    domains = ["Molecular\nSpectroscopy", "Behavioral\nResponse", "Neural\nEncoding", "Environmental\nAdaptation"]
    demo_sensitivity = synthesis_normalized[:4] if synthesis_normalized.size >= 4 else synthesis_normalized

    bars = ax4.bar(domains, demo_sensitivity, color=get_colorblind_palette(4), alpha=0.8)
    ax4.set_ylabel("Model sensitivity demo (unitless)", fontweight="bold")
    ax4.set_title(
        "Cross-Domain Model Sensitivity Demo\n(not predictive accuracy on live specimens)",
        fontweight="bold",
    )
    ax4.set_ylim(0, 1.05)
    ax4.grid(True, alpha=0.3, axis="y")

    for bar, value in zip(bars, demo_sensitivity):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width() / 2.0, height + 0.02, f"{value:.2f}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    return fig


def create_composite_summary_figure(analysis_results, performance_metrics):
    """Create a concise composite multipanel summary using visualization utilities."""
    visualizer = AdvancedVisualizer(style="science")

    metamaterial = analysis_results["metamaterial_analysis"]
    frequency_thz = metamaterial["dielectric"]["frequency"] / 1e12

    data_dict = {
        "Dielectric (n)": {
            "x": frequency_thz,
            "y": metamaterial["dielectric"]["refractive_index"],
            "xlabel": "Frequency (THz)",
            "ylabel": "Refractive Index",
        },
        "Absorption (α)": {
            "x": frequency_thz,
            "y": metamaterial["dielectric"]["absorption_coefficient"],
            "xlabel": "Frequency (THz)",
            "ylabel": "Absorption (m⁻¹)",
        },
        "Performance (Norm)": {
            "x": np.arange(3),
            "y": np.array(
                [
                    performance_metrics["information_processing_score"],
                    performance_metrics["material_performance_score"],
                    performance_metrics["system_efficiency"],
                ]
            )
            / max(
                1e-12,
                max(
                    performance_metrics["information_processing_score"],
                    performance_metrics["material_performance_score"],
                    performance_metrics["system_efficiency"],
                ),
            ),
            "xlabel": "Metrics Index",
            "ylabel": "Normalized Value",
        },
    }

    return visualizer.plot_multi_panel_analysis(data_dict, title="Integrated Analysis Summary")
