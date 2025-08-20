"""
Sensilla morphology analysis functions.

This module provides functions for analyzing sensilla dimensions and
generating visualizations of sensilla morphology data.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Tuple, Union
from .core import validate_numeric_inputs, safe_division


class SensillaData:
    """Container for sensilla measurement data with validation."""
    
    def __init__(self, lengths: Union[List[float], np.ndarray], 
                 diameters: Union[List[float], np.ndarray]):
        """
        Initialize sensilla data.
        
        Args:
            lengths: List or array of sensilla lengths in μm
            diameters: List or array of sensilla diameters in μm
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Convert to lists for validation
        if isinstance(lengths, np.ndarray):
            lengths = lengths.tolist()
        if isinstance(diameters, np.ndarray):
            diameters = diameters.tolist()
            
        if not isinstance(lengths, list) or not isinstance(diameters, list):
            raise ValueError("Lengths and diameters must be lists or arrays")
        
        if len(lengths) != len(diameters):
            raise ValueError("Lengths and diameters must have the same length")
        
        if not lengths:
            # Handle empty lists gracefully
            self.lengths = np.array([], dtype=float)
            self.diameters = np.array([], dtype=float)
            return
        
        # Validate all values are positive numbers
        for i, (length, diameter) in enumerate(zip(lengths, diameters)):
            if not isinstance(length, (int, float)) or length <= 0:
                raise ValueError(f"Length at index {i} must be a positive number, got {length}")
            if not isinstance(diameter, (int, float)) or diameter <= 0:
                raise ValueError(f"Diameter at index {i} must be a positive number, got {diameter}")
        
        self.lengths = np.array(lengths, dtype=float)
        self.diameters = np.array(diameters, dtype=float)
        self._validate_measurements()
    
    def _validate_measurements(self) -> None:
        """Validate that measurements are physically reasonable."""
        # Check for extremely large aspect ratios (>100:1)
        aspect_ratios = self.lengths / self.diameters
        if np.any(aspect_ratios > 100):
            raise ValueError("Aspect ratios greater than 100:1 are not physically reasonable")
        
        # Check for extremely small or large values
        if np.any(self.lengths < 0.1) or np.any(self.lengths > 1000):
            raise ValueError("Lengths must be between 0.1 and 1000 μm")
        if np.any(self.diameters < 0.01) or np.any(self.diameters > 100):
            raise ValueError("Diameters must be between 0.01 and 100 μm")
    
    @property
    def aspect_ratios(self) -> np.ndarray:
        """Calculate aspect ratios (length/diameter)."""
        return self.lengths / self.diameters
    
    @property
    def optimal_wavelengths_quarter(self) -> np.ndarray:
        """Calculate optimal wavelengths for 1/4 wavelength resonance."""
        return self.lengths * 4
    
    @property
    def optimal_wavelengths_half(self) -> np.ndarray:
        """Calculate optimal wavelengths for 1/2 wavelength resonance."""
        return self.lengths * 2
    
    def get_statistics(self) -> Dict[str, float]:
        """Calculate statistical summary of the data."""
        return {
            'mean_length': float(np.mean(self.lengths)),
            'mean_diameter': float(np.mean(self.diameters)),
            'mean_aspect_ratio': float(np.mean(self.aspect_ratios)),
            'std_length': float(np.std(self.lengths)),
            'std_diameter': float(np.std(self.diameters)),
            'std_aspect_ratio': float(np.std(self.aspect_ratios)),
            'min_length': float(np.min(self.lengths)),
            'max_length': float(np.max(self.lengths)),
            'min_diameter': float(np.min(self.diameters)),
            'max_diameter': float(np.max(self.diameters))
        }


def analyze_sensilla_dimensions(lengths: List[float], 
                               diameters: List[float]) -> Dict[str, Union[np.ndarray, float]]:
    """
    Analyze sensilla dimensions and calculate optimal detection wavelengths.
    
    Args:
        lengths: List of sensilla lengths in μm
        diameters: List of sensilla diameters in μm
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If inputs are invalid
    """
    data = SensillaData(lengths, diameters)
    
    # Handle empty data case
    if len(data.lengths) == 0:
        return {
            'lengths': data.lengths,
            'diameters': data.diameters,
            'optimal_wavelengths_quarter': data.optimal_wavelengths_quarter,
            'optimal_wavelengths_half': data.optimal_wavelengths_half,
            'aspect_ratios': data.aspect_ratios,
            'mean_length': 0.0,
            'mean_diameter': 0.0,
            'mean_aspect_ratio': 0.0
        }
    
    return {
        'lengths': data.lengths,
        'diameters': data.diameters,
        'optimal_wavelengths_quarter': data.optimal_wavelengths_quarter,
        'optimal_wavelengths_half': data.optimal_wavelengths_half,
        'aspect_ratios': data.aspect_ratios,
        **data.get_statistics()
    }


def generate_sensilla_visualization(lengths: List[float], 
                                  diameters: List[float],
                                  save_path: Optional[str] = None,
                                  figsize: Tuple[int, int] = (12, 5)) -> plt.Figure:
    """
    Generate a visualization of sensilla dimensions and optimal wavelengths.
    
    Args:
        lengths: List of sensilla lengths in μm
        diameters: List of sensilla diameters in μm
        save_path: Optional path to save the figure
        figsize: Figure size as (width, height) tuple
        
    Returns:
        Matplotlib figure object
        
    Raises:
        ValueError: If inputs are invalid
    """
    if not lengths or not diameters:
        # Handle empty data with a single informative plot
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.text(0.5, 0.5, 'No data to visualize', 
                ha='center', va='center', transform=ax.transAxes,
                fontsize=14, color='gray')
        ax.set_title('Sensilla Visualization - No Data', fontsize=16)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig
    
    # Validate inputs
    data = SensillaData(lengths, diameters)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Plot 1: Sensilla dimensions scatter plot
    ax1.scatter(data.diameters, data.lengths, alpha=0.7, s=100, c='blue', edgecolors='black')
    ax1.set_xlabel('Diameter (μm)', fontsize=12)
    ax1.set_ylabel('Length (μm)', fontsize=12)
    ax1.set_title('Sensilla Dimensions', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add trend line if we have enough data
    if len(data.lengths) > 1:
        z = np.polyfit(data.diameters, data.lengths, 1)
        p = np.poly1d(z)
        ax1.plot(data.diameters, p(data.diameters), "r--", alpha=0.8, linewidth=2)
    
    # Plot 2: Optimal detection wavelengths histogram
    if len(data.optimal_wavelengths_quarter) > 0:
        ax2.hist(data.optimal_wavelengths_quarter, bins=min(20, len(data.lengths)), 
                 alpha=0.7, label='1/4 λ resonance', color='blue', edgecolor='black')
        ax2.hist(data.optimal_wavelengths_half, bins=min(20, len(data.lengths)),
                 alpha=0.7, label='1/2 λ resonance', color='red', edgecolor='black')
        ax2.set_xlabel('Wavelength (μm)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.set_title('Optimal Detection Wavelengths', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def calculate_sensilla_resonance_frequency(length: float, 
                                         diameter: float,
                                         material_density: float = 1.0) -> float:
    """
    Calculate the fundamental resonance frequency of a sensillum.
    
    Args:
        length: Sensillum length in μm
        diameter: Sensillum diameter in μm
        material_density: Material density relative to water (default: 1.0)
        
    Returns:
        Resonance frequency in Hz
        
    Raises:
        ValueError: If inputs are invalid
    """
    validate_numeric_inputs(length, diameter, material_density)
    
    if length <= 0 or diameter <= 0 or material_density <= 0:
        raise ValueError("All inputs must be positive")
    
    # Convert to meters
    length_m = length * 1e-6
    diameter_m = diameter * 1e-6
    
    # Simple mechanical resonance model
    # f = (1/2π) * sqrt(k/m) where k is stiffness and m is mass
    # For a cylindrical structure, k ∝ diameter^2 and m ∝ length * diameter^2
    # This gives f ∝ 1/length for constant diameter
    
    # Base frequency (empirical constant)
    base_frequency = 1000  # Hz
    
    # Frequency scaling based on length
    frequency = base_frequency * (100 / length)  # 100 μm as reference length
    
    # Adjust for material density
    frequency = frequency / np.sqrt(material_density)
    
    return frequency


def calculate_wavelength_matching(sensilla_lengths: np.ndarray, 
                                incident_wavelengths: np.ndarray,
                                resonance_type: str = 'quarter') -> Dict[str, np.ndarray]:
    """
    Calculate wavelength matching between sensilla dimensions and incident radiation.
    
    Args:
        sensilla_lengths: Array of sensilla lengths in μm
        incident_wavelengths: Array of incident wavelengths in μm
        resonance_type: Type of resonance ('quarter' or 'half')
        
    Returns:
        Dictionary with matching analysis results
    """
    if resonance_type == 'quarter':
        optimal_wavelengths = sensilla_lengths * 4
    elif resonance_type == 'half':
        optimal_wavelengths = sensilla_lengths * 2
    else:
        raise ValueError("resonance_type must be 'quarter' or 'half'")
    
    # Calculate matching efficiency for each sensilla-wavelength combination
    matching_matrix = np.zeros((len(sensilla_lengths), len(incident_wavelengths)))
    
    for i, opt_wavelength in enumerate(optimal_wavelengths):
        for j, inc_wavelength in enumerate(incident_wavelengths):
            # Calculate matching efficiency based on wavelength difference
            wavelength_diff = abs(opt_wavelength - inc_wavelength)
            relative_diff = wavelength_diff / opt_wavelength
            
            # Gaussian matching function
            matching_efficiency = np.exp(-(relative_diff / 0.1)**2)
            matching_matrix[i, j] = matching_efficiency
    
    # Find best matches for each sensilla
    best_matches = np.argmax(matching_matrix, axis=1)
    best_match_efficiencies = np.max(matching_matrix, axis=1)
    
    # Calculate overall matching statistics
    mean_matching_efficiency = np.mean(matching_matrix)
    std_matching_efficiency = np.std(matching_matrix)
    
    return {
        'matching_matrix': matching_matrix,
        'optimal_wavelengths': optimal_wavelengths,
        'best_matches': best_matches,
        'best_match_efficiencies': best_match_efficiencies,
        'mean_matching_efficiency': mean_matching_efficiency,
        'std_matching_efficiency': std_matching_efficiency,
        'resonance_type': resonance_type
    }
