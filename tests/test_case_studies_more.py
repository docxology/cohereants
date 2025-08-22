import numpy as np

from src.case_studies.spectral_unmixing import (
    generate_realistic_chc_spectra,
    spectral_feature_extraction,
    advanced_classification_suite,
    performance_metrics_comprehensive,
)

from src.case_studies.sensilla_array_directionality import (
    design_circular_array,
    array_pattern_2d,
    frequency_response_analysis,
    _calculate_bandwidth,
    _calculate_average_q_factor,
)

from src.case_studies.neural_encoding import (
    generate_spike_trains,
    temporal_coding_analysis,
)


def test_spectral_unmixing_advanced_and_metrics():
    # Generate synthetic spectra
    data = generate_realistic_chc_spectra(n_samples=20, n_wavelengths=60, n_components=3, seed=0)
    X = data['mixed_spectra']
    wavelengths = data['wavelengths_um']

    # Feature extraction methods
    feats_peaks = spectral_feature_extraction(X, wavelengths, method='peaks')
    feats_deriv = spectral_feature_extraction(X, wavelengths, method='derivatives')
    feats_all = spectral_feature_extraction(X, wavelengths, method='all')

    # Advanced classification suite uses internal helper classifiers
    # Prepare features and labels
    features = feats_all['statistical_features']
    labels = np.array([0 if i < 10 else 1 for i in range(len(features))])
    results = advanced_classification_suite(features, labels, test_size=0.3, seed=1)
    assert 'lda' in results and 'qda' in results and 'naive_bayes' in results

    # Performance metrics
    y_true = labels
    # Ensure predictions array matches length of true labels
    y_pred = labels.copy()
    perf = performance_metrics_comprehensive(y_true, y_pred)
    assert 'accuracy' in perf


def test_sensilla_array_bandwidth_and_response():
    circ = design_circular_array(10.0, 6)
    positions = np.column_stack([circ['x_positions'], circ['y_positions']])

    # Compute array pattern including coupling
    ap = array_pattern_2d(np.array([5.0, 7.0]), positions, np.ones(positions.shape[0]), include_coupling=True)
    assert 'patterns' in ap and ap['patterns'].ndim == 3

    # Frequency response (should compute q-factor/bandwidth)
    freq_resp = frequency_response_analysis({'positions': positions}, (0.1, 0.5), n_frequencies=20)
    assert 'gain_db' in freq_resp

    # Directly test bandwidth helper with synthetic gain curve
    freqs = np.linspace(0.1, 0.5, 50)
    gain = np.zeros_like(freqs)
    gain[20:30] = 10.0  # artificial peak
    bw = _calculate_bandwidth(freqs, gain)
    assert bw >= 0

    q = _calculate_average_q_factor(freqs, gain, [25])
    assert isinstance(q, float)


def test_neural_encoding_adaptive_and_phasic():
    stim = np.zeros(200)
    stim[50:120] = np.linspace(0, 1, 70)

    # adaptive dynamics
    spikes_adaptive = generate_spike_trains(stim, dt=1e-3, response_dynamics='adaptive', seed=123)
    assert 'spike_trains' in spikes_adaptive

    # phasic-tonic dynamics
    spikes_phasic = generate_spike_trains(stim, dt=1e-3, response_dynamics='phasic-tonic', seed=123)
    assert 'rate_profiles' in spikes_phasic

    # temporal coding analysis with multiple stimulus times -> phase locking branch
    tc = temporal_coding_analysis(spikes_phasic, np.array([0.05, 0.1, 0.15]))
    assert 'vector_strength' in tc


