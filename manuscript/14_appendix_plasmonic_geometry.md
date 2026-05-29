# Appendix F: Plasmonic Nano-Geometry Sweep {#sec:app_plasmonic_geometry}

## Objective
Comprehensive plasmonic nanostructure analysis: frequency-dependent permittivity (Drude), Mie scattering, coupled‑dipole near‑field interactions, geometry optimization, and field‑enhancement mapping for receptor‑scale enhancement.

## Interpretation

Sweeps identify nanoparticle sizes and materials that maximize near-field enhancement at MIR wavelengths relevant to biomimetic bands {{BIOMIMETIC_IR_BAND_UM}}. Results inform whether receptor-scale structures could, in principle, boost weak narrowband signals—not whether insects employ plasmonics in sensilla.

## Claim boundary

\Cref{fig:app_plasmonic_sweep} bounds sensor-design feasibility; it does not establish biological IR olfaction.

## Methods (src)

- `src/case_studies/plasmonic_geometry.py`
  - `drude_model_permittivity(frequency_hz, metal_type)` — material permittivity model
  - `mie_scattering_sphere(radius_m, wavelength_m, eps_particle, eps_medium)` — Mie solutions
  - `coupled_dipoles_near_field(positions, polarizabilities, wavelength)` — multi‑particle interactions
  - `optimize_plasmonic_geometry(wavelength_range, constraints)` — geometry optimization
  - `field_distribution_near_particle(particle_params, grid_points)` — near‑field maps
  - `sweep_plasmonic_quality(radii_m, metal_eps, medium_eps)` — parameter sweeps for Q‑factor analysis

## Script and outputs

- Script: `scripts/generate_plasmonic_geometry_sweep.py`
- Data: `output/data/plasmonic_geometry_comprehensive.npz`
- Figure: `output/figures/plasmonic_geometry_comprehensive_analysis.png`

## Figure

<!-- alt: Plasmonic geometry sweep with Drude permittivity, Mie scattering, and near-field enhancement maps for receptor-scale sensor design. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/plasmonic_geometry_comprehensive_analysis.png}
\caption{Plasmonic geometry sweep with Drude permittivity, Mie scattering, and near-field enhancement maps for receptor-scale sensor design. Claim boundary: bounds sensor feasibility and model assumptions; does not establish biological IR olfaction.}
\label{fig:app_plasmonic_sweep}
\end{figure}

<!-- alt: Integrated metamaterial dielectric and plasmonic response with information-capacity summaries; engineering model panels. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/integrated_analysis_metamaterial_properties.png}
\caption{Integrated metamaterial dielectric and plasmonic response with information-capacity summaries. Claim boundary: engineering model panels only; does not establish biological IR olfaction.}
\label{fig:integrated_metamaterial}
\end{figure}

## Equation references

-- Resonance/wavelength: see main text and the Mathematical Appendix \Cref{sec:mathematical_appendix}.

## Reproducibility

- Run: `python3 scripts/generate_plasmonic_geometry_sweep.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Deterministic radii grid and material parameters via `src/config.set_random_seed(42)`.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}
