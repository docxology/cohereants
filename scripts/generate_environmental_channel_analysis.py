#!/usr/bin/env python3
"""Generate comprehensive environmental channel analysis."""
from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption

ensure_src_on_path()
from src.case_studies.environmental_channel import (
    atmospheric_transmission_comprehensive,
    channel_capacity_analysis,
    optimize_wavelength_for_range,
    environmental_sensitivity_analysis
)


def main() -> int:
    """Generate comprehensive environmental channel analysis."""
    try:
        print("🔄 Starting environmental channel analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()
        
        # Analysis parameters
        wavelengths_um = np.linspace(2.0, 25.0, 200)
        
        # Environmental conditions
        conditions = {
            'clear': {'humidity_percent': 30.0, 'temperature_k': 298.0, 'pressure_pa': 101325.0, 'aerosol_visibility_km': 23.0},
            'humid': {'humidity_percent': 80.0, 'temperature_k': 305.0, 'pressure_pa': 101325.0, 'aerosol_visibility_km': 15.0}
        }
        
        print("📊 Computing atmospheric transmission...")
        # Transmission analysis
        transmission_results = {}
        for condition_name, params in conditions.items():
            transmission_results[condition_name] = atmospheric_transmission_comprehensive(
                wavelengths_um, 100.0, **params
            )
        
        print("💡 Computing channel capacity...")
        # Capacity analysis - convert parameter names for capacity analysis
        capacity_results = {}
        for condition_name, params in conditions.items():
            # Convert parameter names for channel_capacity_analysis
            env_params = {
                'humidity': params['humidity_percent'],
                'temperature': params['temperature_k'], 
                'pressure': params['pressure_pa'],
                'visibility': params['aerosol_visibility_km']
            }
            capacity_results[condition_name] = channel_capacity_analysis(
                wavelengths_um, 100.0, 0.0, environmental_conditions=env_params
            )
        
        print("📈 Creating visualization...")
        # Create comprehensive figure
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Transmission comparison
        ax = axes[0, 0]
        for condition_name, result in transmission_results.items():
            ax.plot(result['wavelengths_um'], result['transmission_total'], 
                   linewidth=2, label=condition_name.capitalize())
        ax.axvspan(2, 5, alpha=0.2, color='red', label='2-5 μm')
        ax.axvspan(8, 14, alpha=0.2, color='green', label='8-14 μm')
        ax.axvspan(17, 25, alpha=0.2, color='blue', label='17-25 μm')
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Transmission')
        ax.set_title('Atmospheric Transmission')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Transmission components (clear)
        ax = axes[0, 1] 
        clear_result = transmission_results['clear']
        ax.plot(clear_result['wavelengths_um'], clear_result['transmission_total'], 'k-', 
               linewidth=2, label='Total')
        ax.plot(clear_result['wavelengths_um'], clear_result['transmission_molecular'], 'b--', 
               label='Molecular')
        ax.plot(clear_result['wavelengths_um'], clear_result['transmission_rayleigh'], 'r--',
               label='Rayleigh')
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Transmission')
        ax.set_title('Transmission Components')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Channel capacity
        ax = axes[0, 2]
        for condition_name, result in capacity_results.items():
            ax.semilogy(result['wavelengths_um'], result['capacity_bps']/1e6, 
                       linewidth=2, label=condition_name.capitalize())
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Capacity (Mbps)')
        ax.set_title('Channel Capacity')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # SNR comparison
        ax = axes[1, 0]
        for condition_name, result in capacity_results.items():
            ax.plot(result['wavelengths_um'], result['snr_db'], 
                   linewidth=2, label=condition_name.capitalize())
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('SNR (dB)')
        ax.set_title('Signal-to-Noise Ratio')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Path loss comparison
        ax = axes[1, 1]
        for condition_name, result in capacity_results.items():
            ax.plot(result['wavelengths_um'], result['atmospheric_excess_db'], 
                   linewidth=2, label=condition_name.capitalize())
        ax.set_xlabel('Wavelength (μm)')
        ax.set_ylabel('Atmospheric Excess Loss (dB)')
        ax.set_title('Atmospheric vs Free Space Loss')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Summary statistics
        ax = axes[1, 2]
        ax.axis('off')
        clear_capacity = np.max(capacity_results['clear']['capacity_bps']) / 1e6
        humid_capacity = np.max(capacity_results['humid']['capacity_bps']) / 1e6
        clear_trans = np.max(transmission_results['clear']['transmission_total'])
        humid_trans = np.max(transmission_results['humid']['transmission_total'])
        
        summary_text = f"""Analysis Summary:

Clear Conditions:
• Max Capacity: {clear_capacity:.1f} Mbps
• Peak Transmission: {clear_trans:.3f}

Humid Conditions: 
• Max Capacity: {humid_capacity:.1f} Mbps
• Peak Transmission: {humid_trans:.3f}

Impact:
• Humidity Loss: {(1-humid_trans/clear_trans)*100:.1f}%
• Best Window: 8-14 μm
        """
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', fontfamily='monospace')

        plt.tight_layout()

        # Save outputs
        out_png = os.path.join(fig_dir, "environmental_channel_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        caption = f"""Comprehensive environmental channel analysis showing atmospheric transmission and channel capacity under clear and humid conditions. Analysis demonstrates {(1-humid_trans/clear_trans)*100:.1f}% transmission loss due to humidity with peak capacity of {clear_capacity:.1f} Mbps under clear conditions and {humid_capacity:.1f} Mbps under humid conditions in the optimal 8-14 μm atmospheric window."""
        
        write_caption(os.path.join(fig_dir, "environmental_channel_comprehensive_analysis.caption.txt"), caption)

        # Save data
        out_npz = os.path.join(data_dir, "environmental_channel_comprehensive.npz")
        np.savez(out_npz,
                wavelengths_um=wavelengths_um,
                clear_transmission=transmission_results['clear']['transmission_total'],
                humid_transmission=transmission_results['humid']['transmission_total'],
                clear_capacity=capacity_results['clear']['capacity_bps'],
                humid_capacity=capacity_results['humid']['capacity_bps'],
                clear_snr=capacity_results['clear']['snr_db'],
                humid_snr=capacity_results['humid']['snr_db'])

        print(f"✅ Success! Generated environmental analysis")
        print(f"Generated: {out_png}")
        print(f"Generated: {out_npz}")
        print(f"Clear max capacity: {clear_capacity:.1f} Mbps")
        print(f"Humid max capacity: {humid_capacity:.1f} Mbps")
        print(out_png)
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
