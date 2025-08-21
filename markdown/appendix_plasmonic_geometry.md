# Appendix F: Plasmonic Nano-Geometry Sweep {#sec:app_plasmonic_geometry}

## Objective
Sweep nanoparticle radii and media to quantify resonance frequency, quality factor, and field enhancement relevant to receptor microstructures.

## Planned Methods (src)
- `src/meta_sweep.py`
  - `sweep_plasmonic_quality(radii_m, metal_eps, medium_eps)`

## Planned Script and Outputs
- Script: `scripts/generate_plasmonic_geometry_sweep.py`
- Data: `output/data/plasmonic_geometry.npz`
- Figure: `output/figures/plasmonic_geometry_sweep.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/plasmonic_geometry_sweep.png}
\caption{Resonance frequency, Q factor, and field enhancement as functions of nanoparticle radius and medium dielectric.}
\label{fig:app_plasmonic_sweep}
\end{figure}

## Equation References
- Resonance/wavelength: see plasmonic definitions in main text; material equations in \cref{sec:mathematical_appendix}.

## Reproducibility
- Run: `python3 scripts/generate_plasmonic_geometry_sweep.py`
- Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
