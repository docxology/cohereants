# Appendix E: Spectral Unmixing and Classification {#sec:app_spectral_unmixing}

## Objective
Comprehensive spectral analysis including advanced unmixing algorithms, feature extraction, and multi-algorithm classification for CHC identification and chemical analysis.

## Methods (src)
- `src/case_studies/spectral_unmixing.py`
  - `generate_realistic_chc_spectra(n_compounds, n_wavelengths)` - Synthetic CHC spectral data
  - `nmf_unmix(spectra, n_components, seed=42)` - Non-negative matrix factorization
  - `vertex_component_analysis(spectra, n_endmembers)` - VCA endmember extraction
  - `independent_component_analysis_spectra(spectra, n_components)` - ICA blind separation
  - `spectral_feature_extraction(spectra, method)` - Multi-method feature extraction
  - `advanced_classification_suite(features, labels)` - Multi-algorithm classification
  - `performance_metrics_comprehensive(y_true, y_pred, y_prob)` - Detailed evaluation metrics
  - `lda_baseline(features, labels, seed=42)` - Linear discriminant baseline

## Script and Outputs
- Script: `scripts/generate_spectral_unmixing.py`
- Data: `output/data/spectral_unmixing_comprehensive.npz`
- Figure: `output/figures/spectral_unmixing_comprehensive_analysis.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/spectral_unmixing_comprehensive_analysis.png}
\caption{Comprehensive spectral analysis: Synthetic CHC spectra with realistic chemical diversity, advanced unmixing using NMF, VCA, and ICA algorithms, multi-method feature extraction (peaks, derivatives, PCA, statistical), and multi-algorithm classification performance comparison. Includes detailed performance metrics, confusion matrices, and algorithmic benchmarking for chemical identification applications.}
\label{fig:app_spectral_unmixing}
\end{figure}

## Equation References
- Spectral overlap: see \eqref{eq:channel_capacity} analogs for information metrics; overlap in main text.

## Reproducibility
- Run: `python3 scripts/generate_spectral_unmixing.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Fixed RNG seed (42) used for NMF initialization and fold splits.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
