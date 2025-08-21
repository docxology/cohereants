"""
Spectroscopy module edge-case tests consolidated from ad hoc final coverage files.
"""

import numpy as np
import pytest
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt


def test_spectraldata_validation_and_ranges():
    from src.spectroscopy import SpectralData

    with pytest.raises(ValueError):
        SpectralData([], [1, 2, 3])
    with pytest.raises(ValueError):
        SpectralData([1, 2, 3], [])
    with pytest.raises(ValueError):
        SpectralData([1, 2], [1, 2, 3])
    with pytest.raises(ValueError):
        SpectralData([-100], [0.5])
    with pytest.raises(ValueError):
        SpectralData([1000], [-0.5])
    with pytest.raises(ValueError):
        SpectralData([5000], [0.5])

    single_point_data = SpectralData([1000.0], [0.5])
    assert isinstance(single_point_data.spectral_range, tuple)
    assert single_point_data.spectral_range[0] == single_point_data.spectral_range[1]

    zero_intensity_data = SpectralData([1000.0, 1500.0], [0.0, 0.0])
    intensity_range = zero_intensity_data.intensity_range
    assert intensity_range == (0.0, 0.0)


def test_peakfinder_and_regions():
    from src.spectroscopy import SpectralData, PeakFinder
    finder = PeakFinder()
    spectral_data = SpectralData([1000, 1500, 2000, 2500], [0.1, 0.8, 0.3, 0.1])
    peaks_result = finder.find_peaks(spectral_data)
    assert isinstance(peaks_result, tuple)
    with pytest.raises(ValueError):
        spectral_data.get_region_mask(2000, 1000)


def test_chc_analyzer_minimal_and_plots():
    from src.spectroscopy import CHCAnalyzer, SpectralData, generate_spectral_plots, calculate_spectral_overlap
    analyzer = CHCAnalyzer()
    minimal_data = SpectralData([1000], [0.5])
    result = analyzer.analyze_spectrum(minimal_data)
    assert isinstance(result, dict)

    with patch('matplotlib.pyplot.subplots') as mock_subplots:
        with patch('matplotlib.pyplot.colorbar'):
            mock_fig = MagicMock()
            mock_ax1 = MagicMock()
            mock_ax2 = MagicMock()
            mock_subplots.return_value = (mock_fig, (mock_ax1, mock_ax2))

            # Multiple spectra triggers correlation matrix path
            multiple_spectra = {
                'species1': np.array([1.0, 2.0, 1.0]),
                'species2': np.array([0.5, 1.5, 0.8]),
                'species3': np.array([2.0, 1.0, 1.5])
            }
            wavelengths = np.array([1, 2, 3])
            fig = generate_spectral_plots(multiple_spectra, wavelengths)
            assert isinstance(fig, (plt.Figure, MagicMock))

            # Single spectrum path
            single_spectrum = {'species1': np.array([1.0, 2.0, 1.0])}
            fig = generate_spectral_plots(single_spectrum, wavelengths)
            assert isinstance(fig, (plt.Figure, MagicMock))

    # Spectral overlap edge cases
    overlap = calculate_spectral_overlap(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 2, 3]))
    assert isinstance(overlap, dict) and 'overlap_integral' in overlap
    overlap = calculate_spectral_overlap(np.array([1, 2, 1]), np.array([1, 2, 1]), np.array([1, 2, 3]))
    assert isinstance(overlap, dict) and 'similarity_index' in overlap


