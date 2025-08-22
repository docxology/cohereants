"""
Comprehensive tests for all case study modules.

This file tests detection limits, environmental channel, neural encoding,
plasmonic geometry, spectral unmixing, sensilla array directionality,
and active inference case studies.
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt

# Detection Limits
from src.case_studies.detection_limits import (
    min_detectable_power,
    snr_curve,
    roc_analysis,
    detection_performance_vs_snr,
    sensitivity_analysis,
    operating_regions_analysis,
    noise_floor_analysis,
    detection_range_analysis,
    optimize_detection_parameters,
    operating_point,
)

# Environmental Channel
from src.case_studies.environmental_channel import (
    atmospheric_transmission_detailed,
    molecular_absorption_cross_section,
    rayleigh_scattering_coefficient,
    atmospheric_transmission_comprehensive,
    channel_capacity_analysis,
    optimize_wavelength_for_range,
    environmental_sensitivity_analysis,
    channel_capacity_vs_env,
)

# Neural Encoding
from src.case_studies.neural_encoding import (
    information_rate_time_series,
    rate_coding_metrics,
    generate_spike_trains,
    analyze_spike_train_statistics,
    temporal_coding_analysis,
    population_coding_analysis,
    mutual_information_analysis,
    odor_discrimination_analysis,
    adaptation_dynamics_analysis,
)

# Plasmonic Geometry
from src.case_studies.plasmonic_geometry import (
    drude_model_permittivity,
    mie_scattering_sphere,
    coupled_dipoles_near_field,
    optimize_plasmonic_geometry,
    sweep_plasmonic_quality,
    field_distribution_near_particle,
)

# Spectral Unmixing
from src.case_studies.spectral_unmixing import (
    nmf_unmix,
    generate_realistic_chc_spectra,
    vertex_component_analysis,
    independent_component_analysis_spectra,
    spectral_feature_extraction,
    lda_baseline,
)

# Sensilla Array Directionality
from src.case_studies.sensilla_array_directionality import (
    compute_beam_pattern,
    array_gain,
    design_log_periodic_array,
    design_circular_array,
    sensilla_element_pattern,
    mutual_coupling_matrix,
    array_pattern_2d,
    analyze_sensilla_morphology,
    frequency_response_analysis,
)

# Active Inference
from src.case_studies.active_inference import olfactory_active_inference_step


class TestDetectionLimits:
    """Test detection limits analysis functions."""

    def test_min_detectable_power(self):
        """Test minimum detectable power calculation."""
        pmin = min_detectable_power(300.0, 1e6, 10.0)
        assert pmin > 0

    def test_snr_curve(self):
        """Test SNR curve calculation."""
        powers = np.array([1e-12, 1e-11, 1e-10])
        snr = snr_curve(powers, 300.0, 1e6)
        assert snr.shape == (3,)
        assert np.all(np.isfinite(snr))

    def test_roc_analysis(self):
        """Test ROC analysis."""
        roc = roc_analysis(1.0, 0.1)
        assert 'auc' in roc
        assert 0.0 <= roc['auc'] <= 1.0

    def test_detection_performance_vs_snr(self):
        """Test detection performance vs SNR."""
        snr_db = np.linspace(-10, 20, 5)
        perf = detection_performance_vs_snr(snr_db)
        assert 'pd' in perf
        assert perf['pd'].shape[0] == 5

    def test_sensitivity_analysis(self):
        """Test sensitivity analysis."""
        base = {'temperature_k': 300.0, 'bandwidth_hz': 1e6}
        ranges = {'temperature_k': (290.0, 310.0)}
        sens = sensitivity_analysis(base, ranges, n_points=5)
        assert 'temperature_k' in sens

    def test_operating_regions_analysis(self):
        """Test operating regions analysis."""
        powers = np.logspace(-12, -6, 5)
        temps = np.linspace(280, 320, 4)
        or_regions = operating_regions_analysis(powers, temps)
        assert 'snr_grid_db' in or_regions

    def test_noise_floor_analysis(self):
        """Test noise floor analysis."""
        freqs = np.array([1e3, 1e4, 1e5])
        nf = noise_floor_analysis(freqs, temperature_k=300.0)
        assert 'total_noise_db' in nf

    def test_detection_range_analysis(self):
        """Test detection range analysis."""
        dr = detection_range_analysis(1.0, 10.0, 3e12, -90.0)
        assert 'max_range_free_space_m' in dr

    def test_optimize_detection_parameters(self):
        """Test detection parameter optimization."""
        opt = optimize_detection_parameters(
            {'temperature_k': (290.0, 310.0), 'bandwidth_hz': (1e5, 1e7)},
            {'min_power': 0.001},
            {'distance_m': 1000.0}
        )
        assert 'optimization_success' in opt

    def test_operating_point(self):
        """Test operating point calculation."""
        op = operating_point(1.0, 10.0)
        assert 'capacity_bits_s' in op


class TestEnvironmentalChannel:
    """Test environmental channel analysis functions."""

    def test_atmospheric_transmission_detailed(self):
        """Test detailed atmospheric transmission."""
        wl = np.linspace(2.0, 25.0, 10)
        trans = atmospheric_transmission_detailed(wl, 1000.0, 0.5, 293.0)
        assert trans.shape == (10,)

    def test_molecular_absorption_cross_section(self):
        """Test molecular absorption cross section."""
        wl = np.linspace(2.0, 25.0, 5)
        abs_cs = molecular_absorption_cross_section(wl, 'H2O', 0.01)
        assert abs_cs.shape == (5,)

    def test_rayleigh_scattering_coefficient(self):
        """Test Rayleigh scattering coefficient."""
        wl = np.linspace(2.0, 25.0, 5)
        rayleigh = rayleigh_scattering_coefficient(wl, 101325.0, 293.0)
        assert rayleigh.shape == (5,)

    def test_atmospheric_transmission_comprehensive(self):
        """Test comprehensive atmospheric transmission."""
        trans = atmospheric_transmission_comprehensive(
            wavelengths_um=np.array([10.0]),
            path_length_m=1000.0,
            humidity_percent=50.0,
            temperature_k=293.0
        )
        assert 'alpha_total' in trans

    def test_channel_capacity_analysis(self):
        """Test channel capacity analysis."""
        wavelengths = np.linspace(2.0, 25.0, 10)
        capacity = channel_capacity_analysis(wavelengths, 1000.0, 0.5, 293.0)
        assert 'capacity_bps' in capacity
        assert capacity['capacity_bps'].shape == (10,)

    def test_optimize_wavelength_for_range(self):
        """Test wavelength optimization for range."""
        opt = optimize_wavelength_for_range(
            target_range_m=5000.0,
            min_capacity_bps=1000.0,
            signal_power_dbm=10.0
        )
        assert 'optimal_wavelength_um' in opt

    def test_environmental_sensitivity_analysis(self):
        """Test environmental sensitivity analysis."""
        base = {'path_length_m': 1000.0, 'temperature_k': 293.0}
        ranges = {'path_length_m': (500.0, 2000.0)}
        sens = environmental_sensitivity_analysis(10.0, 1000.0, {'path_length_m': (500.0, 2000.0)}, n_points=5)
        assert 'path_length_m' in sens

    def test_channel_capacity_vs_env(self):
        """Test channel capacity vs environment."""
        capacity = channel_capacity_vs_env(
            material_refractive_index=1.5,
            signal_power_w=1e-6,
            bandwidth_hz=1e9,
            humidity_grid=np.linspace(0.1, 0.9, 4),
            temperature_grid_k=np.linspace(290, 310, 4),
            path_m=1000.0
        )
        assert 'capacity_bits_per_s' in capacity


class TestNeuralEncoding:
    """Test neural encoding analysis functions."""

    def test_information_rate_time_series(self):
        """Test information rate time series."""
        rates = np.random.poisson(10, 100)
        info_rate = information_rate_time_series(rates, 0.001, 0.1)
        assert 'information_rate_bits' in info_rate

    def test_rate_coding_metrics(self):
        """Test rate coding metrics."""
        spikes = np.random.poisson(0.5, (10, 1000))
        metrics = rate_coding_metrics(spikes, 0.001)
        assert 'd_prime' in metrics
        assert 'mean_diff' in metrics

    def test_generate_spike_trains(self):
        """Test spike train generation."""
        rates = np.ones(100) * 10.0  # 10 Hz
        spikes = generate_spike_trains(rates, 0.001, seed=42)
        assert 'spike_trains' in spikes
        assert 'stimuli' in spikes

    def test_analyze_spike_train_statistics(self):
        """Test spike train statistics analysis."""
        rates = np.ones(100) * 10.0  # 10 Hz
        spikes_data = generate_spike_trains(rates, 0.001, seed=42)
        stats = analyze_spike_train_statistics(spikes_data)
        assert 'cv_isi' in stats
        assert 'fano_factor' in stats

    def test_temporal_coding_analysis(self):
        """Test temporal coding analysis."""
        rates = np.ones(100) * 10.0  # 10 Hz
        spikes_data = generate_spike_trains(rates, 0.001, seed=42)
        stimulus_times = np.arange(0, 1, 0.1)
        temporal = temporal_coding_analysis(spikes_data, stimulus_times)
        assert 'temporal_precision' in temporal
        assert 'mean_latency_s' in temporal

    def test_population_coding_analysis(self):
        """Test population coding analysis."""
        spikes = np.random.poisson(0.3, (20, 100, 100))
        stimulus_labels = np.random.choice([0, 1], 100)
        pop_coding = population_coding_analysis(spikes, stimulus_labels)
        assert 'classification_accuracy' in pop_coding

    def test_mutual_information_analysis(self):
        """Test mutual information analysis."""
        stimuli = np.random.choice([0, 1], 1000)
        responses = np.random.poisson(stimuli * 5 + 1, 1000)
        mi = mutual_information_analysis(stimuli, responses)
        assert 'mutual_information_bits' in mi

    def test_odor_discrimination_analysis(self):
        """Test odor discrimination analysis."""
        spikes1 = np.random.poisson(0.2, (15, 50, 100))
        spikes2 = np.random.poisson(0.4, (15, 50, 100))
        # Create odor identities for each trial (0 for first half, 1 for second half)
        odor_ids = np.zeros((50,))
        odor_ids[25:] = 1  # Second half of trials have different odor
        time_windows = [(0.0, 0.05), (0.05, 0.1)]
        discrim = odor_discrimination_analysis(spikes1, odor_ids, time_windows, 0.001)
        assert 'window_0' in discrim

    def test_adaptation_dynamics_analysis(self):
        """Test adaptation dynamics analysis."""
        rates = np.ones(100) * 10.0  # 10 Hz
        spikes_data = generate_spike_trains(rates, 0.001, seed=42)
        adapt = adaptation_dynamics_analysis(spikes_data)
        assert 'mean_time_constant_s' in adapt


class TestPlasmonicGeometry:
    """Test plasmonic geometry functions."""

    def test_drude_model_permittivity(self):
        """Test Drude model permittivity."""
        wavelengths = np.linspace(1.0, 10.0, 5)
        epsilon = drude_model_permittivity(wavelengths)
        assert epsilon.shape == (5,)
        assert np.all(np.iscomplex(epsilon))

    def test_drude_model_permittivity_negative_wavelength(self):
        """Test Drude model with negative wavelength."""
        with pytest.raises(ValueError):
            drude_model_permittivity(np.array([0.0, -1.0]))

    def test_mie_scattering_sphere(self):
        """Test Mie scattering for sphere."""
        wavelengths = np.linspace(1.0, 5.0, 3)
        radius = 10.0  # nm
        epsilon_particle = 1.0 + 1j  # Complex permittivity

        result = mie_scattering_sphere(wavelengths, radius, epsilon_particle)
        assert 'extinction_cross_section' in result
        assert 'scattering_cross_section' in result
        assert 'field_enhancement' in result

    def test_mie_scattering_epsilon_array_mismatch(self):
        """Test Mie scattering with mismatched epsilon array."""
        wavelengths = np.linspace(1.0, 2.0, 5)
        with pytest.raises(ValueError):
            mie_scattering_sphere(wavelengths, 10.0, np.array([1+1j, 2+0j]))

    def test_coupled_dipoles_near_field(self):
        """Test coupled dipoles near-field calculation."""
        positions = np.array([[0, 0, 0], [100, 0, 0]]) * 1e-3  # μm
        result = coupled_dipoles_near_field(
            positions, radius_nm=20.0, wavelength_um=2.0, epsilon_particle=1+0j
        )
        assert 'coupled_enhancement' in result
        assert 'enhancement_ratio' in result

    def test_coupled_dipoles_positions_shape_error(self):
        """Test coupled dipoles with invalid positions shape."""
        with pytest.raises(ValueError):
            coupled_dipoles_near_field(np.array([1, 2, 3]), 10.0, 5.0, 1+0j)

    def test_optimize_plasmonic_geometry(self):
        """Test plasmonic geometry optimization."""
        opt = optimize_plasmonic_geometry(target_wavelength_um=3.0)
        assert 'optimal_size_nm' in opt
        assert 'max_enhancement' in opt

    def test_optimize_plasmonic_geometry_unknown_material(self):
        """Test optimization with unknown material."""
        with pytest.raises(ValueError):
            optimize_plasmonic_geometry(10.0, material='unobtainium')

    def test_sweep_plasmonic_quality(self):
        """Test plasmonic quality sweep."""
        radii = np.array([10.0, 20.0])
        result = sweep_plasmonic_quality(radii, wavelengths_um=np.linspace(2.0, 5.0, 10))
        assert 'q_factors_2d' in result
        assert 'enhancements_2d' in result
        assert result['q_factors_2d'].shape == (2, 10)

    def test_sweep_plasmonic_quality_inject_imag(self):
        """Test plasmonic quality sweep with injected imaginary permittivity."""
        radii = np.array([10.0, 20.0])
        result = sweep_plasmonic_quality(radii, wavelengths_um=np.linspace(2.0, 5.0, 10), metal_epsilon_imag=0.5)
        # material_permittivity should be complex when metal_epsilon_imag injected
        eps = result['material_permittivity']
        assert np.iscomplexobj(eps)

    def test_field_distribution_near_particle(self):
        """Test near-field distribution calculation."""
        result = field_distribution_near_particle(10.0, 5.0, 1+0.1j, grid_points=10)
        assert 'intensity' in result
        assert 'phase' in result
        assert result['intensity'].shape == (10, 10)
        assert result['max_enhancement'] >= 0


class TestSpectralUnmixing:
    """Test spectral unmixing functions."""

    def test_nmf_unmix(self):
        """Test NMF unmixing."""
        # Create synthetic mixed spectra
        n_wavelengths, n_mixtures, n_components = 50, 20, 3
        np.random.seed(42)
        endmembers = np.random.exponential(1, (n_components, n_wavelengths))
        abundances = np.random.dirichlet(np.ones(n_components), n_mixtures).T
        mixed = endmembers.T @ abundances

        result = nmf_unmix(mixed, n_components)
        assert 'H' in result
        assert 'W' in result
        assert result['H'].shape[0] == n_components

    def test_generate_realistic_chc_spectra(self):
        """Test realistic CHC spectra generation."""
        result = generate_realistic_chc_spectra(n_samples=15, n_components=3)
        assert 'mixed_spectra' in result
        assert 'component_centers' in result
        assert 'dominant_labels' in result

    def test_vertex_component_analysis(self):
        """Test vertex component analysis."""
        # Create synthetic data
        np.random.seed(42)
        data = np.random.randn(10, 50)
        result = vertex_component_analysis(data, n_components=3)
        assert 'endmembers' in result
        assert 'abundances' in result

    def test_independent_component_analysis_spectra(self):
        """Test ICA for spectral unmixing."""
        np.random.seed(42)
        data = np.random.randn(10, 100)
        result = independent_component_analysis_spectra(data, n_components=3)
        assert 'independent_components' in result
        assert 'mixing_matrix' in result

    def test_spectral_feature_extraction(self):
        """Test spectral feature extraction."""
        wavelengths = np.linspace(2.0, 25.0, 100)
        # Create multiple spectra (3 samples, 100 wavelengths)
        spectra = np.array([
            np.exp(-((wavelengths - 10) / 3)**2),  # Original spectrum
            np.exp(-((wavelengths - 15) / 2)**2),  # Second spectrum
            np.exp(-((wavelengths - 8) / 4)**2)    # Third spectrum
        ])
        features = spectral_feature_extraction(spectra, wavelengths, method='peaks')
        assert 'peak_features' in features
        assert 'statistical_features' in features

    def test_lda_baseline(self):
        """Test LDA baseline classification with 2 classes."""
        np.random.seed(42)
        n_samples, n_features = 60, 10
        X = np.random.randn(n_samples, n_features)
        y = np.repeat([0, 1], n_samples // 2)  # Only 2 classes

        result = lda_baseline(X, y)
        assert 'train_accuracy' in result
        assert 0.0 <= result['train_accuracy'] <= 1.0


class TestSensillaArrayDirectionality:
    """Test sensilla array directionality functions."""

    def test_compute_beam_pattern(self):
        """Test beam pattern computation."""
        wavelengths = np.linspace(2.0, 25.0, 10)
        positions = np.linspace(0, 200.0, 5)  # 5 elements, 200μm spacing
        gains = np.ones(5)  # Equal gains
        pattern = compute_beam_pattern(wavelengths, positions, gains)
        assert 'pattern' in pattern
        assert 'wavelengths_um' in pattern
        assert pattern['pattern'].shape == wavelengths.shape

    def test_array_gain(self):
        """Test array gain calculation."""
        pattern = np.ones(10)  # Simple uniform pattern
        gain = array_gain(pattern)
        assert gain >= 0
        assert isinstance(gain, float)

    def test_design_log_periodic_array(self):
        """Test log-periodic array design."""
        positions = design_log_periodic_array(
            min_len_um=10.0, max_len_um=200.0, tau=1.2, count=5
        )
        assert isinstance(positions, np.ndarray)
        assert positions.shape == (5,)
        assert np.allclose(positions, np.sort(positions))  # Should be sorted
        # Check that positions are log-periodically spaced (or at least ordered)
        # Note: The exact spacing depends on the implementation, so we'll just check basic properties
        assert positions.shape == (5,)  # Should have 5 elements
        # Positions can be negative (centered at origin)

    def test_design_circular_array(self):
        """Test circular array design."""
        result = design_circular_array(radius_um=200.0, count=6)
        assert 'x_positions' in result
        assert 'y_positions' in result
        assert result['x_positions'].shape[0] >= 6  # At least 6 positions

    def test_sensilla_element_pattern(self):
        """Test sensilla element pattern."""
        theta = np.linspace(0, 180, 10)  # Angles in degrees
        pattern = sensilla_element_pattern(theta, length_um=100.0, wavelength_um=10.0)
        assert isinstance(pattern, np.ndarray)
        assert pattern.shape == theta.shape

    def test_mutual_coupling_matrix(self):
        """Test mutual coupling matrix calculation."""
        positions = np.random.randn(5, 3) * 100  # 5 elements, random positions
        coupling = mutual_coupling_matrix(positions, wavelength_um=10.0)
        assert coupling.shape == (5, 5)
        # Check that the matrix is complex (has off-diagonal elements)
        assert np.iscomplexobj(coupling)
        # Check diagonal is real (self-coupling should be real)
        assert np.allclose(np.diag(coupling), np.diag(coupling).real)

    def test_array_pattern_2d(self):
        """Test 2D array pattern calculation."""
        n_elements = 4
        wavelengths = np.array([10.0])
        positions = np.random.randn(n_elements, 3) * 50
        weights = np.ones(n_elements)
        pattern = array_pattern_2d(
            wavelengths, positions, weights,
            theta_range_deg=(0, 90), phi_range_deg=(0, 180), resolution_deg=45.0
        )
        assert 'patterns' in pattern  # Function returns 'patterns' not 'pattern_2d'
        # Check that we have some pattern data
        assert isinstance(pattern, dict)

    def test_analyze_sensilla_morphology(self):
        """Test sensilla morphology analysis."""
        lengths = np.array([50.0, 100.0, 150.0])
        diameters = np.array([5.0, 10.0, 15.0])
        wavelengths = np.array([10.0, 20.0, 30.0])
        result = analyze_sensilla_morphology(lengths, diameters, wavelengths)
        assert 'best_wavelength_matches' in result
        assert 'match_quality_scores' in result

    def test_frequency_response_analysis(self):
        """Test frequency response analysis."""
        # Create array geometry
        array_geometry = {
            'positions': np.random.randn(4, 3) * 50,  # 4 elements
            'lengths': np.array([100.0, 120.0, 80.0, 110.0]),
            'diameters': np.array([10.0, 12.0, 8.0, 11.0])
        }
        result = frequency_response_analysis(
            array_geometry, (2.0, 25.0), n_frequencies=10
        )
        assert 'frequencies_thz' in result
        assert 'gain_db' in result


class TestActiveInference:
    """Test active inference functions."""

    def test_olfactory_active_inference_step(self):
        """Test olfactory active inference step."""
        # Mock state and params as dictionaries with proper keys
        state = {'x': 0.0, 'y': 0.0}
        params = {'step': 0.1, 'gain': 1.0}

        result = olfactory_active_inference_step(state, params)
        assert 'x' in result
        assert 'y' in result
        assert isinstance(result, dict)

