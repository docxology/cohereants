# Appendix A: Sensilla Array Directionality and Beam Patterns {#sec:app_sensilla_array}

## Objective
Quantify array directionality, beam patterns, and array gain for sensilla arrangements (log‑periodic and uniform), relating morphology to directional detection.

## Planned Methods (src)
- `src/antenna_arrays.py`
  - `compute_beam_pattern(wavelengths, positions, gains)`
  - `array_gain(pattern)`
  - `design_log_periodic_array(min_len_um, max_len_um, tau, count)`

## Planned Script and Outputs
- Script: `scripts/generate_sensilla_array_directionality.py`
- Data: `output/data/sensilla_array.npz`
- Figure: `output/figures/sensilla_array_beam_patterns.png`
- Caption: `output/figures/sensilla_array_beam_patterns.caption.txt`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/sensilla_array_beam_patterns.png}
\caption{Beam patterns for sensilla arrays across infrared wavelengths; log‑periodic vs uniform arrays, showing half‑power beamwidth and side‑lobe structure.}
\label{fig:app_sensilla_beam}
\end{figure}

## Equation References
- Effective aperture: see \eqref{eq:effective_aperture}
- Gain pattern: see \eqref{eq:gain_pattern}

## Reproducibility
1. Run: `python3 scripts/generate_sensilla_array_directionality.py`
2. Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Mathematical forms: \cref{sec:mathematical_appendix}
