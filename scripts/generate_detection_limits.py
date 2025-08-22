#!/usr/bin/env python3
"""Generate comprehensive detection limits and operating regions analysis."""
from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption

ensure_src_on_path()
from src.case_studies.detection_limits import (
    min_detectable_power,
    roc_analysis,
    detection_performance_vs_snr,
    operating_regions_analysis,
    noise_floor_analysis,
    detection_range_analysis
)


def main() -> int:
    """Generate comprehensive detection limits and performance analysis."""
    try:
        print("🔄 Starting detection limits analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()
        
        # ROC Analysis
        print("📊 Computing ROC analysis...")
        roc_results = {}
        snr_levels = [0, 3, 6, 10]
        for snr_db in snr_levels:
            signal_power = 10**(snr_db / 10.0)
            roc_results[f'snr_{snr_db}db'] = roc_analysis(signal_power, 1.0)
        
        # Detection Performance
        print("🎯 Analyzing detection performance...")
        snr_range_db = np.linspace(-5, 15, 50)
        detection_perf = detection_performance_vs_snr(snr_range_db, pfa_target=1e-3)
        
        # Operating Regions
        print("🗺️ Computing operating regions...")
        power_range = np.logspace(-15, -8, 50)
        temp_range = np.linspace(250, 400, 50)
        operating_regions = operating_regions_analysis(power_range, temp_range)
        
        # Noise Analysis
        print("📡 Analyzing noise components...")
        freq_range = np.logspace(3, 8, 100)
        noise_analysis = noise_floor_analysis(freq_range, temperature_k=300.0)
        
        # Range Analysis
        print("📏 Computing detection range...")
        range_analysis = detection_range_analysis(
            transmit_power_w=1e-6, antenna_gain_db=10.0,
            frequency_hz=3e13, receiver_sensitivity_dbm=-90.0
        )
        
        print("📈 Creating visualization...")
        # Create comprehensive figure
        fig = plt.figure(figsize=(16, 12))
        
        # ROC Curves
        ax1 = plt.subplot(3, 4, 1)
        for snr_db in snr_levels:
            roc_data = roc_results[f'snr_{snr_db}db']
            ax1.plot(roc_data['pfa'], roc_data['pd'], linewidth=2, 
                    label=f'{snr_db} dB (AUC={roc_data["auc"]:.2f})')
        ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        ax1.set_xlabel('False Alarm Probability')
        ax1.set_ylabel('Detection Probability')
        ax1.set_title('ROC Curves')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # Detection Performance vs SNR
        ax2 = plt.subplot(3, 4, 2)
        ax2.plot(detection_perf['snr_db'], detection_perf['pd'], 'b-', linewidth=2)
        ax2.axhline(y=0.9, color='r', linestyle='--', label='90% Detection')
        ax2.axvline(x=detection_perf['mds_snr_db'], color='g', linestyle='--', 
                   label=f'MDS: {detection_perf["mds_snr_db"]:.1f} dB')
        ax2.set_xlabel('SNR (dB)')
        ax2.set_ylabel('Detection Probability')
        ax2.set_title('Detection Performance')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Operating Regions
        ax3 = plt.subplot(3, 4, 3)
        power_grid = operating_regions['power_grid_w']
        temp_grid = operating_regions['temperature_grid_k']
        snr_grid = operating_regions['snr_grid_db']
        
        contour = ax3.contourf(power_grid * 1e12, temp_grid, snr_grid, 
                              levels=[-5, 0, 3, 6, 10, 15], cmap='RdYlGn')
        ax3.set_xlabel('Signal Power (pW)')
        ax3.set_ylabel('Temperature (K)')
        ax3.set_title('Operating Regions (SNR dB)')
        ax3.set_xscale('log')
        plt.colorbar(contour, ax=ax3)

        # Noise Floor Components
        ax4 = plt.subplot(3, 4, 4)
        ax4.loglog(noise_analysis['frequencies_hz'], 10**(noise_analysis['thermal_noise_db']/10), 
                  'b-', linewidth=2, label='Thermal')
        ax4.loglog(noise_analysis['frequencies_hz'], 10**(noise_analysis['total_noise_db']/10), 
                  'k-', linewidth=3, label='Total')
        ax4.set_xlabel('Frequency (Hz)')
        ax4.set_ylabel('Noise Power (W)')
        ax4.set_title('Noise Floor')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # Detection Range
        ax5 = plt.subplot(3, 4, 5)
        distances_km = range_analysis['distances_m'] / 1000
        ax5.semilogx(distances_km, range_analysis['received_power_dbm'], 'b-', linewidth=2)
        ax5.axhline(y=-90, color='r', linestyle='--', label='Sensitivity')
        max_range_km = range_analysis['max_range_atmospheric_m'] / 1000
        ax5.axvline(x=max_range_km, color='g', linestyle='--', 
                   label=f'Max: {max_range_km:.1f} km')
        ax5.set_xlabel('Distance (km)')
        ax5.set_ylabel('Received Power (dBm)')
        ax5.set_title('Detection Range')
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # Min Detectable Power vs Bandwidth
        ax6 = plt.subplot(3, 4, 6)
        bandwidth = np.logspace(3, 8, 100)
        mdp_values = min_detectable_power(300.0, bandwidth, 3.0) * 1e12
        ax6.loglog(bandwidth, mdp_values, 'purple', linewidth=2)
        ax6.set_xlabel('Bandwidth (Hz)')
        ax6.set_ylabel('Min Detectable Power (pW)')
        ax6.set_title('MDP vs Bandwidth')
        ax6.grid(True, alpha=0.3)

        # Temperature Effects
        ax7 = plt.subplot(3, 4, 7)
        temperatures = np.linspace(250, 400, 50)
        mdp_temp = [min_detectable_power(T, 1e6, 3.0) * 1e12 for T in temperatures]
        ax7.plot(temperatures, mdp_temp, 'red', linewidth=2)
        ax7.set_xlabel('Temperature (K)')
        ax7.set_ylabel('Min Detectable Power (pW)')
        ax7.set_title('Temperature Effects')
        ax7.grid(True, alpha=0.3)

        # Processing Gain
        ax8 = plt.subplot(3, 4, 8)
        integration_times = np.logspace(-3, 2, 50)
        processing_gains = 10 * np.log10(integration_times)
        effective_snr = detection_perf['mds_snr_db'] - processing_gains
        ax8.semilogx(integration_times, effective_snr, 'orange', linewidth=2)
        ax8.set_xlabel('Integration Time (s)')
        ax8.set_ylabel('Effective MDS (dB)')
        ax8.set_title('Processing Gain')
        ax8.grid(True, alpha=0.3)

        # ROC Optimal Points
        ax9 = plt.subplot(3, 4, 9)
        roc_6db = roc_results['snr_6db']
        ax9.plot(roc_6db['pfa'], roc_6db['pd'], 'b-', linewidth=2)
        ax9.plot(roc_6db['optimal_pfa'], roc_6db['optimal_pd'], 'ro', markersize=8)
        ax9.set_xlabel('False Alarm Probability')
        ax9.set_ylabel('Detection Probability')
        ax9.set_title('Optimal Operating Point (6 dB)')
        ax9.grid(True, alpha=0.3)

        # Range vs Sensitivity
        ax10 = plt.subplot(3, 4, 10)
        sensitivity_range = range_analysis['sensitivity_range_dbm']
        max_ranges_km = range_analysis['max_ranges_vs_sensitivity_m'] / 1000
        ax10.semilogx(max_ranges_km, sensitivity_range, 'mo-', linewidth=2)
        ax10.set_xlabel('Max Range (km)')
        ax10.set_ylabel('Receiver Sensitivity (dBm)')
        ax10.set_title('Sensitivity Trade-off')
        ax10.grid(True, alpha=0.3)

        # Performance Summary
        ax11 = plt.subplot(3, 4, 11)
        ax11.axis('off')
        
        best_auc = max([roc_results[key]['auc'] for key in roc_results.keys()])
        summary_text = f"""Performance Summary:

Best AUC: {best_auc:.3f}
MDS (90% PD): {detection_perf['mds_snr_db']:.1f} dB
Max Range: {max_range_km:.1f} km
Processing Gain: {detection_perf['processing_gain_db']:.1f} dB

Noise Floor: {noise_analysis['total_noise_db'][0]:.1f} dB
Temperature Impact: Linear with T
Bandwidth Impact: √BW scaling
        """
        
        ax11.text(0.05, 0.95, summary_text, transform=ax11.transAxes,
                 fontsize=10, verticalalignment='top', fontfamily='monospace')

        # Distribution Visualization
        ax12 = plt.subplot(3, 4, 12)
        from scipy.stats import norm
        x_vals = np.linspace(-3, 5, 200)
        
        # 6 dB SNR case
        roc_6db = roc_results['snr_6db']
        noise_pdf = norm.pdf(x_vals, roc_6db['noise_only_mean'], roc_6db['noise_only_std'])
        signal_pdf = norm.pdf(x_vals, roc_6db['signal_plus_noise_mean'], roc_6db['signal_plus_noise_std'])
        
        ax12.plot(x_vals, noise_pdf, 'r-', linewidth=2, label='Noise (H₀)')
        ax12.plot(x_vals, signal_pdf, 'b-', linewidth=2, label='Signal+Noise (H₁)')
        ax12.axvline(x=roc_6db['optimal_threshold'], color='g', linestyle='--', label='Threshold')
        ax12.set_xlabel('Decision Variable')
        ax12.set_ylabel('Probability Density')
        ax12.set_title('Detection Distributions (6 dB)')
        ax12.legend(fontsize=8)
        ax12.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save outputs
        out_png = os.path.join(fig_dir, "detection_limits_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        caption = f"""Comprehensive detection limits analysis: ROC curves showing AUC up to {best_auc:.3f}, detection performance with {detection_perf['mds_snr_db']:.1f} dB MDS, operating regions across power-temperature space, noise floor analysis, and detection range up to {max_range_km:.1f} km. Analysis includes processing gain benefits, optimal threshold selection, and comprehensive performance trade-offs for IR olfactory detection systems."""
        
        write_caption(os.path.join(fig_dir, "detection_limits_comprehensive_analysis.caption.txt"), caption)

        # Save data
        out_npz = os.path.join(data_dir, "detection_limits_comprehensive.npz")
        np.savez(out_npz,
                # ROC data
                roc_6db_pfa=roc_results['snr_6db']['pfa'],
                roc_6db_pd=roc_results['snr_6db']['pd'],
                roc_6db_auc=roc_results['snr_6db']['auc'],
                # Performance data
                snr_db_range=detection_perf['snr_db'],
                detection_probability=detection_perf['pd'],
                mds_snr_db=detection_perf['mds_snr_db'],
                # Operating regions
                power_grid=operating_regions['power_grid_w'],
                temperature_grid=operating_regions['temperature_grid_k'],
                snr_grid=operating_regions['snr_grid_db'],
                # Range analysis
                max_range_atmospheric_m=range_analysis['max_range_atmospheric_m'],
                received_power_dbm=range_analysis['received_power_dbm'],
                # Noise analysis
                frequencies_hz=noise_analysis['frequencies_hz'],
                total_noise_db=noise_analysis['total_noise_db'])

        print(f"✅ Success! Generated detection limits analysis")
        print(f"Generated: {out_png}")
        print(f"Best AUC: {best_auc:.3f}")
        print(f"MDS: {detection_perf['mds_snr_db']:.1f} dB")
        print(f"Max range: {max_range_km:.1f} km")
        print(out_png)
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
