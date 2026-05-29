"""Appendix figure rendering for environmental_channel."""

from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from src.viz.figure_helpers import format_display_metric

from src.viz.warnings_util import suppress_plot_warnings


def render_comprehensive_figure(analysis: Dict[str, object]) -> tuple[object, Dict[str, float]]:
    """Render comprehensive appendix figure and return summary metrics."""
    data = analysis.as_dict() if hasattr(analysis, "as_dict") else analysis
    with suppress_plot_warnings():
        import matplotlib.pyplot as plt

        from src.viz.figure_helpers import format_display_metric

        wavelengths_um = data["wavelengths_um"]
        transmission_results = data["transmission_results"]
        capacity_results = data["capacity_results"]

        fig, axes = plt.subplots(2, 3, figsize=(15, 10))

        ax = axes[0, 0]
        for condition_name, result in transmission_results.items():
            ax.plot(
                result["wavelengths_um"],
                result["transmission_total"],
                linewidth=2,
                label=condition_name.capitalize(),
            )
        ax.axvspan(2, 5, alpha=0.2, color="red", label="2-5 μm")
        ax.axvspan(8, 14, alpha=0.2, color="green", label="8-14 μm")
        ax.axvspan(17, 25, alpha=0.2, color="blue", label="17-25 μm")
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Transmission")
        ax.set_title("Atmospheric Transmission")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[0, 1]
        clear_result = transmission_results["clear"]
        ax.plot(clear_result["wavelengths_um"], clear_result["transmission_total"], "k-", linewidth=2, label="Total")
        ax.plot(
            clear_result["wavelengths_um"],
            clear_result["transmission_molecular"],
            "b--",
            label="Molecular",
        )
        ax.plot(
            clear_result["wavelengths_um"],
            clear_result["transmission_rayleigh"],
            "r--",
            label="Rayleigh",
        )
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Transmission")
        ax.set_title("Transmission Components")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[0, 2]
        for condition_name, result in capacity_results.items():
            ax.semilogy(
                result["wavelengths_um"],
                result["capacity_bps"] / 1e6,
                linewidth=2,
                label=condition_name.capitalize(),
            )
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Capacity (Mbps)")
        ax.set_title("Channel Capacity")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 0]
        for condition_name, result in capacity_results.items():
            ax.plot(result["wavelengths_um"], result["snr_db"], linewidth=2, label=condition_name.capitalize())
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("SNR (dB)")
        ax.set_title("Signal-to-Noise Ratio")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 1]
        for condition_name, result in capacity_results.items():
            ax.plot(
                result["wavelengths_um"],
                result["atmospheric_excess_db"],
                linewidth=2,
                label=condition_name.capitalize(),
            )
        ax.set_xlabel("Wavelength (μm)")
        ax.set_ylabel("Atmospheric Excess Loss (dB)")
        ax.set_title("Atmospheric vs Free Space Loss")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1, 2]
        ax.axis("off")
        clear_capacity = float(np.max(capacity_results["clear"]["capacity_bps"]) / 1e6)
        humid_capacity = float(np.max(capacity_results["humid"]["capacity_bps"]) / 1e6)
        lwir_mask = (wavelengths_um >= 8.0) & (wavelengths_um <= 14.0)
        clear_trans = float(np.mean(transmission_results["clear"]["transmission_total"][lwir_mask]))
        humid_trans = float(np.mean(transmission_results["humid"]["transmission_total"][lwir_mask]))
        humidity_loss_pct = (1.0 - humid_trans / clear_trans) * 100.0 if clear_trans > 1e-9 else float("nan")

        summary_text = f"""Analysis Summary:

        Clear Conditions:
        • Max Capacity: {format_display_metric(clear_capacity, unit='Mbps')}
        • LWIR Mean Transmission: {format_display_metric(clear_trans, precision=3)}

        Humid Conditions:
        • Max Capacity: {format_display_metric(humid_capacity, unit='Mbps')}
        • LWIR Mean Transmission: {format_display_metric(humid_trans, precision=3)}

        Impact:
        • Humidity Loss (LWIR mean): {format_display_metric(humidity_loss_pct, unit='%', precision=1)}
        • Best Window: 8-14 μm
            """
        ax.text(
            0.05,
            0.95,
            summary_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            fontfamily="monospace",
        )

        plt.tight_layout()
        metrics = {
            "clear_capacity_mbps": clear_capacity,
            "humid_capacity_mbps": humid_capacity,
            "clear_trans": clear_trans,
            "humid_trans": humid_trans,
        }
        return fig, metrics

