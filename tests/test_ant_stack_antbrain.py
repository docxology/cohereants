"""
Tests for Ant Stack AntBrain layer classes.
"""

import numpy as np

try:
    from src.ant_stack.antbrain import AntBrainOlfaction, VibrationalGlomeruliCircuit
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.ant_stack.antbrain import AntBrainOlfaction, VibrationalGlomeruliCircuit


class TestVibrationalGlomeruliCircuit:
    def test_frequency_tuning_and_response_shape(self):
        vg = VibrationalGlomeruliCircuit(num_channels=50, q_factor=100.0)
        assert vg.frequency_tuning.shape == (50,)
        assert np.all(vg.frequency_tuning >= 2.0)
        assert np.all(vg.frequency_tuning <= 25.0)

        # Synthetic spectral input (wavelengths in μm with intensities)
        wavelengths = np.linspace(2.0, 25.0, 100)
        intensities = np.exp(-0.5 * ((wavelengths - 10.0) / 1.5) ** 2)  # peak near 10 μm
        responses = vg.process_spectral_input(wavelengths, intensities)

        assert responses.shape == (50,)
        # Peak response should occur near 10 μm tuned channels
        peak_idx = np.argmax(responses)
        assert abs(vg.frequency_tuning[peak_idx] - 10.0) < 1.0


class TestAntBrainOlfaction:
    def test_pipeline_initialization(self):
        brain = AntBrainOlfaction(neuron_count=100000, num_channels=50)
        assert brain.al is not None
        assert brain.mb is not None
        assert brain.cx is not None


