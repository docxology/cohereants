"""
Spectroscopy analysis tests from the main analysis file.

This file contains tests for spectroscopy analysis functions that were
originally part of the large test_analysis.py file.
"""

import numpy as np
import matplotlib.pyplot as plt

# Spectroscopy analysis
from src.spectroscopy import (
    analyze_chc_spectra,
    calculate_spectral_overlap,
    generate_spectral_plots
)


class TestSpectroscopyAnalysis:
    """Test spectroscopy analysis functions."""

    def test_analyze_chc_spectra(self):
        """Test CHC spectra analysis."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        spectrum = np.exp(-((wavelengths - 10) / 3)**2)
        result = analyze_chc_spectra(wavelengths, spectrum)  # Fixed argument order
        assert 'peak_wavelengths' in result
        assert 'peak_intensities' in result

    def test_analyze_chc_spectra_with_species(self):
        """Test CHC spectra analysis with species assignment."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        spectrum = np.exp(-((wavelengths - 10) / 3)**2)
        result = analyze_chc_spectra(wavelengths, spectrum, species='test_species')  # Fixed argument order
        assert result['species'] == 'test_species'

    def test_analyze_chc_spectra_no_peaks(self):
        """Test CHC spectra analysis with flat spectrum (no peaks)."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        spectrum = np.ones_like(wavelengths) * 0.1
        result = analyze_chc_spectra(wavelengths, spectrum)  # Fixed argument order
        assert 'peak_wavelengths' in result

    def test_analyze_chc_spectra_single_peak(self):
        """Test CHC spectra analysis with single peak."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        spectrum = np.zeros_like(wavelengths)
        spectrum[50] = 1.0  # Single peak
        result = analyze_chc_spectra(wavelengths, spectrum)  # Fixed argument order
        assert len(result['peak_wavelengths']) >= 1

    def test_analyze_chc_spectra_compound_identification(self):
        """Test compound identification in CHC spectra."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        spectrum = np.exp(-((wavelengths - 10) / 2)**2) + 0.5 * np.exp(-((wavelengths - 15) / 1)**2)
        result = analyze_chc_spectra(wavelengths, spectrum)  # Fixed argument order
        assert 'compound_identification' in result

    def test_calculate_spectral_overlap(self):
        """Test spectral overlap calculation."""
        spectrum1 = np.array([1.0, 0.5, 0.0])
        spectrum2 = np.array([0.0, 0.5, 1.0])
        overlap = calculate_spectral_overlap(spectrum1, spectrum2)
        assert 0.0 <= overlap <= 1.0

    def test_calculate_spectral_overlap_identical(self):
        """Test spectral overlap with identical spectra."""
        spectrum = np.array([1.0, 0.5, 0.2])
        overlap = calculate_spectral_overlap(spectrum, spectrum)
        assert overlap == 1.0

    def test_calculate_spectral_overlap_orthogonal(self):
        """Test spectral overlap with orthogonal spectra."""
        spectrum1 = np.array([1.0, 0.0, 0.0])
        spectrum2 = np.array([0.0, 1.0, 0.0])
        overlap = calculate_spectral_overlap(spectrum1, spectrum2)
        # Orthogonal spectra have non-zero similarity index due to normalization
        assert abs(overlap - 1/3) < 0.01  # Should be approximately 0.333

    def test_calculate_spectral_overlap_partial(self):
        """Test spectral overlap with partial overlap."""
        spectrum1 = np.array([1.0, 0.5, 0.0])
        spectrum2 = np.array([0.5, 1.0, 0.5])
        overlap = calculate_spectral_overlap(spectrum1, spectrum2)
        assert 0.0 < overlap < 1.0

    def test_calculate_spectral_overlap_zero_spectra(self):
        """Test spectral overlap with zero vs constant spectra."""
        spectrum1 = np.array([0.0, 0.0, 0.0])
        spectrum2 = np.array([1.0, 1.0, 1.0])
        overlap = calculate_spectral_overlap(spectrum1, spectrum2)
        # Both spectra have zero range, so they both normalize to [0.5, 0.5, 0.5] and are identical
        assert overlap == 1.0

    def test_calculate_spectral_overlap_negative_values(self):
        """Test spectral overlap with negative values."""
        spectrum1 = np.array([1.0, -0.5, 0.2])
        spectrum2 = np.array([0.8, 0.3, -0.1])
        overlap = calculate_spectral_overlap(spectrum1, spectrum2)
        # Should handle negative values appropriately
        assert isinstance(overlap, (int, float))

    def test_generate_spectral_plots(self):
        """Test spectral plots generation."""
        wavelengths = np.linspace(2.0, 25.0, 50)
        spectrum = np.exp(-((wavelengths - 10) / 3)**2)
        fig = generate_spectral_plots({'spectrum1': spectrum}, wavelengths)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_spectral_plots_multiple(self):
        """Test spectral plots with multiple spectra."""
        wavelengths = np.linspace(2.0, 25.0, 50)
        spectra = {
            'spectrum1': np.exp(-((wavelengths - 10) / 3)**2),
            'spectrum2': np.exp(-((wavelengths - 15) / 2)**2)
        }
        fig = generate_spectral_plots(spectra, wavelengths)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_spectral_plots_transmittance(self):
        """Test spectral plots with transmittance type."""
        wavelengths = np.linspace(2.0, 25.0, 50)
        spectrum = np.random.rand(50)
        fig = generate_spectral_plots({'spectrum1': spectrum}, wavelengths, plot_type='transmittance')
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_spectral_plots_reflectance(self):
        """Test spectral plots with reflectance type."""
        wavelengths = np.linspace(2.0, 25.0, 50)
        spectrum = np.random.rand(50)
        fig = generate_spectral_plots({'spectrum1': spectrum}, wavelengths, plot_type='reflectance')
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_spectral_plots_empty(self):
        """Test spectral plots with empty spectra dict."""
        wavelengths = np.linspace(2.0, 25.0, 50)
        fig = generate_spectral_plots({}, wavelengths)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
