# Appendix D: Neural Encoding Efficiency on Time-Series {#sec:app_neural_encoding}

## Objective
Estimate information rate and rate-coding metrics from deterministic time-series and labels.

## Planned Methods (src)
- `src/neural_encoding.py`
  - `information_rate_time_series(responses, dt_s, noise_std)`
  - `rate_coding_metrics(responses, labels)`

## Planned Script and Outputs
- Script: `scripts/generate_neural_encoding_analysis.py`
- Data: `output/data/neural_encoding.npz`
- Figure: `output/figures/neural_encoding_information_rate.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/neural_encoding_information_rate.png}
\caption{Estimated information rate and classification metrics for IR-evoked response surrogates under controlled noise levels.}
\label{fig:app_neural_encoding}
\end{figure}

## Equation References
- Information rate: see \eqref{eq:channel_capacity}
- Response time model: see \eqref{eq:response_time}

## Reproducibility
- Run: `python3 scripts/generate_neural_encoding_analysis.py`
- Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
