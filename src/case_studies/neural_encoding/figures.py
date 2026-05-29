"""Appendix figure rendering for neural_encoding."""

from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from src.viz.warnings_util import suppress_plot_warnings


def render_comprehensive_figure(analysis: Dict[str, object]) -> tuple[object, Dict[str, float]]:
    """Render comprehensive appendix figure and return summary metrics."""
    data = analysis.as_dict() if hasattr(analysis, "as_dict") else analysis
    with suppress_plot_warnings():
        import matplotlib.pyplot as plt

        time_axis = data["time_axis"]
        stimuli = data["stimuli"]
        stimulus_labels = data["stimulus_labels"]
        n_neurons = int(data["n_neurons"])
        population_spike_data = data["population_spike_data"]
        population_responses = data["population_responses"]
        spike_stats = data["spike_stats"]
        temporal_results = data["temporal_results"]
        pop_results = data["pop_results"]
        mi_results = data["mi_results"]
        discrimination_results = data["discrimination_results"]
        adaptation_results = data["adaptation_results"]

        fig = plt.figure(figsize=(20, 16))

        ax1 = plt.subplot(4, 5, 1)
        for label in np.unique(stimulus_labels):
            idx = np.where(stimulus_labels == label)[0][0]
            ax1.plot(time_axis[:2000], stimuli[idx, :2000], label=f"Pattern {label}", linewidth=2)
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Stimulus Intensity")
        ax1.set_title("Stimulus Patterns")
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        ax2 = plt.subplot(4, 5, 2)
        neuron_colors = plt.cm.Set1(np.linspace(0, 1, n_neurons))
        y_offset = 0
        for neuron_idx in range(min(3, n_neurons)):
            spike_data = population_spike_data[neuron_idx]
            for trial_idx in range(min(5, len(spike_data["spike_times"]))):
                spike_times = spike_data["spike_times"][trial_idx]
                ax2.scatter(
                    spike_times,
                    np.full_like(spike_times, y_offset + trial_idx),
                    s=8,
                    c=[neuron_colors[neuron_idx]],
                    alpha=0.7,
                )
            y_offset += 6
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Trial + Neuron")
        ax2.set_title("Spike Rasters")
        ax2.grid(True, alpha=0.3)

        ax3 = plt.subplot(4, 5, 3)
        for neuron_idx in range(min(3, n_neurons)):
            mean_rate = np.mean(population_responses[neuron_idx], axis=0)
            ax3.plot(
                time_axis[:2000],
                mean_rate[:2000],
                color=neuron_colors[neuron_idx],
                linewidth=2,
                label=f"Neuron {neuron_idx + 1}",
            )
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Firing Rate (Hz)")
        ax3.set_title("Mean Firing Rates")
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)

        ax4 = plt.subplot(4, 5, 4)
        if len(spike_stats["isi_distribution"]) > 0:
            ax4.hist(spike_stats["isi_distribution"], bins=30, alpha=0.7, density=True)
        ax4.set_xlabel("Inter-Spike Interval (s)")
        ax4.set_ylabel("Density")
        ax4.set_title(f'ISI Distribution\nCV = {spike_stats["cv_isi"]:.2f}')
        ax4.grid(True, alpha=0.3)

        ax5 = plt.subplot(4, 5, 5)
        if len(temporal_results["latencies"]) > 0:
            ax5.hist(temporal_results["latencies"], bins=20, alpha=0.7, density=True)
        ax5.set_xlabel("Response Latency (s)")
        ax5.set_ylabel("Density")
        ax5.set_title(f'Response Latencies\nMean = {temporal_results["mean_latency_s"]:.3f} s')
        ax5.grid(True, alpha=0.3)

        ax6 = plt.subplot(4, 5, 6)
        colors = plt.cm.viridis(np.linspace(0, 1, len(np.unique(stimulus_labels))))
        for i, label in enumerate(np.unique(stimulus_labels)):
            mask = stimulus_labels == label
            ax6.scatter(
                pop_results["pca_scores"][mask, 0],
                pop_results["pca_scores"][mask, 1],
                c=[colors[i]],
                label=f"Pattern {label}",
                alpha=0.7,
                s=30,
            )
        ax6.set_xlabel(f'PC1 ({pop_results["explained_variance_ratio"][0]:.1%})')
        ax6.set_ylabel(f'PC2 ({pop_results["explained_variance_ratio"][1]:.1%})')
        ax6.set_title("PCA of Population Responses")
        ax6.legend(fontsize=8)
        ax6.grid(True, alpha=0.3)

        ax7 = plt.subplot(4, 5, 7)
        ax7.bar(range(1, len(pop_results["explained_variance_ratio"]) + 1), pop_results["explained_variance_ratio"], alpha=0.7)
        ax7.set_xlabel("Principal Component")
        ax7.set_ylabel("Explained Variance Ratio")
        ax7.set_title("PCA Explained Variance")
        ax7.grid(True, alpha=0.3)

        ax8 = plt.subplot(4, 5, 8)
        im = ax8.imshow(pop_results["cross_correlations"], cmap="RdBu_r", vmin=-1, vmax=1)
        ax8.set_xlabel("Neuron")
        ax8.set_ylabel("Neuron")
        ax8.set_title("Neural Cross-Correlations")
        plt.colorbar(im, ax=ax8)

        ax9 = plt.subplot(4, 5, 9)
        window_centers = [(w["time_start"] + w["time_end"]) / 2 for w in discrimination_results.values()]
        accuracies = [w["classification_accuracy"] for w in discrimination_results.values()]
        ax9.plot(window_centers, accuracies, "o-", linewidth=2, markersize=8)
        ax9.set_xlabel("Time Window Center (s)")
        ax9.set_ylabel("Classification Accuracy")
        ax9.set_title("Temporal Discrimination")
        ax9.grid(True, alpha=0.3)

        ax10 = plt.subplot(4, 5, 10)
        if adaptation_results["per_trial_metrics"]:
            peak_responses = [m["peak_response"] for m in adaptation_results["per_trial_metrics"]]
            steady_responses = [m["steady_state_response"] for m in adaptation_results["per_trial_metrics"]]
            ax10.scatter(peak_responses, steady_responses, alpha=0.7, s=30)
            max_val = max(max(peak_responses), max(steady_responses))
            ax10.plot([0, max_val], [0, max_val], "k--", alpha=0.5)
        ax10.set_xlabel("Peak Response (Hz)")
        ax10.set_ylabel("Steady State Response (Hz)")
        ax10.set_title("Adaptation Analysis")
        ax10.grid(True, alpha=0.3)

        best_discrimination = max(w["classification_accuracy"] for w in discrimination_results.values())
        ax11 = plt.subplot(4, 5, 11)
        ax11.axis("off")
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
        ax11.text(0.05, 0.95, summary_text, transform=ax11.transAxes, fontsize=10, verticalalignment="top", fontfamily="monospace")

        plt.tight_layout()
        metrics = {
            "classification_accuracy": float(pop_results["classification_accuracy"]),
            "mutual_information_bits": float(mi_results["mutual_information_bits"]),
            "mean_adaptation_index": float(adaptation_results["mean_adaptation_index"]),
            "best_discrimination": float(best_discrimination),
            "temporal_precision": float(temporal_results["temporal_precision"]),
        }
        return fig, metrics

