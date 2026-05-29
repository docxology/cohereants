"""Appendix figure rendering for sensilla_array_directionality."""

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

        wavelengths = data["wavelengths"]
        log_positions = data["log_positions"]
        log_pattern = data["log_pattern"]
        log_gain = float(data["log_gain"])
        circ_positions = data["circ_positions"]
        morphology_analysis = data["morphology_analysis"]
        freq_response = data["freq_response"]
        angles = data["angles"]
        dipole_pattern = data["dipole_pattern"]
        monopole_pattern = data["monopole_pattern"]
        patch_pattern = data["patch_pattern"]
        coupling_matrix = data["coupling_matrix"]
        morph_correlation = float(data["morph_correlation"])
        n_sensilla = int(data["n_sensilla"])

        fig = plt.figure(figsize=(16, 12))

        ax1 = plt.subplot(3, 3, 1)
        ax1.plot(wavelengths, log_pattern["pattern"], "b-", linewidth=2, label=f"Log-periodic (G={log_gain:.1f})")
        ax1.axvspan(2, 5, alpha=0.2, color="red", label="2-5 μm window")
        ax1.axvspan(8, 14, alpha=0.2, color="green", label="8-14 μm window")
        ax1.axvspan(17, 25, alpha=0.2, color="blue", label="17-25 μm window")
        ax1.set_xlabel("Wavelength (μm)")
        ax1.set_ylabel("Normalized Power")
        ax1.set_title("Array Beam Patterns vs Atmospheric Windows")
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=8)
        ax1.set_xlim(2, 25)

        ax2 = plt.subplot(3, 3, 2)
        scatter = ax2.scatter(
            morphology_analysis["sensilla_lengths_um"],
            morphology_analysis["best_wavelength_matches"],
            c=morphology_analysis["match_quality_scores"],
            cmap="viridis",
            s=30,
            alpha=0.7,
        )
        ax2.plot(
            morphology_analysis["sensilla_lengths_um"],
            morphology_analysis["quarter_wave_resonances_um"],
            "r--",
            alpha=0.5,
            label="λ/4 resonance",
        )
        ax2.plot(
            morphology_analysis["sensilla_lengths_um"],
            morphology_analysis["half_wave_resonances_um"],
            "b--",
            alpha=0.5,
            label="λ/2 resonance",
        )
        ax2.set_xlabel("Sensilla Length (μm)")
        ax2.set_ylabel("Best Match Wavelength (μm)")
        ax2.set_title("Morphology-Wavelength Matching")
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label="Match Quality")

        ax3 = plt.subplot(3, 3, 3)
        ax3.plot(freq_response["frequencies_thz"], freq_response["gain_db"], "g-", linewidth=2)
        if len(freq_response["resonance_frequencies_thz"]) > 0:
            resonance_indices = []
            for rf in freq_response["resonance_frequencies_thz"]:
                closest_idx = int(np.argmin(np.abs(freq_response["frequencies_thz"] - rf)))
                resonance_indices.append(closest_idx)
            ax3.scatter(
                freq_response["resonance_frequencies_thz"],
                freq_response["gain_db"][resonance_indices],
                color="red",
                s=50,
                label="Resonances",
                zorder=5,
            )
        ax3.set_xlabel("Frequency (THz)")
        ax3.set_ylabel("Gain (dB)")
        ax3.set_title(f'Frequency Response (BW={freq_response["bandwidth_3db_thz"]:.1f} THz)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        ax4 = plt.subplot(3, 3, 4)
        ax4.plot(angles, dipole_pattern, "b-", linewidth=2, label="Dipole")
        ax4.plot(angles, monopole_pattern, "r-", linewidth=2, label="Monopole")
        ax4.plot(angles, patch_pattern, "g-", linewidth=2, label="Patch")
        ax4.set_xlabel("Angle (degrees)")
        ax4.set_ylabel("Normalized Pattern")
        ax4.set_title("Individual Element Patterns")
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        ax5 = plt.subplot(3, 3, 5)
        ax5.scatter(circ_positions[:, 0], circ_positions[:, 1], c="blue", s=60, alpha=0.7, label="Circular")
        ax5.scatter(log_positions, np.zeros_like(log_positions), c="red", s=60, marker="s", alpha=0.7, label="Log-periodic")
        ax5.set_xlabel("X Position (μm)")
        ax5.set_ylabel("Y Position (μm)")
        ax5.set_title("Array Geometries")
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.axis("equal")

        ax6 = plt.subplot(3, 3, 6)
        coupling_mag = np.abs(coupling_matrix)
        im = ax6.imshow(coupling_mag, cmap="hot", interpolation="nearest")
        ax6.set_xlabel("Element Index")
        ax6.set_ylabel("Element Index")
        ax6.set_title("Mutual Coupling Magnitude")
        plt.colorbar(im, ax=ax6, label="|Z| (normalized)")

        ax7 = plt.subplot(3, 3, 7)
        ax7.scatter(
            morphology_analysis["aspect_ratios"],
            morphology_analysis["q_factors"],
            c=morphology_analysis["match_quality_scores"],
            cmap="plasma",
            s=30,
            alpha=0.7,
        )
        ax7.set_xlabel("Length/Diameter Ratio")
        ax7.set_ylabel("Estimated Q Factor")
        ax7.set_title("Q Factor vs Aspect Ratio")
        ax7.grid(True, alpha=0.3)

        ax8 = plt.subplot(3, 3, 8)
        ax8.plot(freq_response["frequencies_thz"], freq_response["impedance_real"], "b-", label="Real")
        ax8.plot(freq_response["frequencies_thz"], freq_response["impedance_imag"], "r-", label="Imaginary")
        ax8.set_xlabel("Frequency (THz)")
        ax8.set_ylabel("Impedance (normalized)")
        ax8.set_title("Input Impedance vs Frequency")
        ax8.legend()
        ax8.grid(True, alpha=0.3)

        ax9 = plt.subplot(3, 3, 9)
        ax9.hist(morphology_analysis["best_wavelength_matches"], bins=15, alpha=0.7, color="skyblue", edgecolor="black")
        ax9.axvspan(2, 5, alpha=0.3, color="red", label="2-5 μm")
        ax9.axvspan(8, 14, alpha=0.3, color="green", label="8-14 μm")
        ax9.axvspan(17, 25, alpha=0.3, color="blue", label="17-25 μm")
        ax9.set_xlabel("Best Match Wavelength (μm)")
        ax9.set_ylabel("Count")
        ax9.set_title("Wavelength Distribution")
        ax9.legend(fontsize=8)
        ax9.grid(True, alpha=0.3)

        plt.tight_layout()
        metrics = {
            "log_gain": log_gain,
            "n_circular_elements": float(len(circ_positions)),
            "bandwidth_3db_thz": float(freq_response["bandwidth_3db_thz"]),
            "q_factor_avg": float(freq_response["q_factor_avg"]),
            "morph_correlation": morph_correlation,
            "n_sensilla": float(n_sensilla),
            "n_resonances": float(len(freq_response["resonance_frequencies_thz"])),
        }
        return fig, metrics

