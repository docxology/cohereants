# Methodology {#sec:methodology}

## The Vibrational Theory of Olfaction

The vibrational theory of olfaction proposes that molecular vibrations may contribute to odor recognition, potentially through electron-transfer or related spectroscopic mechanisms [@turin1996spectroscopic]. CohereAnts extends that idea into an insect-focused computational hypothesis: IR cues associated with semiochemicals could complement molecular binding in specific sensory contexts. Because receptor-level evidence remains contested [@block2015implausibility], the code is written as a falsification framework rather than as a proof of biological IR olfaction.

### Core Theoretical Framework

The modeled mechanisms are deliberately separated so each can fail independently:

- **Electromagnetic resonance** in micron-scale sensilla treated as candidate dielectric antenna structures.
- **Atmospheric propagation** through simplified IR transmission windows, with HITRAN-style spectroscopy as the relevant external reference class [@gordon2022hitran].
- **Molecular vibration** in CHC-associated spectral regions measured by ATR-FTIR and related methods [@durak2022atrftir; @blomquist2021hydrocarbons].
- **Mechanotransduction** as an analogy for converting physical deformation or thermal expansion into neural response, not as direct evidence for olfactory IR transduction [@di2023mechanotransduction].
- **Electron-transfer vibration theory** as a contested theoretical mechanism that must survive receptor-level tests [@turin1996spectroscopic; @block2015implausibility].

All computational mechanisms are deterministic and unit-tested; biological interpretation is constrained by the external sources above.

## Environmental Channel and Atmospheric Propagation

### Atmospheric Transmission Modeling

Earth's atmosphere exhibits IR transmission windows that determine signal propagation characteristics and range limits. The baseline `src.core.calculate_atmospheric_transmission()` model is an intentionally coarse window model, while the case-study module adds humidity, temperature, scattering, and path-length sensitivity terms. The code should therefore be read as a scenario generator, not as a substitute for line-by-line radiative transfer.

- **Molecular absorption** (H\textsubscript{2}O, CO\textsubscript{2}, CH\textsubscript{4}, O\textsubscript{3})
- **Rayleigh scattering** from air molecules
- **Aerosol extinction** from particulates
- **Temperature/humidity dependence**
- **Path-length effects** for long-range propagation

**Principal windows represented in the baseline model**:
- **2–5 $\mu\mathrm{m}$ (mid-IR)**: represented as a favorable transmission band.
- **8–14 $\mu\mathrm{m}$ (long-wave IR)**: represented as the strongest atmospheric window.
- **17–25 $\mu\mathrm{m}$ (far-IR extension)**: represented as a lower-confidence exploratory band with stronger environmental dependence.

These windows overlap some CHC- and cuticle-associated vibrational bands, but overlap is only a necessary physical condition. Blackbody peaks from ecologically relevant sources fall near {{FIRE_BLACKBODY_PEAK_UM}} µm for forest fires and ~{{SKIN_BLACKBODY_PEAK_UM}} µm for human skin at {{MOSQUITO_IR_SOURCE_TEMP_C}} °C, aligning pyrophilous and hematophagy IR precedents with the modeled windows [@schmitztrenner2003spectral; @chandel2024thermal]. Detection-range estimates in this manuscript are model outputs from \eqref{eq:atmospheric_transmission}, not measured insect ranges. See \Cref{fig:atmospheric_transmission} and the environmental channel case study \Cref{sec:app_environmental_channel}.

<!-- alt: Atmospheric transmission versus wavelength with shaded mid-IR, long-wave, and far-IR windows and a biomimetic 2.8–6 µm band; coarse model scope, not a range proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=1.0\textwidth]{../output/figures/atmospheric_transmission.png}
\caption{Atmospheric transmission window analysis from \texttt{src.core.calculate\_atmospheric\_transmission()} across 1--30~\(\mu\mathrm{m}\). Shaded bands mark modeled windows and the literature-anchored biomimetic band {{BIOMIMETIC_IR_BAND_UM}}. Claim boundary: window overlap is necessary but not sufficient for semiochemical IR communication.}
\label{fig:atmospheric_transmission}
\end{figure}

## Insect Antenna Morphology and Electromagnetic Design

### Sensilla as Dielectric Antennas

Insect antennae host micron-scale sensilla that can be compared against IR wavelengths using simple quarter- and half-wave estimates. Callahan proposed that sensilla function as dielectric waveguides for far-IR molecular emissions—a mechanism that remains contested but motivates geometric screening [@callahan1965fir; @callahan1977moth]. The current figures use representative sensilla classes from the literature and the published Thripidae measurements of Liu et al. as an anchor, rather than claiming an already completed 500-specimen morphometric dataset [@liu2021thripidae]. We analyze this correspondence through:

- **Representative morphometric ranges** across sensillum classes and taxa
- **Resonance frequency calculations** using cavity resonator theory
- **Waveguide mode analysis** for cylindrical and conical geometries
- **Array effects** including mutual coupling and beam forming

Key functions in `src/sensilla.py`:
- `analyze_sensilla_dimensions()`: Correlates morphology with IR resonances
- `calculate_sensilla_resonance_frequency()`: Computes fundamental modes
- `calculate_wavelength_matching()`: Quantifies spectral alignment

See \Cref{fig:sensilla_wavelength_matching} for representative morphometric inputs and modeled resonance estimates versus atmospheric windows.

<!-- alt: Representative sensilla dimensions and modeled quarter- and half-wave resonance estimates plotted against atmospheric windows; geometry screening, not receptor tuning proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=1.0\textwidth]{../output/figures/sensilla_wavelength_matching.png}
\caption{Representative sensilla dimensions and quarter-/half-wave resonance estimates from \texttt{src.sensilla.analyze\_sensilla\_dimensions()}. Claim boundary: model probes, not measured insect IR receptor tuning curves.}
\label{fig:sensilla_wavelength_matching}
\end{figure}

### Molecular Spectroscopy and Vibrational Signatures

Isotope discrimination studies support the possibility of a molecular vibration-sensing component in Drosophila, while receptor-level critiques argue against broad claims for vibrational olfaction [@franco2011molecular; @block2015implausibility]. Our spectroscopic pipeline therefore treats vibrational features as discriminative spectral variables, not as settled perceptual mechanisms. It includes:

- **Robust wavenumber$\leftrightarrow$wavelength conversions** with unit testing
- **Peak detection algorithms** with $\pm 0.1\,\mu\mathrm{m}$ localization accuracy
- **Isotope effect modeling** for validation against experimental data
- **Spectral unmixing** for complex CHC mixtures

See \Cref{fig:chc_spectra_example} for a deterministic CHC fixture analyzed via \texttt{src.spectroscopy.analyze\_chc\_spectra()}.

<!-- alt: Synthetic cuticular-hydrocarbon infrared spectrum with C-H stretch and bend regions annotated; fixture for spectral feature extraction, not a measured ant spectrum. -->
\begin{figure}[h]
\centering
\includegraphics[width=1.0\textwidth]{../output/figures/chc_spectra_example.png}
\caption{CHC infrared spectrum fixture processed by \texttt{analyze\_chc\_spectra()}. Claim boundary: supports feature extraction and hypothesis generation; does not establish in vivo semiochemical IR olfaction.}
\label{fig:chc_spectra_example}
\end{figure}

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
- Temperature-independent properties within biological ranges (15-35$^{\circ}\mathrm{C}$)
- Negligible radiative losses compared to dielectric absorption
- Electromechanical coupling terms are exploratory; the manuscript does not claim a verified insect olfactory transduction pathway.

### Testing and Validation Strategy

The project enforces the template's $\geq 90\%$ `src/` coverage gate and maps core computations to tests:

**Core Functions:**
- `src/core.py::calculate_atmospheric_transmission()` → `tests/test_core.py::TestAtmosphericTransmission`
- `src/sensilla.py::analyze_sensilla_dimensions()` → `tests/test_sensilla.py::TestSensillaAnalysis`
- `src/spectroscopy.py::analyze_chc_spectra()` → `tests/test_spectroscopy_analysis.py::TestAnalyzeChcSpectra`

**Advanced Case Studies:**
- `src/case_studies/detection_limits.py` → `tests/test_case_studies.py::TestDetectionLimits`
- `src/case_studies/neural_encoding.py` → `tests/test_case_studies.py::TestNeuralEncoding`
- `src/case_studies/environmental_channel.py` → `tests/test_case_studies.py::TestEnvironmentalChannel`

All tests use fixed random seeds ({{RANDOM_SEED}}) and validate numerical stability, broadcasting behavior, and edge conditions.

### Experimental Protocol Specification

Engineering deliverables prioritize preregistered, IR-only assays with thermal controls:

| Parameter | Specification | Source tier |
|-----------|---------------|-------------|
| QCL/LED band | {{PROTOCOL_QCL_BAND_UM}} | `src/manuscript_fixtures.py` |
| Power density | {{PROTOCOL_POWER_DENSITY_MW_CM2}} mW/cm² | protocol default |
| Thermal control | {{PROTOCOL_THERMAL_CONTROL}} | preregistered assay |
| Minimum N | ≥{{PROTOCOL_MIN_N}} per condition | preregistration |
| SNR operating point | {{SNR_OPERATING_DB}} dB (model) | `output/data/detection_limits_spec.json` |

Mosquito thermal-IR host-seeking assays use skin-temperature blackbody sources ({{MOSQUITO_IR_SOURCE_TEMP_C}} °C, peak ~{{MOSQUITO_IR_PEAK_UM}} µm, range ~{{MOSQUITO_IR_RANGE_M}} m) and are not interchangeable with narrowband QCL olfactometry [@chandel2024thermal; @corfas2015trpa1]. *Melanophila* pit-organ photomechanic precedents anchor biomimetic bands {{BIOMIMETIC_IR_BAND_UM}} and literature thresholds {{BIOMIMETIC_THRESHOLD_MW_CM2}} mW/cm² [@schmitz2011infrared; @hammer2001sensitivity; @schmitztrenner2003spectral; @evans2005thermopneumatic; @siebke2014biomimetic].

### Experimental Validation Protocols

Three complementary experimental approaches are specified for hypothesis testing:

1. **Single-Sensillum Electrophysiology:**
   - Isolated sensilla under controlled IR illumination (2–25 $\mu\mathrm{m}$ wavelength range)
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
- **Pinned environment**: `pyproject.toml` and `uv.lock` ensure consistent dependencies across supported Python versions.
- **Deterministic execution**: `src/config.set_random_seed({{RANDOM_SEED}})` for all stochastic processes
- **Platform independence**: Numerical code avoids current known CWD assumptions; full cross-platform CI for this local-only project is outside the present artifact.

### Pipeline and Automation
- **Complete workflow**: `MPLBACKEND=Agg .venv/bin/python scripts/generate_research_figures.py` regenerates the core figures, and the template renderer consumes the manuscript sections.
- **Unit testing**: `MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-report=term-missing` exercises the local project gate.
- **Integration testing**: End-to-end validation of complete analysis pipelines with artifact verification
- **Artifact verification**: Automated checking of output file integrity and figure generation
- **Build validation**: All generated figures and data files verified for existence and correct format

### Data Management
- **Input validation**: All functions perform comprehensive input checking with type hints and runtime validation
- **Output verification**: Generated figures and data verified against expected ranges and formats
- **Version control**: Complete provenance tracking for all computational artifacts with git integration
- **Data persistence**: All intermediate results saved to `output/data/` with structured naming conventions
- **Error recovery**: Graceful handling of computational failures with informative error messages
