# Appendix C: Detection Limits and Operating Points {#sec:app_detection_limits}

## Objective

Comprehensive detection-theory analysis with model operating points informed by electrophysiology literature anchors (not direct re-analysis of raw spike trains): ROC curves for millisecond-scale latency targets, sensitivity analysis for sub-10 ms ORN responses, operating regions in power-temperature space, and noise-floor characterization distinguishing electromagnetic from thermal effects for IR sensor bounds.

## Interpretation

Panels map literature-anchored SNR and power thresholds into ROC and operating-region plots. They answer whether a proposed IR stage could exceed thermal noise under stated assumptions, not whether insects operate at those points in nature.

## Claim boundary

\Cref{fig:app_detection_limits} bounds sensor feasibility; it does not establish biological IR olfaction or measured insect detection ranges.

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

<!-- alt: Detection limits panels with ROC curves, SNR operating regions, and noise floors for IR sensor bounds; model output only. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/detection_limits_comprehensive_analysis.png}
\caption{Detection limits analysis with ROC curves, SNR operating regions, noise floors, and range trade-offs for IR sensor bounds. Claim boundary: bounds sensor feasibility and model assumptions; does not establish biological IR olfaction.}
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
