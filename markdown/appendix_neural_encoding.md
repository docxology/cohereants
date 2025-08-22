# Appendix D: Neural Encoding Efficiency on Time-Series {#sec:app_neural_encoding}

## Objective
Comprehensive neural encoding analysis including spike train generation, temporal dynamics, population coding, mutual information, and adaptation mechanisms for olfactory receptor neurons.

## Methods (src)
- `src/case_studies/neural_encoding.py`
  - `generate_spike_trains(stimuli, dt, baseline_rate, max_rate, dynamics)` - Realistic spike generation
  - `analyze_spike_train_statistics(spike_data)` - ISI, CV, Fano factor analysis
  - `temporal_coding_analysis(spike_data, stimulus_times)` - Latency and precision metrics
  - `population_coding_analysis(population_responses, labels)` - PCA, LDA, correlations
  - `mutual_information_analysis(responses, stimuli)` - Information theory metrics
  - `odor_discrimination_analysis(responses, odor_ids, time_windows)` - Discrimination performance
  - `adaptation_dynamics_analysis(spike_data, stimulus_duration)` - Adaptation characterization
  - `information_rate_time_series(responses, dt_s, noise_std)` - Channel capacity estimation
  - `rate_coding_metrics(responses, labels)` - Basic discriminability metrics

## Script and Outputs
- Script: `scripts/generate_neural_encoding_analysis.py`
- Data: `output/data/neural_encoding_comprehensive.npz`
- Figure: `output/figures/neural_encoding_comprehensive_analysis.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/neural_encoding_comprehensive_analysis.png}
\caption{Comprehensive neural encoding analysis: Multi-neuron spike train generation with diverse response dynamics (exponential, adaptive, phasic-tonic), population coding with PCA dimensionality reduction, temporal precision analysis, inter-spike interval statistics, mutual information quantification, and adaptation dynamics characterization. Includes cross-correlation analysis, discrimination performance across time windows, and information-theoretic metrics for olfactory neural processing.}
\label{fig:app_neural_encoding}
\end{figure}

## Equation References
- Information rate: see \eqref{eq:channel_capacity}
- Response time model: see \eqref{eq:response_time}

## Reproducibility
- Run: `python3 scripts/generate_neural_encoding_analysis.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Deterministic seeds: `src/config.set_random_seed(42)` for surrogate time‑series.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
