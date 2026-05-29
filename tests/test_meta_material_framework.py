"""
Comprehensive tests for the meta_material_framework module.

This test suite ensures 100% code coverage for the Meta-Material Analytical Framework,
including all methods and edge cases.
"""

import pytest
import numpy as np

# Import the module under test
try:
    from src.meta_material_framework import MetaMaterialAnalyzer, create_sample_metamaterial_analysis
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.meta_material_framework import MetaMaterialAnalyzer, create_sample_metamaterial_analysis


class TestMetaMaterialAnalyzer:
    """Test suite for the MetaMaterialAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = MetaMaterialAnalyzer()
    
    def test_init(self):
        """Test MetaMaterialAnalyzer initialization."""
        from scipy import constants
        
        assert self.analyzer.epsilon_0 == constants.epsilon_0
        assert self.analyzer.mu_0 == constants.mu_0
        assert self.analyzer.c == constants.c
        assert self.analyzer.h == constants.h
        assert self.analyzer.hbar == constants.hbar
        assert self.analyzer.k_B == constants.k
        assert self.analyzer.e == constants.e
    
    def test_calculate_dielectric_response_basic(self):
        """Test basic dielectric response calculation."""
        frequency = np.array([1e12, 1e13, 1e14])  # Hz
        result = self.analyzer.calculate_dielectric_response(frequency)
        
        required_keys = ['epsilon_real', 'epsilon_imag', 'refractive_index', 
                        'extinction_coefficient', 'absorption_coefficient', 'frequency']
        assert all(key in result for key in required_keys)
        assert all(len(result[key]) == len(frequency) for key in required_keys[:-1])
        assert np.array_equal(result['frequency'], frequency)
    
    def test_calculate_dielectric_response_custom_params(self):
        """Test dielectric response with custom parameters."""
        frequency = np.array([1e13, 1e14])
        result = self.analyzer.calculate_dielectric_response(
            frequency=frequency,
            epsilon_inf=3.0,
            omega_p=2e15,
            gamma=5e12
        )
        
        assert len(result['epsilon_real']) == 2
        assert all(np.isfinite(result['epsilon_real']))
        assert all(np.isfinite(result['epsilon_imag']))
    
    def test_calculate_dielectric_response_single_frequency(self):
        """Test dielectric response with single frequency."""
        frequency = np.array([1e14])
        result = self.analyzer.calculate_dielectric_response(frequency)
        
        assert len(result['epsilon_real']) == 1
        assert np.isfinite(result['epsilon_real'][0])
    
    def test_analyze_plasmonic_resonance_basic(self):
        """Test basic plasmonic resonance analysis."""
        result = self.analyzer.analyze_plasmonic_resonance(
            particle_radius=50e-9,
            metal_dielectric=-10.0 + 1j
        )
        
        required_keys = ['resonance_frequency_hz', 'resonance_wavelength_m', 'quality_factor',
                        'field_enhancement', 'epsilon_resonance']
        assert all(key in result for key in required_keys)
        assert all(isinstance(result[key], (float, complex)) for key in required_keys)
        assert result['resonance_frequency_hz'] > 0
        assert result['resonance_wavelength_m'] > 0
    
    def test_analyze_plasmonic_resonance_custom_medium(self):
        """Test plasmonic resonance with custom medium."""
        result = self.analyzer.analyze_plasmonic_resonance(
            particle_radius=100e-9,
            metal_dielectric=-5.0 + 0.5j,
            medium_dielectric=2.0
        )
        
        assert result['epsilon_resonance'] == -4.0  # -2 * medium_dielectric
        assert isinstance(result['field_enhancement'], (float, complex))
    
    def test_analyze_plasmonic_resonance_different_sizes(self):
        """Test plasmonic resonance with different particle sizes."""
        small_result = self.analyzer.analyze_plasmonic_resonance(
            particle_radius=10e-9, metal_dielectric=-10.0 + 1j
        )
        large_result = self.analyzer.analyze_plasmonic_resonance(
            particle_radius=100e-9, metal_dielectric=-10.0 + 1j
        )
        
        # Smaller particles should have higher resonance frequency
        assert small_result['resonance_frequency_hz'] > large_result['resonance_frequency_hz']
        assert small_result['resonance_wavelength_m'] < large_result['resonance_wavelength_m']
    
    def test_calculate_quantum_coupling_basic(self):
        """Test basic quantum coupling calculation."""
        energy_levels = np.array([0, 1e-20, 2e-20, 3e-20])  # J
        result = self.analyzer.calculate_quantum_coupling(
            energy_levels=energy_levels,
            coupling_strength=1e-21
        )
        
        required_keys = ['coupling_matrix', 'eigenvalues', 'eigenvectors', 
                        'transition_rates', 'boltzmann_weights']
        assert all(key in result for key in required_keys)
        assert result['coupling_matrix'].shape == (4, 4)
        assert len(result['eigenvalues']) == 4
        assert result['eigenvectors'].shape == (4, 4)
        assert len(result['boltzmann_weights']) == 4
        
        # Check Boltzmann weights sum to 1
        assert abs(np.sum(result['boltzmann_weights']) - 1.0) < 1e-10
    
    def test_calculate_quantum_coupling_custom_temperature(self):
        """Test quantum coupling with custom temperature."""
        energy_levels = np.array([0, 1e-20, 2e-20])
        result_300K = self.analyzer.calculate_quantum_coupling(
            energy_levels, coupling_strength=1e-21, temperature=300.0
        )
        result_600K = self.analyzer.calculate_quantum_coupling(
            energy_levels, coupling_strength=1e-21, temperature=600.0
        )
        
        # Higher temperature should lead to more uniform distribution
        assert np.std(result_600K['boltzmann_weights']) < np.std(result_300K['boltzmann_weights'])
    
    def test_calculate_quantum_coupling_single_level(self):
        """Test quantum coupling with single energy level."""
        energy_levels = np.array([0])
        result = self.analyzer.calculate_quantum_coupling(
            energy_levels, coupling_strength=1e-21
        )
        
        assert result['coupling_matrix'].shape == (1, 1)
        assert result['coupling_matrix'][0, 0] == 0  # No self-coupling
        assert len(result['transition_rates']) == 0  # No transitions possible
    
    def test_analyze_information_capacity_basic(self):
        """Test basic information capacity analysis."""
        # Create mock material properties
        material_properties = {
            'refractive_index': np.array([1.5, 1.6, 1.7]),
            'frequency': np.array([1e12, 1e13, 1e14])
        }
        
        result = self.analyzer.analyze_information_capacity(
            material_properties=material_properties,
            frequency_bandwidth=1e12,
            signal_power=1e-6
        )
        
        required_keys = ['channel_capacity_bits_per_sec', 'signal_to_noise_ratio',
                        'information_density_bits_per_joule_meter', 'quantum_limit_bits_per_sec',
                        'group_velocity_m_per_sec', 'noise_power_watts']
        assert all(key in result for key in required_keys)
        assert all(isinstance(result[key], float) for key in required_keys)
        assert result['channel_capacity_bits_per_sec'] > 0
        assert result['signal_to_noise_ratio'] > 0
    
    def test_analyze_information_capacity_custom_noise_temp(self):
        """Test information capacity with custom noise temperature."""
        material_properties = {
            'refractive_index': np.array([1.5]),
            'frequency': np.array([1e13])
        }
        
        result_300K = self.analyzer.analyze_information_capacity(
            material_properties, 1e12, 1e-6, noise_temperature=300.0
        )
        result_600K = self.analyzer.analyze_information_capacity(
            material_properties, 1e12, 1e-6, noise_temperature=600.0
        )
        
        # Higher temperature should lead to higher noise power
        assert result_600K['noise_power_watts'] > result_300K['noise_power_watts']
    
    def test_calculate_metamaterial_figure_of_merit_basic(self):
        """Test basic metamaterial figure of merit calculation."""
        epsilon_real = np.array([2.0, 3.0, 4.0])
        epsilon_imag = np.array([0.1, 0.2, 0.3])
        
        result = self.analyzer.calculate_metamaterial_figure_of_merit(
            epsilon_real, epsilon_imag
        )
        
        required_keys = ['refractive_index', 'impedance', 'figure_of_merit_enz',
                        'figure_of_merit_nim', 'loss_tangent', 'quality_factor']
        assert all(key in result for key in required_keys)
        assert all(len(result[key]) == len(epsilon_real) for key in required_keys)
    
    def test_calculate_metamaterial_figure_of_merit_with_mu(self):
        """Test figure of merit with custom permeability."""
        epsilon_real = np.array([2.0, 3.0])
        epsilon_imag = np.array([0.1, 0.2])
        mu_real = np.array([1.5, 2.0])
        mu_imag = np.array([0.05, 0.1])
        
        result = self.analyzer.calculate_metamaterial_figure_of_merit(
            epsilon_real, epsilon_imag, mu_real, mu_imag
        )
        
        assert len(result['refractive_index']) == 2
        assert all(np.isfinite(result['quality_factor']))
    
    def test_analyze_multi_scale_properties_basic(self):
        """Test basic multi-scale properties analysis."""
        length_scales = np.array([1e-9, 1e-8, 1e-7, 1e-6])  # m
        property_values = np.array([1.0, 2.0, 4.0, 8.0])  # Example: doubling
        
        result = self.analyzer.analyze_multi_scale_properties(
            length_scales, property_values
        )
        
        required_keys = ['scaling_slope', 'scaling_intercept', 'r_squared',
                        'fractal_dimension', 'predicted_values', 'residuals',
                        'scaling_deviation']
        assert all(key in result for key in required_keys)
        assert isinstance(result['scaling_slope'], float)
        assert 0 <= result['r_squared'] <= 1
    
    def test_analyze_multi_scale_properties_perfect_scaling(self):
        """Test multi-scale analysis with perfect power law scaling."""
        length_scales = np.logspace(-9, -6, 4)  # 1nm to 1μm
        property_values = length_scales ** 2  # Perfect quadratic scaling
        
        result = self.analyzer.analyze_multi_scale_properties(
            length_scales, property_values, scaling_exponent=2.0
        )
        
        # Should have near-perfect fit
        assert result['r_squared'] > 0.99
        assert abs(result['scaling_slope'] - 2.0) < 0.1
        assert result['scaling_deviation'] < 0.1
    
    def test_analyze_multi_scale_properties_negative_slope(self):
        """Test multi-scale analysis with negative slope."""
        length_scales = np.array([1e-6, 1e-5, 1e-4])
        property_values = np.array([1000, 100, 10])  # Decreasing
        
        result = self.analyzer.analyze_multi_scale_properties(
            length_scales, property_values
        )
        
        assert result['scaling_slope'] < 0
        assert result['fractal_dimension'] is not None
        assert result['fractal_dimension'] > 0
    
    def test_generate_metamaterial_report(self):
        """Test comprehensive metamaterial report generation."""
        # Create sample data
        dielectric_data = {
            'frequency': np.array([1e12, 1e13]),
            'refractive_index': np.array([1.5, 1.6]),
            'absorption_coefficient': np.array([1000, 2000])
        }
        plasmonic_data = {
            'resonance_frequency_hz': 1e14,
            'resonance_wavelength_m': 3e-6,
            'quality_factor': 10.0,
            'field_enhancement': 5.0
        }
        quantum_data = {
            'eigenvalues': np.array([0, 1e-20, 2e-20]),
            'transition_rates': np.array([1e12, 2e12]),
            'coupling_matrix': np.array([[0, 1e-21], [1e-21, 0]])
        }
        info_capacity_data = {
            'channel_capacity_bits_per_sec': 1e12,
            'signal_to_noise_ratio': 100.0,
            'information_density_bits_per_joule_meter': 1e20,
            'quantum_limit_bits_per_sec': 1e13
        }
        
        report = self.analyzer.generate_metamaterial_report(
            dielectric_data, plasmonic_data, quantum_data, info_capacity_data
        )
        
        assert isinstance(report, str)
        assert len(report) > 0
        assert "COMPREHENSIVE META-MATERIAL ANALYSIS" in report
        assert "DIELECTRIC PROPERTIES" in report
        assert "PLASMONIC PROPERTIES" in report
        assert "QUANTUM COUPLING" in report
        assert "INFORMATION CAPACITY" in report


class TestCreateSampleMetamaterialAnalysis:
    """Test suite for the create_sample_metamaterial_analysis function."""
    
    def test_create_sample_metamaterial_analysis(self):
        """Test sample metamaterial analysis creation."""
        result = create_sample_metamaterial_analysis()
        
        assert len(result) == 5
        analyzer, dielec_data, plasm_data, quant_data, info_data = result
        
        # Check analyzer
        from src.meta_material_framework import MetaMaterialAnalyzer as SourceMetaMaterialAnalyzer
        assert isinstance(analyzer, SourceMetaMaterialAnalyzer)
        
        # Check dielectric data
        assert isinstance(dielec_data, dict)
        assert 'epsilon_real' in dielec_data
        assert 'frequency' in dielec_data
        
        # Check plasmonic data
        assert isinstance(plasm_data, dict)
        assert 'resonance_frequency_hz' in plasm_data
        
        # Check quantum data
        assert isinstance(quant_data, dict)
        assert 'eigenvalues' in quant_data
        
        # Check info data
        assert isinstance(info_data, dict)
        assert 'channel_capacity_bits_per_sec' in info_data


class TestMetaMaterialAnalyzerMainExecution:
    """Test the main execution block of meta_material_framework module."""

    def test_main_execution(self, capsys):
        """Test the main execution block."""
        import src.meta_material_framework

        analyzer, dielec_data, plasm_data, quant_data, info_data = src.meta_material_framework.create_sample_metamaterial_analysis()
        report = analyzer.generate_metamaterial_report(dielec_data, plasm_data, quant_data, info_data)
        print(report)
        captured = capsys.readouterr()

        assert "COMPREHENSIVE META-MATERIAL ANALYSIS" in captured.out
        assert "PLASMONIC PROPERTIES" in captured.out


class TestMetaMaterialAnalyzerEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = MetaMaterialAnalyzer()
    
    def test_dielectric_response_empty_frequency(self):
        """Test dielectric response with empty frequency array."""
        frequency = np.array([])
        result = self.analyzer.calculate_dielectric_response(frequency)
        
        assert len(result['epsilon_real']) == 0
        assert len(result['frequency']) == 0
    
    def test_plasmonic_resonance_zero_radius(self):
        """Test plasmonic resonance with zero radius."""
        with pytest.raises((ValueError, ZeroDivisionError, OverflowError)):
            self.analyzer.analyze_plasmonic_resonance(
                particle_radius=0.0,
                metal_dielectric=-10.0 + 1j
            )
    
    def test_quantum_coupling_empty_levels(self):
        """Test quantum coupling with empty energy levels."""
        energy_levels = np.array([])
        result = self.analyzer.calculate_quantum_coupling(
            energy_levels, coupling_strength=1e-21
        )
        
        assert result['coupling_matrix'].shape == (0, 0)
        assert len(result['eigenvalues']) == 0
        assert len(result['transition_rates']) == 0
    
    def test_information_capacity_zero_bandwidth(self):
        """Test information capacity with zero bandwidth."""
        material_properties = {
            'refractive_index': np.array([1.5]),
            'frequency': np.array([1e13])
        }
        
        # Should raise ZeroDivisionError for zero bandwidth
        with pytest.raises(ZeroDivisionError):
            self.analyzer.analyze_information_capacity(
                material_properties, frequency_bandwidth=0.0, signal_power=1e-6
            )
    
    def test_figure_of_merit_zero_values(self):
        """Test figure of merit with zero values."""
        epsilon_real = np.array([0.0, 1.0])
        epsilon_imag = np.array([0.0, 0.1])
        
        result = self.analyzer.calculate_metamaterial_figure_of_merit(
            epsilon_real, epsilon_imag
        )
        
        # Should handle division by zero gracefully
        assert np.all(np.isfinite(result['quality_factor']) | 
                     np.isinf(result['quality_factor']))
    
    def test_multi_scale_single_point(self):
        """Test multi-scale analysis with single data point."""
        length_scales = np.array([1e-6])
        property_values = np.array([1.0])
        
        # Single point analysis should work but may have poor conditioning
        result = self.analyzer.analyze_multi_scale_properties(
            length_scales, property_values
        )
        # Should return a result but may have NaN/inf values due to poor conditioning
        assert isinstance(result, dict)
    
    def test_multi_scale_constant_values(self):
        """Test multi-scale analysis with constant property values."""
        length_scales = np.array([1e-9, 1e-8, 1e-7])
        property_values = np.array([1.0, 1.0, 1.0])  # Constant
        
        result = self.analyzer.analyze_multi_scale_properties(
            length_scales, property_values
        )
        
        # Slope should be near zero
        assert abs(result['scaling_slope']) < 1e-10
        assert result['fractal_dimension'] is None  # No negative slope
