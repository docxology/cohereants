"""Case study orchestration for neural_encoding."""
from __future__ import annotations

from .core import *
from .population import *
from .types import NeuralEncodingAnalysis

def compute_neural_encoding_analysis(seed: int = 42) -> NeuralEncodingAnalysis:
    """Compute spike trains, population coding, and discrimination artifacts."""
    rng = np.random.default_rng(seed)
    dt = 1e-4
    duration = 2.0
    n_time = int(duration / dt)
    time_axis = np.arange(n_time) * dt

    n_trials = 20
    stimulus_patterns: list[np.ndarray] = []
    stimulus_labels: list[int] = []

    for _ in range(n_trials // 4):
        stim = np.zeros(n_time)
        onset_time = 0.5 + 0.1 * rng.standard_normal()
        onset_idx = int(max(0, onset_time / dt))
        offset_idx = int(min(n_time, (onset_time + 0.8) / dt))
        stim[onset_idx:offset_idx] = 2.0 + 0.5 * rng.standard_normal()
        stimulus_patterns.append(stim)
        stimulus_labels.append(0)

    for _ in range(n_trials // 4):
        stim = np.zeros(n_time)
        ramp_start = int(0.4 / dt)
        ramp_end = int(1.2 / dt)
        stim[ramp_start:ramp_end] = np.linspace(0, 3.0, ramp_end - ramp_start)
        stimulus_patterns.append(stim)
        stimulus_labels.append(1)

    for _ in range(n_trials // 4):
        stim = np.zeros(n_time)
        for pulse_t in (0.3, 0.7, 1.1, 1.5):
            pulse_idx = int(pulse_t / dt)
            pulse_width = int(0.05 / dt)
            stim[pulse_idx : pulse_idx + pulse_width] = 2.5
        stimulus_patterns.append(stim)
        stimulus_labels.append(2)

    for _ in range(n_trials - 3 * (n_trials // 4)):
        stim = 1.0 + 0.5 * np.sin(2 * np.pi * 2 * time_axis) + 0.3 * rng.standard_normal(n_time)
        stim = np.maximum(0, stim)
        stimulus_patterns.append(stim)
        stimulus_labels.append(3)

    stimuli = np.array(stimulus_patterns)
    stimulus_labels_arr = np.array(stimulus_labels)

    n_neurons = 5
    population_spike_data: list[Dict[str, object]] = []
    population_responses: list[np.ndarray] = []
    for neuron_idx in range(n_neurons):
        baseline = 5.0 + 10.0 * neuron_idx / n_neurons
        max_rate = 50.0 + 50.0 * neuron_idx / n_neurons
        if neuron_idx < 2:
            dynamics = "exponential"
        elif neuron_idx < 4:
            dynamics = "adaptive"
        else:
            dynamics = "phasic-tonic"
        spike_data = generate_spike_trains(
            stimuli,
            dt=dt,
            baseline_rate=baseline,
            max_rate=max_rate,
            response_dynamics=dynamics,
            seed=seed + neuron_idx,
        )
        population_spike_data.append(spike_data)
        population_responses.append(spike_data["rate_profiles"])

    population_responses_arr = np.array(population_responses)
    spike_stats = analyze_spike_train_statistics(population_spike_data[0])
    stimulus_times = np.array([0.5, 1.0, 1.5])
    temporal_results = temporal_coding_analysis(population_spike_data[0], stimulus_times)
    pop_results = population_coding_analysis(population_responses_arr, stimulus_labels_arr)
    mean_rates = np.mean(population_responses_arr[0], axis=1)
    mi_results = mutual_information_analysis(mean_rates, stimulus_labels_arr)
    time_windows = [(0.1, 0.3), (0.3, 0.8), (0.8, 1.5), (1.5, 2.0)]
    discrimination_results = odor_discrimination_analysis(
        population_responses_arr, stimulus_labels_arr, time_windows, dt
    )
    adaptation_results = adaptation_dynamics_analysis(population_spike_data[0], stimulus_duration=1.0)

    return NeuralEncodingAnalysis(
        time_axis=time_axis,
        stimuli=stimuli,
        stimulus_labels=stimulus_labels_arr,
        n_neurons=n_neurons,
        population_spike_data=population_spike_data,
        population_responses=population_responses_arr,
        spike_stats=spike_stats,
        temporal_results=temporal_results,
        pop_results=pop_results,
        mi_results=mi_results,
        discrimination_results=discrimination_results,
        adaptation_results=adaptation_results,
    )

