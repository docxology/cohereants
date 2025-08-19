#!/usr/bin/env python3
"""
Generate example figures for insect perception research.

This script creates visualizations demonstrating the vibrational theory
of olfaction and insect sensilla morphology.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from insect_analysis import (
    calculate_wavelength_from_wavenumber,
    calculate_atmospheric_transmission,
    analyze_sensilla_dimensions
)


def generate_atmospheric_transmission_plot():
    """Generate atmospheric transmission plot showing IR windows."""
    wavelengths = np.linspace(1, 30, 1000)
    transmission = calculate_atmospheric_transmission(wavelengths)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(wavelengths, transmission, 'b-', linewidth=2, label='Atmospheric Transmission')
    
    # Highlight transmission windows
    ax.axvspan(2, 5, alpha=0.3, color='green', label='Mid-IR Window (2-5 μm)')
    ax.axvspan(8, 14, alpha=0.3, color='orange', label='Long-wave IR Window (8-14 μm)')
    ax.axvspan(17, 25, alpha=0.3, color='red', label='Far-IR Window (17-25 μm)')
    
    ax.set_xlabel('Wavelength (μm)')
    ax.set_ylabel('Transmission')
    ax.set_title('Atmospheric Infrared Transmission Windows')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.1)
    
    return fig


def generate_sensilla_wavelength_matching():
    """Generate plot showing sensilla dimensions vs optimal wavelengths."""
    # Example sensilla data from literature
    lengths = [6, 12, 25, 50, 100, 160]  # μm
    diameters = [1, 2, 3, 4, 5, 6]  # μm
    
    analysis = analyze_sensilla_dimensions(lengths, diameters)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Sensilla dimensions
    ax1.scatter(diameters, lengths, s=100, alpha=0.7, color='blue')
    ax1.set_xlabel('Diameter (μm)')
    ax1.set_ylabel('Length (μm)')
    ax1.set_title('Insect Sensilla Dimensions')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Optimal detection wavelengths
    ax2.hist(analysis['optimal_wavelengths_quarter'], bins=15, alpha=0.7, 
             label='1/4 λ resonance', color='blue')
    ax2.hist(analysis['optimal_wavelengths_half'], bins=15, alpha=0.7,
             label='1/2 λ resonance', color='red')
    ax2.set_xlabel('Wavelength (μm)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Optimal Detection Wavelengths')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def generate_chc_spectra_example():
    """Generate example CHC infrared spectra."""
    # Simulate CHC spectra based on literature values
    wavenumbers = np.linspace(2800, 3200, 500)
    
    # C-H stretch region around 2900 cm^-1
    ch_peak = 2900
    ch_intensity = 1.0
    
    # C-H bend region around 1450 cm^-1 (converted to wavenumber)
    ch_bend_peak = 1450
    ch_bend_intensity = 0.6
    
    # Generate spectra with Gaussian peaks
    intensities = np.zeros_like(wavenumbers)
    
    # Add C-H stretch peak
    intensities += ch_intensity * np.exp(-((wavenumbers - ch_peak) / 50)**2)
    
    # Add C-H bend peak (scaled and shifted)
    intensities += ch_bend_intensity * np.exp(-((wavenumbers - ch_bend_peak) / 30)**2)
    
    # Add some noise
    np.random.seed(42)
    intensities += 0.05 * np.random.randn(len(intensities))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(wavenumbers, intensities, 'b-', linewidth=2)
    ax.set_xlabel('Wavenumber (cm⁻¹)')
    ax.set_ylabel('Absorbance')
    ax.set_title('Example Cuticular Hydrocarbon Infrared Spectrum')
    ax.grid(True, alpha=0.3)
    
    # Highlight key regions
    ax.axvspan(2800, 3000, alpha=0.2, color='green', label='C-H Stretch Region')
    ax.axvspan(1400, 1500, alpha=0.2, color='orange', label='C-H Bend Region')
    ax.legend()
    
    return fig


def generate_response_time_comparison():
    """Generate comparison of response times across different sensory modalities."""
    modalities = ['Insect ORNs', 'Insect Photoreceptors', 'Insect Auditory', 'Traditional Olfaction']
    response_times = [2.5, 0.1, 0.16, 10.0]  # ms
    colors = ['blue', 'green', 'orange', 'red']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(modalities, response_times, color=colors, alpha=0.7)
    ax.set_ylabel('Response Time (ms)')
    ax.set_title('Response Time Comparison Across Sensory Modalities')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, time in zip(bars, response_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{time:.1f}', ha='center', va='bottom')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    return fig


def main():
    """Generate all example figures."""
    output_dir = Path(__file__).parent.parent / "output" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating insect perception research figures...")
    
    # Generate atmospheric transmission plot
    fig1 = generate_atmospheric_transmission_plot()
    fig1.savefig(output_dir / "atmospheric_transmission.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / 'atmospheric_transmission.png'}")
    
    # Generate sensilla wavelength matching plot
    fig2 = generate_sensilla_wavelength_matching()
    fig2.savefig(output_dir / "sensilla_wavelength_matching.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / 'sensilla_wavelength_matching.png'}")
    
    # Generate CHC spectra example
    fig3 = generate_chc_spectra_example()
    fig3.savefig(output_dir / "chc_spectra_example.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / 'chc_spectra_example.png'}")
    
    # Generate response time comparison
    fig4 = generate_response_time_comparison()
    fig4.savefig(output_dir / "response_time_comparison.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / 'response_time_comparison.png'}")
    
    # Save data for reproducibility
    data_dir = output_dir.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Save atmospheric transmission data
    wavelengths = np.linspace(1, 30, 1000)
    transmission = calculate_atmospheric_transmission(wavelengths)
    np.savez(data_dir / "atmospheric_transmission.npz", 
             wavelengths=wavelengths, transmission=transmission)
    
    # Save sensilla data
    lengths = [6, 12, 25, 50, 100, 160]
    diameters = [1, 2, 3, 4, 5, 6]
    np.savez(data_dir / "sensilla_data.npz", 
             lengths=lengths, diameters=diameters)
    
    print(f"Saved data files to: {data_dir}")
    print("All figures generated successfully!")
    
    # Close all figures to free memory
    plt.close('all')


if __name__ == "__main__":
    main()
