# Appendix E: Spectral Unmixing and Classification {#sec:app_spectral_unmixing}

## Objective
Unmix composite spectra and evaluate small, deterministic classification baselines on CHC features.

## Planned Methods (src)
- `src/spectral_unmixing.py`
  - `nmf_unmix(spectra, n_components, seed=42)`
  - `lda_baseline(features, labels, seed=42)`

## Planned Script and Outputs
- Script: `scripts/generate_spectral_unmixing.py`
- Data: `output/data/spectral_unmixing.npz`
- Figure: `output/figures/spectral_unmixing_components.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/spectral_unmixing_components.png}
\caption{Unmixed component spectra and reconstruction error across seeds; baseline classification accuracy on deterministic folds.}
\label{fig:app_spectral_unmixing}
\end{figure}

## Equation References
- Spectral overlap: see \eqref{eq:channel_capacity} analogs for information metrics; overlap in main text.

## Reproducibility
- Run: `python3 scripts/generate_spectral_unmixing.py`
- Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
