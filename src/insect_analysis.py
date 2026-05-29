"""
Main Insect Analysis Module

Primary interface for CohereAnts analysis — re-exports from specialized submodules.
"""

from __future__ import annotations

import numpy as np

from src.behavioral import analyze_behavioral_response, calculate_response_statistics, generate_behavioral_plots
from src.core import (
    calculate_atmospheric_transmission,
    calculate_response_time_improvement,
    calculate_wavelength_from_wavenumber,
    calculate_wavenumber_from_wavelength,
)
from src.fermi_estimation import FermiEstimator, create_sample_fermi_analysis
from src.integrated_analysis import IntegratedAnalyzer, create_sample_integrated_analysis
from src.meta_material_framework import MetaMaterialAnalyzer, create_sample_metamaterial_analysis
from src.sensilla import analyze_sensilla_dimensions, calculate_wavelength_matching, generate_sensilla_visualization
from src.manuscript_fixtures import default_olfactory_fixtures
from src.spectroscopy import analyze_chc_spectra, calculate_spectral_overlap, generate_spectral_plots

__all__ = [
    "calculate_wavelength_from_wavenumber",
    "calculate_wavenumber_from_wavelength",
    "calculate_atmospheric_transmission",
    "calculate_response_time_improvement",
    "analyze_sensilla_dimensions",
    "generate_sensilla_visualization",
    "calculate_wavelength_matching",
    "analyze_chc_spectra",
    "calculate_spectral_overlap",
    "generate_spectral_plots",
    "analyze_behavioral_response",
    "calculate_response_statistics",
    "generate_behavioral_plots",
    "FermiEstimator",
    "create_sample_fermi_analysis",
    "MetaMaterialAnalyzer",
    "create_sample_metamaterial_analysis",
    "IntegratedAnalyzer",
    "create_sample_integrated_analysis",
    "run_comprehensive_analysis",
]


def run_comprehensive_analysis() -> dict:
    """Run comprehensive analysis using all available frameworks."""
    print("Running comprehensive insect analysis...")
    integrated_analyzer = IntegratedAnalyzer()

    odorant_properties, receptor_properties, environmental_conditions = default_olfactory_fixtures()

    analysis_results = integrated_analyzer.analyze_olfactory_system(
        odorant_properties, receptor_properties, environmental_conditions
    )
    report = integrated_analyzer.generate_comprehensive_report(analysis_results)
    performance_metrics = integrated_analyzer.calculate_system_performance_metrics(analysis_results)

    return {
        "analysis_results": analysis_results,
        "performance_metrics": performance_metrics,
        "comprehensive_report": report,
    }


if __name__ == "__main__":
    print("Insect Analysis Module - Comprehensive Analysis")
    print("=" * 50)
    results = run_comprehensive_analysis()
    print("\nAnalysis completed successfully!")
    print(f"Performance metrics calculated: {len(results['performance_metrics'])}")
    print(f"Report length: {len(results['comprehensive_report'])} characters")
    metrics = results["performance_metrics"]
    print("\nKey Performance Metrics:")
    print(f"  System Efficiency: {metrics['system_efficiency']:.2e}")
    print(f"  Information Processing Score: {metrics['information_processing_score']:.2e}")
    print(f"  Material Performance Score: {metrics['material_performance_score']:.2e}")
