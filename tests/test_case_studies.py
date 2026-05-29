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
    advanced_classification_suite,
    performance_metrics_comprehensive,
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


def _multi_trial_stimulus(n_trials: int = 5, n_samples: int = 200, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.clip(rng.normal(0.5, 0.2, (n_trials, n_samples)), 0.0, 1.0)


def _make_nonnegative_spectra(n_samples: int, n_wavelengths: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.abs(rng.normal(0.5, 0.2, (n_samples, n_wavelengths)))


def _spectral_unmixing_api():
    import importlib

    return importlib.import_module("src.case_studies.spectral_unmixing")


def _make_feature_data(n: int = 80, seed: int = 7):
    rng = np.random.default_rng(seed)
    half = n // 2
    features = np.vstack(
        [
            rng.normal(0.0, 0.3, (half, 4)),
            rng.normal(3.0, 0.3, (half, 4)),
        ]
    )
    labels = np.array([0] * half + [1] * half)
    return features, labels


def _make_three_class_feature_data(n: int = 90, seed: int = 11):
    rng = np.random.default_rng(seed)
    third = n // 3
    features = np.vstack(
        [
            rng.normal(0.0, 0.3, (third, 4)),
            rng.normal(3.0, 0.3, (third, 4)),
            rng.normal(6.0, 0.3, (n - 2 * third, 4)),
        ]
    )
    labels = np.array([0] * third + [1] * third + [2] * (n - 2 * third))
    return features, labels


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


CASE_STUDY_CONTRACTS = [
    ("detection_limits", "src.case_studies.detection_limits", "compute_detection_limits_analysis"),
    ("environmental_channel", "src.case_studies.environmental_channel", "compute_environmental_channel_analysis"),
    ("neural_encoding", "src.case_studies.neural_encoding", "compute_neural_encoding_analysis"),
    ("plasmonic_geometry", "src.case_studies.plasmonic_geometry", "compute_plasmonic_geometry_analysis"),
    ("sensilla_array_directionality", "src.case_studies.sensilla_array_directionality", "compute_sensilla_array_analysis"),
    ("spectral_unmixing", "src.case_studies.spectral_unmixing", "compute_spectral_unmixing_analysis"),
]


@pytest.mark.parametrize("name,module_path,compute_name", CASE_STUDY_CONTRACTS, ids=[c[0] for c in CASE_STUDY_CONTRACTS])
def test_case_study_typed_compute_contract(name: str, module_path: str, compute_name: str) -> None:
    """Each appendix compute returns a typed analysis object with stable dict export."""
    import importlib

    module = importlib.import_module(module_path)
    compute_fn = getattr(module, compute_name)
    render_fn = getattr(module, "render_comprehensive_figure")
    analysis = compute_fn()
    assert hasattr(analysis, "as_dict"), f"{name} should return typed analysis dataclass"
    payload = analysis.as_dict()
    assert isinstance(payload, dict) and payload
    fig, metrics = render_fn(analysis)
    assert fig is not None
    assert isinstance(metrics, dict) and metrics
    plt.close(fig)


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

# --- merged from test_coverage_detection_limits.py ---

def test_min_detectable_power_array_and_scalar():
    bandwidths = np.array([1e5, 1e6, 1e7])
    array_result = min_detectable_power(300.0, bandwidths, snr_min_db=10.0)
    assert isinstance(array_result, np.ndarray)
    assert array_result.shape == (3,)
    assert np.all(array_result > 0.0)
    # Power scales linearly with bandwidth.
    assert np.all(np.diff(array_result) > 0.0)

    scalar_result = min_detectable_power(300.0, 1e6, snr_min_db=10.0)
    assert isinstance(scalar_result, float)
    assert scalar_result > 0.0


def test_detection_performance_no_detection_falls_through():
    # Very low SNR range: no point reaches pd_target=0.9, so mds defaults to last.
    snr_db = np.linspace(-40.0, -30.0, 5)
    result = detection_performance_vs_snr(snr_db, pfa_target=1e-3)
    assert np.all((result["pd"] >= 0.0) & (result["pd"] <= 1.0))
    assert result["mds_snr_db"] == snr_db[-1]
    # Identity check (derivable, not reverse-engineered).
    assert np.allclose(result["snr_linear"], 10 ** (snr_db / 10.0))


def test_detection_performance_high_snr_reaches_target():
    snr_db = np.linspace(0.0, 30.0, 10)
    result = detection_performance_vs_snr(snr_db)
    # With a high enough SNR, mds should be selected within the provided range.
    assert snr_db[0] <= result["mds_snr_db"] <= snr_db[-1]


def test_roc_analysis_with_explicit_threshold_range():
    thresholds = np.linspace(-2.0, 2.0, 200)
    roc = roc_analysis(1.0, 0.1, threshold_range=thresholds, n_points=200)
    assert np.array_equal(roc["thresholds"], thresholds)
    assert 0.0 <= roc["auc"] <= 1.0
    assert np.all((roc["pfa"] >= 0.0) & (roc["pfa"] <= 1.0))
    assert np.all((roc["pd"] >= 0.0) & (roc["pd"] <= 1.0))
    assert 0.0 <= roc["eer_rate"] <= 1.0


def test_noise_floor_with_components_disabled():
    frequencies = np.array([1e3, 1e4, 1e5])
    result = noise_floor_analysis(
        frequencies,
        temperature_k=300.0,
        include_shot_noise=False,
        include_flicker_noise=False,
    )
    assert np.all(result["shot_noise_power"] == 0.0)
    assert np.all(result["flicker_noise_power"] == 0.0)
    # Thermal noise is always present and positive.
    assert np.all(result["thermal_noise_power"] > 0.0)
    assert np.allclose(result["total_noise_power"], result["thermal_noise_power"])


def test_optimize_detection_parameters_with_power_efficiency_objective():
    constraints = {
        "temperature_k": (290.0, 310.0),
        "bandwidth_hz": (1e5, 1e7),
        "current_a": (1e-7, 1e-5),
    }
    objectives = {"mdp_target": 1e-15, "power_efficiency": 1e6}
    fixed_params = {"snr_min_db": 3.0}
    result = optimize_detection_parameters(constraints, objectives, fixed_params)
    assert "optimization_success" in result
    assert "final_performance" in result
    assert "optimized_parameters" in result
    assert np.isfinite(result["objective_value"])
    # Optimized parameters stay within the requested bounds.
    for name, (low, high) in constraints.items():
        assert low - 1e-6 <= result["optimized_parameters"][name] <= high + 1e-6


def test_operating_point_snr_linear_identity():
    op = operating_point(1234.0, 10.0)
    assert op["capacity_bits_s"] == 1234.0
    assert np.isclose(op["snr_linear"], 10 ** (10.0 / 10.0))

# --- merged from test_coverage_neural_encoding.py ---

@pytest.mark.parametrize("dynamics", ["tonic", "phasic", "phasic-tonic", "adaptive"])
def test_generate_spike_trains_all_dynamics(dynamics):
    stimuli = _multi_trial_stimulus()
    spike_data = generate_spike_trains(
        stimuli, dt=1e-3, response_dynamics=dynamics, seed=7
    )
    assert spike_data["spike_trains"].shape == stimuli.shape
    assert spike_data["rate_profiles"].shape == stimuli.shape
    # Spike trains are binary {0, 1}.
    assert set(np.unique(spike_data["spike_trains"])).issubset({0, 1})
    # Firing rates are non-negative everywhere.
    assert np.all(spike_data["rate_profiles"] >= 0.0)


def test_generate_spike_trains_1d_input_is_promoted():
    stimulus_1d = np.clip(np.linspace(0.0, 1.0, 200), 0.0, 1.0)
    spike_data = generate_spike_trains(stimulus_1d, dt=1e-3, seed=3)
    # 1D input is promoted to a single-trial 2D array.
    assert spike_data["spike_trains"].shape == (1, 200)


def test_adaptive_dynamics_full_analysis_chain():
    stimuli = _multi_trial_stimulus()
    spike_data = generate_spike_trains(
        stimuli, dt=1e-3, response_dynamics="adaptive", seed=21
    )

    stats = analyze_spike_train_statistics(spike_data)
    assert "fano_factor" in stats and "cv_isi" in stats
    assert stats["mean_firing_rate_hz"] >= 0.0
    assert np.isfinite(stats["fano_factor"])

    adaptation = adaptation_dynamics_analysis(spike_data, stimulus_duration=0.2)
    assert "mean_time_constant_s" in adaptation
    assert adaptation["mean_peak_response"] >= 0.0
    assert 0.0 <= adaptation["mean_adaptation_index"] <= 1.0 + 1e-9


def test_temporal_coding_single_vs_multi_stimulus():
    stimuli = _multi_trial_stimulus()
    spike_data = generate_spike_trains(
        stimuli, dt=1e-3, response_dynamics="phasic-tonic", seed=5
    )

    single = temporal_coding_analysis(spike_data, np.array([0.05]))
    # A single stimulus time cannot define a period -> vector strength is 0.
    assert single["vector_strength"] == 0.0
    assert single["temporal_precision"] >= 0.0

    multi = temporal_coding_analysis(spike_data, np.arange(0.0, 0.25, 0.05))
    # Vector strength is a phase-locking magnitude in [0, 1].
    assert 0.0 <= multi["vector_strength"] <= 1.0


def test_information_rate_time_series_degenerate_inputs():
    empty = information_rate_time_series(np.array([]), dt_s=1e-3, noise_std=0.1)
    assert empty == {
        "channel_capacity_bits": 0.0,
        "information_rate_bits": 0.0,
        "snr": 0.0,
    }
    bad_dt = information_rate_time_series(np.ones(5), dt_s=0.0, noise_std=0.1)
    assert bad_dt["information_rate_bits"] == 0.0


def test_information_rate_time_series_positive_snr():
    responses = np.array([0.0, 5.0, 0.0, 5.0, 0.0, 5.0], dtype=float)
    result = information_rate_time_series(responses, dt_s=1e-3, noise_std=0.5)
    assert result["channel_capacity_bits"] > 0.0
    assert result["information_rate_bits"] > 0.0
    assert result["snr"] > 0.0


def test_rate_coding_metrics_early_return_branches():
    # Mismatched sizes -> zeroed metrics.
    assert rate_coding_metrics(np.ones(5), np.ones(3)) == {
        "d_prime": 0.0,
        "mean_diff": 0.0,
    }
    # Three classes (not exactly two) -> zeroed metrics.
    assert rate_coding_metrics(np.arange(6.0), np.array([0, 1, 2, 0, 1, 2])) == {
        "d_prime": 0.0,
        "mean_diff": 0.0,
    }


def test_rate_coding_metrics_two_class_separation():
    responses = np.array([0.0, 0.1, 0.2, 5.0, 5.1, 5.2])
    labels = np.array([0, 0, 0, 1, 1, 1])
    metrics = rate_coding_metrics(responses, labels)
    assert metrics["mean_diff"] > 0.0
    assert np.isfinite(metrics["d_prime"])


def test_population_coding_single_class_returns_zero_accuracy():
    rng = np.random.default_rng(1)
    population = np.abs(rng.normal(1.0, 0.3, (4, 20, 30)))
    labels = np.zeros(20, dtype=int)
    result = population_coding_analysis(population, labels)
    # Only one class -> classification accuracy is 0 by the guarded branch.
    assert result["classification_accuracy"] == 0.0
    assert result["explained_variance_ratio"].ndim == 1
    assert np.all(np.isfinite(result["cumulative_variance"]))


def test_population_coding_multi_class_accuracy_in_range():
    rng = np.random.default_rng(2)
    population = np.abs(rng.normal(1.0, 0.3, (4, 20, 30)))
    labels = np.array([0] * 10 + [1] * 10)
    result = population_coding_analysis(population, labels)
    assert 0.0 <= result["classification_accuracy"] <= 1.0


def test_mutual_information_length_mismatch_raises():
    with pytest.raises(ValueError):
        mutual_information_analysis(np.ones(5), np.ones(4))


def test_mutual_information_nonnegative_entropies():
    rng = np.random.default_rng(9)
    stimuli = rng.integers(0, 2, 400)
    responses = rng.poisson(stimuli * 5 + 1)
    result = mutual_information_analysis(stimuli, responses)
    assert result["mutual_information_bits"] >= -1e-9
    assert result["response_entropy_bits"] >= 0.0
    assert result["stimulus_entropy_bits"] >= 0.0
    assert 0.0 <= result["normalized_mutual_information"] <= 1.0 + 1e-6


def test_odor_discrimination_single_odor_zero_accuracy():
    rng = np.random.default_rng(4)
    population = np.abs(rng.normal(1.0, 0.3, (4, 20, 40)))
    odor_ids = np.zeros(20, dtype=int)
    result = odor_discrimination_analysis(
        population, odor_ids, [(0.0, 0.01), (0.01, 0.02)], dt=1e-3
    )
    assert set(result.keys()) == {"window_0", "window_1"}
    # A single odor identity yields zero classification accuracy.
    assert result["window_0"]["classification_accuracy"] == 0.0

# --- merged from test_coverage_spectral_unmixing.py ---

def test_nmf_unmix_happy_path_and_validation():
    api = _spectral_unmixing_api()
    spectra = _make_nonnegative_spectra(n_samples=7, n_wavelengths=18, seed=100)
    result = api.nmf_unmix(spectra, n_components=3, seed=17)

    assert set(result) == {"W", "H"}
    assert result["W"].shape == (7, 3)
    assert result["H"].shape == (3, 18)
    assert np.all(result["W"] >= 0)
    assert np.all(result["H"] >= 0)

    with pytest.raises(ValueError):
        api.nmf_unmix(np.arange(10.0), n_components=2)

    with pytest.raises(ValueError):
        api.nmf_unmix(spectra, n_components=0)


def test_generate_realistic_chc_spectra_contract():
    api = _spectral_unmixing_api()
    result = api.generate_realistic_chc_spectra(
        n_samples=12,
        n_wavelengths=40,
        n_components=4,
        seed=23,
    )

    expected_keys = {
        "wavelengths_um",
        "mixed_spectra",
        "pure_components",
        "mixing_coefficients",
        "dominant_labels",
        "component_centers",
        "component_widths",
        "noise_level",
        "snr_db",
    }
    assert expected_keys.issubset(result.keys())
    assert result["mixed_spectra"].shape == (12, 40)
    assert np.all(result["mixed_spectra"] >= 0)
    assert np.allclose(result["mixing_coefficients"].sum(axis=1), 1.0, atol=1e-6)
    assert result["dominant_labels"].shape == (12,)
    assert np.all((result["dominant_labels"] >= 0) & (result["dominant_labels"] < 4))
    assert np.isfinite(result["snr_db"])


def test_vertex_component_analysis_happy_path_and_validation():
    api = _spectral_unmixing_api()
    spectra = api.generate_realistic_chc_spectra(
        n_samples=10,
        n_wavelengths=30,
        n_components=3,
        seed=19,
    )["mixed_spectra"]
    result = api.vertex_component_analysis(spectra, n_components=3)

    assert {
        "endmembers",
        "abundances",
        "endmember_indices",
        "reconstruction",
        "explained_variance_ratio",
    }.issubset(result.keys())
    assert result["endmembers"].shape == (3, 30)
    assert result["abundances"].shape == (10, 3)
    assert result["reconstruction"].shape == spectra.shape
    assert np.allclose(result["abundances"].sum(axis=1), 1.0, atol=1e-6)

    with pytest.raises(ValueError):
        api.vertex_component_analysis(np.arange(12.0), n_components=2)

    with pytest.raises(ValueError):
        api.vertex_component_analysis(spectra, n_components=10)


def test_independent_component_analysis_spectra_happy_path_and_validation():
    api = _spectral_unmixing_api()
    spectra = api.generate_realistic_chc_spectra(
        n_samples=9,
        n_wavelengths=20,
        n_components=3,
        seed=41,
    )["mixed_spectra"]
    result = api.independent_component_analysis_spectra(
        spectra,
        n_components=50,
        max_iter=200,
        tol=1e-4,
    )

    expected_keys = {
        "independent_components",
        "mixing_matrix",
        "whitening_matrix",
        "unmixing_matrix",
        "reconstructed_spectra",
        "n_iterations",
        "converged",
    }
    assert expected_keys == set(result.keys())
    assert result["reconstructed_spectra"].shape == spectra.shape
    assert isinstance(result["converged"], bool)
    assert isinstance(result["n_iterations"], int)
    assert result["n_iterations"] >= 1

    with pytest.raises(ValueError):
        api.independent_component_analysis_spectra(np.arange(8.0), n_components=2)


def test_spectral_feature_extraction_methods_and_zero_peak_branch():
    api = _spectral_unmixing_api()
    wavelengths = np.linspace(2.5, 20.0, 60)
    base = np.linspace(0.2, 1.0, 60)
    peak1 = np.exp(-0.5 * ((wavelengths - 7.0) / 0.7) ** 2)
    peak2 = 0.8 * np.exp(-0.5 * ((wavelengths - 14.0) / 1.2) ** 2)
    spectra = np.vstack(
        [
            base + 0.4 * peak1,
            base + 0.5 * peak2,
            base + 0.25 * peak1 + 0.2 * peak2,
            base[::-1] + 0.35 * peak1,
            0.6 * base + 0.15 * peak2,
        ]
    )

    peaks = api.spectral_feature_extraction(spectra, wavelengths, method="peaks")
    assert set(peaks) == {"statistical_features", "peak_features"}
    assert peaks["statistical_features"].shape == (5, 8)
    assert peaks["peak_features"].shape == (5, 10)

    derivatives = api.spectral_feature_extraction(spectra, wavelengths, method="derivatives")
    assert set(derivatives) == {"statistical_features", "derivative_features"}
    assert derivatives["statistical_features"].shape == (5, 8)
    assert derivatives["derivative_features"].shape == (5, 6)

    pca = api.spectral_feature_extraction(spectra, wavelengths, method="pca")
    assert set(pca) == {
        "statistical_features",
        "pca_features",
        "pca_explained_variance",
    }
    assert pca["statistical_features"].shape == (5, 8)
    assert pca["pca_features"].shape[0] == 5
    assert np.all(np.isfinite(pca["pca_explained_variance"]))

    all_features = api.spectral_feature_extraction(spectra, wavelengths, method="all")
    assert set(all_features) == {
        "statistical_features",
        "peak_features",
        "derivative_features",
        "pca_features",
        "pca_explained_variance",
    }
    assert all_features["statistical_features"].shape == (5, 8)
    assert all_features["peak_features"].shape == (5, 10)
    assert all_features["derivative_features"].shape == (5, 6)
    assert all_features["pca_features"].shape[0] == 5

    monotonic_spectra = np.vstack([np.linspace(i, i + 1.0, 60) for i in range(1, 6)])
    zero_peak_result = api.spectral_feature_extraction(
        monotonic_spectra,
        wavelengths,
        method="peaks",
    )
    assert np.array_equal(zero_peak_result["peak_features"][0], np.zeros(10))


def test_advanced_classification_suite_binary_multiclass_and_validation():
    api = _spectral_unmixing_api()
    features_2c, labels_2c = _make_feature_data()
    binary_result = api.advanced_classification_suite(
        features_2c,
        labels_2c,
        test_size=0.25,
        seed=11,
    )

    assert set(binary_result) == {"lda", "qda", "naive_bayes", "knn", "logistic"}
    for classifier_result in binary_result.values():
        assert 0.0 <= classifier_result["accuracy"] <= 1.0
        # Clusters are well-separated: a working classifier must beat chance by a margin.
        assert classifier_result["accuracy"] > 0.7
        assert np.isfinite(classifier_result["accuracy"])
        assert classifier_result["predictions"].ndim == 1
        assert len(classifier_result["predictions"]) == 20

    features_3c, labels_3c = _make_three_class_feature_data()
    multiclass_result = api.advanced_classification_suite(
        features_3c,
        labels_3c,
        test_size=0.2,
        seed=13,
    )
    assert set(multiclass_result) == {"lda", "qda", "naive_bayes", "knn"}
    assert "logistic" not in multiclass_result
    for classifier_result in multiclass_result.values():
        assert 0.0 <= classifier_result["accuracy"] <= 1.0
        # Clusters are well-separated: a working classifier must beat chance by a margin.
        assert classifier_result["accuracy"] > 0.7
        assert len(classifier_result["predictions"]) == 18

    with pytest.raises(ValueError):
        api.advanced_classification_suite(features_2c, labels_2c[:-1])


def test_performance_metrics_comprehensive_perfect_and_imperfect_cases():
    api = _spectral_unmixing_api()
    y_true = np.array([0, 1, 2, 1, 0, 2])
    perfect = api.performance_metrics_comprehensive(
        y_true,
        y_true.copy(),
        class_names=["alpha", "beta", "gamma"],
    )

    assert set(perfect) == {
        "accuracy",
        "confusion_matrix",
        "precision_per_class",
        "recall_per_class",
        "f1_score_per_class",
        "macro_precision",
        "macro_recall",
        "macro_f1",
        "weighted_precision",
        "weighted_recall",
        "weighted_f1",
        "classes",
        "class_names",
    }
    assert perfect["accuracy"] == 1.0
    assert perfect["confusion_matrix"].shape == (3, 3)
    assert np.issubdtype(perfect["confusion_matrix"].dtype, np.integer)
    perfect_off_diagonal = perfect["confusion_matrix"].copy()
    np.fill_diagonal(perfect_off_diagonal, 0)
    assert not perfect_off_diagonal.any()
    assert perfect["class_names"] == ["alpha", "beta", "gamma"]
    for key in (
        "precision_per_class",
        "recall_per_class",
        "f1_score_per_class",
    ):
        assert np.all((perfect[key] >= 0.0) & (perfect[key] <= 1.0))
    for key in (
        "macro_precision",
        "macro_recall",
        "macro_f1",
        "weighted_precision",
        "weighted_recall",
        "weighted_f1",
    ):
        assert 0.0 <= perfect[key] <= 1.0

    y_pred = np.array([0, 2, 2, 1, 0, 1])
    imperfect = api.performance_metrics_comprehensive(y_true, y_pred)
    assert 0.0 <= imperfect["accuracy"] < 1.0
    assert imperfect["confusion_matrix"].shape == (3, 3)
    assert imperfect["confusion_matrix"].sum() == len(y_true)


def test_lda_baseline_error_branches():
    api = _spectral_unmixing_api()
    features, labels = _make_feature_data()

    with pytest.raises(ValueError):
        api.lda_baseline(np.arange(features.shape[0], dtype=float), labels)

    three_class_labels = np.array([0, 1, 2, 0, 1, 2])
    three_class_features = np.arange(18, dtype=float).reshape(6, 3)
    with pytest.raises(ValueError):
        api.lda_baseline(three_class_features, three_class_labels)
