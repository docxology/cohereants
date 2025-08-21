"""
Tests for Ant Stack AntBody layer classes.

I/O contracts verified without mocking; real numerical checks with deterministic behavior.
"""

import numpy as np
import pytest

try:
    from src.ant_stack.antbody import AntBodySensilla, AntBodySpectroscopy
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.ant_stack.antbody import AntBodySensilla, AntBodySpectroscopy


class TestAntBodySensilla:
    def test_resonance_calculation_quarter_and_half(self):
        lengths = np.array([10.0, 15.0, 20.0])  # μm
        diameters = np.array([2.0, 3.0, 4.0])   # μm
        sens = AntBodySensilla(lengths=lengths, diameters=diameters)

        assert sens.lengths.shape == (3,)
        assert sens.diameters.shape == (3,)

        # Quarter/half wavelength heuristics
        np.testing.assert_allclose(sens.optimal_wavelengths_quarter, lengths * 4.0)
        np.testing.assert_allclose(sens.optimal_wavelengths_half, lengths * 2.0)

        stats = sens.get_statistics()
        assert pytest.approx(stats['mean_length'], 1e-9) == 15.0
        assert pytest.approx(stats['mean_diameter'], 1e-9) == 3.0
        assert 'mean_aspect_ratio' in stats


class TestAntBodySpectroscopy:
    def test_transmission_windows_alignment(self):
        spec = AntBodySpectroscopy(spectral_resolution=0.01)
        # Representative wavelengths for each window
        w_mid, w_lwir, w_fir, w_out = 3.0, 10.0, 20.0, 30.0

        assert spec.get_transmission(w_mid, distance=10.0) == 0.8
        assert spec.get_transmission(w_lwir, distance=10.0) == 0.9
        assert spec.get_transmission(w_fir, distance=10.0) == 0.7
        assert spec.get_transmission(w_out, distance=10.0) == 0.1


