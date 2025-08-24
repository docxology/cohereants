# Appendix D: Neural Encoding Efficiency on Time-Series {#sec:app_neural_encoding}

## Objective

Comprehensive neural encoding analysis including spike‑train generation, temporal dynamics, population coding, mutual information, and adaptation mechanisms for olfactory receptor neurons.

## Methods (src)

- `src/case_studies/neural_encoding.py`
  - `generate_spike_trains(stimuli, dt, baseline_rate, max_rate, dynamics)` — realistic spike generation
  - `analyze_spike_train_statistics(spike_data)` — ISI, CV, Fano factor
  - `temporal_coding_analysis(spike_data, stimulus_times)` — latency and precision metrics
  - `population_coding_analysis(population_responses, labels)` — PCA, LDA, correlation structure
  - `mutual_information_analysis(responses, stimuli)` — information‑theoretic metrics
  - `odor_discrimination_analysis(responses, odor_ids, time_windows)` — discrimination performance
  - `adaptation_dynamics_analysis(spike_data, stimulus_duration)` — adaptation characterization
  - `information_rate_time_series(responses, dt_s, noise_std)` — channel‑capacity estimation
  - `rate_coding_metrics(responses, labels)` — separability and discriminability metrics

## Script and outputs

- Script: `scripts/generate_neural_encoding_analysis.py`
- Data: `output/data/neural_encoding_comprehensive.npz`
- Figure: `output/figures/neural_encoding_comprehensive_analysis.png`

## Figure

\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/neural_encoding_comprehensive_analysis.png}
\caption{Neural encoding analyses generated deterministically by `scripts/generate_neural_encoding_analysis.py` using `src/case_studies/neural_encoding.py`. Panels include spike trains, temporal precision, population PCA, ISI statistics, and mutual information metrics.}
\label{fig:app_neural_encoding_full}
\end{figure}

\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/integrated_analysis_information_analysis.png}
\caption{Integrated information analysis (from `scripts/generate_integrated_analysis.py`) showing molecular, receptor, neural and environmental information decomposition. This contextualizes neural encoding metrics in cross-domain information balances.}
\label{fig:integrated_neural_info}
\end{figure}

## Equation references

- Information rate: see \eqref{eq:channel_capacity_gloss}
- Response time model: see \eqref{eq:response_time_components}

## Reproducibility

- Run: `python3 scripts/generate_neural_encoding_analysis.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Deterministic seeds: `src/config.set_random_seed(42)` for surrogate time‑series.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}
