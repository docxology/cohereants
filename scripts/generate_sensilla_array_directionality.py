#!/usr/bin/env python3
"""Generate comprehensive sensilla array directionality analysis.

Comprehensive electromagnetic modeling of sensilla arrays with multiple geometries,
coupling effects, morphological analysis, and frequency response characteristics.
"""
from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption

ensure_src_on_path()
from src.case_studies.sensilla_array_directionality import (
    design_log_periodic_array,
    design_circular_array,
    compute_beam_pattern,
    array_gain,
    array_pattern_2d,
    analyze_sensilla_morphology,
    frequency_response_analysis,
    sensilla_element_pattern,
    mutual_coupling_matrix
)


def main() -> int:
    """Generate comprehensive sensilla array electromagnetic analysis."""
    try:
        print("🔄 Starting comprehensive sensilla array analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()
        
        # Set deterministic seed for reproducible analysis
        np.random.seed(42)
        
        print("📊 Computing array geometries and patterns...")
        
        # Analysis parameters
        wavelengths = np.linspace(2.0, 25.0, 200)
        ir_wavelengths = np.array([2.5, 5.0, 10.0, 15.0, 20.0])  # Key IR bands
        
        # 1. Log-periodic array analysis
        log_positions = design_log_periodic_array(min_len_um=1.0, max_len_um=200.0, tau=1.3, count=8)
        log_pattern = compute_beam_pattern(wavelengths, log_positions, np.ones_like(log_positions))
        log_gain = array_gain(log_pattern['pattern'])

        # 2. Circular array analysis 
        circular_array = design_circular_array(radius_um=50.0, count=12, phase_center=True)
        circ_positions = np.column_stack([circular_array['x_positions'], circular_array['y_positions']])
        circ_weights = np.ones(len(circular_array['x_positions']), dtype=complex)
        
        print("🔬 Analyzing sensilla morphology...")
        # 3. Morphological analysis of sensilla dimensions
        n_sensilla = 50
        sensilla_lengths = np.random.lognormal(mean=2.5, sigma=0.6, size=n_sensilla)  
        sensilla_diameters = sensilla_lengths * np.random.uniform(0.1, 0.3, n_sensilla)  
        
        morphology_analysis = analyze_sensilla_morphology(
            sensilla_lengths, sensilla_diameters, ir_wavelengths
        )
        
        print("📡 Computing frequency response...")
        # 4. Frequency response analysis
        array_geometry = {'positions': circ_positions}
        freq_response = frequency_response_analysis(
            array_geometry, 
            frequency_range_thz=(10, 150),  # 2-30 μm wavelength range
            n_frequencies=150,
            medium_permittivity=2.3  # Typical insect cuticle
        )
        
        print("📐 Analyzing element patterns and coupling...")
        # 5. Element pattern comparison
        angles = np.linspace(0, 180, 181)
        dipole_pattern = sensilla_element_pattern(angles, 10.0, 10.0, 'dipole')
        monopole_pattern = sensilla_element_pattern(angles, 10.0, 10.0, 'monopole')
        patch_pattern = sensilla_element_pattern(angles, 10.0, 10.0, 'patch')
        
        # 6. Mutual coupling analysis
        coupling_matrix = mutual_coupling_matrix(circ_positions, 10.0, coupling_strength=0.2)
        
        print("📈 Creating comprehensive visualization...")
        # Generate comprehensive visualization
        fig = plt.figure(figsize=(16, 12))
        
        # Subplot 1: Array beam patterns comparison
        ax1 = plt.subplot(3, 3, 1)
        ax1.plot(wavelengths, log_pattern['pattern'], 'b-', linewidth=2, label=f'Log-periodic (G={log_gain:.1f})')
        ax1.axvspan(2, 5, alpha=0.2, color='red', label='2-5 μm window')
        ax1.axvspan(8, 14, alpha=0.2, color='green', label='8-14 μm window')
        ax1.axvspan(17, 25, alpha=0.2, color='blue', label='17-25 μm window')
        ax1.set_xlabel('Wavelength (μm)')
        ax1.set_ylabel('Normalized Power')
        ax1.set_title('Array Beam Patterns vs Atmospheric Windows')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=8)
        ax1.set_xlim(2, 25)

        # Subplot 2: Sensilla morphology analysis
        ax2 = plt.subplot(3, 3, 2)
        scatter = ax2.scatter(morphology_analysis['sensilla_lengths_um'], 
                             morphology_analysis['best_wavelength_matches'], 
                             c=morphology_analysis['match_quality_scores'],
                             cmap='viridis', s=30, alpha=0.7)
        ax2.plot(morphology_analysis['sensilla_lengths_um'], 
                 morphology_analysis['quarter_wave_resonances_um'], 
                 'r--', alpha=0.5, label='λ/4 resonance')
        ax2.plot(morphology_analysis['sensilla_lengths_um'], 
                 morphology_analysis['half_wave_resonances_um'], 
                 'b--', alpha=0.5, label='λ/2 resonance')
        ax2.set_xlabel('Sensilla Length (μm)')
        ax2.set_ylabel('Best Match Wavelength (μm)')
        ax2.set_title('Morphology-Wavelength Matching')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label='Match Quality')

        # Subplot 3: Frequency response
        ax3 = plt.subplot(3, 3, 3)
        ax3.plot(freq_response['frequencies_thz'], freq_response['gain_db'], 'g-', linewidth=2)
        if len(freq_response['resonance_frequencies_thz']) > 0:
            # Find closest indices for resonance frequencies
            resonance_indices = []
            for rf in freq_response['resonance_frequencies_thz']:
                closest_idx = np.argmin(np.abs(freq_response['frequencies_thz'] - rf))
                resonance_indices.append(closest_idx)
            ax3.scatter(freq_response['resonance_frequencies_thz'], 
                       freq_response['gain_db'][resonance_indices], 
                       color='red', s=50, label='Resonances', zorder=5)
        ax3.set_xlabel('Frequency (THz)')
        ax3.set_ylabel('Gain (dB)')
        ax3.set_title(f'Frequency Response (BW={freq_response["bandwidth_3db_thz"]:.1f} THz)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Subplot 4: Element patterns comparison
        ax4 = plt.subplot(3, 3, 4)
        ax4.plot(angles, dipole_pattern, 'b-', linewidth=2, label='Dipole')
        ax4.plot(angles, monopole_pattern, 'r-', linewidth=2, label='Monopole')
        ax4.plot(angles, patch_pattern, 'g-', linewidth=2, label='Patch')
        ax4.set_xlabel('Angle (degrees)')
        ax4.set_ylabel('Normalized Pattern')
        ax4.set_title('Individual Element Patterns')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # Subplot 5: Array geometry visualization
        ax5 = plt.subplot(3, 3, 5)
        ax5.scatter(circ_positions[:, 0], circ_positions[:, 1], c='blue', s=60, alpha=0.7, label='Circular')
        ax5.scatter(log_positions, np.zeros_like(log_positions), c='red', s=60, marker='s', alpha=0.7, label='Log-periodic')
        ax5.set_xlabel('X Position (μm)')
        ax5.set_ylabel('Y Position (μm)')
        ax5.set_title('Array Geometries')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.axis('equal')

        # Subplot 6: Coupling matrix visualization
        ax6 = plt.subplot(3, 3, 6)
        coupling_mag = np.abs(coupling_matrix)
        im = ax6.imshow(coupling_mag, cmap='hot', interpolation='nearest')
        ax6.set_xlabel('Element Index')
        ax6.set_ylabel('Element Index') 
        ax6.set_title('Mutual Coupling Magnitude')
        plt.colorbar(im, ax=ax6, label='|Z| (normalized)')

        # Subplot 7: Quality factors vs aspect ratio
        ax7 = plt.subplot(3, 3, 7)
        ax7.scatter(morphology_analysis['aspect_ratios'], morphology_analysis['q_factors'], 
                   c=morphology_analysis['match_quality_scores'], cmap='plasma', s=30, alpha=0.7)
        ax7.set_xlabel('Length/Diameter Ratio')
        ax7.set_ylabel('Estimated Q Factor')
        ax7.set_title('Q Factor vs Aspect Ratio')
        ax7.grid(True, alpha=0.3)

        # Subplot 8: Impedance characteristics
        ax8 = plt.subplot(3, 3, 8)
        ax8.plot(freq_response['frequencies_thz'], freq_response['impedance_real'], 'b-', label='Real')
        ax8.plot(freq_response['frequencies_thz'], freq_response['impedance_imag'], 'r-', label='Imaginary')
        ax8.set_xlabel('Frequency (THz)')
        ax8.set_ylabel('Impedance (normalized)')
        ax8.set_title('Input Impedance vs Frequency')
        ax8.legend()
        ax8.grid(True, alpha=0.3)

        # Subplot 9: Wavelength distribution analysis
        ax9 = plt.subplot(3, 3, 9)
        ax9.hist(morphology_analysis['best_wavelength_matches'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        ax9.axvspan(2, 5, alpha=0.3, color='red', label='2-5 μm')
        ax9.axvspan(8, 14, alpha=0.3, color='green', label='8-14 μm') 
        ax9.axvspan(17, 25, alpha=0.3, color='blue', label='17-25 μm')
        ax9.set_xlabel('Best Match Wavelength (μm)')
        ax9.set_ylabel('Count')
        ax9.set_title('Wavelength Distribution')
        ax9.legend(fontsize=8)
        ax9.grid(True, alpha=0.3)

        plt.tight_layout()

        print("💾 Saving comprehensive analysis...")
        # Save comprehensive figure
        out_png = os.path.join(fig_dir, "sensilla_array_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        # Calculate correlation coefficient
        morph_correlation = np.corrcoef(morphology_analysis['sensilla_lengths_um'], 
                                      morphology_analysis['best_wavelength_matches'])[0,1]

        # Generate detailed caption
        caption = f"""Comprehensive sensilla array electromagnetic analysis: (1) Beam patterns showing correlation with atmospheric transmission windows; (2) Morphological analysis of {n_sensilla} simulated sensilla showing wavelength-length correlations (r={morph_correlation:.3f}); (3) Frequency response with {len(freq_response['resonance_frequencies_thz'])} identified resonances and {freq_response['bandwidth_3db_thz']:.1f} THz bandwidth; (4) Element pattern comparison showing directional characteristics; (5) Array geometry visualization; (6) Mutual coupling analysis; (7) Q-factor scaling with aspect ratio; (8) Impedance characteristics; (9) Wavelength matching distribution across atmospheric windows."""
        
        write_caption(os.path.join(fig_dir, "sensilla_array_comprehensive_analysis.caption.txt"), caption)

        # Save comprehensive data
        out_npz = os.path.join(data_dir, "sensilla_array_comprehensive.npz")
        np.savez(out_npz,
                 # Array geometries
                 log_positions=log_positions,
                 circular_positions=circ_positions,
                 # Beam patterns
                 wavelengths=wavelengths,
                 log_pattern=log_pattern['pattern'],
                 log_gain=log_gain,
                 # Morphology analysis
                 sensilla_lengths=morphology_analysis['sensilla_lengths_um'],
                 sensilla_diameters=morphology_analysis['sensilla_diameters_um'],
                 wavelength_matching_matrix=morphology_analysis['wavelength_matching_matrix'],
                 best_wavelength_matches=morphology_analysis['best_wavelength_matches'],
                 match_quality_scores=morphology_analysis['match_quality_scores'],
                 q_factors=morphology_analysis['q_factors'],
                 # Frequency response
                 frequencies_thz=freq_response['frequencies_thz'],
                 gain_db=freq_response['gain_db'],
                 impedance_real=freq_response['impedance_real'],
                 impedance_imag=freq_response['impedance_imag'],
                 resonance_frequencies=freq_response['resonance_frequencies_thz'],
                 bandwidth_3db=freq_response['bandwidth_3db_thz'],
                 # Element patterns
                 angles=angles,
                 dipole_pattern=dipole_pattern,
                 monopole_pattern=monopole_pattern,
                 patch_pattern=patch_pattern,
                 # Coupling matrix
                 coupling_matrix_magnitude=np.abs(coupling_matrix))

        print(f"✅ Success! Generated comprehensive analysis")
        print(f"Generated: {out_png}")
        print(f"Generated: {out_npz}")
        print(f"Analysis summary:")
        print(f"  - Log-periodic array gain: {log_gain:.2f}")
        print(f"  - Circular array elements: {len(circ_positions)}")
        print(f"  - Frequency bandwidth: {freq_response['bandwidth_3db_thz']:.1f} THz")
        print(f"  - Average Q factor: {freq_response['q_factor_avg']:.1f}")
        print(f"  - Morphology correlation: {morph_correlation:.3f}")

        print(out_png)
        return 0

    except Exception as e:
        print(f"❌ Error generating sensilla array analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())