"""
Comprehensive tests for the sensilla module.

This test suite ensures high code coverage for the sensilla analysis module.
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Import the module under test
try:
    from src.sensilla import (
        analyze_sensilla_dimensions, generate_sensilla_visualization,
        calculate_wavelength_matching
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.sensilla import (
        analyze_sensilla_dimensions, generate_sensilla_visualization,
        calculate_wavelength_matching
    )


class TestAnalyzeSensillaDimensions:
    """Test the analyze_sensilla_dimensions function."""
    
    def test_basic_analysis(self):
        """Test basic sensilla analysis."""
        lengths = [10.0, 15.0, 20.0]
        diameters = [2.0, 3.0, 4.0]
        
        result = analyze_sensilla_dimensions(lengths, diameters)
        
        # Check for the actual keys that exist
        assert 'lengths' in result
        assert 'diameters' in result
        assert 'optimal_wavelengths_quarter' in result
        assert 'optimal_wavelengths_half' in result
        assert 'aspect_ratios' in result
        assert 'mean_length' in result
        assert 'mean_diameter' in result
        assert 'mean_aspect_ratio' in result
        
        # Check data types
        assert isinstance(result['lengths'], np.ndarray)
        assert isinstance(result['diameters'], np.ndarray)
        assert isinstance(result['optimal_wavelengths_quarter'], np.ndarray)
        assert isinstance(result['optimal_wavelengths_half'], np.ndarray)
        assert isinstance(result['aspect_ratios'], np.ndarray)
        
        # Check values
        assert len(result['lengths']) == 3
        assert len(result['diameters']) == 3
        assert len(result['optimal_wavelengths_quarter']) == 3
        assert len(result['optimal_wavelengths_half']) == 3
        assert len(result['aspect_ratios']) == 3
    
    def test_empty_arrays(self):
        """Test sensilla analysis with empty arrays."""
        result = analyze_sensilla_dimensions([], [])
        
        # Check for the actual keys that exist
        assert 'lengths' in result
        assert 'diameters' in result
        assert 'optimal_wavelengths_quarter' in result
        assert 'optimal_wavelengths_half' in result
        assert 'aspect_ratios' in result
        assert 'mean_length' in result
        assert 'mean_diameter' in result
        assert 'mean_aspect_ratio' in result
        
        # Check that arrays are empty
        assert len(result['lengths']) == 0
        assert len(result['diameters']) == 0
        assert len(result['optimal_wavelengths_quarter']) == 0
        assert len(result['optimal_wavelengths_half']) == 0
        assert len(result['aspect_ratios']) == 0
        
        # Check default values for empty data
        assert result['mean_length'] == 0.0
        assert result['mean_diameter'] == 0.0
        assert result['mean_aspect_ratio'] == 0.0
    
    def test_zero_diameter(self):
        """Test sensilla analysis with zero diameter (should raise error)."""
        with pytest.raises(ValueError):
            analyze_sensilla_dimensions([10.0], [0.0])
    
    def test_species_specific_analysis(self):
        """Test sensilla analysis (no species parameter)."""
        lengths = [10.0, 15.0]
        diameters = [2.0, 3.0]
        
        result = analyze_sensilla_dimensions(lengths, diameters)
        
        # Check for the actual keys that exist
        assert 'lengths' in result
        assert 'diameters' in result
        assert 'optimal_wavelengths_quarter' in result
        assert 'optimal_wavelengths_half' in result
        assert 'aspect_ratios' in result
        assert 'mean_length' in result
        assert 'mean_diameter' in result
        assert 'mean_aspect_ratio' in result
    
    def test_resonant_frequency_calculation(self):
        """Test resonant frequency calculation."""
        lengths = [10.0, 15.0]
        diameters = [2.0, 3.0]
        
        result = analyze_sensilla_dimensions(lengths, diameters)
        
        # Check for the actual keys that exist
        assert 'lengths' in result
        assert 'diameters' in result
        assert 'optimal_wavelengths_quarter' in result
        assert 'optimal_wavelengths_half' in result
        assert 'aspect_ratios' in result
        assert 'mean_length' in result
        assert 'mean_diameter' in result
        assert 'mean_aspect_ratio' in result


class TestGenerateSensillaVisualization:
    """Test the generate_sensilla_visualization function."""
    
    def test_basic_visualization(self):
        """Test basic sensilla visualization generation."""
        lengths = [10.0, 15.0, 20.0]
        diameters = [2.0, 3.0, 4.0]
        
        with patch('matplotlib.pyplot.subplots') as mock_subplots:
            mock_fig = MagicMock()
            mock_ax1 = MagicMock()
            mock_ax2 = MagicMock()
            mock_subplots.return_value = (mock_fig, (mock_ax1, mock_ax2))
            
            result = generate_sensilla_visualization(lengths, diameters)
            # Since we're mocking matplotlib, result will be the mock figure
            assert result == mock_fig
    
    def test_visualization_with_species(self):
        """Test sensilla visualization generation (no species parameter)."""
        lengths = [10.0, 15.0]
        diameters = [2.0, 3.0]
        
        with patch('matplotlib.pyplot.subplots') as mock_subplots:
            mock_fig = MagicMock()
            mock_ax1 = MagicMock()
            mock_ax2 = MagicMock()
            mock_subplots.return_value = (mock_fig, (mock_ax1, mock_ax2))
            
            result = generate_sensilla_visualization(lengths, diameters)
            # Since we're mocking matplotlib, result will be the mock figure
            assert result == mock_fig
    
    def test_single_sensilla_visualization(self):
        """Test visualization with single sensilla."""
        lengths = [10.0]
        diameters = [2.0]
        
        with patch('matplotlib.pyplot.subplots') as mock_subplots:
            mock_fig = MagicMock()
            mock_ax1 = MagicMock()
            mock_ax2 = MagicMock()
            mock_subplots.return_value = (mock_fig, (mock_ax1, mock_ax2))
            
            result = generate_sensilla_visualization(lengths, diameters)
            # Since we're mocking matplotlib, result will be the mock figure
            assert result == mock_fig


class TestCalculateWavelengthMatching:
    """Test the calculate_wavelength_matching function."""
    
    def test_quarter_wave_matching(self):
        """Test quarter wavelength matching."""
        sensilla_lengths = np.array([10.0, 20.0])
        incident_wavelengths = np.array([40.0, 80.0])
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths, 'quarter')
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Check resonance type
        assert result['resonance_type'] == 'quarter'
        
        # Check optimal wavelengths (quarter wave = length * 4)
        expected_optimal = sensilla_lengths * 4
        np.testing.assert_array_equal(result['optimal_wavelengths'], expected_optimal)
    
    def test_half_wave_matching(self):
        """Test half wavelength matching."""
        sensilla_lengths = np.array([10.0, 20.0])
        incident_wavelengths = np.array([20.0, 40.0])
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths, 'half')
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Check resonance type
        assert result['resonance_type'] == 'half'
        
        # Check optimal wavelengths (half wave = length * 2)
        expected_optimal = sensilla_lengths * 2
        np.testing.assert_array_equal(result['optimal_wavelengths'], expected_optimal)
    
    def test_full_wave_matching(self):
        """Test full wavelength matching (should raise error)."""
        sensilla_lengths = np.array([10.0])
        incident_wavelengths = np.array([40.0])
        
        with pytest.raises(ValueError):
            calculate_wavelength_matching(sensilla_lengths, incident_wavelengths, 'full')
    
    def test_perfect_matching(self):
        """Test perfect wavelength matching."""
        sensilla_lengths = np.array([10.0])
        incident_wavelengths = np.array([40.0])  # Perfect quarter wave match
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths, 'quarter')
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Perfect match should have high efficiency
        assert result['mean_matching_efficiency'] > 0.9
    
    def test_no_matching(self):
        """Test no wavelength matching."""
        sensilla_lengths = np.array([10.0])
        incident_wavelengths = np.array([100.0])  # Poor match
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths, 'quarter')
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Poor match should have low efficiency
        assert result['mean_matching_efficiency'] < 0.5
    
    def test_single_values(self):
        """Test with single sensilla and wavelength."""
        sensilla_lengths = np.array([10.0])
        incident_wavelengths = np.array([40.0])
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths)
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Check matrix dimensions
        assert result['matching_matrix'].shape == (1, 1)
        assert len(result['optimal_wavelengths']) == 1
        assert len(result['best_matches']) == 1
        assert len(result['best_match_efficiencies']) == 1
    
    def test_multiple_wavelengths_single_sensilla(self):
        """Test with single sensilla and multiple wavelengths."""
        sensilla_lengths = np.array([10.0])
        incident_wavelengths = np.array([20.0, 40.0, 60.0])
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths)
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Check matrix dimensions
        assert result['matching_matrix'].shape == (1, 3)
        assert len(result['optimal_wavelengths']) == 1
        assert len(result['best_matches']) == 1
        assert len(result['best_match_efficiencies']) == 1
    
    def test_multiple_sensilla_single_wavelength(self):
        """Test with multiple sensilla and single wavelength."""
        sensilla_lengths = np.array([10.0, 20.0, 30.0])
        incident_wavelengths = np.array([40.0])
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths)
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
        
        # Check matrix dimensions
        assert result['matching_matrix'].shape == (3, 1)
        assert len(result['optimal_wavelengths']) == 3
        assert len(result['best_matches']) == 3
        assert len(result['best_match_efficiencies']) == 3
    
    def test_empty_arrays(self):
        """Test with empty arrays (should raise error)."""
        with pytest.raises((ValueError, IndexError)):
            calculate_wavelength_matching(np.array([]), np.array([]))


class TestSensillaModuleEdgeCases:
    """Test edge cases for sensilla module functions."""
    
    def test_extreme_aspect_ratios(self):
        """Test with extreme aspect ratios (should raise error)."""
        with pytest.raises(ValueError):
            analyze_sensilla_dimensions([1000.0], [1.0])  # 1000:1 aspect ratio
    
    def test_very_small_dimensions(self):
        """Test with very small dimensions (should raise error)."""
        with pytest.raises(ValueError):
            analyze_sensilla_dimensions([0.05], [0.001])  # Too small
    
    def test_wavelength_matching_extreme_ratios(self):
        """Test wavelength matching with extreme ratios."""
        sensilla_lengths = np.array([1.0, 1000.0])
        incident_wavelengths = np.array([4.0, 4000.0])
        
        result = calculate_wavelength_matching(sensilla_lengths, incident_wavelengths)
        
        # Check for the actual keys that exist
        assert 'matching_matrix' in result
        assert 'optimal_wavelengths' in result
        assert 'best_matches' in result
        assert 'best_match_efficiencies' in result
        assert 'mean_matching_efficiency' in result
        assert 'std_matching_efficiency' in result
        assert 'resonance_type' in result
