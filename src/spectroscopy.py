"""
Cuticular hydrocarbon (CHC) spectroscopy analysis functions.

This module provides functions for analyzing infrared spectra of
cuticular hydrocarbons and related compounds.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from scipy.signal import find_peaks
from .core import calculate_wavelength_from_wavenumber, validate_numeric_inputs
import matplotlib.pyplot as plt


class SpectralData:
    """Container for spectral data with validation and analysis methods."""
    
    def __init__(self, wavenumbers: Union[np.ndarray, List[float]], 
                 intensities: Union[np.ndarray, List[float]],
                 species: str = "Unknown"):
        """
        Initialize spectral data.
        
        Args:
            wavenumbers: Array or list of wavenumbers in cm^-1
            intensities: Array or list of intensity values
            species: Species name for identification
            
        Raises:
            ValueError: If inputs are invalid
        """
        self.wavenumbers = np.asarray(wavenumbers, dtype=float)
        self.intensities = np.asarray(intensities, dtype=float)
        self.species = str(species)
        
        self._validate_inputs()
    
    def _validate_inputs(self) -> None:
        """Validate spectral data inputs."""
        if len(self.wavenumbers) != len(self.intensities):
            raise ValueError("Wavenumbers and intensities must have the same length")
        
        if len(self.wavenumbers) == 0:
            raise ValueError("Spectral data cannot be empty")
        
        if np.any(self.wavenumbers <= 0):
            raise ValueError("All wavenumbers must be positive")
        
        if np.any(self.intensities < 0):
            raise ValueError("All intensities must be non-negative")
        
        # Check for reasonable wavenumber range (typical IR range)
        if np.any(self.wavenumbers < 400) or np.any(self.wavenumbers > 4000):
            raise ValueError("Wavenumbers should be in typical IR range (400-4000 cm^-1)")
    
    @property
    def num_points(self) -> int:
        """Number of spectral data points."""
        return len(self.wavenumbers)
    
    @property
    def spectral_range(self) -> Tuple[float, float]:
        """Range of wavenumbers covered."""
        return float(np.min(self.wavenumbers)), float(np.max(self.wavenumbers))
    
    @property
    def intensity_range(self) -> Tuple[float, float]:
        """Range of intensity values."""
        return float(np.min(self.intensities)), float(np.max(self.intensities))
    
    def get_region_mask(self, min_wavenumber: float, max_wavenumber: float) -> np.ndarray:
        """
        Get boolean mask for a specific wavenumber region.
        
        Args:
            min_wavenumber: Lower bound of region in cm^-1
            max_wavenumber: Upper bound of region in cm^-1
            
        Returns:
            Boolean array indicating points in the region
        """
        if min_wavenumber >= max_wavenumber:
            raise ValueError("min_wavenumber must be less than max_wavenumber")
        
        return (self.wavenumbers >= min_wavenumber) & (self.wavenumbers <= max_wavenumber)
    
    def get_region_data(self, min_wavenumber: float, max_wavenumber: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get spectral data for a specific wavenumber region.
        
        Args:
            min_wavenumber: Lower bound of region in cm^-1
            max_wavenumber: Upper bound of region in cm^-1
            
        Returns:
            Tuple of (wavenumbers, intensities) for the region
        """
        mask = self.get_region_mask(min_wavenumber, max_wavenumber)
        return self.wavenumbers[mask], self.intensities[mask]


class PeakFinder:
    """Peak detection and analysis for spectral data."""
    
    def __init__(self, threshold_factor: float = 0.2, min_distance: int = 5):
        """
        Initialize peak finder.
        
        Args:
            threshold_factor: Factor of maximum intensity to use as threshold
            min_distance: Minimum distance between peaks in data points
        """
        self.threshold_factor = threshold_factor
        self.min_distance = min_distance
    
    def find_peaks(self, spectral_data: SpectralData) -> Tuple[np.ndarray, Dict]:
        """
        Find peaks in spectral data.
        
        Args:
            spectral_data: SpectralData object to analyze
            
        Returns:
            Tuple of (peak_indices, peak_properties)
        """
        threshold = self.threshold_factor * np.max(spectral_data.intensities)
        
        peaks, properties = find_peaks(
            spectral_data.intensities,
            height=threshold,
            distance=self.min_distance,
            prominence=threshold * 0.1  # Minimum prominence
        )
        
        return peaks, properties
    
    def analyze_peaks(self, spectral_data: SpectralData) -> Dict:
        """
        Analyze peaks and return comprehensive peak information.
        
        Args:
            spectral_data: SpectralData object to analyze
            
        Returns:
            Dictionary containing peak analysis results
        """
        peaks, properties = self.find_peaks(spectral_data)
        
        if len(peaks) == 0:
            return {
                'peak_wavenumbers': np.array([]),
                'peak_wavelengths': np.array([]),
                'peak_intensities': np.array([]),
                'peak_prominences': np.array([]),
                'num_peaks': 0
            }
        
        peak_wavenumbers = spectral_data.wavenumbers[peaks]
        peak_intensities = spectral_data.intensities[peaks]
        
        # Calculate wavelengths
        peak_wavelengths = np.array([
            calculate_wavelength_from_wavenumber(w) for w in peak_wavenumbers
        ])
        
        # Get peak prominences if available
        peak_prominences = properties.get('prominences', np.full(len(peaks), np.nan))
        
        return {
            'peak_wavenumbers': peak_wavenumbers,
            'peak_wavelengths': peak_wavelengths,
            'peak_intensities': peak_intensities,
            'peak_prominences': peak_prominences,
            'num_peaks': len(peaks)
        }


class CHCAnalyzer:
    """Analyzer for cuticular hydrocarbon spectra."""
    
    def __init__(self, peak_finder: Optional[PeakFinder] = None):
        """
        Initialize CHC analyzer.
        
        Args:
            peak_finder: Optional PeakFinder instance
        """
        self.peak_finder = peak_finder or PeakFinder()
        
        # Define key spectral regions for CHC analysis
        self.spectral_regions = {
            'ch_stretch': (2800, 3000),      # C-H stretch
            'ch_bend': (1350, 1480),         # C-H bend
            'cc_stretch': (1600, 1680),      # C=C stretch
            'cc_bend': (700, 800),           # C=C bend
            'oh_stretch': (3200, 3600),      # O-H stretch
            'nh_stretch': (3300, 3500)       # N-H stretch
        }
    
    def analyze_spectrum(self, spectral_data: SpectralData) -> Dict:
        """
        Perform comprehensive CHC spectral analysis.
        
        Args:
            spectral_data: SpectralData object to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Peak analysis
        peak_analysis = self.peak_finder.analyze_peaks(spectral_data)
        
        # Regional analysis
        regional_analysis = self._analyze_spectral_regions(spectral_data)
        
        # Overall spectral properties
        spectral_properties = self._calculate_spectral_properties(spectral_data)
        
        return {
            'species': spectral_data.species,
            **peak_analysis,
            **regional_analysis,
            **spectral_properties
        }
    
    def _analyze_spectral_regions(self, spectral_data: SpectralData) -> Dict:
        """Analyze specific spectral regions of interest."""
        regional_results = {}
        
        for region_name, (min_wav, max_wav) in self.spectral_regions.items():
            mask = spectral_data.get_region_mask(min_wav, max_wav)
            
            if np.any(mask):
                region_intensities = spectral_data.intensities[mask]
                region_wavenumbers = spectral_data.wavenumbers[mask]
                
                regional_results[f'{region_name}_intensity'] = float(np.mean(region_intensities))
                regional_results[f'{region_name}_max_intensity'] = float(np.max(region_intensities))
                regional_results[f'{region_name}_area'] = float(np.trapezoid(region_intensities, region_wavenumbers))
            else:
                regional_results[f'{region_name}_intensity'] = 0.0
                regional_results[f'{region_name}_max_intensity'] = 0.0
                regional_results[f'{region_name}_area'] = 0.0
        
        return regional_results
    
    def _calculate_spectral_properties(self, spectral_data: SpectralData) -> Dict:
        """Calculate overall spectral properties."""
        return {
            'total_spectral_area': float(np.trapezoid(spectral_data.intensities, spectral_data.wavenumbers)),
            'mean_intensity': float(np.mean(spectral_data.intensities)),
            'max_intensity': float(np.max(spectral_data.intensities)),
            'spectral_centroid': float(np.average(spectral_data.wavenumbers, weights=spectral_data.intensities)),
            'spectral_width': float(np.max(spectral_data.wavenumbers) - np.min(spectral_data.wavenumbers))
        }


def analyze_chc_spectra(wavenumbers: Union[np.ndarray, List[float]], 
                        intensities: Union[np.ndarray, List[float]],
                        species: str = "Unknown") -> Dict:
    """
    Analyze cuticular hydrocarbon (CHC) infrared spectra.
    
    Args:
        wavenumbers: Array or list of wavenumbers in cm^-1
        intensities: Array or list of intensity values
        species: Species name for identification
        
    Returns:
        Dictionary containing spectral analysis results
        
    Raises:
        ValueError: If inputs are invalid
    """
    # Create spectral data object
    spectral_data = SpectralData(wavenumbers, intensities, species)
    
    # Create analyzer and perform analysis
    analyzer = CHCAnalyzer()
    results = analyzer.analyze_spectrum(spectral_data)
    
    return results


def identify_chc_compounds(peak_wavenumbers: List[float], 
                          tolerance: float = 10.0) -> List[Dict]:
    """
    Identify potential CHC compounds based on peak positions.
    
    Args:
        peak_wavenumbers: List of peak wavenumbers in cm^-1
        tolerance: Tolerance for peak matching in cm^-1
        
    Returns:
        List of dictionaries containing compound information
    """
    # Common CHC peak assignments (simplified)
    chc_peaks = {
        2850: "CH2 symmetric stretch",
        2920: "CH2 asymmetric stretch",
        2955: "CH3 asymmetric stretch",
        2870: "CH3 symmetric stretch",
        1465: "CH2 bend",
        1375: "CH3 symmetric bend",
        720: "CH2 rock",
        890: "CH2 wag"
    }
    
    identified_compounds = []
    
    for peak_wav in peak_wavenumbers:
        for reference_wav, compound_name in chc_peaks.items():
            if abs(peak_wav - reference_wav) <= tolerance:
                identified_compounds.append({
                    'peak_wavenumber': peak_wav,
                    'compound': compound_name,
                    'reference_wavenumber': reference_wav,
                    'deviation': peak_wav - reference_wav
                })
                break
    
    return identified_compounds


def calculate_spectral_overlap(spectrum1: np.ndarray, 
                              spectrum2: np.ndarray,
                              wavelengths: np.ndarray) -> Dict[str, float]:
    """
    Calculate spectral overlap between two spectra.
    
    Args:
        spectrum1: First spectrum (absorbance or transmittance)
        spectrum2: Second spectrum (absorbance or transmittance)
        wavelengths: Wavelength array corresponding to spectra
        
    Returns:
        Dictionary with overlap analysis results
    """
    # Normalize spectra to 0-1 range
    spectrum1_norm = (spectrum1 - np.min(spectrum1)) / (np.max(spectrum1) - np.min(spectrum1))
    spectrum2_norm = (spectrum2 - np.min(spectrum2)) / (np.max(spectrum2) - np.min(spectrum2))
    
    # Calculate correlation coefficient
    correlation = np.corrcoef(spectrum1_norm, spectrum2_norm)[0, 1]
    
    # Calculate overlap integral
    overlap_integral = np.trapz(np.minimum(spectrum1_norm, spectrum2_norm), wavelengths)
    total_area = np.trapz(np.maximum(spectrum1_norm, spectrum2_norm), wavelengths)
    overlap_ratio = overlap_integral / total_area if total_area > 0 else 0
    
    # Calculate spectral similarity index
    similarity_index = 1 - np.mean(np.abs(spectrum1_norm - spectrum2_norm))
    
    return {
        'correlation_coefficient': float(correlation),
        'overlap_ratio': float(overlap_ratio),
        'similarity_index': float(similarity_index),
        'overlap_integral': float(overlap_integral),
        'total_area': float(total_area)
    }

def generate_spectral_plots(spectra: Dict[str, np.ndarray],
                           wavelengths: np.ndarray,
                           plot_type: str = 'absorbance') -> plt.Figure:
    """
    Generate spectral plots for multiple compounds.
    
    Args:
        spectra: Dictionary with compound names as keys and spectral data as values
        wavelengths: Wavelength array
        plot_type: Type of spectral data ('absorbance', 'transmittance', 'reflectance')
        
    Returns:
        Matplotlib figure with spectral plots
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Individual spectra
    colors = plt.cm.Set3(np.linspace(0, 1, len(spectra)))
    for i, (compound, spectrum) in enumerate(spectra.items()):
        ax1.plot(wavelengths, spectrum, label=compound, color=colors[i], linewidth=2)
    
    ax1.set_xlabel('Wavelength (μm)')
    ax1.set_ylabel(plot_type.capitalize())
    ax1.set_title(f'{plot_type.capitalize()} Spectra Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Spectral correlation matrix
    if len(spectra) > 1:
        compound_names = list(spectra.keys())
        correlation_matrix = np.zeros((len(compound_names), len(compound_names)))
        
        for i, name1 in enumerate(compound_names):
            for j, name2 in enumerate(compound_names):
                if i == j:
                    correlation_matrix[i, j] = 1.0
                else:
                    overlap_result = calculate_spectral_overlap(
                        spectra[name1], spectra[name2], wavelengths
                    )
                    correlation_matrix[i, j] = overlap_result['correlation_coefficient']
        
        im = ax2.imshow(correlation_matrix, cmap='RdYlBu_r', vmin=-1, vmax=1)
        ax2.set_xticks(range(len(compound_names)))
        ax2.set_yticks(range(len(compound_names)))
        ax2.set_xticklabels(compound_names, rotation=45)
        ax2.set_yticklabels(compound_names)
        ax2.set_title('Spectral Correlation Matrix')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax2)
        cbar.set_label('Correlation Coefficient')
        
        # Add correlation values to matrix
        for i in range(len(compound_names)):
            for j in range(len(compound_names)):
                text = ax2.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                               ha="center", va="center", color="black", fontweight='bold')
    
    plt.tight_layout()
    return fig
