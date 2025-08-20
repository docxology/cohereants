"""
Main Insect Analysis Module

This module serves as the primary interface for insect analysis, importing and
re-exporting functions from specialized submodules. It provides comprehensive
analysis capabilities for the vibrational theory of olfaction and infrared
sensing in insects.

The module integrates:
- Core physical calculations
- Sensilla analysis and visualization
- Spectroscopy analysis
- Behavioral analysis
- Fermi Estimation analysis
- Meta-material analytical framework
- Integrated cross-domain analysis
"""

import numpy as np

try:
    # Standard import path
    from src.core import (
        calculate_wavelength_from_wavenumber,
        calculate_wavenumber_from_wavelength,
        calculate_atmospheric_transmission,
        calculate_response_time_improvement
    )
    from src.sensilla import (
        analyze_sensilla_dimensions,
        generate_sensilla_visualization,
        calculate_wavelength_matching
    )
    from src.spectroscopy import (
        analyze_chc_spectra,
        calculate_spectral_overlap,
        generate_spectral_plots
    )
    from src.behavioral import (
        analyze_behavioral_response,
        calculate_response_statistics,
        generate_behavioral_plots
    )
    from src.fermi_estimation import (
        FermiEstimator,
        create_sample_fermi_analysis
    )
    from src.meta_material_framework import (
        MetaMaterialAnalyzer,
        create_sample_metamaterial_analysis
    )
    from src.integrated_analysis import (
        IntegratedAnalyzer,
        create_sample_integrated_analysis
    )
    
except ImportError:
    # Fallback for when running tests or as standalone script
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from src.core import (
        calculate_wavelength_from_wavenumber,
        calculate_wavenumber_from_wavelength,
        calculate_atmospheric_transmission,
        calculate_response_time_improvement
    )
    from src.sensilla import (
        analyze_sensilla_dimensions,
        generate_sensilla_visualization,
        calculate_wavelength_matching
    )
    from src.spectroscopy import (
        analyze_chc_spectra,
        calculate_spectral_overlap,
        generate_spectral_plots
    )
    from src.behavioral import (
        analyze_behavioral_response,
        calculate_response_statistics,
        generate_behavioral_plots
    )
    from src.fermi_estimation import (
        FermiEstimator,
        create_sample_fermi_analysis
    )
    from src.meta_material_framework import (
        MetaMaterialAnalyzer,
        create_sample_metamaterial_analysis
    )
    from src.integrated_analysis import (
        IntegratedAnalyzer,
        create_sample_integrated_analysis
    )

# Core analysis functions
__all__ = [
    # Core physics
    'calculate_wavelength_from_wavenumber',
    'calculate_wavenumber_from_wavelength',
    'calculate_atmospheric_transmission',
    'calculate_response_time_improvement',
    
    # Sensilla analysis
    'analyze_sensilla_dimensions',
    'generate_sensilla_visualization',
    'calculate_wavelength_matching',
    
    # Spectroscopy analysis
    'analyze_chc_spectra',
    'calculate_spectral_overlap',
    'generate_spectral_plots',
    
    # Behavioral analysis
    'analyze_behavioral_response',
    'calculate_response_statistics',
    'generate_behavioral_plots',
    
    # Fermi Estimation analysis
    'FermiEstimator',
    'create_sample_fermi_analysis',
    
    # Meta-material framework
    'MetaMaterialAnalyzer',
    'create_sample_metamaterial_analysis',
    
    # Integrated analysis
    'IntegratedAnalyzer',
    'create_sample_integrated_analysis'
]

def run_comprehensive_analysis():
    """
    Run comprehensive analysis using all available frameworks.
    
    Returns:
        Dictionary containing all analysis results
    """
    print("Running comprehensive insect analysis...")
    
    # Initialize integrated analyzer
    integrated_analyzer = IntegratedAnalyzer()
    
    # Sample parameters for comprehensive analysis
    odorant_properties = {
        'molecular_weight': 150.0,  # Typical odorant
        'symmetry_number': 2,
        'vibrational_modes': 15
    }
    
    receptor_properties = {
        'binding_energies': np.array([-25.0, -20.0, -15.0, -10.0, -5.0]),
        'response_amplitudes': np.random.normal(1.0, 0.3, 100),
        'epsilon_inf': 2.0,
        'omega_p': 5e15,
        'gamma': 1e13,
        'particle_radius': 50e-9,
        'metal_dielectric': -10.0 + 1j,
        'medium_dielectric': 1.5,
        'frequency_bandwidth': 1e12,
        'signal_power': 1e-6
    }
    
    environmental_conditions = {
        'temperature_range': (273.15, 313.15),
        'humidity_range': (0.3, 0.8),
        'pressure_range': (101000, 102000),
        'noise_temperature': 300.0
    }
    
    # Perform integrated analysis
    analysis_results = integrated_analyzer.analyze_olfactory_system(
        odorant_properties, receptor_properties, environmental_conditions
    )
    
    # Generate comprehensive report
    report = integrated_analyzer.generate_comprehensive_report(analysis_results)
    
    # Calculate performance metrics
    performance_metrics = integrated_analyzer.calculate_system_performance_metrics(analysis_results)
    
    return {
        'analysis_results': analysis_results,
        'performance_metrics': performance_metrics,
        'comprehensive_report': report
    }

if __name__ == "__main__":
    # Example usage
    print("Insect Analysis Module - Comprehensive Analysis")
    print("=" * 50)
    
    try:
        # Run comprehensive analysis
        results = run_comprehensive_analysis()
        
        print("\nAnalysis completed successfully!")
        print(f"Performance metrics calculated: {len(results['performance_metrics'])}")
        print(f"Report length: {len(results['comprehensive_report'])} characters")
        
        # Display key performance metrics
        metrics = results['performance_metrics']
        print(f"\nKey Performance Metrics:")
        print(f"  System Efficiency: {metrics['system_efficiency']:.2e}")
        print(f"  Information Processing Score: {metrics['information_processing_score']:.2e}")
        print(f"  Material Performance Score: {metrics['material_performance_score']:.2e}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
