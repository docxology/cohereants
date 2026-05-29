# Appendix D: Neural Encoding Efficiency on Time-Series {#sec:app_neural_encoding}

## Objective

Comprehensive neural encoding analysis including spike‑train generation, temporal dynamics, population coding, mutual information, and adaptation mechanisms for olfactory receptor neurons.

## Interpretation

Synthetic spike trains and population metrics explore how fast ORN-like encoders could carry timing information if an IR-sensitive stage existed. The analysis separates already-fast molecular latencies from hypothetical sub-millisecond components that falsifier 4 in \Cref{sec:discussion} targets.

## Claim boundary

\Cref{fig:app_neural_encoding_full} uses generated time series; it does not reanalyze published electrophysiology recordings or prove IR transduction.

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

<!-- alt: Neural encoding panels with spike trains, population PCA, and information metrics on synthetic ORN time series; model output only. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/neural_encoding_comprehensive_analysis.png}
\caption{Neural encoding panels with spike trains, population PCA, and information metrics on synthetic ORN time series. Claim boundary: model output only; does not establish biological IR olfaction.}
\label{fig:app_neural_encoding_full}
\end{figure}

<!-- Integrated analysis figure is used elsewhere; removed duplicate to prevent redundancy. -->

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
