# Appendix B: Environmental Channel Modeling {#sec:app_environmental_channel}

## Objective

Comprehensive atmospheric channel modeling benchmarked against atmospheric spectroscopy concepts: molecular absorption (H\textsubscript{2}O, CO\textsubscript{2}, CH\textsubscript{4}, O\textsubscript{3}), Rayleigh scattering, aerosol effects, channel-capacity mapping with 8-14 $\mu\mathrm{m}$ window emphasis, wavelength optimization over selected ranges, and environmental sensitivity analysis for candidate IR communication scenarios [@gordon2022hitran].

## Interpretation

The case study compares how humidity, temperature, and path length shift usable windows and Shannon capacity under simplified atmospheric models. Results inform where narrowband signatures could propagate, complementing \Cref{fig:atmospheric_transmission} without replacing line-by-line radiative transfer.

## Claim boundary

\Cref{fig:app_env_channel} reports engineering channel bounds under modeled conditions; it is not a measured insect communication range.

## Methods (src)

- `src/case_studies/environmental_channel.py`
  - `molecular_absorption_cross_section(wavelengths, molecule_type)` — H2O, CO2, CH4 absorption
  - `rayleigh_scattering_coefficient(wavelengths, air_density)` — molecular scattering
  - `atmospheric_transmission_comprehensive(wavelengths, conditions)` — multi‑component transmission
  - `channel_capacity_analysis(wavelengths, environmental_conditions)` — Shannon capacity mapping
  - `optimize_wavelength_for_range(target_range, capacity_requirements)` — wavelength selection
  - `environmental_sensitivity_analysis(parameter_variations)` — parameter sensitivity
  - `atmospheric_transmission_detailed(wavelengths, humidity, temperature, path)` — basic transmission utility
  - `channel_capacity_vs_env(material_props, env_grid)` — grid mapping of capacity vs environment

## Script and outputs

- Script: `scripts/generate_environmental_channel_analysis.py`
- Data: `output/data/environmental_channel_comprehensive.npz`
- Figure: `output/figures/environmental_channel_comprehensive_analysis.png`

## Figure

<!-- alt: Atmospheric channel model with absorption, scattering, and capacity maps across humidity and temperature; engineering channel bounds. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/environmental_channel_comprehensive_analysis.png}
\caption{Environmental channel model with absorption, scattering, and capacity maps across humidity and temperature grids. Claim boundary: channel-capacity sensitivity demo under modeled clear/humid conditions; not a measured insect range.}
\label{fig:app_env_channel}
\end{figure}

<!-- Removed duplicate figure: uses the primary `app_env_channel` figure above -->

<!-- alt: Integrated information decomposition across molecular, receptor, neural, and environmental terms; bounds sensor throughput, not biological proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/integrated_analysis_information_analysis.png}
\caption{Integrated information decomposition across molecular, receptor, neural, and environmental terms. Claim boundary: bounds sensor throughput; does not establish biological IR olfaction.}
\label{fig:integrated_info}
\end{figure}

## Equation references

- Atmospheric transmission: see \eqref{eq:atmospheric_transmission}
- Channel capacity: see \eqref{eq:channel_capacity_gloss}

## Reproducibility

- Run: `python3 scripts/generate_environmental_channel_analysis.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Deterministic grids via `src/config.set_random_seed(42)`.

## Context Note on Biological Ranges

Some insects exhibit sensitivity to thermal IR in natural behaviors. *Aedes aegypti* integrates thermal IR around the human skin-temperature spectrum with other host cues [@chandel2024thermal]. *Rhodnius prolixus* discriminates radiant IR from convective heat via antennal warm-cell combinatorial coding; forced convection disrupts that quotient [@zopf2014infrared; @zopf2015convection]. Lazzari reviewed how radiant IR operates at longer range than convective heat near hosts [@lazzari2009orientation]. These behavioral constraints complement the electromagnetic window analysis and motivate species- and wavelength-specific range predictions.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}
