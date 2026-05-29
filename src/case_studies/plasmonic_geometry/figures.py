"""Appendix figure rendering for plasmonic_geometry."""

from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from src.viz.warnings_util import suppress_plot_warnings


def render_comprehensive_figure(analysis: Dict[str, object]) -> tuple[object, Dict[str, float]]:
    """Render comprehensive appendix figure and return summary metrics."""
    data = analysis.as_dict() if hasattr(analysis, "as_dict") else analysis
    with suppress_plot_warnings():
        import matplotlib.pyplot as plt

        radii_nm = data["radii_nm"]
        wavelengths_um = data["wavelengths_um"]
        ir_wavelengths = data["ir_wavelengths"]
        sweep_gold = data["sweep_gold"]
        sweep_silver = data["sweep_silver"]
        optimized_geometries = data["optimized_geometries"]
        gold_epsilon = data["gold_epsilon"]
        silver_epsilon = data["silver_epsilon"]
        positions_nm = data["positions_nm"]
        coupling_analysis = data["coupling_analysis"]
        optimal_radius = float(data["optimal_radius"])
        field_dist = data["field_dist"]

        fig = plt.figure(figsize=(18, 14))

        ax1 = plt.subplot(3, 4, 1)
        im1 = ax1.imshow(
            sweep_gold["q_factors_2d"],
            aspect="auto",
            origin="lower",
            extent=[wavelengths_um[0], wavelengths_um[-1], radii_nm[0], radii_nm[-1]],
        )
        ax1.set_xlabel("Wavelength (μm)")
        ax1.set_ylabel("Radius (nm)")
        ax1.set_title("Gold Q-Factor Map")
        plt.colorbar(im1, ax=ax1, label="Q Factor")
        ax1.axvspan(2, 5, alpha=0.3, color="red")
        ax1.axvspan(8, 14, alpha=0.3, color="green")
        ax1.axvspan(17, 25, alpha=0.3, color="blue")

        ax2 = plt.subplot(3, 4, 2)
        im2 = ax2.imshow(
            np.log10(sweep_gold["enhancements_2d"]),
            aspect="auto",
            origin="lower",
            extent=[wavelengths_um[0], wavelengths_um[-1], radii_nm[0], radii_nm[-1]],
        )
        ax2.set_xlabel("Wavelength (μm)")
        ax2.set_ylabel("Radius (nm)")
        ax2.set_title("Gold Enhancement (log₁₀)")
        plt.colorbar(im2, ax=ax2, label="log₁₀(Enhancement)")
        ax2.axvspan(2, 5, alpha=0.3, color="red")
        ax2.axvspan(8, 14, alpha=0.3, color="green")
        ax2.axvspan(17, 25, alpha=0.3, color="blue")

        ax3 = plt.subplot(3, 4, 3)
        ax3.plot(wavelengths_um, gold_epsilon.real, "b-", linewidth=2, label="Gold Re(ε)")
        ax3.plot(wavelengths_um, gold_epsilon.imag, "b--", linewidth=2, label="Gold Im(ε)")
        ax3.plot(wavelengths_um, silver_epsilon.real, "r-", linewidth=2, label="Silver Re(ε)")
        ax3.plot(wavelengths_um, silver_epsilon.imag, "r--", linewidth=2, label="Silver Im(ε)")
        ax3.set_xlabel("Wavelength (μm)")
        ax3.set_ylabel("Permittivity")
        ax3.set_title("Material Permittivity (Drude)")
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(2, 25)

        ax4 = plt.subplot(3, 4, 4)
        ax4.plot(radii_nm, sweep_gold["resonance_wavelengths"], "o-", color="gold", linewidth=2, markersize=4, label="Gold")
        ax4.plot(radii_nm, sweep_silver["resonance_wavelengths"], "s-", color="silver", linewidth=2, markersize=4, label="Silver")
        ax4.axhspan(2, 5, alpha=0.2, color="red", label="2-5 μm")
        ax4.axhspan(8, 14, alpha=0.2, color="green", label="8-14 μm")
        ax4.axhspan(17, 25, alpha=0.2, color="blue", label="17-25 μm")
        ax4.set_xlabel("Radius (nm)")
        ax4.set_ylabel("Resonance Wavelength (μm)")
        ax4.set_title("Resonance vs Size")
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3)

        gold_opt_sizes = [opt["optimal_size_nm"] for opt in optimized_geometries["gold"]]
        gold_opt_enhancements = [opt["max_enhancement"] for opt in optimized_geometries["gold"]]
        silver_opt_sizes = [opt["optimal_size_nm"] for opt in optimized_geometries["silver"]]
        silver_opt_enhancements = [opt["max_enhancement"] for opt in optimized_geometries["silver"]]

        ax5 = plt.subplot(3, 4, 5)
        ax5.scatter(ir_wavelengths, gold_opt_sizes, c="gold", s=100, alpha=0.8, label="Gold Optimal Size")
        ax5.scatter(ir_wavelengths, silver_opt_sizes, c="silver", s=100, alpha=0.8, label="Silver Optimal Size")
        ax5.set_xlabel("Target Wavelength (μm)")
        ax5.set_ylabel("Optimal Radius (nm)")
        ax5.set_title("Optimized Geometries")
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        ax6 = plt.subplot(3, 4, 6)
        ax6.bar(ir_wavelengths - 0.2, gold_opt_enhancements, 0.4, color="gold", alpha=0.7, label="Gold")
        ax6.bar(ir_wavelengths + 0.2, silver_opt_enhancements, 0.4, color="silver", alpha=0.7, label="Silver")
        ax6.set_xlabel("Target Wavelength (μm)")
        ax6.set_ylabel("Max Enhancement Factor")
        ax6.set_title("Optimized Enhancement")
        ax6.legend()
        ax6.grid(True, alpha=0.3)

        ax7 = plt.subplot(3, 4, 7)
        ax7.scatter(positions_nm[:, 0], positions_nm[:, 1], c="red", s=200, alpha=0.7)
        for i, pos in enumerate(positions_nm):
            ax7.annotate(f"P{i + 1}", (pos[0], pos[1]), xytext=(5, 5), textcoords="offset points", fontsize=10)
        ax7.set_xlabel("X Position (nm)")
        ax7.set_ylabel("Y Position (nm)")
        ax7.set_title("Coupled Particle Geometry")
        ax7.axis("equal")
        ax7.grid(True, alpha=0.3)

        ax8 = plt.subplot(3, 4, 8)
        particle_indices = np.arange(len(coupling_analysis["enhancement_ratio"]))
        ax8.bar(particle_indices, coupling_analysis["enhancement_ratio"], color=["red", "green", "blue"], alpha=0.7)
        ax8.set_xlabel("Particle Index")
        ax8.set_ylabel("Enhancement Ratio")
        ax8.set_title(f'Coupling Enhancement\n(Max: {np.max(coupling_analysis["enhancement_ratio"]):.1f}×)')
        ax8.grid(True, alpha=0.3)

        ax9 = plt.subplot(3, 4, 9)
        extent = [-field_dist["x_nm"][-1], field_dist["x_nm"][-1], -field_dist["y_nm"][-1], field_dist["y_nm"][-1]]
        im9 = ax9.imshow(field_dist["intensity"], extent=extent, origin="lower", cmap="hot", interpolation="bilinear")
        circle = plt.Circle((0, 0), optimal_radius, fill=False, color="white", linewidth=2)
        ax9.add_patch(circle)
        ax9.set_xlabel("X Position (nm)")
        ax9.set_ylabel("Y Position (nm)")
        ax9.set_title(f'Near-Field Intensity\n(Max: {field_dist["max_enhancement"]:.1f}×)')
        plt.colorbar(im9, ax=ax9, label="|E|²")

        ax10 = plt.subplot(3, 4, 10)
        im10 = ax10.imshow(
            sweep_silver["q_factors_2d"],
            aspect="auto",
            origin="lower",
            extent=[wavelengths_um[0], wavelengths_um[-1], radii_nm[0], radii_nm[-1]],
        )
        ax10.set_xlabel("Wavelength (μm)")
        ax10.set_ylabel("Radius (nm)")
        ax10.set_title("Silver Q-Factor Map")
        plt.colorbar(im10, ax=ax10, label="Q Factor")
        ax10.axvspan(2, 5, alpha=0.3, color="red")
        ax10.axvspan(8, 14, alpha=0.3, color="green")
        ax10.axvspan(17, 25, alpha=0.3, color="blue")

        ax11 = plt.subplot(3, 4, 11)
        ax11.plot(radii_nm, sweep_gold["max_enhancements"], "o-", color="gold", linewidth=2, label="Gold")
        ax11.plot(radii_nm, sweep_silver["max_enhancements"], "s-", color="silver", linewidth=2, label="Silver")
        ax11.set_xlabel("Radius (nm)")
        ax11.set_ylabel("Max Enhancement Factor")
        ax11.set_title("Peak Enhancement vs Size")
        ax11.legend()
        ax11.grid(True, alpha=0.3)
        ax11.set_yscale("log")

        gold_q_at_opt = [opt["resonance_quality"] for opt in optimized_geometries["gold"]]
        silver_q_at_opt = [opt["resonance_quality"] for opt in optimized_geometries["silver"]]
        ax12 = plt.subplot(3, 4, 12)
        ax12.plot(ir_wavelengths, gold_q_at_opt, "o-", color="gold", linewidth=2, markersize=8, label="Gold")
        ax12.plot(ir_wavelengths, silver_q_at_opt, "s-", color="silver", linewidth=2, markersize=8, label="Silver")
        ax12.set_xlabel("Target Wavelength (μm)")
        ax12.set_ylabel("Quality Factor")
        ax12.set_title("Q-Factor at Optimized Sizes")
        ax12.legend()
        ax12.grid(True, alpha=0.3)

        plt.tight_layout()

        max_gold_enhancement = float(np.max(sweep_gold["max_enhancements"]))
        max_silver_enhancement = float(np.max(sweep_silver["max_enhancements"]))
        avg_coupling_enhancement = float(np.mean(coupling_analysis["enhancement_ratio"]))
        metrics = {
            "max_gold_enhancement": max_gold_enhancement,
            "max_silver_enhancement": max_silver_enhancement,
            "avg_coupling_enhancement": avg_coupling_enhancement,
            "field_max_enhancement": float(field_dist["max_enhancement"]),
            "min_gold_opt_size": float(min(gold_opt_sizes)),
            "max_gold_opt_size": float(max(gold_opt_sizes)),
        }
        return fig, metrics

