# Appendix A: Sensilla Array Directionality and Beam Patterns {#sec:app_sensilla_array}

## Objective
Comprehensive electromagnetic antenna modeling for sensilla arrays including circular array design, element pattern modeling, mutual coupling effects, 2D radiation patterns, morphology analysis, and frequency response characterization for directional olfactory detection.

## Methods (src)
- `src/case_studies/sensilla_array_directionality.py`
  - `design_circular_array(n_elements, radius_m, wavelength_m)` - Circular array geometry
  - `sensilla_element_pattern(sensilla_type, frequency_hz, dimensions)` - Individual element patterns
  - `mutual_coupling_matrix(positions, wavelength_m)` - Inter-element coupling
  - `array_pattern_2d(positions, element_patterns, frequency, coupling)` - 2D radiation patterns
  - `analyze_sensilla_morphology(dimensions, frequency_range)` - Morphology analysis
  - `frequency_response_analysis(array_config, freq_range)` - Bandwidth and Q-factor
  - `compute_beam_pattern(wavelengths, positions, gains)` - Basic beam pattern
  - `array_gain(pattern)` - Gain calculation
  - `design_log_periodic_array(min_len, max_len, tau, count)` - Log-periodic design

## Script and Outputs
- Script: `scripts/generate_sensilla_array_directionality.py`
- Data: `output/data/sensilla_array_comprehensive.npz`
- Figure: `output/figures/sensilla_array_comprehensive_analysis.png`
- Caption: `output/figures/sensilla_array_comprehensive_analysis.caption.txt`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/sensilla_array_comprehensive_analysis.png}
\caption{Comprehensive sensilla array analysis: Circular, linear, and log-periodic array configurations with 2D radiation patterns, individual element patterns (dipole, monopole, patch), mutual coupling effects, morphological analysis relating sensilla dimensions to resonant wavelengths, and frequency response characterization. Includes beam steering capabilities, array gain optimization, and directional sensitivity patterns for enhanced spatial resolution in olfactory detection.}
\label{fig:app_sensilla_beam}
\end{figure}

## Equation References
- Effective aperture: see \eqref{eq:effective_aperture}
- Gain pattern: see \eqref{eq:gain_pattern}

## Reproducibility
1. Run: `python3 scripts/generate_sensilla_array_directionality.py`
2. Artifacts saved to `output/data/` and `output/figures/`.
3. Deterministic seed set via `src/config.set_random_seed(42)`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Mathematical forms: \cref{sec:mathematical_appendix}
