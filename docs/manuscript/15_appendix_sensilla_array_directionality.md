# Appendix A: Sensilla Array Directionality and Beam Patterns {#sec:app_sensilla_array}

## Objective
Electromagnetic antenna modeling for sensilla arrays benchmarked against peer-reviewed morphometric ranges: circular/log-periodic designs inspired by insect antenna structures, element patterns, mutual coupling, 2D radiation patterns, representative morphology-to-resonance comparisons, and frequency-response characterization for candidate directional olfactory detection [@liu2021thripidae].

## Interpretation

Beam patterns and coupling matrices translate morphometric presets into directional gain estimates. They support the behavioral directionality discussion in \Cref{sec:experimental_results} while requiring IR-only assays to validate any link to orientation behavior.

## Claim boundary

\Cref{fig:app_sensilla_beam} reports model gain and resonance maps; it is not field proof of semiochemical IR olfaction.

## Methods (src)
- `src/case_studies/sensilla_array_directionality.py`
  - `design_circular_array(n_elements: int, radius_m: float, wavelength_m: float) -> np.ndarray`
  - `sensilla_element_pattern(sensilla_type: str, frequency_hz: float, dimensions: dict) -> np.ndarray`
  - `mutual_coupling_matrix(positions: np.ndarray, wavelength_m: float) -> np.ndarray`
  - `array_pattern_2d(positions: np.ndarray, element_patterns: np.ndarray, frequency: float, coupling: np.ndarray) -> np.ndarray`
  - `analyze_sensilla_morphology(dimensions: np.ndarray, frequency_range: np.ndarray) -> dict`
  - `frequency_response_analysis(array_config: dict, freq_range: np.ndarray) -> dict`
  - `compute_beam_pattern(wavelengths: np.ndarray, positions: np.ndarray, gains: np.ndarray) -> np.ndarray`
  - `array_gain(pattern: np.ndarray) -> float`
  - `design_log_periodic_array(min_len: float, max_len: float, tau: float, count: int) -> np.ndarray`

## Script and outputs
- Script: `scripts/generate_sensilla_array_directionality.py`
- Data: `output/data/sensilla_array_comprehensive.npz`
- Figure: `output/figures/sensilla_array_comprehensive_analysis.png`
- Caption metadata: `output/figures/sensilla_array_comprehensive_analysis.caption.txt`

## Figure
<!-- alt: Sensilla array beam patterns, coupling, and morphology-to-resonance maps from antenna models; bounds directional gain, not field proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/sensilla_array_comprehensive_analysis.png}
\caption{Sensilla array beam patterns, coupling, and morphology-to-resonance maps from antenna models. Claim boundary: bounds directional gain; not field proof of semiochemical IR olfaction.}
\label{fig:app_sensilla_beam}
\end{figure}

## Equation references
- Effective aperture: see \eqref{eq:effective_aperture}
- Gain pattern: see \eqref{eq:gain_pattern}

## Reproducibility
1. Run: `python3 scripts/generate_sensilla_array_directionality.py`
2. Artifacts: `output/data/` and `output/figures/`
3. Deterministic seed: `src/config.set_random_seed(42)`

## Cross‑references
- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math: \Cref{sec:mathematical_appendix}
