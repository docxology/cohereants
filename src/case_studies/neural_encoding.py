"""Appendix D: Neural encoding efficiency and temporal dynamics analysis.

This module provides comprehensive neural encoding analysis for olfactory receptor neurons
(ORNs), including temporal dynamics, spike train analysis, population coding metrics,
and information-theoretic measures.
"""
from __future__ import annotations

from typing import Dict, List, Tuple, Union, Optional
import numpy as np
from scipy.signal import find_peaks, filtfilt, butter
from scipy.stats import poisson, entropy

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def information_rate_time_series(responses: np.ndarray, dt_s: float, noise_std: float) -> Dict[str, float]:
    """
    Estimate information metrics using a Gaussian channel approximation.
    Deterministic and vectorized.
    """
    x = np.asarray(responses, dtype=float)
    n = x.size
    if n == 0 or dt_s <= 0:
        return {'channel_capacity_bits': 0.0, 'information_rate_bits': 0.0, 'snr': 0.0}
    signal_power = float(np.var(x))
    noise_power = float(noise_std ** 2)
    snr = signal_power / (noise_power + 1e-30)
    capacity = 0.5 * np.log2(1.0 + snr)
    info_rate = capacity * n
    return {'channel_capacity_bits': float(capacity), 'information_rate_bits': float(info_rate), 'snr': float(snr)}


def rate_coding_metrics(responses: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
    """
    Compute simple separability metrics (means/stds) deterministically.
    """
    r = np.asarray(responses, dtype=float)
    y = np.asarray(labels)
    if r.size == 0 or y.size == 0 or r.size != y.size:
        return {'d_prime': 0.0, 'mean_diff': 0.0}
    classes = np.unique(y)
    if classes.size != 2:
        return {'d_prime': 0.0, 'mean_diff': 0.0}
    m0 = float(np.mean(r[y == classes[0]]))
    m1 = float(np.mean(r[y == classes[1]]))
    s0 = float(np.std(r[y == classes[0]]) + 1e-12)
    s1 = float(np.std(r[y == classes[1]]) + 1e-12)
    dprime = (m1 - m0) / np.sqrt(0.5 * (s0 ** 2 + s1 ** 2))
    return {'d_prime': float(dprime), 'mean_diff': float(m1 - m0)}


def generate_spike_trains(stimuli: np.ndarray, dt: float = 1e-4, 
                         baseline_rate: float = 10.0, max_rate: float = 100.0,
                         response_dynamics: str = 'exponential', seed: int = 42) -> Dict[str, np.ndarray]:
    """
    Generate realistic spike trains for ORN responses to odor stimuli.
    
    Args:
        stimuli: Array of stimulus intensities (shape: n_time or n_trials x n_time)
        dt: Time step in seconds
        baseline_rate: Baseline firing rate (Hz)
        max_rate: Maximum firing rate (Hz)
        response_dynamics: Type of response dynamics ('exponential', 'adaptive', 'phasic-tonic')
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary with spike times, spike trains, and rate profiles
    """
    np.random.seed(seed)
    stimuli = np.asarray(stimuli)
    
    if stimuli.ndim == 1:
        stimuli = stimuli[np.newaxis, :]
    
    n_trials, n_time = stimuli.shape
    time_axis = np.arange(n_time) * dt
    
    spike_trains = []
    spike_times_all = []
    rate_profiles = []
    
    for trial_idx in range(n_trials):
        stimulus = stimuli[trial_idx]
        
        # Convert stimulus to firing rate
        if response_dynamics == 'exponential':
            # Simple exponential response
            rate = baseline_rate + (max_rate - baseline_rate) * (1 - np.exp(-stimulus))
        elif response_dynamics == 'adaptive':
            # Adaptation dynamics
            tau_fast = 0.01  # 10 ms
            tau_slow = 0.1   # 100 ms
            rate = np.zeros_like(stimulus, dtype=float)
            r_fast, r_slow = 0.0, 0.0
            
            for i in range(len(stimulus)):
                r_fast = r_fast * np.exp(-dt/tau_fast) + stimulus[i] * dt/tau_fast
                r_slow = r_slow * np.exp(-dt/tau_slow) + stimulus[i] * dt/tau_slow
                rate[i] = baseline_rate + (max_rate - baseline_rate) * (r_fast - 0.5 * r_slow)
                rate[i] = max(0, rate[i])
        else:  # phasic-tonic
            # Phasic-tonic response
            rate = baseline_rate + (max_rate - baseline_rate) * stimulus
            # Add phasic component for stimulus onset
            diff_stim = np.concatenate([[0], np.diff(stimulus)])
            phasic = 50.0 * np.maximum(0, diff_stim) * np.exp(-time_axis * 20)
            rate = rate + phasic
        
        rate_profiles.append(rate)
        
        # Generate spikes using inhomogeneous Poisson process
        spike_probs = rate * dt
        spike_train = np.random.rand(n_time) < spike_probs
        spike_times = time_axis[spike_train]
        
        spike_trains.append(spike_train.astype(int))
        spike_times_all.append(spike_times)
    
    return {
        'spike_trains': np.array(spike_trains),
        'spike_times': spike_times_all,
        'rate_profiles': np.array(rate_profiles),
        'time_axis': time_axis,
        'stimuli': stimuli
    }


def analyze_spike_train_statistics(spike_data: Dict[str, np.ndarray]) -> Dict[str, Union[float, np.ndarray]]:
    """
    Compute comprehensive spike train statistics.
    
    Args:
        spike_data: Output from generate_spike_trains
        
    Returns:
        Dictionary with firing rates, ISI statistics, CV, Fano factor, etc.
    """
    spike_trains = spike_data['spike_trains']
    spike_times_all = spike_data['spike_times']
    time_axis = spike_data['time_axis']
    dt = time_axis[1] - time_axis[0]
    
    n_trials, n_time = spike_trains.shape
    
    # Firing rates
    firing_rates = np.sum(spike_trains, axis=1) / (n_time * dt)
    mean_firing_rate = float(np.mean(firing_rates))
    
    # Inter-spike interval analysis
    all_isis = []
    cv_values = []
    
    for spike_times in spike_times_all:
        if len(spike_times) > 1:
            isis = np.diff(spike_times)
            all_isis.extend(isis)
            cv = np.std(isis) / (np.mean(isis) + 1e-10)
            cv_values.append(cv)
    
    all_isis = np.array(all_isis)
    mean_isi = float(np.mean(all_isis)) if len(all_isis) > 0 else 0.0
    std_isi = float(np.std(all_isis)) if len(all_isis) > 0 else 0.0
    mean_cv = float(np.mean(cv_values)) if len(cv_values) > 0 else 0.0
    
    # Fano factor (variance-to-mean ratio)
    spike_counts_per_trial = np.sum(spike_trains, axis=1)
    fano_factor = float(np.var(spike_counts_per_trial) / (np.mean(spike_counts_per_trial) + 1e-10))
    
    # Time-binned analysis
    bin_size = 0.01  # 10 ms bins
    n_bins = int(time_axis[-1] / bin_size)
    binned_spikes = np.zeros((n_trials, n_bins))
    
    for trial_idx, spike_times in enumerate(spike_times_all):
        bin_indices = np.floor(spike_times / bin_size).astype(int)
        bin_indices = bin_indices[bin_indices < n_bins]
        binned_spikes[trial_idx, bin_indices] += 1
    
    return {
        'mean_firing_rate_hz': mean_firing_rate,
        'firing_rates_per_trial': firing_rates,
        'mean_isi_s': mean_isi,
        'std_isi_s': std_isi,
        'cv_isi': mean_cv,
        'fano_factor': fano_factor,
        'binned_spikes': binned_spikes,
        'bin_size_s': bin_size,
        'isi_distribution': all_isis
    }


def temporal_coding_analysis(spike_data: Dict[str, np.ndarray], 
                           stimulus_times: np.ndarray) -> Dict[str, Union[float, np.ndarray]]:
    """
    Analyze temporal coding precision and response latency.
    
    Args:
        spike_data: Output from generate_spike_trains
        stimulus_times: Times of stimulus onset/offset
        
    Returns:
        Dictionary with latency statistics, temporal precision, etc.
    """
    spike_times_all = spike_data['spike_times']
    time_axis = spike_data['time_axis']
    
    latencies = []
    jitters = []
    
    for trial_idx, spike_times in enumerate(spike_times_all):
        for stim_time in stimulus_times:
            # Find first spike after stimulus onset
            post_stim_spikes = spike_times[spike_times >= stim_time]
            if len(post_stim_spikes) > 0:
                latency = post_stim_spikes[0] - stim_time
                latencies.append(latency)
    
    latencies = np.array(latencies)
    
    if len(latencies) > 0:
        mean_latency = float(np.mean(latencies))
        std_latency = float(np.std(latencies))
        temporal_precision = 1.0 / (std_latency + 1e-10)
    else:
        mean_latency = std_latency = temporal_precision = 0.0
    
    # Phase locking analysis (if periodic stimulus)
    if len(stimulus_times) > 1:
        period = stimulus_times[1] - stimulus_times[0]
        all_phases = []
        
        for spike_times in spike_times_all:
            for stim_time in stimulus_times:
                post_stim = spike_times[spike_times >= stim_time]
                if len(post_stim) > 0:
                    relative_time = (post_stim[0] - stim_time) % period
                    phase = 2 * np.pi * relative_time / period
                    all_phases.append(phase)
        
        if len(all_phases) > 0:
            phases = np.array(all_phases)
            # Vector strength (phase locking measure)
            vector_strength = float(np.abs(np.mean(np.exp(1j * phases))))
        else:
            vector_strength = 0.0
    else:
        vector_strength = 0.0
    
    return {
        'mean_latency_s': mean_latency,
        'std_latency_s': std_latency,
        'temporal_precision': temporal_precision,
        'vector_strength': vector_strength,
        'latencies': latencies
    }


def population_coding_analysis(population_responses: np.ndarray, 
                              stimulus_labels: np.ndarray) -> Dict[str, Union[float, np.ndarray]]:
    """
    Analyze population coding efficiency across multiple ORNs.
    
    Args:
        population_responses: Array of shape (n_neurons, n_trials, n_time)
        stimulus_labels: Array of stimulus class labels for each trial
        
    Returns:
        Dictionary with PCA results, discriminability, etc.
    """
    population_responses = np.asarray(population_responses)
    stimulus_labels = np.asarray(stimulus_labels)
    
    n_neurons, n_trials, n_time = population_responses.shape
    
    # Flatten responses for analysis
    responses_flat = population_responses.mean(axis=2)  # Average over time
    
    # PCA analysis
    pca = PCA()
    pca_scores = pca.fit_transform(responses_flat.T)
    explained_variance = pca.explained_variance_ratio_
    
    # Linear Discriminant Analysis
    if len(np.unique(stimulus_labels)) > 1:
        lda = LinearDiscriminantAnalysis()
        lda_scores = lda.fit_transform(responses_flat.T, stimulus_labels)
        lda_score = float(lda.score(responses_flat.T, stimulus_labels))
    else:
        lda_scores = np.zeros((n_trials, 1))
        lda_score = 0.0
    
    # Population vector analysis
    pop_vector_angles = []
    for trial in range(n_trials):
        response_vector = responses_flat[:, trial]
        angle = np.arctan2(response_vector[1] if n_neurons > 1 else 0, 
                          response_vector[0])
        pop_vector_angles.append(angle)
    
    pop_vector_angles = np.array(pop_vector_angles)
    
    # Cross-correlation analysis between neurons
    cross_correlations = np.corrcoef(responses_flat)
    mean_correlation = float(np.mean(cross_correlations[np.triu_indices(n_neurons, k=1)]))
    
    # Signal and noise correlations
    signal_corr_matrix = np.zeros((n_neurons, n_neurons))
    noise_corr_matrix = np.zeros((n_neurons, n_neurons))
    
    for i in range(n_neurons):
        for j in range(i+1, n_neurons):
            # Signal correlation (across stimuli)
            mean_responses_i = np.array([np.mean(responses_flat[i, stimulus_labels == label]) 
                                       for label in np.unique(stimulus_labels)])
            mean_responses_j = np.array([np.mean(responses_flat[j, stimulus_labels == label]) 
                                       for label in np.unique(stimulus_labels)])
            
            if len(mean_responses_i) > 1:
                signal_corr = float(np.corrcoef(mean_responses_i, mean_responses_j)[0, 1])
            else:
                signal_corr = 0.0
                
            signal_corr_matrix[i, j] = signal_corr_matrix[j, i] = signal_corr
            
            # Noise correlation (trial-to-trial variability)
            residuals_i = responses_flat[i, :] - np.mean(responses_flat[i, :])
            residuals_j = responses_flat[j, :] - np.mean(responses_flat[j, :])
            noise_corr = float(np.corrcoef(residuals_i, residuals_j)[0, 1])
            noise_corr_matrix[i, j] = noise_corr_matrix[j, i] = noise_corr
    
    mean_signal_correlation = float(np.mean(signal_corr_matrix[np.triu_indices(n_neurons, k=1)]))
    mean_noise_correlation = float(np.mean(noise_corr_matrix[np.triu_indices(n_neurons, k=1)]))
    
    return {
        'pca_scores': pca_scores,
        'explained_variance_ratio': explained_variance,
        'cumulative_variance': np.cumsum(explained_variance),
        'lda_scores': lda_scores,
        'classification_accuracy': lda_score,
        'population_vector_angles': pop_vector_angles,
        'cross_correlations': cross_correlations,
        'mean_correlation': mean_correlation,
        'mean_signal_correlation': mean_signal_correlation,
        'mean_noise_correlation': mean_noise_correlation,
        'signal_correlation_matrix': signal_corr_matrix,
        'noise_correlation_matrix': noise_corr_matrix
    }


def mutual_information_analysis(neural_responses: np.ndarray, 
                               stimuli: np.ndarray,
                               n_bins: int = 10) -> Dict[str, float]:
    """
    Compute mutual information between neural responses and stimuli.
    
    Args:
        neural_responses: Array of neural response values
        stimuli: Array of corresponding stimulus values
        n_bins: Number of bins for discretization
        
    Returns:
        Dictionary with mutual information metrics
    """
    responses = np.asarray(neural_responses).flatten()
    stim_values = np.asarray(stimuli).flatten()
    
    if len(responses) != len(stim_values):
        raise ValueError("Response and stimulus arrays must have same length")
    
    # Discretize continuous values
    response_bins = np.histogram_bin_edges(responses, bins=n_bins)
    stimulus_bins = np.histogram_bin_edges(stim_values, bins=n_bins)
    
    response_discrete = np.digitize(responses, response_bins) - 1
    stimulus_discrete = np.digitize(stim_values, stimulus_bins) - 1
    
    # Ensure bins are within valid range
    response_discrete = np.clip(response_discrete, 0, n_bins - 1)
    stimulus_discrete = np.clip(stimulus_discrete, 0, n_bins - 1)
    
    # Compute joint histogram
    joint_hist, _, _ = np.histogram2d(response_discrete, stimulus_discrete, 
                                     bins=[n_bins, n_bins])
    joint_prob = joint_hist / np.sum(joint_hist)
    
    # Marginal probabilities
    response_prob = np.sum(joint_prob, axis=1)
    stimulus_prob = np.sum(joint_prob, axis=0)
    
    # Compute entropies
    h_response = -np.sum(response_prob[response_prob > 0] * np.log2(response_prob[response_prob > 0]))
    h_stimulus = -np.sum(stimulus_prob[stimulus_prob > 0] * np.log2(stimulus_prob[stimulus_prob > 0]))
    
    # Joint entropy
    h_joint = -np.sum(joint_prob[joint_prob > 0] * np.log2(joint_prob[joint_prob > 0]))
    
    # Mutual information
    mutual_info = h_response + h_stimulus - h_joint
    
    # Normalized mutual information
    normalized_mi = mutual_info / min(h_response, h_stimulus) if min(h_response, h_stimulus) > 0 else 0.0
    
    return {
        'mutual_information_bits': float(mutual_info),
        'normalized_mutual_information': float(normalized_mi),
        'response_entropy_bits': float(h_response),
        'stimulus_entropy_bits': float(h_stimulus),
        'joint_entropy_bits': float(h_joint)
    }


def odor_discrimination_analysis(population_responses: np.ndarray,
                                odor_identities: np.ndarray,
                                time_windows: List[Tuple[float, float]],
                                dt: float = 1e-4) -> Dict[str, Union[float, np.ndarray]]:
    """
    Analyze odor discrimination performance across different time windows.
    
    Args:
        population_responses: Array of shape (n_neurons, n_trials, n_time)
        odor_identities: Array of odor class labels for each trial
        time_windows: List of (start, end) time windows in seconds
        dt: Time step in seconds
        
    Returns:
        Dictionary with discrimination performance metrics
    """
    population_responses = np.asarray(population_responses)
    odor_identities = np.asarray(odor_identities)
    
    n_neurons, n_trials, n_time = population_responses.shape
    time_axis = np.arange(n_time) * dt
    
    results = {}
    
    for window_idx, (t_start, t_end) in enumerate(time_windows):
        # Extract responses in time window
        time_mask = (time_axis >= t_start) & (time_axis <= t_end)
        window_responses = population_responses[:, :, time_mask]
        
        # Average over time window
        mean_responses = np.mean(window_responses, axis=2)  # Shape: (n_neurons, n_trials)
        
        # Compute pairwise discriminability (d-prime) between odors
        unique_odors = np.unique(odor_identities)
        n_odors = len(unique_odors)
        discriminability_matrix = np.zeros((n_odors, n_odors))
        
        for i, odor1 in enumerate(unique_odors):
            for j, odor2 in enumerate(unique_odors):
                if i != j:
                    responses1 = mean_responses[:, odor_identities == odor1]
                    responses2 = mean_responses[:, odor_identities == odor2]
                    
                    # Pool across neurons
                    pooled1 = np.mean(responses1, axis=0)
                    pooled2 = np.mean(responses2, axis=0)
                    
                    # Compute d-prime
                    mean_diff = np.mean(pooled2) - np.mean(pooled1)
                    pooled_std = np.sqrt(0.5 * (np.var(pooled1) + np.var(pooled2)))
                    d_prime = mean_diff / (pooled_std + 1e-10)
                    
                    discriminability_matrix[i, j] = d_prime
        
        # Classification analysis using LDA
        if n_odors > 1:
            lda = LinearDiscriminantAnalysis()
            classification_accuracy = lda.fit(mean_responses.T, odor_identities).score(mean_responses.T, odor_identities)
        else:
            classification_accuracy = 0.0
        
        results[f'window_{window_idx}'] = {
            'time_start': t_start,
            'time_end': t_end,
            'discriminability_matrix': discriminability_matrix,
            'mean_discriminability': float(np.mean(discriminability_matrix[discriminability_matrix != 0])),
            'classification_accuracy': float(classification_accuracy)
        }
    
    return results


def adaptation_dynamics_analysis(spike_data: Dict[str, np.ndarray],
                                stimulus_duration: float = 1.0) -> Dict[str, Union[float, np.ndarray]]:
    """
    Analyze adaptation dynamics in neural responses.
    
    Args:
        spike_data: Output from generate_spike_trains
        stimulus_duration: Duration of stimulus presentation (seconds)
        
    Returns:
        Dictionary with adaptation metrics
    """
    rate_profiles = spike_data['rate_profiles']
    time_axis = spike_data['time_axis']
    
    n_trials, n_time = rate_profiles.shape
    dt = time_axis[1] - time_axis[0]
    
    # Find stimulus onset/offset
    stimuli = spike_data['stimuli']
    stim_onset = np.argmax(stimuli[0] > 0) if np.any(stimuli[0] > 0) else 0
    stim_offset = stim_onset + int(stimulus_duration / dt)
    stim_offset = min(stim_offset, n_time - 1)
    
    # Analyze adaptation during stimulus
    adaptation_metrics = []
    
    for trial in range(n_trials):
        rate = rate_profiles[trial, stim_onset:stim_offset]
        time = time_axis[stim_onset:stim_offset]
        
        if len(rate) > 10:  # Need sufficient data points
            # Fit exponential decay
            peak_response = np.max(rate)
            peak_time = time[np.argmax(rate)]
            
            # Adaptation index: (peak - steady) / peak
            steady_state = np.mean(rate[-int(len(rate)/4):])  # Last quarter
            adaptation_index = (peak_response - steady_state) / (peak_response + 1e-10)
            
            # Time constant estimation (simplified)
            post_peak_idx = np.argmax(rate)
            if post_peak_idx < len(rate) - 5:
                post_peak_rate = rate[post_peak_idx:]
                post_peak_time = time[post_peak_idx:]
                
                # Exponential fit: y = A * exp(-t/tau) + C
                try:
                    # Simplified estimation
                    half_max_value = steady_state + (peak_response - steady_state) / 2
                    half_max_idx = np.argmin(np.abs(post_peak_rate - half_max_value))
                    tau_estimate = post_peak_time[half_max_idx] - peak_time
                except:
                    tau_estimate = 0.1  # Default value
            else:
                tau_estimate = 0.1
            
            adaptation_metrics.append({
                'peak_response': float(peak_response),
                'steady_state_response': float(steady_state),
                'adaptation_index': float(adaptation_index),
                'time_constant_s': float(tau_estimate)
            })
    
    # Average across trials
    if adaptation_metrics:
        mean_peak = float(np.mean([m['peak_response'] for m in adaptation_metrics]))
        mean_steady = float(np.mean([m['steady_state_response'] for m in adaptation_metrics]))
        mean_adaptation = float(np.mean([m['adaptation_index'] for m in adaptation_metrics]))
        mean_tau = float(np.mean([m['time_constant_s'] for m in adaptation_metrics]))
    else:
        mean_peak = mean_steady = mean_adaptation = mean_tau = 0.0
    
    return {
        'mean_peak_response': mean_peak,
        'mean_steady_state': mean_steady,
        'mean_adaptation_index': mean_adaptation,
        'mean_time_constant_s': mean_tau,
        'per_trial_metrics': adaptation_metrics
    }


