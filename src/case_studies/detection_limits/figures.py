"""Appendix figure rendering for detection_limits."""

from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from src.viz.warnings_util import suppress_plot_warnings


def render_comprehensive_figure(analysis: Dict[str, object]) -> tuple[object, Dict[str, float]]:
    """Render comprehensive appendix figure and return summary metrics."""
    data = analysis.as_dict() if hasattr(analysis, "as_dict") else analysis
    with suppress_plot_warnings():
        from src.case_studies.detection_limits import min_detectable_power

        import matplotlib.pyplot as plt

        roc_results = data["roc_results"]
        snr_levels = data["snr_levels"]
        detection_perf = data["detection_perf"]
        operating_regions = data["operating_regions"]
        noise_analysis = data["noise_analysis"]
        range_analysis = data["range_analysis"]

        fig = plt.figure(figsize=(16, 12))

        ax1 = plt.subplot(3, 4, 1)
        for snr_db in snr_levels:
            roc_data = roc_results[f"snr_{snr_db}db"]
            ax1.plot(
                roc_data["pfa"],
                roc_data["pd"],
                linewidth=2,
                label=f"{snr_db} dB (AUC={roc_data['auc']:.2f})",
            )
        ax1.plot([0, 1], [0, 1], "k--", alpha=0.5)
        ax1.set_xlabel("False Alarm Probability")
        ax1.set_ylabel("Detection Probability")
        ax1.set_title("ROC Curves")
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        ax2 = plt.subplot(3, 4, 2)
        ax2.plot(detection_perf["snr_db"], detection_perf["pd"], "b-", linewidth=2)
        ax2.axhline(y=0.9, color="r", linestyle="--", label="90% Detection")
        ax2.axvline(
            x=detection_perf["mds_snr_db"],
            color="g",
            linestyle="--",
            label=f"MDS: {detection_perf['mds_snr_db']:.1f} dB",
        )
        ax2.set_xlabel("SNR (dB)")
        ax2.set_ylabel("Detection Probability")
        ax2.set_title("Detection Performance")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        ax3 = plt.subplot(3, 4, 3)
        power_grid = operating_regions["power_grid_w"]
        temp_grid = operating_regions["temperature_grid_k"]
        snr_grid = operating_regions["snr_grid_db"]
        contour = ax3.contourf(power_grid * 1e12, temp_grid, snr_grid, levels=[-5, 0, 3, 6, 10, 15], cmap="RdYlGn")
        ax3.set_xlabel("Signal Power (pW)")
        ax3.set_ylabel("Temperature (K)")
        ax3.set_title("Operating Regions (SNR dB)")
        ax3.set_xscale("log")
        plt.colorbar(contour, ax=ax3)

        ax4 = plt.subplot(3, 4, 4)
        ax4.loglog(
            noise_analysis["frequencies_hz"],
            10 ** (noise_analysis["thermal_noise_db"] / 10),
            "b-",
            linewidth=2,
            label="Thermal",
        )
        ax4.loglog(
            noise_analysis["frequencies_hz"],
            10 ** (noise_analysis["total_noise_db"] / 10),
            "k-",
            linewidth=3,
            label="Total",
        )
        ax4.set_xlabel("Frequency (Hz)")
        ax4.set_ylabel("Noise Power (W)")
        ax4.set_title("Noise Floor")
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        ax5 = plt.subplot(3, 4, 5)
        distances_km = range_analysis["distances_m"] / 1000
        ax5.semilogx(distances_km, range_analysis["received_power_dbm"], "b-", linewidth=2)
        ax5.axhline(y=-90, color="r", linestyle="--", label="Sensitivity")
        max_range_km = range_analysis["max_range_atmospheric_m"] / 1000
        ax5.axvline(x=max_range_km, color="g", linestyle="--", label=f"Max: {max_range_km:.1f} km")
        ax5.set_xlabel("Distance (km)")
        ax5.set_ylabel("Received Power (dBm)")
        ax5.set_title("Detection Range")
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        ax6 = plt.subplot(3, 4, 6)
        bandwidth = np.logspace(3, 8, 100)
        mdp_values = min_detectable_power(300.0, bandwidth, 3.0) * 1e12
        ax6.loglog(bandwidth, mdp_values, "purple", linewidth=2)
        ax6.set_xlabel("Bandwidth (Hz)")
        ax6.set_ylabel("Min Detectable Power (pW)")
        ax6.set_title("MDP vs Bandwidth")
        ax6.grid(True, alpha=0.3)

        ax7 = plt.subplot(3, 4, 7)
        temperatures = np.linspace(250, 400, 50)
        mdp_temp = [min_detectable_power(temperature, 1e6, 3.0) * 1e12 for temperature in temperatures]
        ax7.plot(temperatures, mdp_temp, "red", linewidth=2)
        ax7.set_xlabel("Temperature (K)")
        ax7.set_ylabel("Min Detectable Power (pW)")
        ax7.set_title("Temperature Effects")
        ax7.grid(True, alpha=0.3)

        ax8 = plt.subplot(3, 4, 8)
        integration_times = np.logspace(-3, 2, 50)
        processing_gains = 10 * np.log10(integration_times)
        effective_snr = detection_perf["mds_snr_db"] - processing_gains
        ax8.semilogx(integration_times, effective_snr, "orange", linewidth=2)
        ax8.set_xlabel("Integration Time (s)")
        ax8.set_ylabel("Effective MDS (dB)")
        ax8.set_title("Processing Gain")
        ax8.grid(True, alpha=0.3)

        ax9 = plt.subplot(3, 4, 9)
        roc_6db = roc_results["snr_6db"]
        ax9.plot(roc_6db["pfa"], roc_6db["pd"], "b-", linewidth=2)
        ax9.plot(roc_6db["optimal_pfa"], roc_6db["optimal_pd"], "ro", markersize=8)
        ax9.set_xlabel("False Alarm Probability")
        ax9.set_ylabel("Detection Probability")
        ax9.set_title("Optimal Operating Point (6 dB)")
        ax9.grid(True, alpha=0.3)

        ax10 = plt.subplot(3, 4, 10)
        sensitivity_range = range_analysis["sensitivity_range_dbm"]
        max_ranges_km = range_analysis["max_ranges_vs_sensitivity_m"] / 1000
        ax10.semilogx(max_ranges_km, sensitivity_range, "mo-", linewidth=2)
        ax10.set_xlabel("Max Range (km)")
        ax10.set_ylabel("Receiver Sensitivity (dBm)")
        ax10.set_title("Sensitivity Trade-off")
        ax10.grid(True, alpha=0.3)

        best_auc = max(roc_results[key]["auc"] for key in roc_results)
        ax11 = plt.subplot(3, 4, 11)
        ax11.axis("off")
        summary_text = f"""Performance Summary:

        Best AUC: {best_auc:.3f}
        MDS (90% PD): {detection_perf['mds_snr_db']:.1f} dB
        Max Range: {max_range_km:.1f} km
        Processing Gain: {detection_perf['processing_gain_db']:.1f} dB

        Noise Floor: {noise_analysis['total_noise_db'][0]:.1f} dB
        Temperature Impact: Linear with T
        Bandwidth Impact: √BW scaling
            """
        ax11.text(
            0.05,
            0.95,
            summary_text,
            transform=ax11.transAxes,
            fontsize=10,
            verticalalignment="top",
            fontfamily="monospace",
        )

        ax12 = plt.subplot(3, 4, 12)
        x_vals = np.linspace(-3, 5, 200)
        noise_pdf = norm.pdf(x_vals, roc_6db["noise_only_mean"], roc_6db["noise_only_std"])
        signal_pdf = norm.pdf(x_vals, roc_6db["signal_plus_noise_mean"], roc_6db["signal_plus_noise_std"])
        ax12.plot(x_vals, noise_pdf, "r-", linewidth=2, label="Noise (H₀)")
        ax12.plot(x_vals, signal_pdf, "b-", linewidth=2, label="Signal+Noise (H₁)")
        ax12.axvline(x=roc_6db["optimal_threshold"], color="g", linestyle="--", label="Threshold")
        ax12.set_xlabel("Decision Variable")
        ax12.set_ylabel("Probability Density")
        ax12.set_title("Detection Distributions (6 dB)")
        ax12.legend(fontsize=8)
        ax12.grid(True, alpha=0.3)

        plt.tight_layout()
        metrics = {
            "best_auc": float(best_auc),
            "mds_snr_db": float(detection_perf["mds_snr_db"]),
            "max_range_km": float(max_range_km),
        }
        return fig, metrics

