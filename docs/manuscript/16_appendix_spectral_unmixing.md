# Appendix E: Spectral Unmixing and Classification {#sec:app_spectral_unmixing}

## Objective

Comprehensive spectral analysis: realistic CHC data generation, feature extraction, unmixing (NMF, VCA, ICA), and multi‑algorithm classification with deterministic evaluation.

## Interpretation

Synthetic mixtures benchmark unmixing and classification pipelines against known ground truth. Performance metrics justify spectroscopic feature extraction in \Cref{fig:chc_spectra_example} while leaving in vivo perceptual use of those bands as an open test.

## Claim boundary

\Cref{fig:app_spectral_unmixing} and \Cref{fig:integrated_classification} report algorithm evaluation on synthetic spectra; they are not species-identification proof on live specimens.

## Methods (src)

- `src/case_studies/spectral_unmixing.py`
  - `generate_realistic_chc_spectra(n_compounds: int, n_wavelengths: int, seed: int=42) -> dict` — synthetic CHC spectra with ground truth
  - `nmf_unmix(spectra: np.ndarray, n_components: int, seed: int=42) -> (W, H)` — deterministic NMF
  - `vertex_component_analysis(spectra: np.ndarray, n_endmembers: int) -> np.ndarray` — VCA endmember extraction
  - `independent_component_analysis_spectra(spectra: np.ndarray, n_components: int) -> np.ndarray` — ICA separation
  - `spectral_feature_extraction(spectra: np.ndarray, wavelengths: np.ndarray, method: str='peaks') -> dict` — peaks, derivatives, PCA, statistical features
  - `advanced_classification_suite(features: np.ndarray, labels: np.ndarray) -> dict` — multi‑algorithm benchmark
  - `performance_metrics_comprehensive(y_true: np.ndarray, y_pred: np.ndarray, y_prob: Optional[np.ndarray]=None) -> dict`
  - `lda_baseline(features: np.ndarray, labels: np.ndarray, seed: int=42) -> dict` — closed‑form LDA baseline

## Script and outputs

- Script: `scripts/generate_spectral_unmixing.py`
- Data: `output/data/spectral_unmixing_comprehensive.npz`
- Figure: `output/figures/spectral_unmixing_comprehensive_analysis.png`

## Figure

<!-- alt: Synthetic CHC spectral unmixing and classification benchmarks with NMF/VCA/ICA panels; algorithm evaluation, not species identification proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/spectral_unmixing_comprehensive_analysis.png}
\caption{Synthetic CHC spectral unmixing and classification benchmarks with NMF/VCA/ICA panels. Claim boundary: algorithm evaluation; not species identification proof.}
\label{fig:app_spectral_unmixing}
\end{figure}

<!-- alt: Cross-domain synthesis of normalized performance metrics across information, material, and efficiency domains; evidence ladder panel. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/integrated_analysis_cross_domain_synthesis.png}
\caption{Cross-domain synthesis from \texttt{scripts/generate\_integrated\_analysis.py}: normalized model metrics across information, material, and efficiency domains. Panel D reports unitless model sensitivity demo values, not predictive accuracy on live specimens. Claim boundary: engineering synthesis panel, not empirical classification proof.}
\label{fig:integrated_classification}
\end{figure}

## Equation References

## Reproducibility

- Run: `python3 scripts/generate_spectral_unmixing.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Fixed RNG seed (42) used for deterministic NMF initialization and cross‑validation splits.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}
