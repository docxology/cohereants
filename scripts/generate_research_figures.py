#!/usr/bin/env python3
"""Generate comprehensive research figures for the manuscript.

Thin orchestrator that composes figures using src/ business logic only.
Figures:
- Atmospheric transmission windows (uses src.core)
- Sensilla wavelength matching (uses src.sensilla)
- Example CHC spectra (uses src.spectroscopy)
- Response time comparison (domain summary)
- Composite multi-panel synthesis figure (uses src.visualization)
"""
from __future__ import annotations

import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, List, Dict


def _ensure_src_on_path() -> None:
    """Ensure src/ is on Python path for imports."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # Prefer adding the repository root so we can import using the "src." package prefix
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


def _setup_directories() -> Tuple[str, str, str]:
    """Setup output directories and return paths."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(repo_root, "output")
    data_dir = os.path.join(output_dir, "data")
    figure_dir = os.path.join(output_dir, "figures")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figure_dir, exist_ok=True)
    
    return output_dir, data_dir, figure_dir


# Note: The convergence plot from the previous template is intentionally
# omitted to keep figures domain-relevant for insect IR sensing.


# Removed legacy experimental_setup figure generation (template holdover)


def generate_atmospheric_transmission_plot(figure_dir: str, data_dir: str) -> str:
    """Generate atmospheric transmission plot showing IR windows using src.core."""
    from src.core import calculate_atmospheric_transmission

    wavelengths = np.linspace(1, 30, 1000)
    transmission = calculate_atmospheric_transmission(wavelengths)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(wavelengths, transmission, 'b-', linewidth=2, label='Atmospheric Transmission')
    ax.axvspan(2, 5, alpha=0.3, color='green', label='Mid-IR Window (2-5 μm)')
    ax.axvspan(8, 14, alpha=0.3, color='orange', label='Long-wave IR Window (8-14 μm)')
    ax.axvspan(17, 25, alpha=0.3, color='red', label='Far-IR Window (17-25 μm)')
    ax.set_xlabel('Wavelength (μm)')
    ax.set_ylabel('Transmission')
    ax.set_title('Atmospheric Infrared Transmission Windows')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.1)

    figure_path = os.path.join(figure_dir, "atmospheric_transmission.png")
    fig.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    # save data
    np.savez(os.path.join(data_dir, "atmospheric_transmission.npz"), wavelengths=wavelengths, transmission=transmission)
    # save caption
    with open(os.path.join(figure_dir, "atmospheric_transmission.caption.txt"), "w") as cf:
        cf.write("Atmospheric IR transmission windows computed via src.core.calculate_atmospheric_transmission across 1–30 μm.")
    return figure_path


def generate_sensilla_wavelength_matching(figure_dir: str, data_dir: str) -> str:
    """Generate plot showing sensilla dimensions vs optimal wavelengths using src.sensilla."""
    from src.sensilla import analyze_sensilla_dimensions

    lengths = [6, 12, 25, 50, 100, 160]
    diameters = [1, 2, 3, 4, 5, 6]
    analysis = analyze_sensilla_dimensions(lengths, diameters)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(diameters, lengths, s=100, alpha=0.7, color='blue')
    ax1.set_xlabel('Diameter (μm)')
    ax1.set_ylabel('Length (μm)')
    ax1.set_title('Insect Sensilla Dimensions')
    ax1.grid(True, alpha=0.3)

    ax2.hist(analysis['optimal_wavelengths_quarter'], bins=15, alpha=0.7, label='1/4 λ resonance', color='blue')
    ax2.hist(analysis['optimal_wavelengths_half'], bins=15, alpha=0.7, label='1/2 λ resonance', color='red')
    ax2.set_xlabel('Wavelength (μm)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Optimal Detection Wavelengths')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    figure_path = os.path.join(figure_dir, "sensilla_wavelength_matching.png")
    fig.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    np.savez(os.path.join(data_dir, "sensilla_data.npz"), lengths=lengths, diameters=diameters)
    with open(os.path.join(figure_dir, "sensilla_wavelength_matching.caption.txt"), "w") as cf:
        cf.write("Sensilla dimensions and implied quarter/half-wavelength resonances via src.sensilla.analyze_sensilla_dimensions.")
    return figure_path


def generate_chc_spectra_example(figure_dir: str, data_dir: str) -> str:
    """Generate example CHC infrared spectra."""
    # Use deterministic synthetic spectrum for demonstration
    wavenumbers = np.linspace(1200, 3400, 1200)
    ch_peak = 2900
    ch_intensity = 1.0
    ch_bend_peak = 1465
    ch_bend_intensity = 0.6
    intensities = np.zeros_like(wavenumbers)
    intensities += ch_intensity * np.exp(-((wavenumbers - ch_peak) / 50) ** 2)
    intensities += ch_bend_intensity * np.exp(-((wavenumbers - ch_bend_peak) / 35) ** 2)
    rng = np.random.default_rng(42)
    intensities += 0.03 * rng.standard_normal(len(intensities))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(wavenumbers, intensities, 'b-', linewidth=2)
    # Add automatic peak annotations
    try:
        peak_indices = np.argpartition(intensities, -3)[-3:]
        for idx in sorted(peak_indices):
            ax.plot(wavenumbers[idx], intensities[idx], 'ro', markersize=5)
            ax.annotate(f"{int(wavenumbers[idx])} cm⁻¹", (wavenumbers[idx], intensities[idx]),
                        textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
    except Exception:
        pass
    ax.set_xlabel('Wavenumber (cm⁻¹)')
    ax.set_ylabel('Absorbance')
    ax.set_title('Example Cuticular Hydrocarbon Infrared Spectrum')
    ax.grid(True, alpha=0.3)
    ax.axvspan(2800, 3000, alpha=0.2, color='green', label='C-H Stretch Region')
    ax.axvspan(1400, 1500, alpha=0.2, color='orange', label='C-H Bend Region')
    ax.legend()

    figure_path = os.path.join(figure_dir, "chc_spectra_example.png")
    fig.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    with open(os.path.join(figure_dir, "chc_spectra_example.caption.txt"), "w") as cf:
        cf.write("Deterministic synthetic CHC spectrum with C–H stretch and bend regions for illustration.")
    return figure_path


def generate_response_time_comparison(figure_dir: str, data_dir: str) -> str:
    """Generate comparison of response times across different sensory modalities."""
    modalities = ['Insect ORNs', 'Insect Photoreceptors', 'Insect Auditory', 'Traditional Olfaction']
    response_times = [2.5, 0.1, 0.16, 10.0]
    colors = ['blue', 'green', 'orange', 'red']
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(modalities, response_times, color=colors, alpha=0.7)
    # Add improvement annotations vs traditional olfaction
    try:
        baseline = response_times[-1]
        for i, m in enumerate(modalities[:-1]):
            factor = baseline / response_times[i]
            ax.text(i, response_times[i] + 0.3, f"×{factor:.1f}", ha='center', fontsize=9)
    except Exception:
        pass
    ax.set_ylabel('Response Time (ms)')
    ax.set_title('Response Time Comparison Across Sensory Modalities')
    ax.grid(True, alpha=0.3, axis='y')
    for bar, time in zip(bars, response_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1, f'{time:.1f}', ha='center', va='bottom')
    plt.xticks(rotation=45, ha='right')
    figure_path = os.path.join(figure_dir, "response_time_comparison.png")
    fig.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    with open(os.path.join(figure_dir, "response_time_comparison.caption.txt"), "w") as cf:
        cf.write("Response time comparison across sensory modalities.")
    return figure_path


def generate_composite_multipanel(figure_dir: str) -> str:
    """Generate a composite multi-panel figure using src.visualization and src modules."""
    # Import visualization orchestrator utilities
    from src.visualization import AdvancedVisualizer
    from src.core import calculate_atmospheric_transmission
    from src.sensilla import analyze_sensilla_dimensions

    visualizer = AdvancedVisualizer(style='science')

    # Panel A: Atmospheric transmission
    wavelengths = np.linspace(1, 30, 400)
    transmission = calculate_atmospheric_transmission(wavelengths)

    # Panel B: Sensilla quarter/half wavelength hist data
    lengths = np.array([6, 12, 25, 50, 100, 160], dtype=float)
    diameters = np.array([1, 2, 3, 4, 5, 6], dtype=float)
    sens = analyze_sensilla_dimensions(lengths.tolist(), diameters.tolist())

    # Panel C: CHC synthetic region intensity histogram (reuse from above generator)
    wavenumbers = np.linspace(1200, 3400, 1200)
    ch_peak = 2900
    ch_bend_peak = 1465
    intensities = np.exp(-((wavenumbers - ch_peak) / 50) ** 2) + 0.6 * np.exp(-((wavenumbers - ch_bend_peak) / 35) ** 2)

    # Compose data dict for plot_multi_panel_analysis
    data_dict: Dict[str, Dict] = {
        'Atmospheric Transmission': {
            'x': wavelengths,
            'y': transmission,
            'xlabel': 'Wavelength (μm)',
            'ylabel': 'Transmission'
        },
        'Sensilla Resonances (Hist)': {
            'histogram_data': sens['optimal_wavelengths_quarter'],
            'xlabel': 'Optimal Quarter-λ (μm)'
        },
        'CHC Spectrum (Segment)': {
            'x': wavenumbers,
            'y': intensities,
            'xlabel': 'Wavenumber (cm⁻¹)',
            'ylabel': 'Absorbance (a.u.)'
        }
    }

    fig = visualizer.plot_multi_panel_analysis(data_dict, title='Cross-Domain Synthesis Overview')
    out_path = os.path.join(figure_dir, 'composite_cross_domain_overview.png')
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    with open(os.path.join(figure_dir, 'composite_cross_domain_overview.caption.txt'), 'w') as cf:
        cf.write('Composite overview: atmospheric transmission, sensilla resonance distribution, and CHC spectrum segment.')
    return out_path


def validate_outputs(figure_dir: str, data_dir: str) -> tuple[bool, list[str]]:
    """Validate that all expected outputs were generated correctly."""
    missing = []
    
    expected_figures = [
        "atmospheric_transmission.png",
        "sensilla_wavelength_matching.png", 
        "chc_spectra_example.png",
        "response_time_comparison.png",
        "composite_cross_domain_overview.png"
    ]
    
    expected_data = [
        "atmospheric_transmission.npz",
        "sensilla_data.npz"
    ]
    
    expected_captions = [
        "atmospheric_transmission.caption.txt",
        "sensilla_wavelength_matching.caption.txt",
        "chc_spectra_example.caption.txt", 
        "response_time_comparison.caption.txt",
        "composite_cross_domain_overview.caption.txt"
    ]
    
    # Check figures
    for fig in expected_figures:
        path = os.path.join(figure_dir, fig)
        if not os.path.exists(path):
            missing.append(f"Figure: {fig}")
        elif os.path.getsize(path) == 0:
            missing.append(f"Empty figure: {fig}")
    
    # Check data files  
    for data in expected_data:
        path = os.path.join(data_dir, data)
        if not os.path.exists(path):
            missing.append(f"Data: {data}")
        elif os.path.getsize(path) == 0:
            missing.append(f"Empty data: {data}")
            
    # Check captions
    for caption in expected_captions:
        path = os.path.join(figure_dir, caption)
        if not os.path.exists(path):
            missing.append(f"Caption: {caption}")
        elif os.path.getsize(path) == 0:
            missing.append(f"Empty caption: {caption}")
    
    return len(missing) == 0, missing


def main() -> None:
    """Generate all research figures using src/ modules with enhanced reporting."""
    start_time = time.time()
    
    try:
        print("🚀 Starting research figure generation...")
        os.environ.setdefault("MPLBACKEND", "Agg")
        _ensure_src_on_path()
        
        # Use centralized configuration and deterministic seeding
        print("🔧 Configuring analysis environment...")
        try:
            from src.config import set_random_seed
            from src.visualization import set_plot_style
            set_random_seed(42)
            set_plot_style('science')
            print("   ✅ Applied centralized configuration")
        except Exception as e:
            # If config is unavailable, ensure deterministic numpy behavior locally
            np.random.seed(42)
            print(f"   ⚠️  Using fallback configuration: {e}")
        
        output_dir, data_dir, figure_dir = _setup_directories()
        
        print("\n📊 Generating research figures using src/ modules...")
        
        # Generate all core research figures using src/ methods where available
        figures: List[str] = []
        
        # Core figures with progress tracking
        print("   🌍 Generating atmospheric transmission plot...")
        figures.append(generate_atmospheric_transmission_plot(figure_dir, data_dir))
        
        print("   📡 Generating sensilla wavelength matching...")
        figures.append(generate_sensilla_wavelength_matching(figure_dir, data_dir))
        
        print("   🧪 Generating CHC spectra example...")
        figures.append(generate_chc_spectra_example(figure_dir, data_dir))
        
        print("   ⚡ Generating response time comparison...")
        figures.append(generate_response_time_comparison(figure_dir, data_dir))
        
        print("   📈 Generating composite multipanel overview...")
        figures.append(generate_composite_multipanel(figure_dir))
        
        # Filter out any empty results
        figures = [f for f in figures if f]
        
        # Validate outputs
        print("\n🔍 Validating generated outputs...")
        is_valid, missing = validate_outputs(figure_dir, data_dir)
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        print(f"\n✅ Generated {len(figures)} research figures in {total_duration:.2f}s:")
        for fig in figures:
            print(f"   📄 {os.path.basename(fig)}")
        
        if not is_valid:
            print(f"\n⚠️  Warning: {len(missing)} missing outputs:")
            for item in missing:
                print(f"   ❌ {item}")
        else:
            print("\n✅ All expected outputs generated successfully!")
        
        print(f"\n📁 All outputs saved to: {output_dir}")
        print(f"   📈 Figures: {figure_dir}")
        print(f"   💾 Data: {data_dir}")
        
        print(f"\n🔗 Integration with src/ modules demonstrated:")
        print(f"   - Core physics (src.core), sensilla analysis (src.sensilla)")
        print(f"   - Centralized config and styling (src.config, src.visualization)")
        print(f"   - Proper error handling for missing imports")
        
    except Exception as e:
        print(f"❌ Error during figure generation: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
