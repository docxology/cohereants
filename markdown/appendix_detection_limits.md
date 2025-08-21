# Appendix C: Detection Limits and Operating Points {#sec:app_detection_limits}

## Objective
Quantify minimum detectable power, SNR curves, and operating points for IR olfactory channels.

## Planned Methods (src)
- `src/detection_limits.py`
  - `min_detectable_power(temperature_k, bandwidth_hz, snr_min_db)`
  - `snr_curve(signal_power_w, noise_temp_k, bandwidth_hz)`
  - `operating_point(capacity_bits_s, snr_db)`

## Planned Script and Outputs
- Script: `scripts/generate_detection_limits.py`
- Data: `output/data/detection_limits.npz`
- Figure: `output/figures/detection_limits_operating_points.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/detection_limits_operating_points.png}
\caption{Minimum detectable power contours and operating regions vs bandwidth and temperature; SNR and capacity overlays.}
\label{fig:app_detection_limits}
\end{figure}

## Equation References
- Minimum power: see \eqref{eq:min_power}
- Capacity: see \eqref{eq:channel_capacity}

## Reproducibility
- Run: `python3 scripts/generate_detection_limits.py`
- Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
