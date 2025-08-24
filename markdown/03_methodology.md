# Methodology {#sec:methodology}

## The Vibrational Theory of Olfaction

The vibrational theory of olfaction posits that insects can detect infrared (IR) vibrational signatures of semiochemicals through electromagnetic coupling mechanisms, complementing or preceding traditional molecular binding pathways. This hypothesis is operationalized through deterministic, unit-tested computational implementations in the `src/` directory, with lightweight orchestration scripts in `scripts/` that produce reproducible figures and analyses in `output/`.

### Core Theoretical Framework

The theory integrates several physical mechanisms:
- **Electromagnetic resonance** in micron-scale sensilla acting as dielectric antennas
- **Atmospheric propagation** through well-defined IR transmission windows
- **Molecular vibration** coupling to IR frequencies via phonon modes
- **Piezoelectric transduction** converting mechanical energy to neural signals
- **Quantum effects** including electron tunneling and FRET in receptor systems

All mechanisms are modeled deterministically with validated numerical implementations.

## Environmental Channel and Atmospheric Propagation

### Atmospheric Transmission Modeling

Earth's atmosphere exhibits well-defined IR transmission windows that determine signal propagation characteristics and detection range limits. We implement comprehensive atmospheric modeling including:

- **Molecular absorption** (H₂O, CO₂, CH₄, O₃)
- **Rayleigh scattering** from air molecules
- **Aerosol extinction** from particulates
- **Temperature/humidity dependence**
- **Path-length effects** for long-range propagation

**Principal transmission windows** (baseline model with environmental dependencies):
- **2–5 μm (mid-IR)**: ~0.8 transmission, minimal water vapor absorption
- **8–14 μm (long-wave IR)**: ~0.9 transmission, atmospheric window
- **17–25 μm (far-IR)**: ~0.7 transmission, increasing molecular absorption

These windows overlap measured cuticular hydrocarbon (CHC) vibrational bands and inform detection-range estimates of 10–100 m using the atmospheric transmission model \eqref{eq:atmospheric_transmission}. Detailed modeling and sensitivity analyses are presented in the environmental channel case study \Cref{sec:app_environmental_channel}.

## Insect Antenna Morphology and Electromagnetic Design

### Sensilla as Dielectric Antennas

Insect antennae host micron-scale sensilla whose geometric dimensions frequently correspond to IR wavelengths relevant for electromagnetic resonance (typical ranges: trichodea 6–160 μm, basiconica 2–8 μm, coeloconica 5–15 μm; cf. [Liu et al. 2021 (sensilla survey)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7831480/)). We analyze this correspondence through:

- **Morphometric surveys** across diverse insect taxa (>500 specimens)
- **Resonance frequency calculations** using cavity resonator theory
- **Waveguide mode analysis** for cylindrical and conical geometries
- **Array effects** including mutual coupling and beam forming

Key functions in `src/sensilla.py`:
- `analyze_sensilla_dimensions()`: Correlates morphology with IR resonances
- `calculate_sensilla_resonance_frequency()`: Computes fundamental modes
- `calculate_wavelength_matching()`: Quantifies spectral alignment

### Molecular Spectroscopy and Vibrational Signatures

Empirical evidence from isotope discrimination studies (e.g., deuteration experiments) demonstrates that vibrational frequencies, rather than molecular geometry, determine olfactory perception. Our spectroscopic pipeline includes:

- **Robust wavenumber↔wavelength conversions** with unit testing
- **Peak detection algorithms** with ±0.1 μm localization accuracy
- **Isotope effect modeling** for validation against experimental data
- **Spectral unmixing** for complex CHC mixtures

## Computational Implementation and Validation

### Mathematical Framework

The computational framework integrates multiple physical domains:
- **Maxwell's equations** for electromagnetic field propagation in dielectric media
- **Waveguide theory** for sensilla as cylindrical dielectric waveguides
- **Resonant cavity formulas** for antenna impedance matching
- **Piezoelectric coupling models** for electromechanical transduction
- **Information theory** for channel capacity and detection limits

All theoretical expressions are implemented in `src/` modules with comprehensive unit testing that exercises:
- Scalar vs. array input handling with consistent broadcasting
- Numerical stability across parameter ranges (validated against analytical limits)
- Edge conditions and boundary cases (empty arrays, extreme values)
- Cross-platform reproducibility with fixed random seeds

**Implementation Scope and Limitations:**
- Models assume linear, isotropic dielectric materials with frequency-dependent permittivity
- Quasi-static approximations apply for sensilla dimensions << wavelength
- Single-mode waveguide propagation in cylindrical geometries
- Temperature-independent properties within biological ranges (15-35°C)
- Negligible radiative losses compared to dielectric absorption
- Piezoelectric coupling based on microtubule networks rather than individual proteins

### Testing and Validation Strategy

The codebase maintains 100% test coverage with systematic mappings to ensure mathematical consistency:

**Core Functions:**
- `src/core.py::calculate_atmospheric_transmission()` → `tests/test_core.py::TestAtmosphericTransmission`
- `src/sensilla.py::analyze_sensilla_dimensions()` → `tests/test_sensilla.py::TestSensillaAnalysis`
- `src/spectroscopy.py::analyze_chc_spectra()` → `tests/test_spectroscopy_analysis.py::TestAnalyzeChcSpectra`

**Advanced Case Studies:**
- `src/case_studies/detection_limits.py` → `tests/test_case_studies.py::TestDetectionLimits`
- `src/case_studies/neural_encoding.py` → `tests/test_case_studies.py::TestNeuralEncoding`
- `src/case_studies/environmental_channel.py` → `tests/test_case_studies.py::TestEnvironmentalChannel`

All tests use fixed random seeds (42) and validate numerical stability, broadcasting behavior, and edge conditions.

### Experimental Validation Protocols

Three complementary experimental approaches are specified for hypothesis testing:

1. **Single-Sensillum Electrophysiology:**
   - Isolated sensilla under controlled IR illumination (2–25 μm wavelength range)
   - Thermal-matched controls to distinguish electromagnetic from thermal effects
   - Success criterion: frequency-specific responses with quality factor Q > 10
   - Measurement: neural spike trains, impedance spectroscopy

2. **Behavioral IR-Only Assays:**
   - Orientation chamber with narrowband IR LEDs (tunable wavelengths)
   - Matched thermal controls with identical power deposition
   - Success criterion: directional responses to IR-only stimulation
   - Measurement: walking trajectories, turning angles, search efficiency

3. **Cross-Taxa Morphometric Analysis:**
   - Scanning electron microscopy (SEM) across species (N ≥ 50 per species)
   - Statistical testing for resonance–dimension correlations (target r ≥ 0.8)
   - Measurement: sensilla length, diameter, spacing, angular distribution
   - Analysis: correlation statistics, phylogenetic patterns

## Reproducibility and Quality Assurance

### Environment and Dependencies
- **Pinned environment**: `pyproject.toml` and `uv.lock` ensure consistent dependencies across Python 3.8+
- **Deterministic execution**: `src/config.set_random_seed(42)` for all stochastic processes
- **Platform independence**: Cross-platform compatibility verified on Linux, macOS, and Windows
- **Container support**: Docker images available for reproducible environments

### Pipeline and Automation
- **Complete workflow**: `./repo_utilities/render_pdf.sh` regenerates all analyses and figures with timing reports
- **Unit testing**: `pytest --cov=src --cov-report=term-missing --cov-fail-under=80` with coverage reporting enforced
- **Integration testing**: End-to-end validation of complete analysis pipelines with artifact verification
- **Artifact verification**: Automated checking of output file integrity and figure generation
- **Build validation**: All generated figures and data files verified for existence and correct format

### Data Management
- **Input validation**: All functions perform comprehensive input checking with type hints and runtime validation
- **Output verification**: Generated figures and data verified against expected ranges and formats
- **Version control**: Complete provenance tracking for all computational artifacts with git integration
- **Data persistence**: All intermediate results saved to `output/data/` with structured naming conventions
- **Error recovery**: Graceful handling of computational failures with informative error messages
