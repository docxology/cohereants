# Appendix F: Plasmonic Nano-Geometry Sweep {#sec:app_plasmonic_geometry}

## Objective
Comprehensive plasmonic nanostructure analysis including frequency-dependent permittivity, Mie scattering theory, coupled dipole interactions, field enhancement optimization, and near-field distribution modeling for receptor enhancement applications.

## Methods (src)
- `src/case_studies/plasmonic_geometry.py`
  - `drude_model_permittivity(frequency_hz, metal_type)` - Frequency-dependent material properties
  - `mie_scattering_sphere(radius_m, wavelength_m, eps_particle, eps_medium)` - Exact scattering solutions
  - `coupled_dipoles_near_field(positions, polarizabilities, wavelength)` - Multi-particle interactions
  - `optimize_plasmonic_geometry(wavelength_range, constraints)` - Geometry optimization
  - `field_distribution_near_particle(particle_params, grid_points)` - Near-field calculations
  - `sweep_plasmonic_quality(radii_m, metal_eps, medium_eps)` - Parameter sweeps

## Script and Outputs
- Script: `scripts/generate_plasmonic_geometry_analysis.py`
- Data: `output/data/plasmonic_geometry_comprehensive.npz`
- Figure: `output/figures/plasmonic_geometry_comprehensive_analysis.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/plasmonic_geometry_comprehensive_analysis.png}
\caption{Comprehensive plasmonic analysis: Drude model frequency-dependent permittivity for various metals, Mie scattering efficiency and resonance peaks, coupled dipole near-field enhancement, geometry optimization results, and spatial field distribution maps. Includes resonance tuning, field enhancement optimization, and multi-particle coupling effects for enhanced molecular detection applications.}
\label{fig:app_plasmonic_sweep}
\end{figure}

## Equation References
- Resonance/wavelength: see plasmonic definitions in main text; material equations in \cref{sec:mathematical_appendix}.

## Reproducibility
- Run: `python3 scripts/generate_plasmonic_geometry_sweep.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Deterministic radii grid and material parameters via seed 42.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
