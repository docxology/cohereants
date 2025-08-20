import numpy as np
from src.spectroscopy import SpectralData, identify_chc_compounds, CHCAnalyzer


def test_spectroscopy_validation_and_identification():
    try:
        SpectralData([1000, 2000], [1.0])
        raise AssertionError('Expected ValueError for mismatched lengths')
    except ValueError:
        pass

    try:
        SpectralData([10, 20], [0.1, 0.2])
        raise AssertionError('Expected ValueError for out of range wavenumbers')
    except ValueError:
        pass

    w = np.array([2850.0, 2920.0, 2955.0])
    inten = np.array([0.5, 1.0, 0.8])
    sd = SpectralData(w, inten, species='Test')
    identified = identify_chc_compounds([2920.0], tolerance=5.0)
    assert any(d['compound'].startswith('CH2') for d in identified)

    analyzer = CHCAnalyzer()
    result = analyzer.analyze_spectrum(sd)
    assert 'num_peaks' in result


