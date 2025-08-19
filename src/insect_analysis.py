"""
Insect Perception Research Analysis Functions

This module provides functions for analyzing insect perception data,
infrared spectroscopy, and sensilla morphology measurements.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional


def calculate_wavelength_from_wavenumber(wavenumber: float) -> float:
    """
    Convert wavenumber (cm^-1) to wavelength (μm).
    
    Args:
        wavenumber: Wavenumber in cm^-1
        
    Returns:
        Wavelength in micrometers
    """
    return 10000 / wavenumber


def calculate_wavenumber_from_wavelength(wavelength: float) -> float:
    """
    Convert wavelength (μm) to wavenumber (cm^-1).
    
    Args:
        wavelength: Wavelength in micrometers
        
    Returns:
        Wavenumber in cm^-1
    """
    return 10000 / wavelength


def analyze_sensilla_dimensions(lengths: List[float], 
                               diameters: List[float]) -> dict:
    """
    Analyze sensilla dimensions and calculate optimal detection wavelengths.
    
    Args:
        lengths: List of sensilla lengths in μm
        diameters: List of sensilla diameters in μm
        
    Returns:
        Dictionary containing analysis results
    """
    if len(lengths) != len(diameters):
        raise ValueError("Lengths and diameters must have the same length")
    
    if not lengths:  # Handle empty lists
        return {
            'lengths': [],
            'diameters': [],
            'optimal_wavelengths_quarter': [],
            'optimal_wavelengths_half': [],
            'aspect_ratios': [],
            'mean_length': 0.0,
            'mean_diameter': 0.0,
            'mean_aspect_ratio': 0.0
        }
    
    # Calculate optimal detection wavelengths based on antenna theory
    # Optimal length is typically 1/4 to 1/2 wavelength
    optimal_wavelengths_quarter = [length * 4 for length in lengths]
    optimal_wavelengths_half = [length * 2 for length in lengths]
    
    # Aspect ratios
    aspect_ratios = [length / diameter for length, diameter in zip(lengths, diameters)]
    
    return {
        'lengths': lengths,
        'diameters': diameters,
        'optimal_wavelengths_quarter': optimal_wavelengths_quarter,
        'optimal_wavelengths_half': optimal_wavelengths_half,
        'aspect_ratios': aspect_ratios,
        'mean_length': np.mean(lengths),
        'mean_diameter': np.mean(diameters),
        'mean_aspect_ratio': np.mean(aspect_ratios)
    }


def calculate_atmospheric_transmission(wavelengths: np.ndarray) -> np.ndarray:
    """
    Calculate atmospheric transmission for given wavelengths.
    
    Args:
        wavelengths: Array of wavelengths in μm
        
    Returns:
        Array of transmission values (0-1)
    """
    transmission = np.ones_like(wavelengths)
    
    # Mid-infrared window (2-5 μm)
    mid_ir_mask = (wavelengths >= 2) & (wavelengths <= 5)
    transmission[mid_ir_mask] = 0.8
    
    # Long-wave infrared window (8-14 μm)
    lwir_mask = (wavelengths >= 8) & (wavelengths <= 14)
    transmission[lwir_mask] = 0.9
    
    # Far-infrared window (17-25 μm)
    fir_mask = (wavelengths >= 17) & (wavelengths <= 25)
    transmission[fir_mask] = 0.7
    
    # Outside windows - reduced transmission
    outside_windows = ~(mid_ir_mask | lwir_mask | fir_mask)
    transmission[outside_windows] = 0.1
    
    return transmission


def analyze_chc_spectra(wavenumbers: np.ndarray, 
                        intensities: np.ndarray,
                        species: str = "Unknown") -> dict:
    """
    Analyze cuticular hydrocarbon (CHC) infrared spectra.
    
    Args:
        wavenumbers: Array of wavenumbers in cm^-1
        intensities: Array of intensity values
        species: Species name for identification
        
    Returns:
        Dictionary containing spectral analysis results
    """
    # Find peak positions with a more robust threshold
    from scipy.signal import find_peaks
    
    # Use a higher threshold to avoid detecting noise as peaks
    threshold = 0.2 * np.max(intensities)
    peaks, properties = find_peaks(intensities, height=threshold)
    
    peak_wavenumbers = wavenumbers[peaks]
    peak_intensities = intensities[peaks]
    
    # Convert peaks to wavelengths
    peak_wavelengths = [calculate_wavelength_from_wavenumber(w) for w in peak_wavenumbers]
    
    # Analyze key regions
    ch_region = (wavenumbers >= 2800) & (wavenumbers <= 3000)  # C-H stretch
    ch_intensity = np.mean(intensities[ch_region]) if np.any(ch_region) else 0
    
    return {
        'species': species,
        'peak_wavenumbers': peak_wavenumbers,
        'peak_wavelengths': peak_wavelengths,
        'peak_intensities': peak_intensities,
        'ch_stretch_intensity': ch_intensity,
        'total_spectral_area': np.trapezoid(intensities, wavenumbers),
        'num_peaks': len(peaks)
    }


def calculate_response_time_improvement(traditional_time: float, 
                                     insect_time: float) -> float:
    """
    Calculate the improvement in response time compared to traditional olfaction.
    
    Args:
        traditional_time: Traditional olfaction response time in ms
        insect_time: Insect ORN response time in ms
        
    Returns:
        Improvement factor (traditional_time / insect_time)
    """
    if insect_time <= 0:
        raise ValueError("Insect response time must be positive")
    
    return traditional_time / insect_time


def generate_sensilla_visualization(lengths: List[float], 
                                  diameters: List[float],
                                  save_path: Optional[str] = None) -> plt.Figure:
    """
    Generate a visualization of sensilla dimensions and optimal wavelengths.
    
    Args:
        lengths: List of sensilla lengths in μm
        diameters: List of sensilla diameters in μm
        save_path: Optional path to save the figure
        
    Returns:
        Matplotlib figure object
    """
    if not lengths or not diameters:
        # Handle empty data
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.text(0.5, 0.5, 'No data to visualize', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Sensilla Visualization - No Data')
        return fig
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Sensilla dimensions
    ax1.scatter(diameters, lengths, alpha=0.7, s=100)
    ax1.set_xlabel('Diameter (μm)')
    ax1.set_ylabel('Length (μm)')
    ax1.set_title('Sensilla Dimensions')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Optimal detection wavelengths
    analysis = analyze_sensilla_dimensions(lengths, diameters)
    if analysis['optimal_wavelengths_quarter']:  # Only plot if we have data
        ax2.hist(analysis['optimal_wavelengths_quarter'], bins=20, alpha=0.7, 
                 label='1/4 λ resonance', color='blue')
        ax2.hist(analysis['optimal_wavelengths_half'], bins=20, alpha=0.7,
                 label='1/2 λ resonance', color='red')
        ax2.set_xlabel('Wavelength (μm)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Optimal Detection Wavelengths')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def analyze_behavioral_response(treatment: str, 
                              response_times: List[float],
                              control_times: List[float]) -> dict:
    """
    Analyze behavioral response data comparing treatment to control.
    
    Args:
        treatment: Description of the treatment
        response_times: Response times under treatment conditions
        control_times: Response times under control conditions
        
    Returns:
        Dictionary containing statistical analysis results
    """
    from scipy import stats
    
    # Basic statistics
    treatment_mean = np.mean(response_times)
    control_mean = np.mean(control_times)
    
    # Handle edge cases
    if len(response_times) < 2 or len(control_times) < 2:
        # Not enough data for statistical testing
        return {
            'treatment': treatment,
            'treatment_mean': treatment_mean,
            'control_mean': control_mean,
            'difference': treatment_mean - control_mean,
            't_statistic': np.nan,
            'p_value': np.nan,
            'cohens_d': np.nan,
            'significant': False
        }
    
    # Statistical test
    try:
        t_stat, p_value = stats.ttest_ind(response_times, control_times)
    except:
        # Fallback for edge cases
        t_stat, p_value = np.nan, np.nan
    
    # Effect size (Cohen's d)
    try:
        pooled_std = np.sqrt(((len(response_times) - 1) * np.var(response_times) + 
                              (len(control_times) - 1) * np.var(control_times)) / 
                             (len(response_times) + len(control_times) - 2))
        
        if pooled_std == 0:
            cohens_d = np.nan
        else:
            cohens_d = (treatment_mean - control_mean) / pooled_std
    except:
        cohens_d = np.nan
    
    # Ensure significant is a proper boolean
    significant = bool(p_value < 0.05) if not np.isnan(p_value) else False
    
    return {
        'treatment': treatment,
        'treatment_mean': treatment_mean,
        'control_mean': control_mean,
        'difference': treatment_mean - control_mean,
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'significant': significant
    }
