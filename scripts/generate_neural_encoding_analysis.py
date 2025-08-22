#!/usr/bin/env python3
"""Generate comprehensive neural encoding and temporal dynamics analysis."""
from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from _utils import ensure_src_on_path, setup_paths, set_mpl_backend, write_caption

ensure_src_on_path()
from src.case_studies.neural_encoding import (
    generate_spike_trains,
    analyze_spike_train_statistics,
    temporal_coding_analysis,
    population_coding_analysis,
    mutual_information_analysis,
    odor_discrimination_analysis,
    adaptation_dynamics_analysis,
    information_rate_time_series,
    rate_coding_metrics
)


def main() -> int:
    """Generate comprehensive neural encoding analysis."""
    try:
        print("🔄 Starting neural encoding analysis...")
        set_mpl_backend()
        fig_dir, data_dir = setup_paths()
        
        # Generate stimulus patterns
        print("🧠 Generating stimulus patterns...")
        dt = 1e-4  # 0.1 ms time step
        duration = 2.0  # 2 seconds
        n_time = int(duration / dt)
        time_axis = np.arange(n_time) * dt
        
        # Create different stimulus types
        n_trials = 20
        stimulus_patterns = []
        stimulus_labels = []
        
        # Pattern 1: Step function (odor onset)
        for trial in range(n_trials // 4):
            stim = np.zeros(n_time)
            onset_time = 0.5 + 0.1 * np.random.randn()
            onset_idx = int(max(0, onset_time / dt))
            offset_idx = int(min(n_time, (onset_time + 0.8) / dt))
            stim[onset_idx:offset_idx] = 2.0 + 0.5 * np.random.randn()
            stimulus_patterns.append(stim)
            stimulus_labels.append(0)
        
        # Pattern 2: Ramp stimulus
        for trial in range(n_trials // 4):
            stim = np.zeros(n_time)
            ramp_start = int(0.4 / dt)
            ramp_end = int(1.2 / dt)
            stim[ramp_start:ramp_end] = np.linspace(0, 3.0, ramp_end - ramp_start)
            stimulus_patterns.append(stim)
            stimulus_labels.append(1)
        
        # Pattern 3: Pulsed stimulus
        for trial in range(n_trials // 4):
            stim = np.zeros(n_time)
            pulse_times = [0.3, 0.7, 1.1, 1.5]
            for pulse_t in pulse_times:
                pulse_idx = int(pulse_t / dt)
                pulse_width = int(0.05 / dt)
                stim[pulse_idx:pulse_idx+pulse_width] = 2.5
            stimulus_patterns.append(stim)
            stimulus_labels.append(2)
        
        # Pattern 4: Noisy continuous
        for trial in range(n_trials - 3 * (n_trials // 4)):
            stim = 1.0 + 0.5 * np.sin(2 * np.pi * 2 * time_axis) + 0.3 * np.random.randn(n_time)
            stim = np.maximum(0, stim)
            stimulus_patterns.append(stim)
            stimulus_labels.append(3)
        
        stimuli = np.array(stimulus_patterns)
        stimulus_labels = np.array(stimulus_labels)
        
        # Generate spike trains for multiple neurons
        print("⚡ Generating spike trains...")
        n_neurons = 5
        population_spike_data = []
        population_responses = []
        
        for neuron_idx in range(n_neurons):
            # Different response properties for each neuron
            baseline = 5.0 + 10.0 * neuron_idx / n_neurons
            max_rate = 50.0 + 50.0 * neuron_idx / n_neurons
            
            if neuron_idx < 2:
                dynamics = 'exponential'
            elif neuron_idx < 4:
                dynamics = 'adaptive'
            else:
                dynamics = 'phasic-tonic'
            
            spike_data = generate_spike_trains(
                stimuli, dt=dt, baseline_rate=baseline, max_rate=max_rate,
                response_dynamics=dynamics, seed=42 + neuron_idx
            )
            
            population_spike_data.append(spike_data)
            population_responses.append(spike_data['rate_profiles'])
        
        population_responses = np.array(population_responses)
        
        # Spike train statistics analysis
        print("📊 Analyzing spike train statistics...")
        spike_stats = analyze_spike_train_statistics(population_spike_data[0])
        
        # Temporal coding analysis
        print("⏱️ Analyzing temporal coding...")
        stimulus_times = np.array([0.5, 1.0, 1.5])
        temporal_results = temporal_coding_analysis(population_spike_data[0], stimulus_times)
        
        # Population coding analysis
        print("👥 Analyzing population coding...")
        pop_results = population_coding_analysis(population_responses, stimulus_labels)
        
        # Mutual information analysis
        print("📈 Computing mutual information...")
        mean_rates = np.mean(population_responses[0], axis=1)
        mi_results = mutual_information_analysis(mean_rates, stimulus_labels)
        
        # Odor discrimination analysis
        print("👃 Analyzing odor discrimination...")
        time_windows = [(0.1, 0.3), (0.3, 0.8), (0.8, 1.5), (1.5, 2.0)]
        discrimination_results = odor_discrimination_analysis(
            population_responses, stimulus_labels, time_windows, dt
        )
        
        # Adaptation dynamics analysis
        print("🔄 Analyzing adaptation dynamics...")
        adaptation_results = adaptation_dynamics_analysis(population_spike_data[0], stimulus_duration=1.0)
        
        print("📈 Creating visualization...")
        fig = plt.figure(figsize=(20, 16))
        
        # Stimulus patterns
        ax1 = plt.subplot(4, 5, 1)
        for i, label in enumerate(np.unique(stimulus_labels)):
            idx = np.where(stimulus_labels == label)[0][0]
            ax1.plot(time_axis[:2000], stimuli[idx, :2000], label=f'Pattern {label}', linewidth=2)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Stimulus Intensity')
        ax1.set_title('Stimulus Patterns')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # Spike trains (raster plot)
        ax2 = plt.subplot(4, 5, 2)
        neuron_colors = plt.cm.Set1(np.linspace(0, 1, n_neurons))
        y_offset = 0
        for neuron_idx in range(min(3, n_neurons)):
            spike_data = population_spike_data[neuron_idx]
            for trial_idx in range(min(5, len(spike_data['spike_times']))):
                spike_times = spike_data['spike_times'][trial_idx]
                ax2.scatter(spike_times, np.full_like(spike_times, y_offset + trial_idx), 
                           s=8, c=[neuron_colors[neuron_idx]], alpha=0.7)
            y_offset += 6
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Trial + Neuron')
        ax2.set_title('Spike Rasters')
        ax2.grid(True, alpha=0.3)

        # Firing rate profiles
        ax3 = plt.subplot(4, 5, 3)
        for neuron_idx in range(min(3, n_neurons)):
            mean_rate = np.mean(population_responses[neuron_idx], axis=0)
            ax3.plot(time_axis[:2000], mean_rate[:2000], 
                    color=neuron_colors[neuron_idx], linewidth=2, 
                    label=f'Neuron {neuron_idx+1}')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Firing Rate (Hz)')
        ax3.set_title('Mean Firing Rates')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)

        # ISI distribution
        ax4 = plt.subplot(4, 5, 4)
        if len(spike_stats['isi_distribution']) > 0:
            ax4.hist(spike_stats['isi_distribution'], bins=30, alpha=0.7, density=True)
        ax4.set_xlabel('Inter-Spike Interval (s)')
        ax4.set_ylabel('Density')
        ax4.set_title(f'ISI Distribution\nCV = {spike_stats["cv_isi"]:.2f}')
        ax4.grid(True, alpha=0.3)

        # Latency analysis
        ax5 = plt.subplot(4, 5, 5)
        if len(temporal_results['latencies']) > 0:
            ax5.hist(temporal_results['latencies'], bins=20, alpha=0.7, density=True)
        ax5.set_xlabel('Response Latency (s)')
        ax5.set_ylabel('Density')
        ax5.set_title(f'Response Latencies\nMean = {temporal_results["mean_latency_s"]:.3f} s')
        ax5.grid(True, alpha=0.3)

        # PCA of population responses
        ax6 = plt.subplot(4, 5, 6)
        colors = plt.cm.viridis(np.linspace(0, 1, len(np.unique(stimulus_labels))))
        for i, label in enumerate(np.unique(stimulus_labels)):
            mask = stimulus_labels == label
            ax6.scatter(pop_results['pca_scores'][mask, 0], pop_results['pca_scores'][mask, 1], 
                       c=[colors[i]], label=f'Pattern {label}', alpha=0.7, s=30)
        ax6.set_xlabel(f'PC1 ({pop_results["explained_variance_ratio"][0]:.1%})')
        ax6.set_ylabel(f'PC2 ({pop_results["explained_variance_ratio"][1]:.1%})')
        ax6.set_title('PCA of Population Responses')
        ax6.legend(fontsize=8)
        ax6.grid(True, alpha=0.3)

        # Explained variance
        ax7 = plt.subplot(4, 5, 7)
        ax7.bar(range(1, len(pop_results['explained_variance_ratio'])+1), 
               pop_results['explained_variance_ratio'], alpha=0.7)
        ax7.set_xlabel('Principal Component')
        ax7.set_ylabel('Explained Variance Ratio')
        ax7.set_title('PCA Explained Variance')
        ax7.grid(True, alpha=0.3)

        # Cross-correlations
        ax8 = plt.subplot(4, 5, 8)
        im = ax8.imshow(pop_results['cross_correlations'], cmap='RdBu_r', vmin=-1, vmax=1)
        ax8.set_xlabel('Neuron')
        ax8.set_ylabel('Neuron')
        ax8.set_title('Neural Cross-Correlations')
        plt.colorbar(im, ax=ax8)

        # Discrimination performance by time window
        ax9 = plt.subplot(4, 5, 9)
        window_centers = [(w['time_start'] + w['time_end'])/2 for w in discrimination_results.values()]
        accuracies = [w['classification_accuracy'] for w in discrimination_results.values()]
        ax9.plot(window_centers, accuracies, 'o-', linewidth=2, markersize=8)
        ax9.set_xlabel('Time Window Center (s)')
        ax9.set_ylabel('Classification Accuracy')
        ax9.set_title('Temporal Discrimination')
        ax9.grid(True, alpha=0.3)

        # Adaptation dynamics
        ax10 = plt.subplot(4, 5, 10)
        if adaptation_results['per_trial_metrics']:
            peak_responses = [m['peak_response'] for m in adaptation_results['per_trial_metrics']]
            steady_responses = [m['steady_state_response'] for m in adaptation_results['per_trial_metrics']]
            ax10.scatter(peak_responses, steady_responses, alpha=0.7, s=30)
            max_val = max(max(peak_responses), max(steady_responses))
            ax10.plot([0, max_val], [0, max_val], 'k--', alpha=0.5)
        ax10.set_xlabel('Peak Response (Hz)')
        ax10.set_ylabel('Steady State Response (Hz)')
        ax10.set_title('Adaptation Analysis')
        ax10.grid(True, alpha=0.3)

        # Performance summary
        ax11 = plt.subplot(4, 5, 11)
        ax11.axis('off')
        
        best_discrimination = max([w['classification_accuracy'] for w in discrimination_results.values()])
        summary_text = f"""Performance Summary:

Firing Rate: {spike_stats['mean_firing_rate_hz']:.1f} Hz
CV of ISI: {spike_stats['cv_isi']:.2f}
Fano Factor: {spike_stats['fano_factor']:.2f}

Temporal Precision: {temporal_results['temporal_precision']:.1f}
Vector Strength: {temporal_results['vector_strength']:.3f}

Classification: {pop_results['classification_accuracy']:.1%}
Best Discrimination: {best_discrimination:.1%}

Mutual Information: {mi_results['mutual_information_bits']:.2f} bits
Adaptation Index: {adaptation_results['mean_adaptation_index']:.2f}
        """
        
        ax11.text(0.05, 0.95, summary_text, transform=ax11.transAxes,
                 fontsize=10, verticalalignment='top', fontfamily='monospace')

        plt.tight_layout()

        # Save outputs
        out_png = os.path.join(fig_dir, "neural_encoding_comprehensive_analysis.png")
        fig.savefig(out_png, dpi=300, bbox_inches="tight")
        plt.close(fig)

        caption = f"""Comprehensive neural encoding analysis: Multi-neuron spike train generation with diverse response dynamics, population coding achieving {pop_results['classification_accuracy']:.1%} classification accuracy, temporal precision of {temporal_results['temporal_precision']:.1f}, and adaptation dynamics with {adaptation_results['mean_adaptation_index']:.2f} adaptation index. Analysis includes mutual information ({mi_results['mutual_information_bits']:.2f} bits) and discrimination performance up to {best_discrimination:.1%} accuracy."""
        
        write_caption(os.path.join(fig_dir, "neural_encoding_comprehensive_analysis.caption.txt"), caption)

        # Save data
        out_npz = os.path.join(data_dir, "neural_encoding_comprehensive.npz")
        np.savez(out_npz,
                time_axis=time_axis,
                stimuli=stimuli,
                stimulus_labels=stimulus_labels,
                mean_firing_rate_hz=spike_stats['mean_firing_rate_hz'],
                cv_isi=spike_stats['cv_isi'],
                fano_factor=spike_stats['fano_factor'],
                mean_latency_s=temporal_results['mean_latency_s'],
                temporal_precision=temporal_results['temporal_precision'],
                classification_accuracy=pop_results['classification_accuracy'],
                mutual_information_bits=mi_results['mutual_information_bits'],
                mean_adaptation_index=adaptation_results['mean_adaptation_index'])

        print(f"✅ Success! Generated neural encoding analysis")
        print(f"Generated: {out_png}")
        print(f"Classification accuracy: {pop_results['classification_accuracy']:.1%}")
        print(f"Mutual information: {mi_results['mutual_information_bits']:.2f} bits")
        print(out_png)
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
