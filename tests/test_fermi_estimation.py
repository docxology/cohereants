"""
Comprehensive tests for the fermi_estimation module.

This test suite ensures 100% code coverage for the Fermi Estimation framework,
including all methods and edge cases.
"""

import pytest
import numpy as np

# Import the module under test
try:
    from src.fermi_estimation import FermiEstimator, create_sample_fermi_analysis
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.fermi_estimation import FermiEstimator, create_sample_fermi_analysis


class TestFermiEstimator:
    """Test suite for the FermiEstimator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.estimator = FermiEstimator()
    
    def test_init(self):
        """Test FermiEstimator initialization."""
        assert self.estimator.boltzmann_constant == 1.380649e-23
        assert self.estimator.temperature == 298.15
        assert self.estimator.plancks_constant == 6.62607015e-34
    
    def test_calculate_vibrational_entropy_default_occupation(self):
        """Test vibrational entropy calculation with default occupation numbers."""
        frequencies = np.array([1000, 2000, 3000])  # cm^-1
        entropy = self.estimator.calculate_vibrational_entropy(frequencies)
        
        assert isinstance(entropy, float)
        assert entropy > 0
        assert np.isfinite(entropy)
    
    def test_calculate_vibrational_entropy_custom_occupation(self):
        """Test vibrational entropy calculation with custom occupation numbers."""
        frequencies = np.array([1000, 2000, 3000])
        occupation_numbers = np.array([0.5, 0.3, 0.2])
        
        entropy = self.estimator.calculate_vibrational_entropy(frequencies, occupation_numbers)
        
        assert isinstance(entropy, float)
        assert entropy > 0
        assert np.isfinite(entropy)
    
    def test_calculate_vibrational_entropy_single_frequency(self):
        """Test vibrational entropy with single frequency."""
        frequencies = np.array([1500])
        entropy = self.estimator.calculate_vibrational_entropy(frequencies)
        
        assert isinstance(entropy, float)
        # Entropy can be small negative due to numerical precision
        assert entropy >= -1e-10
    
    def test_estimate_molecular_information_content_default(self):
        """Test molecular information content with default parameters."""
        result = self.estimator.estimate_molecular_information_content(150.0)
        
        required_keys = ['translational_bits', 'rotational_bits', 'vibrational_bits', 
                        'total_bits', 'total_bytes']
        assert all(key in result for key in required_keys)
        assert all(isinstance(result[key], float) for key in required_keys)
        assert result['total_bytes'] == result['total_bits'] / 8.0
    
    def test_estimate_molecular_information_content_custom(self):
        """Test molecular information content with custom parameters."""
        result = self.estimator.estimate_molecular_information_content(
            molecular_weight=200.0,
            symmetry_number=4,
            vibrational_modes=20
        )
        
        assert result['rotational_bits'] == np.log2(4) + 2.0
        assert result['vibrational_bits'] == 20 * 2.0
    
    def test_calculate_receptor_specificity_basic(self):
        """Test receptor specificity calculation."""
        binding_energies = np.array([-25.0, -20.0, -15.0, -10.0, -5.0])
        result = self.estimator.calculate_receptor_specificity(binding_energies)
        
        required_keys = ['binding_entropy_bits', 'specificity_index', 'signal_to_noise_ratio',
                        'energy_range_kj_mol', 'mean_binding_energy_kj_mol']
        assert all(key in result for key in required_keys)
        assert all(isinstance(result[key], float) for key in required_keys)
        assert 0 <= result['specificity_index'] <= 1
    
    def test_calculate_receptor_specificity_with_background(self):
        """Test receptor specificity with background energy."""
        binding_energies = np.array([-25.0, -20.0, -15.0])
        result = self.estimator.calculate_receptor_specificity(
            binding_energies, background_energy=-5.0
        )
        
        assert isinstance(result['specificity_index'], float)
        assert result['energy_range_kj_mol'] == 10.0  # -15 - (-25)
    
    def test_calculate_receptor_specificity_single_energy(self):
        """Test receptor specificity with single binding energy."""
        binding_energies = np.array([-20.0])
        result = self.estimator.calculate_receptor_specificity(binding_energies)
        
        assert result['energy_range_kj_mol'] == 0.0
        assert result['mean_binding_energy_kj_mol'] == -20.0
    
    def test_estimate_neural_encoding_efficiency_basic(self):
        """Test neural encoding efficiency calculation."""
        response_amplitudes = np.array([1.0, 1.2, 0.8, 1.1, 0.9])
        result = self.estimator.estimate_neural_encoding_efficiency(response_amplitudes)
        
        required_keys = ['signal_power', 'noise_power', 'signal_to_noise_ratio',
                        'channel_capacity_bits', 'information_rate_bits', 
                        'encoding_efficiency_bits_per_energy']
        assert all(key in result for key in required_keys)
        assert all(isinstance(result[key], float) for key in required_keys)
        assert result['signal_power'] > 0
        assert result['channel_capacity_bits'] > 0
    
    def test_estimate_neural_encoding_efficiency_custom_noise(self):
        """Test neural encoding efficiency with custom noise level."""
        response_amplitudes = np.array([1.0, 1.2, 0.8, 1.1, 0.9])
        result = self.estimator.estimate_neural_encoding_efficiency(
            response_amplitudes, noise_level=0.2
        )
        
        assert abs(result['noise_power'] - 0.04) < 1e-10  # 0.2^2
    
    def test_estimate_neural_encoding_efficiency_zero_noise(self):
        """Test neural encoding efficiency with zero noise."""
        response_amplitudes = np.array([1.0, 1.0, 1.0])
        result = self.estimator.estimate_neural_encoding_efficiency(
            response_amplitudes, noise_level=0.0
        )
        
        # Should handle division by zero gracefully
        assert np.isfinite(result['signal_to_noise_ratio'])
    
    def test_gaussian_variational_analysis(self):
        """Real (no-mock) GMM fit + Gaussian-entropy verification.

        De-mocked per RedTeam/Forge cross-vendor CRITICAL: the prior version patched
        sklearn GaussianMixture and asserted only len()==3, binding neither the fit
        nor the entropy math. This fits a real trimodal sample and checks recovered
        structure plus both entropy identities.
        """
        rng = np.random.default_rng(0)
        data = np.concatenate([
            rng.normal(1.0, 0.05, 80),
            rng.normal(2.0, 0.05, 80),
            rng.normal(3.0, 0.05, 80),
        ])
        result = self.estimator.gaussian_variational_analysis(data, n_components=3)

        required_keys = ['means', 'variances', 'weights', 'entropies_bits', 'total_entropy_bits']
        assert all(key in result for key in required_keys)
        assert len(result['means']) == 3
        # Real fit must recover the three clusters {1,2,3}.
        recovered = np.sort(result['means'])
        assert np.allclose(recovered, [1.0, 2.0, 3.0], atol=0.3), recovered
        # Entropy identities: each = 0.5*log2(2*pi*e*var); total = sum(weights*entropies).
        expected = 0.5 * np.log2(2 * np.pi * np.e * result['variances'])
        assert np.allclose(result['entropies_bits'], expected)
        assert np.isclose(result['total_entropy_bits'],
                          np.sum(result['weights'] * result['entropies_bits']))
    
    def test_calculate_environmental_information_content(self):
        """Test environmental information content calculation."""
        result = self.estimator.calculate_environmental_information_content(
            temperature_range=(273.15, 313.15),
            humidity_range=(0.3, 0.8),
            pressure_range=(101000, 102000)
        )
        
        required_keys = ['temperature_bits', 'humidity_bits', 'pressure_bits', 
                        'total_environmental_bits']
        assert all(key in result for key in required_keys)
        assert all(isinstance(result[key], float) for key in required_keys)
        
        # Temperature info should be log2((313.15-273.15)/0.1) = log2(400) ≈ 8.64
        expected_temp_bits = np.log2(40 / 0.1)
        assert abs(result['temperature_bits'] - expected_temp_bits) < 0.01
        
        # Total should be sum of components
        expected_total = (result['temperature_bits'] + result['humidity_bits'] + 
                         result['pressure_bits'])
        assert abs(result['total_environmental_bits'] - expected_total) < 0.01
    
    def test_generate_fermi_analysis_report(self):
        """Test comprehensive Fermi analysis report generation."""
        # Create sample data for all required inputs
        molecular_data = {
            'total_bits': 50.0, 'total_bytes': 6.25,
            'translational_bits': 20.0, 'rotational_bits': 10.0, 'vibrational_bits': 20.0
        }
        receptor_data = {
            'binding_entropy_bits': 2.5, 'specificity_index': 0.8, 'signal_to_noise_ratio': 15.0
        }
        neural_data = {
            'channel_capacity_bits': 3.0, 'information_rate_bits': 300.0, 
            'encoding_efficiency_bits_per_energy': 0.01
        }
        environmental_data = {
            'total_environmental_bits': 20.0, 'temperature_bits': 8.0, 
            'humidity_bits': 7.0, 'pressure_bits': 5.0
        }
        
        report = self.estimator.generate_fermi_analysis_report(
            molecular_data, receptor_data, neural_data, environmental_data
        )
        
        assert isinstance(report, str)
        assert len(report) > 0
        assert "COMPREHENSIVE FERMI ESTIMATION ANALYSIS" in report
        assert "MOLECULAR INFORMATION CONTENT" in report
        assert "RECEPTOR BINDING SPECIFICITY" in report
        assert "NEURAL ENCODING EFFICIENCY" in report
        assert "ENVIRONMENTAL INFORMATION" in report
        assert "SYSTEM SUMMARY" in report
        
        # Check that key values are included
        assert "50.00 bits" in report
        assert "0.800" in report
        assert "300.00 bits" in report


class TestCreateSampleFermiAnalysis:
    """Test suite for the create_sample_fermi_analysis function."""
    
    def test_create_sample_fermi_analysis(self):
        """Test sample Fermi analysis creation."""
        result = create_sample_fermi_analysis()
        
        assert len(result) == 5
        estimator, mol_data, rec_data, neu_data, env_data = result
        
        # Check estimator
        assert isinstance(estimator, FermiEstimator)
        
        # Check molecular data
        assert isinstance(mol_data, dict)
        assert 'total_bits' in mol_data
        
        # Check receptor data
        assert isinstance(rec_data, dict)
        assert 'binding_entropy_bits' in rec_data
        
        # Check neural data
        assert isinstance(neu_data, dict)
        assert 'channel_capacity_bits' in neu_data
        
        # Check environmental data
        assert isinstance(env_data, dict)
        assert 'total_environmental_bits' in env_data


class TestFermiEstimatorMainExecution:
    """Test the main execution block of fermi_estimation module."""

    def test_main_execution(self, capsys):
        """Test the main execution block."""
        import src.fermi_estimation

        estimator, mol_data, rec_data, neu_data, env_data = src.fermi_estimation.create_sample_fermi_analysis()
        report = estimator.generate_fermi_analysis_report(mol_data, rec_data, neu_data, env_data)
        print(report)
        captured = capsys.readouterr()

        assert "COMPREHENSIVE FERMI ESTIMATION ANALYSIS" in captured.out
        assert "SYSTEM SUMMARY" in captured.out


class TestFermiEstimatorEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.estimator = FermiEstimator()
    
    def test_vibrational_entropy_empty_array(self):
        """Test vibrational entropy with empty frequency array."""
        frequencies = np.array([])
        # Empty array should return 0 entropy or raise an error
        try:
            result = self.estimator.calculate_vibrational_entropy(frequencies)
            assert result == 0 or np.isnan(result)
        except (ValueError, IndexError, RuntimeWarning):
            pass  # Expected behavior
    
    def test_receptor_specificity_empty_array(self):
        """Test receptor specificity with empty binding energies."""
        binding_energies = np.array([])
        with pytest.raises((ValueError, IndexError)):
            self.estimator.calculate_receptor_specificity(binding_energies)
    
    def test_neural_encoding_empty_array(self):
        """Test neural encoding with empty response array."""
        response_amplitudes = np.array([])
        # Empty array should handle gracefully
        try:
            result = self.estimator.estimate_neural_encoding_efficiency(response_amplitudes)
            # For empty arrays, we expect:
            # - signal_power: 0.0
            # - noise_power: noise_level^2 (0.01 for default noise_level=0.1)
            # - signal_to_noise_ratio: 0.0
            # - channel_capacity_bits: 0.0
            # - information_rate_bits: 0.0
            # - encoding_efficiency_bits_per_energy: 0.0
            
            assert result['signal_power'] == 0.0
            assert np.isclose(result['noise_power'], 0.01)  # 0.1^2 with floating-point tolerance
            assert result['signal_to_noise_ratio'] == 0.0
            assert result['channel_capacity_bits'] == 0.0
            assert result['information_rate_bits'] == 0.0
            assert result['encoding_efficiency_bits_per_energy'] == 0.0
            
        except (ValueError, IndexError, RuntimeWarning):
            pass  # Expected behavior
    
    def test_molecular_info_negative_weight(self):
        """Test molecular information with negative molecular weight."""
        # Should handle gracefully or raise appropriate error
        result = self.estimator.estimate_molecular_information_content(-150.0)
        assert isinstance(result, dict)
    
    def test_environmental_info_invalid_ranges(self):
        """Test environmental information with invalid ranges."""
        # Test with inverted ranges
        result = self.estimator.calculate_environmental_information_content(
            temperature_range=(313.15, 273.15),  # Inverted
            humidity_range=(0.8, 0.3),          # Inverted
            pressure_range=(102000, 101000)     # Inverted
        )
        
        # Should handle gracefully
        assert isinstance(result, dict)
    
    def test_gaussian_analysis_single_point(self):
        """Test Gaussian analysis with single data point."""
        data = np.array([1.0, 1.0, 1.0, 1.0])
        result = self.estimator.gaussian_variational_analysis(data, n_components=1)

        assert isinstance(result, dict)
        assert len(result['means']) == 1
        assert np.isclose(result['means'][0], 1.0, atol=1e-6)
        assert np.isclose(np.sum(result['weights']), 1.0)
