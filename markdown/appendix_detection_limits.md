# Appendix C: Detection Limits and Operating Points {#sec:app_detection_limits}

## Objective

Comprehensive detection‑theory analysis with validation against electrophysiological studies: ROC curves for 1-5 ms latency detection, sensitivity analysis for sub-10 ms ORN responses, operating regions in power-temperature space, and noise‑floor characterization distinguishing electromagnetic from thermal effects for IR olfactory detection systems.

## Methods (src)

- `src/case_studies/detection_limits.py`
  - `min_detectable_power(temperature_k, bandwidth_hz, snr_min_db)` — thermal‑noise‑limited detection
  - `roc_analysis(signal_power, noise_power)` — ROC curves and optimal thresholds
  - `detection_performance_vs_snr(snr_range_db, pfa_target)` — performance curves and MDS
  - `sensitivity_analysis(power_range, temp_range, param_variations)` — parameter sensitivity
  - `operating_regions_analysis(power_range, temp_range)` — SNR contours in operating space
  - `noise_floor_analysis(freq_range, temperature_k)` — multi‑component noise analysis
  - `detection_range_analysis(tx_power, antenna_gain, frequency, sensitivity)` — range calculations
  - `optimize_detection_parameters(constraints, objectives)` — system optimization

## Script and outputs

- Script: `scripts/generate_detection_limits.py`
- Data: `output/data/detection_limits_comprehensive.npz`
- Figure: `output/figures/detection_limits_comprehensive_analysis.png`

## Figure

\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/detection_limits_comprehensive_analysis.png}
\caption{Comprehensive detection analysis: ROC curves with AUC metrics, detection performance vs SNR showing minimum detectable signal (MDS), operating regions in power-temperature space, noise-floor components, detection range analysis, and parameter optimization. Includes processing gain effects, optimal threshold selection, and performance trade-offs for IR olfactory detection systems.}
\label{fig:app_detection_limits}
\end{figure}

<!-- Removed duplicate figure block to avoid repeated insertion; primary figure `app_detection_limits` remains above. -->

## Equation references

- Minimum power: see \eqref{eq:min_power_gloss}
- Capacity: see \eqref{eq:channel_capacity_gloss}

## Reproducibility

- Run: `python3 scripts/generate_detection_limits.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Deterministic operating points via `src/config.set_random_seed(42)`.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}
