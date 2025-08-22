"""
Comprehensive tests for analysis modules.

This file tests spectroscopy analysis, sensilla analysis, integrated analysis,
and related functionality.
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt

# Core modules
from src.core import (
    calculate_atmospheric_transmission,
    calculate_response_time_improvement,
    validate_numeric_inputs,
    safe_division
)

# Sensilla analysis
from src.sensilla import (
    analyze_sensilla_dimensions,
    generate_sensilla_visualization,
    calculate_wavelength_matching,
    calculate_sensilla_resonance_frequency
)

# Spectroscopy analysis
from src.spectroscopy import (
    analyze_chc_spectra,
    calculate_spectral_overlap,
    generate_spectral_plots
)

# Integrated analysis
from src.integrated_analysis import IntegratedAnalyzer

# Behavioral analysis
from src.behavioral import (
    analyze_behavioral_response,
    calculate_response_statistics,
    calculate_power_analysis
)











class TestIntegratedAnalysis:
    """Test integrated analysis functions."""

    def test_integrated_analyzer_comprehensive_report(self):
        """Test integrated analyzer comprehensive report."""
        analyzer = IntegratedAnalyzer()

        # Create comprehensive mock analysis results with expected structure
        analysis_results = {
            'fermi_analysis': {
                'molecular': {
                    'total_bits': 100.0,
                    'total_bytes': 12.5,
                    'translational_bits': 30.0,
                    'rotational_bits': 25.0,
                    'vibrational_bits': 45.0
                },
                'receptor': {
                    'specificity_index': 0.8,
                    'binding_entropy_bits': 15.0,
                    'signal_to_noise_ratio': 25.0
                },
                'neural': {
                    'encoding_efficiency_bits_per_energy': 50.0,
                    'spike_train_efficiency': 0.85,
                    'temporal_precision_bits': 20.0,
                    'channel_capacity_bits': 150.0,
                    'information_rate_bits': 75.0
                },
                'environmental': {
                    'temperature': 298.0,
                    'humidity': 0.6,
                    'atmospheric_pressure': 101325.0,
                    'total_environmental_bits': 25.0,
                    'temperature_bits': 10.0,
                    'humidity_bits': 8.0,
                    'pressure_bits': 7.0
                }
            },
            'metamaterial_analysis': {
                'dielectric': {
                    'refractive_index': [1.5, 1.6, 1.4],
                    'frequency': np.linspace(0.1, 2.0, 50) * 1e12,  # 0.1-2.0 THz
                    'absorption_coefficient': np.random.uniform(100, 1000, 50)
                },
                'plasmonic': {
                    'quality_factor': 100.0,
                    'resonance_frequency_hz': 5e11,  # 0.5 THz
                    'resonance_wavelength_m': 6e-4,  # 600 μm
                    'field_enhancement': 25.0
                },
                'quantum': {
                    'eigenvalues': np.array([0.0, 1e-20, 2e-20]),
                    'transition_rates': np.array([1e-12, 1e-12]),
                    'coupling_matrix': np.array([[0.0, 1e-21], [1e-21, 0.0]])
                },
                'information_capacity': {
                    'channel_capacity_bits_per_sec': 1000.0,
                    'spectral_efficiency': 0.85,
                    'bandwidth_hz': 1e9,
                    'signal_to_noise_ratio': 25.0,
                    'information_density_bits_per_joule_meter': 1e12,
                    'quantum_limit_bits_per_sec': 500.0
                }
            }
        }

        report = analyzer.comprehensive_report(analysis_results)
        assert isinstance(report, str)
        assert len(report) > 0

    def test_integrated_analyzer_visualization(self):
        """Test integrated analyzer visualization."""
        analyzer = IntegratedAnalyzer()
        fig = analyzer.generate_visualization()
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestBehavioralAnalysis:
    """Test behavioral analysis functions."""

    def test_analyze_behavioral_response(self):
        """Test behavioral response analysis."""
        response_data = np.random.randn(10, 50)
        result = analyze_behavioral_response(response_data)
        assert 'mean_response' in result
        assert 'response_variability' in result

    def test_analyze_behavioral_response_single_values(self):
        """Test behavioral response with single values."""
        response_data = np.array([1.0, 2.0, 3.0])
        result = analyze_behavioral_response(response_data)
        assert 'mean_response' in result

    def test_analyze_behavioral_response_insufficient_data(self):
        """Test behavioral response with insufficient data."""
        response_data = np.array([[1.0], [2.0]])
        result = analyze_behavioral_response(response_data)
        # Function returns analysis results even for insufficient data
        assert isinstance(result, dict)
        assert 'treatment' in result
        assert 'treatment_mean' in result
        assert 'control_mean' in result

    def test_analyze_behavioral_response_equal_means(self):
        """Test behavioral response with equal means."""
        response_data = np.ones((5, 10))
        result = analyze_behavioral_response(response_data)
        assert 'mean_response' in result

    def test_analyze_behavioral_response_edge_case_handling(self):
        """Test behavioral response edge case handling."""
        response_data = np.array([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])
        result = analyze_behavioral_response(response_data)
        assert 'mean_response' in result

    def test_analyze_behavioral_response_variance_exception(self):
        """Test behavioral response variance exception handling."""
        response_data = np.array([[1.0, 1.0], [1.0, 1.0]])
        result = analyze_behavioral_response(response_data)
        assert 'mean_response' in result

    def test_calculate_response_statistics(self):
        """Test response statistics calculation."""
        data = np.random.randn(100)
        stats = calculate_response_statistics(data)
        assert 'mean' in stats
        assert 'std' in stats
        assert 'min' in stats
        assert 'max' in stats

    def test_calculate_response_statistics_constant_response(self):
        """Test response statistics with constant response."""
        data = np.ones(50) * 5.0
        stats = calculate_response_statistics(data)
        assert stats['mean'] == 5.0
        assert stats['std'] == 0.0

    def test_calculate_power_analysis(self):
        """Test power analysis calculation."""
        treatment_times = [1.0, 2.0, 3.0, 4.0, 5.0]
        power_result = calculate_power_analysis(treatment_times, n_subjects=20, effect_size=0.8)
        assert 'power' in power_result
        assert 'required_sample_size' in power_result
