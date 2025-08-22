import numpy as np
import pytest

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

from src.case_studies.plasmonic_geometry import (
    drude_model_permittivity,
    mie_scattering_sphere,
    coupled_dipoles_near_field,
    optimize_plasmonic_geometry,
    sweep_plasmonic_quality,
    field_distribution_near_particle,
)

from src.case_studies.spectral_unmixing import (
    nmf_unmix,
    generate_realistic_chc_spectra,
    vertex_component_analysis,
    independent_component_analysis_spectra,
    spectral_feature_extraction,
    lda_baseline,
)

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

from src.case_studies.active_inference import olfactory_active_inference_step


def test_detection_limits_basic():
    pmin = min_detectable_power(300.0, 1e6, 10.0)
    assert pmin > 0

    s = snr_curve(np.array([0.0, pmin, 10 * pmin]), 300.0, 1e6)
    assert s.shape == (3,) and np.all(np.isfinite(s))

    roc = roc_analysis(1.0, 0.1)
    assert 'auc' in roc and 0.0 <= roc['auc'] <= 1.0

    perf = detection_performance_vs_snr(np.linspace(-10, 20, 5))
    assert 'pd' in perf and perf['pd'].shape[0] == 5

    base = {'temperature_k': 300.0, 'bandwidth_hz': 1e6}
    ranges = {'temperature_k': (290.0, 310.0)}
    sens = sensitivity_analysis(base, ranges, n_points=5)
    assert 'temperature_k' in sens

    or_regions = operating_regions_analysis(np.logspace(-12, -6, 5), np.linspace(280, 320, 4))
    assert 'snr_grid_db' in or_regions

    nf = noise_floor_analysis(np.array([1e3, 1e4, 1e5]), temperature_k=300.0)
    assert 'total_noise_db' in nf

    dr = detection_range_analysis(1.0, 10.0, 3e12, -90.0)
    assert 'max_range_free_space_m' in dr

    opt = optimize_detection_parameters({'temperature_k': (290.0, 310.0), 'bandwidth_hz': (1e5, 1e7)},
                                        {'mdp_target': 1e-20}, {'current_a': 1e-6})
    assert 'optimized_parameters' in opt

    op = operating_point(1000.0, 3.0)
    assert op['snr_linear'] == pytest.approx(10 ** (3.0 / 10.0))


def test_environmental_channel_and_capacity():
    wl = np.array([3.0, 10.0, 20.0])
    t = atmospheric_transmission_detailed(wl, humidity=0.5, temperature_k=300.0, path_m=100.0)
    assert t.shape == wl.shape

    cs = molecular_absorption_cross_section(wl, molecule='H2O')
    assert cs.shape == wl.shape

    rc = rayleigh_scattering_coefficient(wl)
    assert rc.shape == wl.shape

    comp = atmospheric_transmission_comprehensive(wl, 100.0)
    assert 'transmission_total' in comp

    cap = channel_capacity_analysis(wl, 100.0, -10.0)
    assert 'capacity_bps' in cap

    opt_w = optimize_wavelength_for_range(100.0, 1.0)
    assert 'optimal_wavelength_um' in opt_w

    sens = environmental_sensitivity_analysis(10.0, 100.0, {'humidity': (10.0, 90.0)})
    assert 'humidity' in sens

    grid = channel_capacity_vs_env(1.5, 1e-6, 1e6, np.linspace(0.2, 0.8, 3), np.linspace(280.0, 320.0, 2), 100.0)
    assert 'capacity_bits_per_s' in grid


def test_neural_encoding_and_spike_generation():
    x = np.sin(np.linspace(0, 2 * np.pi, 100))
    ir = information_rate_time_series(x, dt_s=0.001, noise_std=0.1)
    assert ir['channel_capacity_bits'] >= 0

    y = np.r_[np.zeros(50), np.ones(50)]
    rc = rate_coding_metrics(np.random.randn(100), y)
    assert 'd_prime' in rc

    stimuli = np.zeros(200)
    stimuli[50:100] = 1.0
    spikes = generate_spike_trains(stimuli, dt=1e-3, baseline_rate=5.0, max_rate=50.0, seed=42)
    stats = analyze_spike_train_statistics(spikes)
    assert 'mean_firing_rate_hz' in stats

    tc = temporal_coding_analysis(spikes, np.array([0.05]))
    assert 'mean_latency_s' in tc

    pop = np.random.rand(3, 4, 50)
    labels = np.array([0, 1, 0, 1])
    pca = population_coding_analysis(pop, labels)
    assert 'explained_variance_ratio' in pca

    mi = mutual_information_analysis(np.random.rand(100), np.random.randint(0, 2, 100))
    assert 'mutual_information_bits' in mi

    # Odor discrimination: small synthetic
    n_neurons = 2
    n_trials = 4
    n_time = 20
    population_responses = np.random.rand(n_neurons, n_trials, n_time)
    odors = np.array([0, 0, 1, 1])
    od = odor_discrimination_analysis(population_responses, odors, [(0.0, 0.01)], dt=1e-3)
    assert 'window_0' in od

    ad = adaptation_dynamics_analysis(spikes, stimulus_duration=0.1)
    assert 'mean_peak_response' in ad


def test_plasmonic_and_field_models():
    wl = np.linspace(1.0, 10.0, 10)
    eps = drude_model_permittivity(wl)
    assert eps.shape == wl.shape

    mie = mie_scattering_sphere(wl, 20.0, epsilon_particle=1.5 + 0.1j)
    assert 'quality_factor' in mie

    pos = np.array([[0, 0, 0], [50, 0, 0]])
    near = coupled_dipoles_near_field(pos, 20.0, 5.0, 1.5 + 0.1j)
    assert 'coupling_strength' in near

    opt = optimize_plasmonic_geometry(8.0)
    assert 'optimal_size_nm' in opt

    # sweep with default wavelengths
    sweep = sweep_plasmonic_quality(np.linspace(10.0, 100.0, 5))
    assert 'q_factor_proxy' in sweep

    fd = field_distribution_near_particle(20.0, 5.0, 1.5 + 0.1j)
    assert 'intensity' in fd


def test_spectral_unmixing_and_lda():
    rng = np.random.default_rng(42)
    W = rng.random((10, 2))
    H = rng.random((2, 15))
    X = W @ H
    nmf = nmf_unmix(X, n_components=2, seed=42)
    assert 'W' in nmf and 'H' in nmf

    spec = generate_realistic_chc_spectra(3, 50)
    # returns dict with 'mixed_spectra' key
    assert 'mixed_spectra' in spec and spec['mixed_spectra'].shape[1] == 50

    vca = vertex_component_analysis(X, 2)
    ica = independent_component_analysis_spectra(X, 2)
    wavelengths = np.linspace(2.5, 25.0, X.shape[1])
    feats = spectral_feature_extraction(X, wavelengths, method='peaks')
    # Use statistical features (n_samples x n_features) for LDA baseline
    stat_feats = feats['statistical_features']
    labels = np.r_[np.zeros(stat_feats.shape[0]//2), np.ones(stat_feats.shape[0] - stat_feats.shape[0]//2)]
    lda = lda_baseline(stat_feats, labels, seed=42)
    assert 'train_accuracy' in lda


def test_sensilla_array_and_active_inference():
    wl = np.linspace(2.0, 8.0, 20)
    pos = design_log_periodic_array(1.0, 20.0, 1.3, 5)
    gains = np.ones_like(pos)
    bp = compute_beam_pattern(wl, pos, gains)
    assert 'wavelengths_um' in bp

    g = array_gain(np.ones(10))
    assert np.isfinite(g)

    circ = design_circular_array(10.0, 4)
    # legacy API exposes x/y positions
    assert 'x_positions' in circ and 'y_positions' in circ

    theta = np.linspace(0, 180, 37)
    elem_pattern = sensilla_element_pattern(theta, 10.0, 5.0)
    assert np.all(elem_pattern >= 0)

    mc = mutual_coupling_matrix(np.array([[0,0,0],[1,0,0]]), 5.0)
    ap = array_pattern_2d(np.array([5.0]), np.array([[0.0, 0.0]]), np.ones(1))
    morph = analyze_sensilla_morphology(np.array([10.0]), np.array([1.0]), np.array([2.0, 5.0]))
    # frequency_response_analysis expects positions as (N,2) array
    fr = frequency_response_analysis({'positions': np.column_stack([pos, np.zeros_like(pos)])}, [wl.min(), wl.max()])
    assert isinstance(morph, dict)

    s = {'x': 1.0, 'y': 0.0}
    p = {'step': 0.1, 'gain': 1.0}
    new_s = olfactory_active_inference_step(s, p)
    assert 'x' in new_s


