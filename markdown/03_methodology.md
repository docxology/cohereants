# Methodology {#sec:methodology}

## The Vibrational Theory of Olfaction

The vibrational theory proposes that insects can detect infrared (IR) vibrational signatures emitted by odor molecules in addition to—or upstream of—molecular binding. We operationalize this hypothesis with deterministic, unit-tested implementations in `src/` and lightweight scripts in `scripts/` that produce reproducible figures in `output/figures/`.

### Atmospheric Transmission and Detection Range

Earth's atmosphere has well-defined IR transmission windows that constrain signal propagation and detection range. We model atmospheric attenuation, molecular absorption, Rayleigh scattering, and aerosol extinction in the Appendices and expose parameterized functions for sensitivity analysis. Code performs input validation and supports scalar/array broadcasting. See the environmental channel case study (\cref{sec:app_environmental_channel}) and detection limits (\cref{sec:app_detection_limits}).

**Transmission windows** (baseline model):
- **2–5 μm (mid-IR)**: ~0.8 transmission
- **8–14 μm (long-wave IR)**: ~0.9 transmission
- **17–25 μm (far-IR)**: ~0.7 transmission

These windows overlap measured CHC bands and inform detection-range estimates (10–100 m) using the atmospheric transmission model (\eqref{eq:atmospheric_transmission}). \Cref{fig:atmospheric_transmission} illustrates the model outputs; generation details are in \cref{sec:app_environmental_channel}.

## Insect antenna morphology as electromagnetic antennas

### Sensilla architecture and dimensions

Insect antennae host micron-scale sensilla whose lengths and diameters often fall in ranges relevant to IR wavelengths. We compute resonance predictions with `src/sensilla.py::analyze_sensilla_dimensions` and validate against measured samples; results and visualizations are in \cref{sec:app_sensilla_array}.

### Molecular spectroscopy and isotope effects

Empirical isotope discrimination (e.g., deuteration) alters vibrational frequencies while preserving molecular geometry; such findings are consistent with vibrational sensitivity. Our pipeline implements robust wavenumber↔wavelength conversions and peak detection with ±0.1 μm localization as unit-tested utilities.

### Cuticular hydrocarbon spectroscopy

CHC spectra contain distinct vibrational bands that frequently lie inside atmospheric windows. Feature extraction, unmixing, and baseline classification are implemented in `src/case_studies/spectral_unmixing.py`; reproducible figures are in the Appendix (\cref{sec:app_spectral_unmixing}).

## Computational implementation and validation

### Mathematical framework

Our computational framework integrates Maxwell's equations, waveguide theory, resonant-cavity formulas, and piezoelectric coupling models. All theoretical expressions are implemented in `src/` with unit tests that exercise branching and array-versus-scalar paths. Mathematical derivations appear in the Mathematical Appendix (\cref{sec:mathematical_appendix}).

### Validation and testing

Representative mappings between code and tests include:
- `calculate_atmospheric_transmission` → `tests/test_core.py::TestAtmosphericTransmission`
- `analyze_sensilla_dimensions` → `tests/test_sensilla.py::TestSensillaAnalysis`
- `analyze_chc_spectra` → `tests/test_spectroscopy_analysis.py::TestAnalyzeChcSpectra`

Tests use a fixed seed (42) where applicable and validate numerical stability, broadcasting, and edge conditions.

### Experimental validation protocols (summarized)

1. **Single-sensillum IR sensitivity** — isolated sensilla under controlled IR illumination (2–25 μm) with thermal-matched controls; success criterion: frequency-specific responses (Q>10).
2. **Behavioral IR-only assays** — orientation chamber with IR LEDs and thermal controls; success: directional responses to narrowband IR.
3. **Cross-taxa dimensional analysis** — SEM measurements across species (N≥50 per species), statistical testing for resonance–dimension correlations (target r≥0.8).

### Reproducibility

- Environment pinned via `pyproject.toml`/`uv.lock`.
- Deterministic execution via `src/config.set_random_seed(42)`.
- Complete pipeline: `bash ./repo_utilities/render_pdf.sh` regenerates analyses and figures.
- Unit and integration testing enforced via `pytest`.
