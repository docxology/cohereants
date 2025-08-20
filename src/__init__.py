"""
Insect Analysis Package

This package provides comprehensive analysis capabilities for the vibrational theory
of olfaction and infrared sensing in insects. It integrates multiple analytical
frameworks to provide quantitative, empirically-grounded analysis.

Modules:
- core: Basic physical calculations and conversions
- sensilla: Sensilla morphology analysis and visualization
- spectroscopy: CHC spectral analysis and processing
- behavioral: Behavioral response analysis and statistics
- fermi_estimation: Comprehensive Fermi Estimation type analysis
- meta_material_framework: Meta-material analytical framework
- integrated_analysis: Cross-domain synthesis and integration
- insect_analysis: Main interface and comprehensive analysis

The package provides both individual module access and integrated analysis
capabilities for comprehensive manuscript analysis.
"""

# Version information
__version__ = "3.0.0"
__author__ = "Tucker Chambers, Daniel A. Friedman"

# Import main analysis classes and functions
try:
    from .core import (
        calculate_wavelength_from_wavenumber,
        calculate_wavenumber_from_wavelength,
        calculate_atmospheric_transmission,
        calculate_response_time_improvement
    )
    
    from .sensilla import (
        analyze_sensilla_dimensions,
        generate_sensilla_visualization,
        calculate_wavelength_matching
    )
    
    from .spectroscopy import (
        analyze_chc_spectra,
        calculate_spectral_overlap,
        generate_spectral_plots
    )
    
    from .behavioral import (
        analyze_behavioral_response,
        calculate_response_statistics,
        generate_behavioral_plots
    )
    
    from .fermi_estimation import (
        FermiEstimator,
        create_sample_fermi_analysis
    )
    
    from .meta_material_framework import (
        MetaMaterialAnalyzer,
        create_sample_metamaterial_analysis
    )
    
    from .integrated_analysis import (
        IntegratedAnalyzer,
        create_sample_integrated_analysis
    )
    
    from .insect_analysis import (
        run_comprehensive_analysis
    )

    from .config import (
        ConfigManager,
        get_config,
        init_config,
        set_temperature,
        set_plot_style,
        enable_verbose_logging,
        set_random_seed
    )

    from .visualization import (
        AdvancedVisualizer,
        PlotStyler,
        create_publication_figure,
        get_colorblind_palette,
        create_subplots
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
    
    from src.insect_analysis import (
        run_comprehensive_analysis
    )

    from src.config import (
        ConfigManager,
        get_config,
        init_config,
        set_temperature,
        set_plot_style,
        enable_verbose_logging,
        set_random_seed
    )

    from src.visualization import (
        AdvancedVisualizer,
        PlotStyler,
        create_publication_figure,
        get_colorblind_palette,
        create_subplots
    )

# Package-level exports
__all__ = [
    # Core physics functions
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
    
    # Fermi Estimation framework
    'FermiEstimator',
    'create_sample_fermi_analysis',
    
    # Meta-material framework
    'MetaMaterialAnalyzer',
    'create_sample_metamaterial_analysis',
    
    # Integrated analysis
    'IntegratedAnalyzer',
    'create_sample_integrated_analysis',
    
    # Comprehensive analysis
    'run_comprehensive_analysis',

    # Configuration system
    'ConfigManager',
    'get_config',
    'init_config',
    'set_temperature',
    'set_plot_style',
    'enable_verbose_logging',
    'set_random_seed',

    # Advanced visualization
    'AdvancedVisualizer',
    'PlotStyler',
    'create_publication_figure',
    'get_colorblind_palette',
    'create_subplots',

    # Package utilities
    'get_package_info',
    'run_demo_analysis'
]

def get_package_info():
    """
    Get comprehensive package information.
    
    Returns:
        Dictionary with package details
    """
    return {
        'name': 'Insect Analysis Package',
        'version': __version__,
        'author': __author__,
        'description': 'Comprehensive analysis for vibrational theory of olfaction and infrared sensing in insects',
        'modules': [
            'core - Basic physical calculations',
            'sensilla - Sensilla morphology analysis',
            'spectroscopy - CHC spectral analysis',
            'behavioral - Behavioral response analysis',
            'fermi_estimation - Fermi Estimation framework',
            'meta_material_framework - Meta-material analysis',
            'integrated_analysis - Cross-domain synthesis',
            'insect_analysis - Main interface'
        ],
        'frameworks': [
            'Fermi Estimation Analysis',
            'Meta-Material Analytical Framework',
            'Integrated Cross-Domain Analysis'
        ]
    }

def run_demo_analysis():
    """
    Run a demonstration analysis using all available frameworks.
    
    Returns:
        Dictionary with demo results
    """
    print("Insect Analysis Package - Demo Analysis")
    print("=" * 50)
    
    try:
        # Run comprehensive analysis
        results = run_comprehensive_analysis()
        
        print("\nDemo analysis completed successfully!")
        print(f"Generated {len(results['performance_metrics'])} performance metrics")
        print(f"Comprehensive report: {len(results['comprehensive_report'])} characters")
        
        return results
        
    except Exception as e:
        print(f"Error during demo analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Display package information
    info = get_package_info()
    print(f"{info['name']} v{info['version']}")
    print(f"Author: {info['author']}")
    print(f"Description: {info['description']}")
    print("\nAvailable modules:")
    for module in info['modules']:
        print(f"  - {module}")
    print("\nAnalytical frameworks:")
    for framework in info['frameworks']:
        print(f"  - {framework}")
    
    print("\nRunning demo analysis...")
    demo_results = run_demo_analysis()
