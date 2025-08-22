# Appendix B: Environmental Channel Modeling {#sec:app_environmental_channel}

## Objective
Comprehensive atmospheric channel modeling including molecular absorption, Rayleigh scattering, aerosol effects, channel capacity analysis, wavelength optimization, and environmental parameter sensitivity for IR communication systems.

## Methods (src)
- `src/case_studies/environmental_channel.py`
  - `molecular_absorption_cross_section(wavelengths, molecule_type)` - H2O, CO2, CH4 absorption
  - `rayleigh_scattering_coefficient(wavelengths, air_density)` - Molecular scattering
  - `atmospheric_transmission_comprehensive(wavelengths, conditions)` - Multi-component transmission
  - `channel_capacity_analysis(wavelengths, environmental_conditions)` - Shannon capacity mapping
  - `optimize_wavelength_for_range(target_range, capacity_requirements)` - Wavelength selection
  - `environmental_sensitivity_analysis(parameter_variations)` - Parameter sensitivity
  - `atmospheric_transmission_detailed(wavelengths, humidity, temperature, path)` - Basic transmission
  - `channel_capacity_vs_env(material_props, env_grid)` - Environmental capacity mapping

## Script and Outputs
- Script: `scripts/generate_environmental_channel_analysis.py`
- Data: `output/data/environmental_channel_comprehensive.npz`
- Figure: `output/figures/environmental_channel_comprehensive_analysis.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/environmental_channel_comprehensive_analysis.png}
\caption{Comprehensive environmental channel analysis: Molecular absorption cross-sections for H2O, CO2, and CH4, atmospheric transmission including Rayleigh scattering and aerosol effects, Shannon channel capacity mapping across environmental conditions, wavelength optimization for target ranges, and environmental parameter sensitivity analysis. Includes atmospheric windows identification and optimal operating conditions for IR communication.}
\label{fig:app_env_channel}
\end{figure}

## Equation References
- Atmospheric transmission: see \eqref{eq:atmospheric_transmission}
- Channel capacity: see \eqref{eq:channel_capacity}

## Reproducibility
- Run: `python3 scripts/generate_environmental_channel_analysis.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Set seed: `src/config.set_random_seed(42)` to ensure deterministic grids.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
