#!/usr/bin/env python3
"""Generate comprehensive plasmonic nanoparticle analysis.

Comprehensive electromagnetic modeling of plasmonic nanostructures with
resonance analysis, field enhancement, coupling effects, and optimization.
"""
from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption

ensure_src_on_path()
from src.case_studies.plasmonic_geometry import (
    sweep_plasmonic_quality,
    mie_scattering_sphere,
    drude_model_permittivity,
    optimize_plasmonic_geometry,
    coupled_dipoles_near_field,
    field_distribution_near_particle
)


def main() -> int:
    """Generate comprehensive plasmonic nanoparticle electromagnetic analysis."""
    try:
        print("🔄 Starting comprehensive plasmonic analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()
        
        # Set deterministic seed for reproducible analysis
        np.random.seed(42)
        
        print("📊 Computing plasmonic parameter sweeps...")
        
        # Analysis parameters
        radii_nm = np.linspace(5, 100, 50)
        wavelengths_um = np.linspace(2.0, 25.0, 200)
        ir_wavelengths = np.array([3.0, 5.0, 10.0, 15.0, 20.0])  # Key IR bands
        
        # 1. Comprehensive quality factor sweep
        sweep_gold = sweep_plasmonic_quality(radii_nm, wavelengths_um, 'gold', 2.25)
        sweep_silver = sweep_plasmonic_quality(radii_nm, wavelengths_um, 'silver', 2.25)
        
        print("🎯 Optimizing geometries for IR wavelengths...")
        # 2. Geometry optimization for each IR wavelength
        optimized_geometries = {}
        for material in ['gold', 'silver']:
            optimized_geometries[material] = []
            for wl in ir_wavelengths:
                opt_result = optimize_plasmonic_geometry(
                    wl, 'sphere', material, 2.25, (5.0, 100.0)
                )
                optimized_geometries[material].append(opt_result)
        
        print("🔬 Analyzing material permittivity...")
        # 3. Material permittivity analysis
        gold_epsilon = drude_model_permittivity(wavelengths_um, 0.138, 27.0)
        silver_epsilon = drude_model_permittivity(wavelengths_um, 0.137, 17.0)
        
        print("🌐 Computing near-field coupling...")
        # 4. Coupled nanoparticle analysis
        # Create a small cluster of particles
        positions_nm = np.array([[0, 0, 0], [30, 0, 0], [15, 26, 0]])  # Triangular arrangement
        coupling_wavelength = 10.0  # μm
        gold_eps_at_10um = drude_model_permittivity(np.array([10.0]), 0.138, 27.0)[0]
        
        coupling_analysis = coupled_dipoles_near_field(
            positions_nm, 25.0, coupling_wavelength, gold_eps_at_10um, 2.25
        )
        
        print("📡 Computing field distributions...")
        # 5. Near-field distribution around optimized particle
        optimal_radius = optimized_geometries['gold'][2]['optimal_size_nm']  # 10 μm optimization
        field_dist = field_distribution_near_particle(
            optimal_radius, 10.0, gold_eps_at_10um, 2.25, 300.0, 80
        )
        
        print("📈 Creating comprehensive visualization...")
        # Generate comprehensive visualization
        fig = plt.figure(figsize=(18, 14))
        
        # Subplot 1: Quality factor sweep (2D heatmap)
        ax1 = plt.subplot(3, 4, 1)
        im1 = ax1.imshow(sweep_gold['q_factors_2d'], aspect='auto', origin='lower',
                        extent=[wavelengths_um[0], wavelengths_um[-1], radii_nm[0], radii_nm[-1]])
        ax1.set_xlabel('Wavelength (μm)')
        ax1.set_ylabel('Radius (nm)')
        ax1.set_title('Gold Q-Factor Map')
        plt.colorbar(im1, ax=ax1, label='Q Factor')
        
        # Add atmospheric windows
        ax1.axvspan(2, 5, alpha=0.3, color='red')
        ax1.axvspan(8, 14, alpha=0.3, color='green')
        ax1.axvspan(17, 25, alpha=0.3, color='blue')

        # Subplot 2: Enhancement factor sweep (2D heatmap)  
        ax2 = plt.subplot(3, 4, 2)
        im2 = ax2.imshow(np.log10(sweep_gold['enhancements_2d']), aspect='auto', origin='lower',
                        extent=[wavelengths_um[0], wavelengths_um[-1], radii_nm[0], radii_nm[-1]])
        ax2.set_xlabel('Wavelength (μm)')
        ax2.set_ylabel('Radius (nm)')
        ax2.set_title('Gold Enhancement (log₁₀)')
        plt.colorbar(im2, ax=ax2, label='log₁₀(Enhancement)')
        ax2.axvspan(2, 5, alpha=0.3, color='red')
        ax2.axvspan(8, 14, alpha=0.3, color='green')
        ax2.axvspan(17, 25, alpha=0.3, color='blue')

        # Subplot 3: Material comparison - permittivity
        ax3 = plt.subplot(3, 4, 3)
        ax3.plot(wavelengths_um, gold_epsilon.real, 'b-', linewidth=2, label='Gold Re(ε)')
        ax3.plot(wavelengths_um, gold_epsilon.imag, 'b--', linewidth=2, label='Gold Im(ε)')
        ax3.plot(wavelengths_um, silver_epsilon.real, 'r-', linewidth=2, label='Silver Re(ε)')
        ax3.plot(wavelengths_um, silver_epsilon.imag, 'r--', linewidth=2, label='Silver Im(ε)')
        ax3.set_xlabel('Wavelength (μm)')
        ax3.set_ylabel('Permittivity')
        ax3.set_title('Material Permittivity (Drude)')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(2, 25)

        # Subplot 4: Resonance wavelengths vs size
        ax4 = plt.subplot(3, 4, 4)
        ax4.plot(radii_nm, sweep_gold['resonance_wavelengths'], 'o-', color='gold', 
                linewidth=2, markersize=4, label='Gold')
        ax4.plot(radii_nm, sweep_silver['resonance_wavelengths'], 's-', color='silver',
                linewidth=2, markersize=4, label='Silver')
        ax4.axhspan(2, 5, alpha=0.2, color='red', label='2-5 μm')
        ax4.axhspan(8, 14, alpha=0.2, color='green', label='8-14 μm')
        ax4.axhspan(17, 25, alpha=0.2, color='blue', label='17-25 μm')
        ax4.set_xlabel('Radius (nm)')
        ax4.set_ylabel('Resonance Wavelength (μm)')
        ax4.set_title('Resonance vs Size')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3)

        # Subplot 5: Optimization results
        ax5 = plt.subplot(3, 4, 5)
        gold_opt_sizes = [opt['optimal_size_nm'] for opt in optimized_geometries['gold']]
        gold_opt_enhancements = [opt['max_enhancement'] for opt in optimized_geometries['gold']]
        silver_opt_sizes = [opt['optimal_size_nm'] for opt in optimized_geometries['silver']]
        silver_opt_enhancements = [opt['max_enhancement'] for opt in optimized_geometries['silver']]
        
        ax5.scatter(ir_wavelengths, gold_opt_sizes, c='gold', s=100, alpha=0.8, 
                   label='Gold Optimal Size')
        ax5.scatter(ir_wavelengths, silver_opt_sizes, c='silver', s=100, alpha=0.8, 
                   label='Silver Optimal Size')
        ax5.set_xlabel('Target Wavelength (μm)')
        ax5.set_ylabel('Optimal Radius (nm)')
        ax5.set_title('Optimized Geometries')
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # Subplot 6: Enhancement factors for optimized geometries
        ax6 = plt.subplot(3, 4, 6)
        ax6.bar(ir_wavelengths - 0.2, gold_opt_enhancements, 0.4, 
               color='gold', alpha=0.7, label='Gold')
        ax6.bar(ir_wavelengths + 0.2, silver_opt_enhancements, 0.4,
               color='silver', alpha=0.7, label='Silver')
        ax6.set_xlabel('Target Wavelength (μm)')
        ax6.set_ylabel('Max Enhancement Factor')
        ax6.set_title('Optimized Enhancement')
        ax6.legend()
        ax6.grid(True, alpha=0.3)

        # Subplot 7: Coupled particle geometry
        ax7 = plt.subplot(3, 4, 7)
        ax7.scatter(positions_nm[:, 0], positions_nm[:, 1], c='red', s=200, alpha=0.7)
        for i, pos in enumerate(positions_nm):
            ax7.annotate(f'P{i+1}', (pos[0], pos[1]), xytext=(5, 5), 
                        textcoords='offset points', fontsize=10)
        ax7.set_xlabel('X Position (nm)')
        ax7.set_ylabel('Y Position (nm)')
        ax7.set_title('Coupled Particle Geometry')
        ax7.axis('equal')
        ax7.grid(True, alpha=0.3)

        # Subplot 8: Coupling enhancement ratios
        ax8 = plt.subplot(3, 4, 8)
        particle_indices = np.arange(len(coupling_analysis['enhancement_ratio']))
        ax8.bar(particle_indices, coupling_analysis['enhancement_ratio'], 
               color=['red', 'green', 'blue'], alpha=0.7)
        ax8.set_xlabel('Particle Index')
        ax8.set_ylabel('Enhancement Ratio')
        ax8.set_title(f'Coupling Enhancement\n(Max: {np.max(coupling_analysis["enhancement_ratio"]):.1f}×)')
        ax8.grid(True, alpha=0.3)

        # Subplot 9: Near-field intensity distribution
        ax9 = plt.subplot(3, 4, 9)
        extent = [-field_dist['x_nm'][-1], field_dist['x_nm'][-1], 
                 -field_dist['y_nm'][-1], field_dist['y_nm'][-1]]
        im9 = ax9.imshow(field_dist['intensity'], extent=extent, origin='lower', 
                        cmap='hot', interpolation='bilinear')
        
        # Add particle boundary
        circle = plt.Circle((0, 0), optimal_radius, fill=False, color='white', linewidth=2)
        ax9.add_patch(circle)
        ax9.set_xlabel('X Position (nm)')
        ax9.set_ylabel('Y Position (nm)')
        ax9.set_title(f'Near-Field Intensity\n(Max: {field_dist["max_enhancement"]:.1f}×)')
        plt.colorbar(im9, ax=ax9, label='|E|²')

        # Subplot 10: Silver Q-factor comparison
        ax10 = plt.subplot(3, 4, 10)
        im10 = ax10.imshow(sweep_silver['q_factors_2d'], aspect='auto', origin='lower',
                          extent=[wavelengths_um[0], wavelengths_um[-1], radii_nm[0], radii_nm[-1]])
        ax10.set_xlabel('Wavelength (μm)')
        ax10.set_ylabel('Radius (nm)')
        ax10.set_title('Silver Q-Factor Map')
        plt.colorbar(im10, ax=ax10, label='Q Factor')
        ax10.axvspan(2, 5, alpha=0.3, color='red')
        ax10.axvspan(8, 14, alpha=0.3, color='green')
        ax10.axvspan(17, 25, alpha=0.3, color='blue')

        # Subplot 11: Max enhancement comparison
        ax11 = plt.subplot(3, 4, 11)
        ax11.plot(radii_nm, sweep_gold['max_enhancements'], 'o-', color='gold', 
                 linewidth=2, label='Gold')
        ax11.plot(radii_nm, sweep_silver['max_enhancements'], 's-', color='silver',
                 linewidth=2, label='Silver')
        ax11.set_xlabel('Radius (nm)')
        ax11.set_ylabel('Max Enhancement Factor')
        ax11.set_title('Peak Enhancement vs Size')
        ax11.legend()
        ax11.grid(True, alpha=0.3)
        ax11.set_yscale('log')

        # Subplot 12: Quality factor comparison at optimal wavelengths
        ax12 = plt.subplot(3, 4, 12)
        gold_q_at_opt = []
        silver_q_at_opt = []
        for opt_gold, opt_silver in zip(optimized_geometries['gold'], optimized_geometries['silver']):
            gold_q_at_opt.append(opt_gold['resonance_quality'])
            silver_q_at_opt.append(opt_silver['resonance_quality'])
        
        ax12.plot(ir_wavelengths, gold_q_at_opt, 'o-', color='gold', linewidth=2, 
                 markersize=8, label='Gold')
        ax12.plot(ir_wavelengths, silver_q_at_opt, 's-', color='silver', linewidth=2,
                 markersize=8, label='Silver')
        ax12.set_xlabel('Target Wavelength (μm)')
        ax12.set_ylabel('Quality Factor')
        ax12.set_title('Q-Factor at Optimized Sizes')
        ax12.legend()
        ax12.grid(True, alpha=0.3)

        plt.tight_layout()

        print("💾 Saving comprehensive analysis...")
        # Save comprehensive figure
        out_png = os.path.join(fig_dir, "plasmonic_geometry_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        # Generate detailed caption
        max_gold_enhancement = np.max(sweep_gold['max_enhancements'])
        max_silver_enhancement = np.max(sweep_silver['max_enhancements'])
        avg_coupling_enhancement = np.mean(coupling_analysis['enhancement_ratio'])
        
        caption = f"""Comprehensive plasmonic nanoparticle electromagnetic analysis: (1-2) Q-factor and enhancement maps showing resonance optimization across size-wavelength parameter space; (3) Drude model permittivity for gold and silver across IR spectrum; (4) Resonance wavelength scaling with particle size; (5-6) Geometry optimization results for key IR wavelengths showing optimal sizes and maximum enhancements; (7-8) Coupled particle analysis with triangular arrangement showing {avg_coupling_enhancement:.1f}× average coupling enhancement; (9) Near-field intensity distribution with {field_dist['max_enhancement']:.0f}× peak enhancement; (10-12) Material comparison showing silver achieving {max_silver_enhancement:.0f}× vs gold's {max_gold_enhancement:.0f}× maximum enhancement factors."""
        
        write_caption(os.path.join(fig_dir, "plasmonic_geometry_comprehensive_analysis.caption.txt"), caption)

        # Save comprehensive data
        out_npz = os.path.join(data_dir, "plasmonic_geometry_comprehensive.npz")
        np.savez(out_npz,
                 # Parameter sweeps
                 radii_nm=radii_nm,
                 wavelengths_um=wavelengths_um,
                 ir_wavelengths=ir_wavelengths,
                 # Gold results
                 gold_q_factors_2d=sweep_gold['q_factors_2d'],
                 gold_enhancements_2d=sweep_gold['enhancements_2d'],
                 gold_resonance_wavelengths=sweep_gold['resonance_wavelengths'],
                 gold_max_enhancements=sweep_gold['max_enhancements'],
                 # Silver results
                 silver_q_factors_2d=sweep_silver['q_factors_2d'],
                 silver_enhancements_2d=sweep_silver['enhancements_2d'],
                 silver_resonance_wavelengths=sweep_silver['resonance_wavelengths'],
                 silver_max_enhancements=sweep_silver['max_enhancements'],
                 # Material properties
                 gold_permittivity=gold_epsilon,
                 silver_permittivity=silver_epsilon,
                 # Optimization results
                 gold_optimal_sizes=gold_opt_sizes,
                 gold_optimal_enhancements=gold_opt_enhancements,
                 silver_optimal_sizes=silver_opt_sizes,
                 silver_optimal_enhancements=silver_opt_enhancements,
                 # Coupling analysis
                 coupling_positions=positions_nm,
                 coupling_enhancement_ratios=coupling_analysis['enhancement_ratio'],
                 coupling_strength=coupling_analysis['coupling_strength'],
                 # Near-field distribution
                 field_x_nm=field_dist['x_nm'],
                 field_y_nm=field_dist['y_nm'],
                 field_intensity=field_dist['intensity'],
                 field_max_enhancement=field_dist['max_enhancement'])

        print(f"✅ Success! Generated comprehensive plasmonic analysis")
        print(f"Generated: {out_png}")
        print(f"Generated: {out_npz}")
        print(f"Analysis summary:")
        print(f"  - Gold max enhancement: {max_gold_enhancement:.0f}×")
        print(f"  - Silver max enhancement: {max_silver_enhancement:.0f}×")
        print(f"  - Coupling enhancement: {avg_coupling_enhancement:.1f}× average")
        print(f"  - Near-field peak: {field_dist['max_enhancement']:.0f}×")
        print(f"  - Optimal radius range: {min(gold_opt_sizes):.1f}-{max(gold_opt_sizes):.1f} nm")

        print(out_png)
        return 0

    except Exception as e:
        print(f"❌ Error generating plasmonic analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())