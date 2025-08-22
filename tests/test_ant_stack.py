"""
Comprehensive tests for Ant Stack components.

This file tests all ant stack modules including antbody, antbrain, and antmind.
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt

# Ant Stack modules
from src.ant_stack.antbody import AntBodySensilla, AntBodySpectroscopy
from src.ant_stack.antbrain import VibrationalGlomeruliCircuit, AntBrainOlfaction
from src.ant_stack.antmind import AntMindOlfaction, AntMindStigmergy


class TestAntBodySensilla:
    """Test AntBodySensilla functionality."""

    def test_antbody_sensilla_initialization(self):
        """Test AntBodySensilla initialization."""
        lengths = np.array([50.0, 100.0, 150.0])
        diameters = np.array([5.0, 10.0, 15.0])
        body = AntBodySensilla(lengths, diameters)
        assert hasattr(body, 'optimal_wavelengths_quarter')
        assert hasattr(body, 'optimal_wavelengths_half')

    def test_antbody_spectroscopy_initialization(self):
        """Test AntBodySpectroscopy initialization."""
        body = AntBodySpectroscopy()
        assert hasattr(body, 'calculate_transmission')


class TestAntBrain:
    """Test AntBrain functionality."""

    def test_vibrational_glomeruli_initialization(self):
        """Test VibrationalGlomeruliCircuit initialization."""
        circuit = VibrationalGlomeruliCircuit(num_channels=10, q_factor=50.0)
        assert circuit.num_channels == 10
        assert circuit.q_factor == 50.0
        assert circuit.frequency_tuning.shape == (10,)

    def test_vibrational_glomeruli_invalid_init(self):
        """Test invalid initialization parameters."""
        with pytest.raises(ValueError):
            VibrationalGlomeruliCircuit(num_channels=0)
        with pytest.raises(ValueError):
            VibrationalGlomeruliCircuit(num_channels=10, q_factor=0)

    def test_vibrational_glomeruli_process_spectral_input(self):
        """Test spectral input processing."""
        circuit = VibrationalGlomeruliCircuit(num_channels=5, q_factor=50.0)
        wavelengths = np.linspace(2.0, 25.0, 10)
        intensities = np.ones_like(wavelengths)

        responses = circuit.process_spectral_input(wavelengths, intensities)
        assert responses.shape == (5,)
        assert np.all(np.isfinite(responses))

    def test_vibrational_glomeruli_channel_centers(self):
        """Test channel center retrieval."""
        circuit = VibrationalGlomeruliCircuit(num_channels=8, q_factor=100.0)
        centers = circuit.get_channel_centers()
        assert centers.shape == (8,)
        assert np.all(centers >= 2.0) and np.all(centers <= 25.0)

    def test_vibrational_glomeruli_bandwidths(self):
        """Test effective bandwidth calculation."""
        circuit = VibrationalGlomeruliCircuit(num_channels=6, q_factor=75.0)
        bandwidths = circuit.get_effective_bandwidths()
        assert bandwidths.shape == (6,)
        assert np.all(bandwidths > 0)

    def test_antbrain_olfaction_initialization(self):
        """Test AntBrainOlfaction initialization."""
        brain = AntBrainOlfaction(neuron_count=50000, num_channels=15)
        assert brain.neuron_count == 50000
        assert isinstance(brain.al, VibrationalGlomeruliCircuit)
        assert brain.al.num_channels == 15

    def test_antbrain_olfaction_summarize_channels(self):
        """Test channel summary generation."""
        brain = AntBrainOlfaction(neuron_count=10000, num_channels=10)
        summary = brain.summarize_channels()
        assert 'num_channels' in summary
        assert 'centers_um_min' in summary
        assert 'centers_um_max' in summary
        assert 'median_bandwidth_um' in summary
        assert summary['num_channels'] == 10


class TestAntMindOlfaction:
    """Test AntMindOlfaction functionality."""

    def test_antmind_olfaction_initialization(self):
        """Test AntMindOlfaction initialization."""
        mind = AntMindOlfaction(policy_horizon=2.0)
        assert hasattr(mind, 'policy_horizon')
        assert mind.policy_horizon == 2.0

    def test_antmind_olfaction_learning(self):
        """Test olfactory learning functionality."""
        mind = AntMindOlfaction(policy_horizon=1.5)

        # Test policy selection with different states
        state1 = {"stimulus": np.array([0.8, 0.2, 0.1]), "position": np.array([0.0, 0.0])}
        state2 = {"stimulus": np.array([0.1, 0.8, 0.2]), "position": np.array([1.0, 1.0])}

        policy1 = mind.select_policy(state1)
        policy2 = mind.select_policy(state2)

        # Both should return 2D action vectors
        assert policy1.shape == (2,)
        assert policy2.shape == (2,)

        # Policies should be deterministic for the same input
        policy1_again = mind.select_policy(state1)
        np.testing.assert_array_equal(policy1, policy1_again)

    def test_antmind_stigmergy_initialization(self):
        """Test AntMindStigmergy initialization."""
        mind = AntMindStigmergy(grid_shape=(50, 50), decay_rate=0.05, diffusion_coefficient=0.2)
        assert mind.pheromone_field.shape == (50, 50)
        assert hasattr(mind, 'decay_rate')
        assert mind.decay_rate == 0.05


class TestAntStackIntegration:
    """Test integration between Ant Stack components."""

    def test_sensilla_brain_integration(self):
        """Test integration between AntBodySensilla and AntBrain."""
        # Initialize sensilla array
        lengths = np.array([50.0, 100.0, 150.0])
        diameters = np.array([5.0, 10.0, 15.0])
        sensilla = AntBodySensilla(lengths, diameters)

        # Initialize brain
        brain = AntBrainOlfaction(num_channels=8)

        # Get resonant wavelengths from sensilla
        resonant_wavelengths = sensilla.get_resonant_wavelengths()

        # Process through brain channels
        wavelengths = np.linspace(2.0, 25.0, 20)
        intensities = np.ones_like(wavelengths)
        brain_response = brain.al.process_spectral_input(wavelengths, intensities)

        # Verify integration
        assert 'quarter' in resonant_wavelengths
        assert 'half' in resonant_wavelengths
        assert brain_response.shape == (8,)
        assert np.all(np.isfinite(brain_response))

    def test_brain_olfaction_integration(self):
        """Test integration between AntBrain and AntMindOlfaction."""
        brain = AntBrainOlfaction(num_channels=6)
        mind = AntMindOlfaction(policy_horizon=1.0)

        # Generate brain output
        wavelengths = np.linspace(2.0, 25.0, 15)
        intensities = np.ones_like(wavelengths)
        brain_output = brain.al.process_spectral_input(wavelengths, intensities)

        # Create state for mind
        current_state = {
            'brain_patterns': brain_output,
            'position': np.array([0.0, 0.0]),
            'heading': 0.0
        }

        # Get policy from mind
        action = mind.select_policy(current_state)
        assert action.shape == (2,)
        assert np.all(np.isfinite(action))

    def test_stigmergy_system(self):
        """Test AntMindStigmergy functionality."""
        mind = AntMindStigmergy(grid_shape=(50, 50), decay_rate=0.05)

        # Add some pheromone deposits
        deposits = [(10, 10, 1.0), (20, 20, 1.0), (30, 30, 1.0)]
        mind.update_pheromone_field(deposits)

        # Check that pheromone field is updated
        assert mind.pheromone_field.shape == (50, 50)
        assert np.any(mind.pheromone_field > 0)  # Some pheromone should remain

    def test_complete_ant_workflow(self):
        """Test complete ant workflow integration."""
        # Initialize components
        lengths = np.array([80.0, 120.0, 160.0])
        diameters = np.array([8.0, 12.0, 16.0])
        sensilla = AntBodySensilla(lengths, diameters)
        brain = AntBrainOlfaction(num_channels=10)
        mind = AntMindOlfaction(policy_horizon=1.5)

        # Simulate sensory input
        wavelengths = np.linspace(2.0, 25.0, 25)
        intensities = np.exp(-((wavelengths - 10) / 3)**2) * 0.8

        # Process through sensilla -> brain -> mind pipeline
        resonant_wavelengths = sensilla.get_resonant_wavelengths()
        brain_patterns = brain.al.process_spectral_input(wavelengths, intensities)

        current_state = {
            'brain_patterns': brain_patterns,
            'resonant_wavelengths': resonant_wavelengths,
            'sensory_input': intensities
        }

        action = mind.select_policy(current_state)

        # Verify complete pipeline
        assert resonant_wavelengths['quarter'].shape[0] == 3  # 3 sensilla
        assert brain_patterns.shape == (10,)  # 10 brain channels
        assert action.shape == (2,)  # 2D action vector
        assert np.all(np.isfinite(action))
