# Appendix B: Environmental Channel Modeling {#sec:app_environmental_channel}

## Objective
Model atmospheric transmission beyond plateau windows with humidity/temperature/path effects; map channel capacity versus environment.

## Planned Methods (src)
- `src/environmental_channel.py`
  - `atmospheric_transmission_detailed(wavelengths, humidity, temperature_k, path_m)`
  - `channel_capacity_vs_env(material_props, env_grid)`

## Planned Script and Outputs
- Script: `scripts/generate_environmental_channel_analysis.py`
- Data: `output/data/environmental_channel.npz`
- Figure: `output/figures/environmental_channel_capacity.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/environmental_channel_capacity.png}
\caption{Channel capacity as a function of humidity and temperature across IR wavelengths using detailed transmission modeling.}
\label{fig:app_env_channel}
\end{figure}

## Equation References
- Atmospheric transmission: see \eqref{eq:atmospheric_transmission}
- Channel capacity: see \eqref{eq:channel_capacity}

## Reproducibility
- Run: `python3 scripts/generate_environmental_channel_analysis.py`
- Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
