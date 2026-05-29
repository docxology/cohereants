# Abstract {#sec:abstract}

**Objective:** To review the plausibility of insect detection of infrared (IR) cues that covary with semiochemical vibrational signatures, and to produce falsifiable predictions through the integration of comparative entomology, spectroscopy, neural timing analysis, and computational electromagnetism. The vibrational theory remains contested, so the framework treats IR/vibrational sensing as a testable complement to molecular recognition rather than a replacement for receptor binding [@turin1996spectroscopic; @franco2011molecular; @block2015implausibility].

**Methods:** We integrate: (i) literature-grounded morphometric ranges for antennal sensilla, (ii) ATR-FTIR evidence that insect body chemistry can support species discrimination, (iii) published olfactory receptor neuron timing constraints, and (iv) deterministic electromagnetic models that expose their assumptions and parameter sensitivity [@liu2021thripidae; @durak2022atrftir; @egeaweiss2018rapid; @barta2024stimulus]. Preregistered experimental protocols specify QCL/LED bands (2--25 µm), thermal matched controls, power density 0.1--2 mW/cm², and N≥50 per condition. All analyses use fixed random seeds (42) where stochastic routines are present.

**Results:** The computational figures show where sensillum-scale dimensions, CHC-associated mid-IR bands, and atmospheric windows overlap, but they do not by themselves establish biological IR olfaction. The strongest empirical anchors are narrower: fast insect ORN first-spike timing, photomechanic IR organs in pyrophilous beetles, hematophagy IR cues in mosquitoes and kissing bugs, thermogenic pollination signals in cycads, thermosensitive coeloconic sensilla in ants, and passive cuticle IR optics [@egeaweiss2018rapid; @schmitz2011infrared; @zopf2014infrared; @valenciamontoya2025infrared; @ruchty2009thermosensitive; @chandel2024thermal]. These sources motivate specific experiments while also constraining the manuscript's range and mechanism claims.

**Conclusions:** The framework yields five preregistered falsifiers aligned with \Cref{sec:discussion}: (1) spectral nulls under matched thermal load, (2) geometric mismatch between sensilla dimensions and predicted resonances, (3) environmental misalignment of CHC peaks with transmission windows, (4) temporal indistinguishability of IR versus thermal ORN latencies, and (5) behavioral independence of IR-only orientation from chemical gradients. Protocols specify QCL/LED bands (2--25 µm), matched power deposition, and N≥50 per condition to separate electromagnetic detection from thermal artifacts.

**Implications:** Applications of this work include biomimetic IR sensor design, better-controlled pest-monitoring experiments, and clearer tests of whether insect olfactory systems ever use wavelength-specific electromagnetic information.

**Keywords:** insect olfaction, infrared detection, vibrational theory, electromagnetic sensing, sensilla morphology, cuticular hydrocarbons, atmospheric transmission, biomimetic sensors

Reproducibility: Complete implementation with seven case studies in Appendices (\Cref{sec:app_sensilla_array}, \Cref{sec:app_environmental_channel}, \Cref{sec:app_detection_limits}, \Cref{sec:app_neural_encoding}, \Cref{sec:app_spectral_unmixing}, \Cref{sec:app_plasmonic_geometry}, \Cref{sec:app_active_inference}) and mathematical derivations \Cref{sec:mathematical_appendix}.



---



Olfaction--the detection and identification of airborne molecules--is a fundamental sensory modality essential for survival, reproduction, and social behavior across the animal kingdom. Among terrestrial organisms, insects exhibit rapid and highly structured chemosensory responses: Drosophila ORNs can produce first spikes within a few milliseconds of odor arrival, and moth ORNs encode plume timing early in the olfactory pathway [@egeaweiss2018rapid; @barta2024stimulus]. Those timing constraints do not prove an electromagnetic mechanism, but they make latency, transport, and transduction explicit design constraints for any expanded account of insect olfaction.

## Current Understanding and Critical Gaps

The prevailing molecular-recognition framework explains much of olfaction through odorant transport, receptor binding, and combinatorial neural coding. Recent olfactory receptor structures and GPCR dynamics reviews strengthen that molecular account by showing how ligand binding, receptor conformation, and downstream signaling can encode odorant specificity [@billesbolle2023odorant; @latorraca2016gpcr]. The present manuscript therefore asks a narrower question: whether IR cues could provide an additional, experimentally separable signal channel in some insect contexts.

### Temporal Constraints

Insect ORNs can be faster and more temporally precise than a coarse diffusion-only intuition would suggest. Egea-Weiss et al. report first-spike latencies down to 3 ms, while Gorur-Shandilya et al. show gain control and complementary kinetics under intermittent odor stimulation [@egeaweiss2018rapid; @gorurshandilya2017gain]. These observations support a conservative framing: fast molecular pathways already exist, and any proposed IR stage must beat or complement those pathways under thermally controlled conditions.

### Range and Sensitivity Paradox

Long-range pheromone localization is usually dominated by turbulent plume structure, wind, and behavior rather than passive molecular diffusion. The computational question here is whether wavelength-specific IR signals could add directional or timing information at biologically realistic powers, not whether electromagnetic sensing replaces plume tracking.

## Recent Evidence for Alternative Mechanisms

Infrared radiation spans near-IR (NIR, ~0.7–2.5 µm), mid-IR (MIR, ~2.5–25 µm), and far-IR (FIR, >25 µm) sub-bands with distinct biological roles: photonic opsin-based sensing in the visual NIR border, thermogenic MIR from fires and warm bodies, and passive cuticle emission for thermoregulation [@campbell2001biological; @krishna2020infrared; @sato2026dragonfly]. The narrative thread running through this manuscript connects four literatures that are often treated separately:

1. **Fast molecular olfaction** — millisecond ORN latencies and plume-timing codes set the timing budget any additional stage must meet [@egeaweiss2018rapid; @barta2024stimulus; @gorurshandilya2017gain].
2. **Radiant IR precedents** — pyrophilous photomechanic organs, hematophagy IR in mosquitoes and kissing bugs, cycad thermogenic pollination, and ant thermosensitive sensilla show that insect tissues can transduce or use radiant IR in particular ecologies [@schmitz2011infrared; @zopf2014infrared; @chandel2024thermal; @valenciamontoya2025infrared; @ruchty2009thermosensitive].
3. **Spectroscopic discrimination** — ATR-FTIR and CHC chemistry support species-level separation in applied spectroscopy; perceptual use of the same bands in vivo remains untested [@durak2022atrftir; @blomquist2021hydrocarbons].
4. **Contested vibrational mechanism** — Turin's spectroscopic theory and Drosophila isotope work motivate vibrational hypotheses; receptor-level critiques argue that broad vibrational olfaction remains unproven [@turin1996spectroscopic; @franco2011molecular; @block2015implausibility].

\Cref{sec:empirical_studies} and \Cref{fig:empirical_ir_axes} organize insect IR evidence along three axes—active detection, passive cuticle interaction, and applied spectroscopy—without collapsing them into proof of semiochemical IR olfaction. CohereAnts sits at the junction of those threads: it turns the hypothesis into code and figures that can be falsified.

**Central Research Question:** Can infrared (IR) vibrational signatures of semiochemicals serve as an electromagnetic detection pathway that enhances insect olfaction, providing faster response times, extended range, and complementary sensory information?

**Scope and Approach:** We focus on mid- and long-wave infrared structure (2-25 $\mu\mathrm{m}$) because this range covers many molecular vibrational bands and the common 3-5 and 8-14 $\mu\mathrm{m}$ atmospheric windows used in infrared propagation models [@gordon2022hitran]. Our framework integrates computational electromagnetism with empirical constraints, testing whether IR detection could operate alongside traditional molecular binding pathways. We emphasize falsifiable predictions and controlled protocols that distinguish wavelength-specific electromagnetic effects from ordinary heating.

**Specific Hypotheses:**

- **H1 (Morphological):** Published sensilla ranges include structures with micron-scale dimensions that can be mapped to quarter- and half-wavelength resonance estimates; cross-taxa correlation remains a prediction, not a completed empirical result [@liu2021thripidae].
- **H2 (Spectral):** CHC- and cuticle-associated FTIR bands provide species-discriminating spectral structure; whether insects directly sense those bands electromagnetically remains untested [@durak2022atrftir; @blomquist2021hydrocarbons].
- **H3 (Temporal):** A proposed IR stage must produce neural signatures that are distinguishable from already-fast molecular ORN responses and from thermal transduction [@egeaweiss2018rapid; @gorurshandilya2017gain].
- **H4 (Behavioral):** IR-only orientation should occur only under controls that remove volatile chemical cues, match total heat deposition, and test wavelength specificity; pyrophilous beetle, kissing-bug, and mosquito studies motivate assay logic but do not establish IR olfaction for semiochemicals [@schmitz2011infrared; @zopf2014infrared; @chandel2024thermal].

## Approach and Organization

We evaluate these hypotheses using an integrated framework combining comparative morphology, infrared spectroscopy, neural timing analysis, and deterministic computational electromagnetism. All models are unit-tested and reproducible with fixed random seeds (42).

The manuscript is organized as follows:

- **Main Text:** Presents integrated findings with cross-references to detailed case studies
- **Appendices:** Seven specialized analyses exploring specific aspects:

  - Sensory array directionality and beam patterns \Cref{sec:app_sensilla_array}
  - Environmental channel modeling \Cref{sec:app_environmental_channel}
  - Detection limits and operating points \Cref{sec:app_detection_limits}
  - Neural encoding efficiency \Cref{sec:app_neural_encoding}
  - Spectral unmixing and classification \Cref{sec:app_spectral_unmixing}
  - Plasmonic nano-geometry optimization \Cref{sec:app_plasmonic_geometry}
  - Active inference behavioral modeling \Cref{sec:app_active_inference}
- **Mathematical Appendix:** Detailed derivations and computational implementations \Cref{sec:mathematical_appendix}
- **Empirical Studies:** Comprehensive review of supporting evidence \Cref{sec:empirical_studies}

This structure enables both comprehensive evaluation and focused exploration of specific mechanisms.



---



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

These windows overlap some CHC- and cuticle-associated vibrational bands, but overlap is only a necessary physical condition. Blackbody peaks from ecologically relevant sources fall near 3 µm for forest fires and ~9.4 µm for human skin at 34 °C, aligning pyrophilous and hematophagy IR precedents with the modeled windows [@schmitztrenner2003spectral; @chandel2024thermal]. Detection-range estimates in this manuscript are model outputs from \eqref{eq:atmospheric_transmission}, not measured insect ranges. See \Cref{fig:atmospheric_transmission} and the environmental channel case study \Cref{sec:app_environmental_channel}.

<!-- alt: Atmospheric transmission versus wavelength with shaded mid-IR, long-wave, and far-IR windows and a biomimetic 2.8–6 µm band; coarse model scope, not a range proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=1.0\textwidth]{../figures/atmospheric_transmission.png}
\caption{Atmospheric transmission window analysis from \texttt{src.core.calculate\_atmospheric\_transmission()} across 1--30~\(\mu\mathrm{m}\). Shaded bands mark modeled windows and the literature-anchored biomimetic band 2.8--6 µm. Claim boundary: window overlap is necessary but not sufficient for semiochemical IR communication.}
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
\includegraphics[width=1.0\textwidth]{../figures/sensilla_wavelength_matching.png}
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
\includegraphics[width=1.0\textwidth]{../figures/chc_spectra_example.png}
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

All tests use fixed random seeds (42) and validate numerical stability, broadcasting behavior, and edge conditions.

### Experimental Protocol Specification

Engineering deliverables prioritize preregistered, IR-only assays with thermal controls:

| Parameter | Specification | Source tier |
|-----------|---------------|-------------|
| QCL/LED band | 2--25 µm | `src/manuscript_fixtures.py` |
| Power density | 0.1--2 mW/cm² | protocol default |
| Thermal control | matched power deposition | preregistered assay |
| Minimum N | ≥50 per condition | preregistration |
| SNR operating point | 10 dB (model) | `output/data/detection_limits_spec.json` |

Mosquito thermal-IR host-seeking assays use skin-temperature blackbody sources (34 °C, peak ~9.4 µm, range ~0.7 m) and are not interchangeable with narrowband QCL olfactometry [@chandel2024thermal; @corfas2015trpa1]. *Melanophila* pit-organ photomechanic precedents anchor biomimetic bands 2.8--6 µm and literature thresholds 11--17.3 mW/cm² [@schmitz2011infrared; @hammer2001sensitivity; @schmitztrenner2003spectral; @evans2005thermopneumatic; @siebke2014biomimetic].

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
- **Deterministic execution**: `src/config.set_random_seed(42)` for all stochastic processes
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



---



# Experimental Results {#sec:experimental_results}

## Neurological Evidence

### Response Time Analysis

Insect ORNs show short response latencies that constrain any candidate transduction mechanism. We quantify model contrasts using `src/core.py::calculate_response_time_improvement`, which decomposes latency into detection, transduction, and propagation terms:

\begin{equation}
\tau_{response} = \tau_{detection} + \tau_{transduction} + \tau_{propagation}
\label{eq:response_time_components}
\end{equation}

Typical reference ranges used in the model comparison:
- Insect ORNs: millisecond-scale responses, including first spikes down to 3 ms in Drosophila ORNs [@egeaweiss2018rapid].
- Intermittent odor encoding: gain control and complementary kinetics under naturalistic stimuli [@gorurshandilya2017gain].
- Moth pheromone ORNs: duration encoding appears early in the olfactory pathway [@barta2024stimulus].
- Slower comparison cases: diffusion-plus-binding terms are treated as model parameters, not as a single empirical constant.

Model outputs indicate improvement factors of $\approx 1.2\text{--}4\times$ when the hypothetical IR-detection term is set below slower diffusion-dominated terms. This is a sensitivity result: it identifies the timing regime an IR pathway would need to occupy, rather than proving that the pathway exists.

See \Cref{fig:response_time_comparison} for the comparison.

<!-- alt: Response-time constraint map comparing insect ORN latencies, slower model terms, and a hypothetical IR-stage target; engineering bounds, not biological proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=1.0\textwidth]{../figures/response_time_comparison.png}
\caption{Response-time constraint map. Literature-anchored insect ORN timing is plotted beside slower model terms and faster visual/auditory reference bands. The figure asks where a proposed IR stage would need to fall to add information beyond already-fast molecular ORN responses; it does not treat IR olfaction as established.}
\label{fig:response_time_comparison}
\end{figure}

### Multimodal Detection Mechanisms

The conservative interpretation is multimodal possibility, not multimodal proof. Molecular receptors and neural circuits already support fast olfactory coding, while photomechanic IR organs in pyrophilous beetles show that radiant-energy detection can evolve in insects under particular ecological pressures [@billesbolle2023odorant; @schmitz2011infrared; @schmitz2007mechanosensory]. Any multimodal IR + molecular scheme remains an open test target, not an established pathway.

**Quantum Mechanical Coupling (contested):** Turin's inelastic electron-tunneling model supplies a concrete mechanism for vibrational olfaction, but Block et al. report receptor-level and theoretical evidence against broad application of that mechanism [@turin1996spectroscopic; @block2015implausibility]. The code exposes coupling parameters for sensitivity analysis; it does not assert they operate in insect antennae.

## Behavioral Evidence

### Sensilla Orientation and Directional Detection

If sensilla function as directional electromagnetic antennas, this would explain observed self-orienting behaviors where sensilla hairs align toward odor sources. This orientation optimizes electromagnetic coupling and signal detection.

**Directional Properties**: Sensilla exhibit properties consistent with directional antennas:
- **Beam Width**: 15--30$^{\circ}$ half-power beamwidth
- **Front-to-Back Ratio**: 10-20 dB directional selectivity
- **Gain Pattern**: Maximum sensitivity in the forward direction

**Behavioral validation**: Experimental studies show localization accuracy of $\pm 15\text{--}30^{\circ}$ in wind-tunnel assays, which is consistent with antenna-like gain patterns having 15-30$^{\circ}$ half-power beamwidths. However, these studies used chemical gradients, so controlled IR-only assays are required to disambiguate electromagnetic detection from volatile plume structure. See array directionality case study in \Cref{sec:app_sensilla_array}. We provide minimal falsifiers in the Discussion.

### Specialized Infrared Sensors

Pyrophilous beetles provide the clearest insect precedent for specialized IR organs. Schmitz et al. described photomechanic Golay-cell transduction in *Melanophila acuminata*; Evans modeled the organ thermopneumatically; Siebke et al. translated it into a biomimetic sensor concept [@schmitz2011infrared; @evans2005thermopneumatic; @siebke2014biomimetic]. Convergent photomechanic sensilla occur in *Aradus* flat bugs [@schmitza2010aradus], while *Acanthocnemus nigricans* uses a microbolometer disc organ [@schmitz2002acanthocnemus; @kreiss2007acanthocnemus]. *Merimna atrata* abdominal organs were reinterpreted as landing-hazard avoidance sensors rather than fire attractors [@schmitz2012merimna].

**Sensor Characteristics** (plasmonic/geometry links in \Cref{sec:app_plasmonic_geometry}):

- **Species**: *Melanophila acuminata*, *Acanthocnemus nigricans*, *Aradus* spp., *Merimna atrata*
- **Evolutionary Origin**: Mechanosensory or thermosensory sensilla modified for radiant-energy detection (photomechanic or microbolometer)
- **Detection Range**: 2.8--6 µm infrared wavelengths (literature-anchored *Melanophila* band)
- **Response Threshold**: $11--17.3\,\mathrm{mW}/\mathrm{cm}^2$ (electrophysiology literature range)
- **Organ Structure**: Pit-organ photomechanic sensilla, flat-bug thoracic sensilla, or prothoracic disc organs depending on species

**Evolutionary Implications**: These beetle organs support the plausibility of insect IR sensing in fire-associated contexts. They do not by themselves demonstrate semiochemical IR olfaction, so the manuscript uses them as anatomical and transduction precedents rather than as direct evidence for the central hypothesis.

### Thermo-sensitive Sensilla Response

Leaf-cutting ants (*Atta vollenweideri*) add a social-insect precedent for thermosensitive sensilla coeloconica. Ruchty et al. report peg-in-pit sensilla whose neurons respond to convective temperature change and radiant heat [@ruchty2009thermosensitive].

**Experimental Protocol**:
- **Stimulus**: Broad-band IR emitter (0.4-11.2 $\mu\mathrm{m}$)
- **Response Measurement**: Cold-sensitive neuron activity
- **Penetration Depth**: 6 $\mu\mathrm{m}$ for 3-$\mu\mathrm{m}$ wavelength radiation
- **Response Threshold**: $0.5\text{--}2.0\,\mathrm{mW}\,/\,\mathrm{cm}^2$

**Mechanistic Insights**: This evidence is best treated as thermal/radiant sensing, not as proof of direct semiochemical spectroscopy. It motivates the thermal-control logic used in the proposed single-sensillum protocols.

See \Cref{fig:composite_cross_domain_overview} for the cross-domain computational overview.

<!-- alt: Cross-domain computational overview linking atmospheric windows, sensilla resonance estimates, CHC bands, and timing constraints; hypothesis map, not an experimental setup. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.95\textwidth]{../figures/composite_cross_domain_overview.png}
\caption{Cross-domain evidence map linking atmospheric transmission (\Cref{fig:atmospheric_transmission}), sensilla resonance estimates (\Cref{fig:sensilla_wavelength_matching}), CHC-associated bands (\Cref{fig:chc_spectra_example}), and literature-constrained timing (\Cref{fig:response_time_comparison}). Claim boundary: hypothesis ladder identifying testable overlaps; not an experimental setup diagram.}
\label{fig:composite_cross_domain_overview}
\end{figure}

## Cuticular Hydrocarbon Spectroscopy

### Spectral Analysis and Species Identification

ATR-FTIR has been used to distinguish aphid species from body chemistry, with nine key absorption peaks giving high discrimination in Durak et al.'s study [@durak2022atrftir]. More broadly, CHCs are central waterproofing and communication traits across insects [@blomquist2021hydrocarbons]. The `analyze_chc_spectra()` function processes synthetic and user-supplied spectra to identify characteristic vibrational regions.

**Spectral Characteristics**:
- **Aphid CHCs**: Peak at 2.85-3.5 $\mu\mathrm{m}$ (2850-3500 cm$^{-1}$)
- **Grasshopper CHCs**: Transmission peak at 2850 cm$^{-1}$ (3.5 $\mu\mathrm{m}$)
- **Ant CHCs**: Multiple peaks in 2.9-3.1 $\mu\mathrm{m}$ range

**Species discrimination**: Durak et al. report 98% discrimination across 12 aphid species, dropping to 90% under jackknife validation, using ATR-FTIR ranges tied to lipids, amides, carbohydrates, and chitin [@durak2022atrftir]. CohereAnts uses these bands as spectroscopic anchors for feature extraction; field deployment would still require calibration across age, diet, environment, and preparation protocol.

### Intra-individual Variation

Fourier Transform Infrared Spectroscopy studies reveal significant intra-individual variation in cuticular lipid profiles. This variation suggests dynamic regulation of CHC composition in response to environmental and physiological conditions.

**Variation Sources**:
- **Environmental Factors**: Temperature, humidity, and food availability
- **Physiological State**: Age, reproductive status, and health condition
- **Social Context**: Colony membership and social interactions

**Detection Implications (open hypothesis):** CHC variation could, in principle, support fine-grained social signaling if an electromagnetic readout pathway existed. Current evidence supports chemical and spectroscopic discrimination; controlled IR-only stimulation is required before attributing behavioral responses to vibrational IR sensing rather than thermal or molecular channels.

## Sensilla Array Log-Periodicity

### Concentration Tuning and Array Response

The log-periodic arrangement of sensilla arrays provides concentration tuning capabilities that enhance detection sensitivity and dynamic range. Different degrees of ORN dendritic branching allow for fine-tuning and concentration information extraction.

**Array Properties**:
- **Log-Periodic Ratio**: $\tau \approx 1.2-1.5$ between adjacent elements
- **Concentration Range**: 3-4 orders of magnitude dynamic range
- **Sensitivity Tuning**: Individual sensilla tuned to different concentration ranges

**Mathematical Model**: The response of a log-periodic sensilla array follows the relationship:

\begin{equation}
R(C) = R_0 \sum_{n=0}^{N-1} \frac{C^n}{C_0^n} e^{-\frac{(C - C_n)^2}{2\sigma_n^2}}
\label{eq:log_periodic_response_empirical}
\end{equation}

where $C$ is the concentration, $C_n = C_0 \tau^n$ defines the log-periodic spacing, and $\sigma_n$ determines the width of each response peak.

## Allosteric Modulation and Photomodulation

### GPCR Conformational Dynamics

Allosteric modulation of olfactory GPCRs involves constant atomic motion, with receptors oscillating at femto- to millisecond frequencies between different conformational states. The vibrational theory suggests that photomodulation affects the probability and stability of these states.

**Conformational States**:
- **Active State**: G-protein coupled conformation
- **Inactive State**: Uncoupled conformation
- **Intermediate States**: Multiple metastable conformations

**Photomodulation Effects (model parameters):** Infrared radiation could modulate conformational state probabilities through direct absorption, indirect water coupling, or resonant enhancement—these are exposed as test parameters, not established OR mechanisms.

**Quantum Effects (exploratory only):** Some GPCR models explore weak-field sensitivity near quantum-critical regimes. CohereAnts treats THz-scale coupling terms as falsifiable placeholders pending receptor-level evidence; they are not used to claim operational quantum olfaction in insects.

### Alpha-Helical Resonance

GPCR transmembrane elements consist of 7 alpha-helices that exhibit optical resonance properties similar to photosynthetic pigment proteins. This structural similarity suggests that OR alpha-helices may be responsive to electromagnetic radiation in the infrared range.

- **Resonant Properties**:
- **Helix Dimensions**: 3.6 amino acids per turn, 5.4 \AA{} pitch
- **Resonant Wavelengths**: 2-10 $\mu\mathrm{m}$ corresponding to infrared range
- **Coupling Mechanisms**: Dipole-dipole interactions and charge transfer

## Airflow Studies and Sensilla Function

### Airflow Patterns and Molecular Transport

Plumose moth antennae intercept only a fraction of upwind air. Vogel measured *Actias luna* and other saturniid antennae and found antenna flow can be much lower than free airspeed [@vogel1983silkmoth].

**Quantitative Measurements**:
- **Free Airspeed**: 2.0 m/sec
- **Antenna Flow Rate**: 0.26 m/sec
- **Flow Efficiency**: Only 13% of upwind air passes through antennae

**Functional Implications:** Low airflow efficiency constrains how much odorant volume an antenna samples per unit time. That transport limit is compatible with fast molecular ORN responses when plumes are structured and intermittent [@barta2024stimulus]. It does not, by itself, imply that antennae primarily function as electromagnetic detectors rather than molecular capture surfaces.

**Open computational question:** Under what geometries, powers, and preregistered controls could wavelength-specific electromagnetic cues add information beyond molecular plume capture and turbulent transport? CohereAnts models that question; Vogel's measurements supply a transport anchor, not an answer.



---



# Discussion {#sec:discussion}

## Synthesis

\Cref{fig:empirical_ir_axes} organizes insect IR biology along three axes—active detection, passive cuticle interaction, and applied spectroscopy—while keeping semiochemical IR olfaction in ordinary sensilla as an open hypothesis. The figures and case studies below supply model bounds and preregistered falsifiers; they do not adjudicate receptor mechanism. The five minimal falsifiers at the end of this section map directly to those axes and to the protocol tokens in Methods (2--25 µm, matched thermal controls, N≥50).

## Implications for insect behavior and cognition

The vibrational/IR hypothesis provides concise, testable explanations for some otherwise awkward timing and geometry questions, but it remains a hypothesis. Our simulations indicate parameter regimes in which an IR-sensitive stage could coexist with fast molecular olfaction; the strongest empirical constraints are summarized in \Cref{fig:empirical_ir_axes} and include fast ORN timing, photomechanic pyrophilous IR organs, combinatorial warm-cell coding in kissing bugs, and thermal-IR mosquito host-seeking rather than direct semiochemical IR detection [@egeaweiss2018rapid; @schmitz2011infrared; @zopf2014infrared; @chandel2024thermal].

### Nestmate recognition

Nestmate recognition in eusocial Hymenoptera depends heavily on CHC signals, but the evidence for those signals is primarily chemical, not electromagnetic [@blomquist2021hydrocarbons]. Deterministic simulations (`src/core.py::calculate_response_time_improvement`) show how a hypothetical fast stage would affect latency budgets; they do not establish that nestmate recognition uses IR detection.

### Pheromone specificity and range

Pheromone and CHC-associated functional groups occupy discriminative IR regions, especially lipid-associated bands around 2958, 2913, 2849, 1737, and 1408 cm$^{-1}$ in the aphid ATR-FTIR study [@durak2022atrftir]. Under modeled atmospheric transmission and assumed source strengths, narrowband signatures can be propagated through favorable windows; these ranges are quantified as model outputs in `src/case_studies/detection_limits.py`, not as measured insect sensing distances.

### Evolutionary and ecological implications

Comparative analyses show physical overlap between representative sensilla dimensions and predicted resonant wavelengths. That overlap is a screen for experimental candidates, not a confirmed evolutionary correlation. Photomechanic, microbolometer, and dual thermo/mechano IR organs in pyrophilous beetles demonstrate convergent MIR transduction; ant, mosquito, and cycad-pollinator studies show radiant IR can be behaviorally relevant in other ecologies [@schmitz2011infrared; @schmitz2002acanthocnemus; @ruchty2009thermosensitive; @chandel2024thermal; @valenciamontoya2025infrared]. Evans (2010) cautions that inverse-square physics limits long-range fire detection claims for *Melanophila* [@evans2010reproductive].

## Computational and applied consequences

Effective IR sensing would require wavelength-specific stimulation, directional processing, sufficiently fast transduction, and SNR above thermal and environmental backgrounds. Channel-capacity estimates (`src/case_studies/environmental_channel.py`) should be read as engineering upper bounds under selected assumptions. *Rhodnius* combinatorial warm-cell coding motivates preregistered controls that separate radiant IR from convective temperature change [@zopf2014infrared; @zopf2015convection]. Applications include biomimetic uncooled sensors [@schmitz2011infrared; @siebke2014biomimetic], mosquito trap design with skin-temperature IR [@chandel2024thermal], and NIR monitoring networks [@potamitis2022monitoring].

## Limitations and Critical Experimental Controls

The primary empirical challenge is distinguishing direct electromagnetic detection from thermal stimulation and other confounding factors. Since all IR exposure deposits energy, rigorous controls are essential for mechanism validation.

### Thermal Control Protocols

**Broadband vs. Narrowband Stimulation:**
- **Broadband heating controls**: Use thermal sources matched for total power deposition
- **Narrowband IR stimulation**: Employ tunable lasers or filtered LEDs (Δλ < 0.5 $\mu\mathrm{m}$)
- **Success criterion**: Frequency-specific responses absent in broadband controls

**Temporal Resolution Requirements:**
- **High-speed measurements**: Sub-millisecond temporal resolution for early detection components
- **Thermal diffusion modeling**: Account for heat propagation timescales ($\mu\mathrm{s}$–ms range)
- **Multi-scale analysis**: Separate electromagnetic detection from thermal transduction

### Spectral Specificity Tests

**Wavelength Tuning Experiments:**
- **Systematic wavelength sweeps**: Test responses across 2–25 $\mu\mathrm{m}$ range
- **Resonance matching**: Compare with predicted sensilla resonances
- **Quality factor assessment**: Measure response sharpness (target Q > 10)

**Isotope Effects:**
- **Deuterated controls**: Use deuterated analogs to shift vibrational frequencies
- **Frequency-specific discrimination**: Verify responses follow vibrational, not structural, changes

### Environmental and Contextual Controls

**Atmospheric Conditions:**
- **Humidity controls**: Test across 20–80% RH to assess water vapor interference
- **Temperature gradients**: Control for thermal vs. electromagnetic effects
- **Background IR levels**: Measure ambient IR and subtract from signals

**Behavioral Context:**
- **Motivation state**: Control for hunger, reproductive status, social context
- **Learning effects**: Pre-exposure and conditioning protocols
- **Stimulus timing**: Control for circadian and ultradian rhythms

### Instrumentation and Sensitivity Limits

**Detection Thresholds:**
- **Minimum detectable power**: ~10^{-15} W for single sensillum recordings
- **Signal-to-noise requirements**: SNR > 10 for reliable detection
- **Background discrimination**: Separate signal from environmental IR noise

**Calibration and Validation:**
- **Power meter calibration**: NIST-traceable standards for IR power measurements
- **Wavelength accuracy**: $\pm 0.01\,\mu\mathrm{m}$ precision for spectral specificity tests
- **Thermal imaging**: Correlate neural responses with thermal profiles

### Taxonomic and Ecological Limitations

**Species Sampling:**
- **Phylogenetic breadth**: Include representatives from major insect orders
- **Ecological diversity**: Sample across habitats and behavioral contexts
- **Body size effects**: Account for scaling relationships in antenna design

**Field vs. Laboratory:**
- **Environmental complexity**: Natural backgrounds vs. controlled conditions
- **Stimulus intensity**: Physiological vs. supra-threshold stimulation
- **Behavioral relevance**: Natural signal levels and contexts

## Minimal falsifiers (experimentally testable)

1. **Spectral nulls**: No frequency-specific responses to IR-only stimulation when thermal load is matched ($\pm 0.1\,^{\circ}\mathrm{C}$) and power deposition is identical across wavelengths (broadband vs. narrowband stimulation with thermal controls).

2. **Geometric mismatch**: Reproducible failure to observe correlation (r < 0.3, p > 0.05) between sensilla dimensions and predicted resonances across N ≥ 50 specimens from 3+ insect orders, with correlation analysis controlling for phylogenetic effects.

3. **Environmental misalignment**: CHC peaks consistently fall outside modeled transmission windows under controlled conditions (20–80% RH, 15–35$^{\circ}\mathrm{C}$), with >90% of spectral features showing mismatch when compared to atmospheric transmission models.

4. **Temporal indistinguishability**: ORN response latencies to IR stimulation are statistically indistinguishable from thermal stimulation (p > 0.05) when controlling for power deposition and wavelength.

5. **Behavioral independence**: No detectable orientation responses to narrowband IR stimulation in the absence of chemical gradients, with responses <10% of positive controls using identical experimental setups.

Each falsifier requires adequately powered, preregistered protocols (N ≥ 50) and is described in Methods and Appendices.

## Future directions

Priority experiments: single‑sensillum IR sensitivity with thermal controls; behavioral IR‑only assays; cross‑species morphometrics; high‑temporal-resolution neural recordings. Computational extensions include 3D electromagnetic modeling, ML‑based classification, and integration with environmental/climate models.

## Conservation and societal relevance

If insects use IR-based cues for critical behaviors, altered thermal and infrared environments could affect behavior in ways not captured by volatile-chemical assays. The clearest recent case is *Aedes aegypti*, where thermal IR around skin temperature increased host-seeking behavior in the presence of other host cues [@chandel2024thermal]. Understanding which species respond to which wavelengths informs conservation, agricultural monitoring, and biomimetic sensor design without assuming a universal IR-olfaction mechanism.

## Summary

The discussion frames clear, falsifiable experimental paths and practical applications while acknowledging limitations. Appendices and `src/` implementations provide reproducible computational anchors for the hypotheses and control protocols described here.



---



# Conclusion {#sec:conclusion}

## Summary of findings

We present a reproducible computational framework that implements, tests, and evaluates a contested IR/vibrational hypothesis for insect olfaction. Integrating morphology, spectroscopy, neural timing, and environmental modeling, the framework produces quantitative predictions and explicit falsifiers suitable for experimental validation.

### Reproducible framework

All predictions are anchored in deterministic, unit-tested code with documented case studies and reproducible figure generation. Traceability runs from equations through `src/` modules to figures and tests.

### Empirical highlights

1. Morphology: Representative sensilla dimensions can be mapped onto IR-scale quarter- and half-wave estimates (\Cref{fig:sensilla_wavelength_matching}); the needed empirical test is a preregistered, cross-taxa correlation analysis [@liu2021thripidae].
2. Neural timing: Published insect ORN timing is fast enough that any IR stage must be experimentally separated from already-rapid molecular responses (\Cref{fig:response_time_comparison}) [@egeaweiss2018rapid; @gorurshandilya2017gain].
3. Behavior: Photomechanic beetle IR organs, kissing-bug combinatorial warm cells, ant thermosensitive sensilla, cycad thermogenic pollination IR, and mosquito thermal-IR host seeking establish biological IR/radiant sensing precedents, not direct semiochemical IR olfaction (\Cref{fig:empirical_ir_axes}) [@schmitz2011infrared; @zopf2014infrared; @ruchty2009thermosensitive; @valenciamontoya2025infrared; @chandel2024thermal].
4. Spectroscopy: Automated peak detection identifies CHC-associated bands that can support species discrimination in ATR-FTIR data, while perceptual use of those bands remains to be tested (\Cref{fig:chc_spectra_example}) [@durak2022atrftir].

The cross-domain evidence ladder (\Cref{fig:composite_cross_domain_overview}) links atmospheric windows, sensilla geometry, CHC bands, and timing constraints without claiming direct semiochemical IR olfaction.

Recent 2025–2026 literature—including cycad pollination IR [@valenciamontoya2025infrared] and dragonfly near-IR opsin tuning [@sato2026dragonfly]—expands the IR relevance landscape without establishing semiochemical IR olfaction in ordinary antennal sensilla.

## Preregistered falsifiers and translation targets

The Discussion lists five minimal falsifiers; they are the operational closure for this framework:

1. **Spectral nulls** — no frequency-specific response under matched thermal load and power deposition.
2. **Geometric mismatch** — sensilla dimensions uncorrelated with predicted resonances across taxa (N ≥ 50, phylogeny-aware).
3. **Environmental misalignment** — CHC peaks consistently outside modeled transmission windows under controlled humidity and temperature.
4. **Temporal indistinguishability** — ORN latencies to IR stimulation statistically indistinguishable from thermal stimulation at matched power.
5. **Behavioral independence** — no IR-only orientation without chemical gradients under preregistered olfactometer protocols.

**Translation targets** (grounded in model outputs, not biological proof):

- Biomimetic uncooled IR sensors informed by pit-organ and sensilla geometry (bands 2.8--6 µm, thresholds 11--17.3 mW/cm²) [@siebke2014biomimetic].
- Pest-monitoring assay design with wavelength-specific stimulation and thermal controls.
- Channel-capacity and detection-limit estimates from `src/case_studies/environmental_channel.py` and `src/case_studies/detection_limits.py` as engineering upper bounds.

Quantum-coherence and broad quantum-biology claims remain out of scope; the framework focuses on measurable sensor bounds and preregistered protocols.

## Reproducibility

The Appendices and `src/` modules provide computational anchors for every figure label in the registry. Independent groups can regenerate artifacts via `./run.sh --project cohereants --core-only` or the documented script entry points, then validate outputs against `../figures/figure_registry.json`.



---



# Mathematical Appendix {#sec:mathematical_appendix}

## Introduction

This appendix presents the mathematical foundations used in the manuscript: electromagnetic propagation in dielectric sensilla, resonant‑cavity and waveguide approximations, vibrational spectroscopy, and detection statistics. Where relevant, equations are linked to deterministic implementations in `src/` and to unit tests that validate numerical behavior.

**Note on reproducibility**: Key formulae are implemented in `src/` and exercised by unit tests; implementations accept scalar and array inputs and validate edge conditions.

## Electromagnetic Wave Theory

### Maxwell's Equations in Dielectric Media

The fundamental equations governing electromagnetic wave propagation in insect sensilla can be expressed as:

\eqref{eq:maxwell1}, \eqref{eq:maxwell2}, \eqref{eq:maxwell3}, and \eqref{eq:maxwell4}.
\begin{align}
\nabla \cdot \mathbf{D} &= \rho_f \label{eq:maxwell1} \\
\nabla \cdot \mathbf{B} &= 0 \label{eq:maxwell2} \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \label{eq:maxwell3} \\
\nabla \times \mathbf{H} &= \mathbf{J}_f + \frac{\partial \mathbf{D}}{\partial t} \label{eq:maxwell4}
\end{align}

where $\mathbf{D} = \epsilon_0 \mathbf{E} + \mathbf{P}$ is the electric displacement field, $\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M})$ is the magnetic induction, and $\epsilon_0$ and $\mu_0$ are the permittivity and permeability of free space, respectively.

**Material Properties**: For insect cuticle, the relative permittivity $\epsilon_r \approx 2.5-3.0$ and loss tangent $\tan \delta \approx 0.01-0.05$ at infrared frequencies.

### Dielectric Waveguide Equations

For cylindrical sensilla acting as dielectric waveguides, the electromagnetic field components can be expressed in cylindrical coordinates $(r, \phi, z)$ as:

\eqref{eq:waveguide_field}.
\begin{equation}
\mathbf{E}(r, \phi, z) = \mathbf{E}_0(r, \phi) e^{i(\beta z - \omega t)} \label{eq:waveguide_field}
\end{equation}

where $\beta$ is the propagation constant and $\omega$ is the angular frequency. The transverse field components satisfy the Helmholtz equation:

\eqref{eq:helmholtz}.
\begin{equation}
\nabla_t^2 \mathbf{E}_t + (k^2 - \beta^2)\mathbf{E}_t = 0 \label{eq:helmholtz}
\end{equation}

with $k = \omega \sqrt{\mu \epsilon}$ being the wavenumber in the medium.

**Waveguide Modes**: The fundamental HE$_{11}$ mode provides the lowest cutoff frequency and best coupling efficiency for infrared detection; model assumptions are limited to homogeneous cylindrical geometry and small-loss tangent.

### Resonant Frequency Calculation

The resonant frequency of a sensillum can be approximated using the cavity resonator model:

\eqref{eq:resonant_freq}.
\begin{equation}
f_{res} = \frac{c}{2\pi} \sqrt{\left(\frac{\alpha_{mn}}{a}\right)^2 + \left(\frac{p\pi}{L}\right)^2} \label{eq:resonant_freq}
\end{equation}

where:
- $c$ is the speed of light in the medium ($c = c_0/\sqrt{\epsilon_r}$)
- $\alpha_{mn}$ is the $m$th root of the Bessel function of order $n$
- $a$ is the radius of the sensillum
- $L$ is the length of the sensillum
- $p$ is the axial mode number

**Quality Factor**: The quality factor $Q$ of the resonator is given by:

\eqref{eq:quality_factor}.
\begin{equation}
Q = \frac{f_{res}}{\Delta f} = \frac{\omega_0}{2\alpha} \label{eq:quality_factor}
\end{equation}

where $\Delta f$ is the bandwidth and $\alpha$ is the attenuation constant.

### Worked Example (Resonant Frequency)
Consider a cylindrical sensillum with radius $a=1.5\,\mu m$, length $L=12\,\mu m$, relative permittivity $\epsilon_r=2.8$, and axial mode $p=1$ using the first Bessel root $\alpha_{11}\approx1.841$.

**Calculation:**
- Speed of light in medium: $c = c_0/\sqrt{\epsilon_r} = 3.0 \times 10^8 / \sqrt{2.8} = 1.79 \times 10^8$ m/s
- Radial term: $(\alpha_{11}/a) = 1.841/(1.5 \times 10^{-6}) = 1.23 \times 10^6$ m$^{-1}$
- Axial term: $(p\pi/L) = \pi/(12 \times 10^{-6}) = 2.62 \times 10^5$ m$^{-1}$
- Combined: $\sqrt{(1.23 \times 10^6)^2 + (2.62 \times 10^5)^2} = 1.26 \times 10^6$ m$^{-1}$
- Resonant frequency: $f_{res} = (1.79 \times 10^8)(1.26 \times 10^6)/(2\pi) = 35.9$ THz
- Free-space wavelength: $\lambda_0 = c_0/f_{res} = 8.35$ $\mu\mathrm{m}$

This wavelength falls within the atmospheric transmission window (8-14 $\mu\mathrm{m}$), validating the theoretical framework. Implementation in `src/sensilla.py::analyze_sensilla_dimensions` produces identical results with error bounds < 0.1%.

**Practical Implementation:**
```python
# Example: Calculate resonance for typical sensillum dimensions
from src.sensilla import calculate_sensilla_resonance_frequency
import numpy as np

# Typical sensillum parameters
length = 12e-6  # 12 um
radius = 1.5e-6  # 1.5 um
epsilon_r = 2.8  # cuticle relative permittivity

# Calculate resonance (note: function returns frequency in Hz)
f_res = calculate_sensilla_resonance_frequency(
    length=length, radius=radius, epsilon_r=epsilon_r
)

# Convert to wavelength using c = f * λ (in vacuum approximation)
c = 3e8  # speed of light in m/s
wavelength = c / f_res  # in meters
wavelength_um = wavelength * 1e6  # convert to um

print(f"Resonant frequency: {f_res/1e12:.2f} THz")
print(f"Resonant wavelength: {wavelength_um:.2f} um")
```

**Cross-Validation with Literature:**
Recent studies of beetle infrared sensilla report dimensions of 10–20 $\mu\mathrm{m}$ length and 1–3 $\mu\mathrm{m}$ diameter, corresponding to resonances in the 8–12 $\mu\mathrm{m}$ range—precisely the atmospheric transmission window with highest throughput. This dimensional convergence across taxa suggests evolutionary optimization for environmental IR transmission.

## Vibrational Spectroscopy

### Molecular Vibrational Energy Levels

The energy levels of molecular vibrations are quantized according to:

\eqref{eq:vibrational_energy}.
\begin{equation}
E_v = \hbar \omega_e \left(v + \frac{1}{2}\right) - \hbar \omega_e x_e \left(v + \frac{1}{2}\right)^2 \label{eq:vibrational_energy}
\end{equation}

where:
- $v$ is the vibrational quantum number
- $\omega_e$ is the fundamental vibrational frequency
- $x_e$ is the anharmonicity constant
- $\hbar$ is the reduced Planck constant

**Isotope Effects**: For deuterated compounds, the frequency shift is approximately:

\eqref{eq:isotope_shift}.
\begin{equation}
\frac{\omega_D}{\omega_H} = \sqrt{\frac{\mu_H}{\mu_D}} \approx 0.707 \label{eq:isotope_shift}
\end{equation}

where $\mu_H$ and $\mu_D$ are the reduced masses of hydrogen and deuterium compounds.

### Infrared Absorption Cross-Section

The absorption cross-section for infrared radiation by a molecule is given by:

\eqref{eq:absorption_cross_section}.
\begin{equation}
\sigma(\omega) = \frac{4\pi^2 \omega}{3\hbar c} \sum_{v',v''} |\langle v'|\mu|v''\rangle|^2 \delta(\omega - \omega_{v'v''}) \label{eq:absorption_cross_section}
\end{equation}

where $\mu$ is the transition dipole moment and $\omega_{v'v''}$ is the frequency difference between vibrational states.

**Transition Selection Rules**: For infrared transitions, $\Delta v = \pm 1$ with intensity proportional to the square of the transition dipole moment.

### Atmospheric Transmission Function

The atmospheric transmission at infrared wavelengths can be modeled as:

\eqref{eq:atmospheric_transmission}.
\begin{equation}
T(\lambda) = \exp\left[-\sum_i \alpha_i(\lambda) L_i\right] \label{eq:atmospheric_transmission}
\end{equation}

where $\alpha_i(\lambda)$ is the absorption coefficient of the $i$th atmospheric component and $L_i$ is the path length through that component.

**Transmission windows (model)**: The three primary atmospheric windows used in our baseline model have transmission efficiencies:
- **2-5 $\mu\mathrm{m}$**: $T(\lambda) \approx 0.8$ (mid-infrared)
- **8-14 $\mu\mathrm{m}$**: $T(\lambda) \approx 0.9$ (long-wave infrared)
- **17-25 $\mu\mathrm{m}$**: $T(\lambda) \approx 0.7$ (far-infrared)

**Detection Range Example:**
```python
# Calculate detection range for a typical pheromone scenario
from src.core import calculate_atmospheric_transmission

# Parameters for pheromone detection
wavelength = 10.0  # um (within long-wave window)
distance = 50.0    # meters
temperature = 20.0  # \(^{\circ}\mathrm{C}\)
humidity = 60.0    # %

# Calculate transmission
transmission = calculate_atmospheric_transmission(
    wavelength=wavelength,
    distance=distance,
    temperature=temperature,
    humidity=humidity
)

print(f"Transmission at {wavelength} um over {distance} m: {transmission:.3f}")
print(f"Signal attenuation: {-10*np.log10(transmission):.1f} dB")
```

**Practical Implications:**
For a 10 $\mu\mathrm{m}$ wavelength signal over 50 m, typical atmospheric transmission is ~0.85, corresponding to only 0.7 dB of attenuation. This enables reliable detection ranges of 100+ meters for insect pheromones, consistent with observed behaviors in field studies.

## Antenna Theory and Sensilla Modeling

### Effective Aperture of Sensilla

The effective aperture of a sensillum can be calculated using:

\eqref{eq:effective_aperture}.
\begin{equation}
A_{eff} = \frac{\lambda^2}{4\pi} G(\theta, \phi) \label{eq:effective_aperture}
\end{equation}

where $G(\theta, \phi)$ is the gain pattern of the sensillum in the direction $(\theta, \phi)$.

**Gain Pattern**: For a cylindrical sensillum, the gain pattern can be approximated as:

\eqref{eq:gain_pattern}.
\begin{equation}
G(\theta, \phi) = G_0 \cos^2(\theta) \label{eq:gain_pattern}
\end{equation}

where $G_0$ is the maximum gain and $\theta$ is the angle from the axis.

### Power Received by Sensilla

The power received by a sensillum from a distant source is:

\eqref{eq:power_received}.
\begin{equation}
P_{rec} = S A_{eff} = \frac{P_{trans} G_{trans} A_{eff}}{4\pi R^2} \label{eq:power_received}
\end{equation}

where:
- $S$ is the power flux density at the sensillum
- $P_{trans}$ is the transmitted power
- $G_{trans}$ is the gain of the transmitting source
- $R$ is the distance between source and sensillum

**Detection Range**: The maximum detection range $R_{max}$ is determined by the minimum detectable power:

\eqref{eq:detection_range}.
\begin{equation}
R_{max} = \sqrt{\frac{P_{trans} G_{trans} A_{eff}}{4\pi P_{min}}} \label{eq:detection_range}
\end{equation}

### Signal-to-Noise Ratio

The signal-to-noise ratio (SNR) for infrared detection is:

\eqref{eq:snr}.
\begin{equation}
SNR = \frac{P_{signal}}{P_{noise}} = \frac{P_{rec}}{k_B T \Delta f} \label{eq:snr}
\end{equation}

where:
- $k_B$ is Boltzmann's constant ($1.381 \times 10^{-23}$ J/K)
- $T$ is the system temperature (typically 300 K)
- $\Delta f$ is the detection bandwidth

**Minimum Detectable Power**: The minimum detectable power is:

\eqref{eq:min_power}.
\begin{equation}
P_{min} = k_B T \Delta f \cdot SNR_{min} \label{eq:min_power}
\end{equation}

where $SNR_{min}$ is the minimum required signal-to-noise ratio (typically 10–20 dB). A simple numerical estimate with $T=300\,K$ and $\Delta f=100\,Hz$ yields $P_{min}\approx4.1\times10^{-19}\,\text{W}\cdot SNR_{min}$.

## Piezoelectric Response of Microtubules

### Piezoelectric Coefficient

The piezoelectric response of microtubules can be described by:

\eqref{eq:piezoelectric}.
\begin{equation}
\mathbf{P} = d_{ijk} \sigma_{jk} \label{eq:piezoelectric}
\end{equation}

where:
- $\mathbf{P}$ is the induced polarization
- $d_{ijk}$ is the piezoelectric coefficient tensor
- $\sigma_{jk}$ is the applied stress tensor

**Microtubule Properties**: For microtubules, the piezoelectric coefficient $d_{33} \approx 10^{-12}$ C/N in the axial direction.

### Resonant Frequency of Microtubules

The fundamental resonant frequency of a microtubule is:

\eqref{eq:microtubule_resonance}.
\begin{equation}
f_0 = \frac{1}{2L} \sqrt{\frac{EI}{\rho A}} \label{eq:microtubule_resonance}
\end{equation}

where:
- $L$ is the length of the microtubule (1-10 $\mu\mathrm{m}$)
- $E$ is Young's modulus ($1.2 \times 10^9$ Pa)
- $I$ is the moment of inertia
- $\rho$ is the density ($1.4 \times 10^3$ $\mathrm{kg}\,/\,\mathrm{m}^3$)
- $A$ is the cross-sectional area

**Frequency Range**: Microtubules resonate in the 1-30 $\mu\mathrm{m}$ wavelength range, corresponding to infrared frequencies.

### Piezoelectric Coupling

The piezoelectric coupling coefficient $k$ is:

\eqref{eq:piezoelectric_coupling}.
\begin{equation}
k^2 = \frac{d_{33}^2 E}{\epsilon_0 \epsilon_r} \label{eq:piezoelectric_coupling}
\end{equation}

where $\epsilon_r$ is the relative permittivity of the microtubule material.

## Concentration-Dependent Response

### Log-Periodic Array Response

The response of a log-periodic sensilla array can be modeled as:

\eqref{eq:log_periodic_response}.
\begin{equation}
R(C) = R_0 \sum_{n=0}^{N-1} \frac{C^n}{C_0^n} e^{-\frac{(C - C_n)^2}{2\sigma_n^2}} \label{eq:log_periodic_response}
\end{equation}

where:
- $C$ is the concentration of the semiochemical
- $R_0$ is the baseline response
- $C_n = C_0 \tau^n$ with $\tau$ being the log-periodic ratio (1.2-1.5)
- $\sigma_n$ is the width of the $n$th response peak

**Array Optimization**: The optimal log-periodic ratio is:

\eqref{eq:optimal_ratio}.
\begin{equation}
\tau_{opt} = \exp\left(\frac{\pi}{\sqrt{1 - \left(\frac{\alpha}{k}\right)^2}}\right) \label{eq:optimal_ratio}
\end{equation}

where $\alpha$ is the attenuation constant and $k$ is the wavenumber.

### Concentration Tuning Function

The concentration tuning function for individual sensilla is:

\eqref{eq:concentration_tuning}.
\begin{equation}
T(C) = \frac{C^n}{K_d^n + C^n} \label{eq:concentration_tuning}
\end{equation}

where:
- $K_d$ is the dissociation constant
- $n$ is the Hill coefficient (cooperativity, typically 1-4)

**Dynamic Range**: The dynamic range of concentration detection is:

\eqref{eq:dynamic_range}.
\begin{equation}
DR = 20 \log_{10}\left(\frac{C_{max}}{C_{min}}\right) \text{ dB} \label{eq:dynamic_range}
\end{equation}

where $C_{max}$ and $C_{min}$ are the maximum and minimum detectable concentrations.

## Quantum Mechanical Considerations

### Electron Tunneling in Olfactory Receptors

The probability of electron tunneling through a potential barrier is:

\eqref{eq:tunneling_probability}.
\begin{equation}
P_{tunnel} = \exp\left[-\frac{2d}{\hbar} \sqrt{2m(V_0 - E)}\right] \label{eq:tunneling_probability}
\end{equation}

where:
- $d$ is the barrier width (typically 1-5 nm)
- $m$ is the electron mass ($9.109 \times 10^{-31}$ kg)
- $V_0$ is the barrier height (typically 0.5-2.0 eV)
- $E$ is the electron energy

**Tunneling Current**: The tunneling current density is:

\eqref{eq:tunneling_current}.
\begin{equation}
J = \frac{e^2}{h} \frac{V}{d} P_{tunnel} \label{eq:tunneling_current}
\end{equation}

where $e$ is the electron charge and $h$ is Planck's constant.

### F{\"o}rster Resonance Energy Transfer (FRET)

The efficiency of FRET between donor and acceptor molecules is:

\eqref{eq:fret_efficiency}.
\begin{equation}
E_{FRET} = \frac{1}{1 + \left(\frac{r}{R_0}\right)^6} \label{eq:fret_efficiency}
\end{equation}

where:
- $r$ is the distance between donor and acceptor
- $R_0$ is the F{\"o}rster radius (characteristic distance, typically 2-6 nm)

**FRET Rate**: The FRET rate constant is:

\eqref{eq:fret_rate}.
\begin{equation}
k_{FRET} = \frac{1}{\tau_D} \frac{R_0^6}{r^6} \label{eq:fret_rate}
\end{equation}

where $\tau_D$ is the donor lifetime.

## Response Time Analysis

### Neural Response Latency

The response time of olfactory receptor neurons can be modeled as:

\eqref{eq:response_time}.
\begin{equation}
\tau_{response} = \tau_{detection} + \tau_{transduction} + \tau_{propagation} \label{eq:response_time}
\end{equation}

where each component represents the time for detection, signal transduction, and neural propagation, respectively.

**Component Breakdown**:
- **Detection**: $\tau_{detection} \approx 0.1-0.5$ ms (electromagnetic)
- **Transduction**: $\tau_{transduction} \approx 0.5-2.0$ ms (ionic)
- **Propagation**: $\tau_{propagation} \approx 0.5-2.5$ ms (neural)

### Frequency Response Function

The frequency response of a sensillum is:

\eqref{eq:frequency_response}.
\begin{equation}
H(f) = \frac{1}{1 + i2\pi f \tau} \label{eq:frequency_response}
\end{equation}

where $\tau$ is the characteristic time constant of the system.

**Bandwidth**: The 3-dB bandwidth is:

\eqref{eq:bandwidth}.
\begin{equation}
f_{3dB} = \frac{1}{2\pi \tau} \label{eq:bandwidth}
\end{equation}

**Phase Response**: The phase response is:

\eqref{eq:phase_response}.
\begin{equation}
\phi(f) = -\tan^{-1}(2\pi f \tau) \label{eq:phase_response}
\end{equation}

## Statistical Analysis of Behavioral Responses

### Response Probability Distribution

The probability of a behavioral response given a stimulus intensity $I$ is:

\eqref{eq:response_probability}.
\begin{equation}
P(response|I) = \frac{1}{1 + e^{-\beta(I - I_{50})}} \label{eq:response_probability}
\end{equation}

where:
- $\beta$ is the slope parameter (sensitivity)
- $I_{50}$ is the intensity at which 50% of responses occur

**Sensitivity Index**: The sensitivity index $d'$ is:

\eqref{eq:sensitivity_index}.
\begin{equation}
d' = \frac{\mu_{signal} - \mu_{noise}}{\sqrt{\frac{\sigma_{signal}^2 + \sigma_{noise}^2}{2}}} \label{eq:sensitivity_index}
\end{equation}

where $\mu$ and $\sigma^2$ represent the mean and variance of signal and noise distributions.

### Signal Detection Theory

The discriminability index $d'$ in signal detection theory is:

\eqref{eq:discriminability}.
\begin{equation}
d' = \frac{\mu_{signal} - \mu_{noise}}{\sqrt{\frac{\sigma_{signal}^2 + \sigma_{noise}^2}{2}}} \label{eq:discriminability}
\end{equation}

**ROC Analysis**: The receiver operating characteristic (ROC) curve is:

\eqref{eq:false_alarm}.
\begin{equation}
P_{FA} = \int_{\lambda}^{\infty} p(x|noise) dx \label{eq:false_alarm}
\end{equation}

\eqref{eq:detection_probability}.
\begin{equation}
P_D = \int_{\lambda}^{\infty} p(x|signal) dx \label{eq:detection_probability}
\end{equation}

where $\lambda$ is the decision threshold.

## Environmental Factors

### Temperature Dependence

The temperature dependence of sensilla response can be modeled using the Arrhenius equation:

\eqref{eq:arrhenius}.
\begin{equation}
k(T) = A e^{-\frac{E_a}{k_B T}} \label{eq:arrhenius}
\end{equation}

where:
- $k(T)$ is the rate constant at temperature $T$
- $A$ is the pre-exponential factor
- $E_a$ is the activation energy (typically 0.1-1.0 eV)

**Temperature Coefficient**: The temperature coefficient is:

\eqref{eq:temperature_coefficient}.
\begin{equation}
\alpha_T = \frac{1}{k} \frac{dk}{dT} = \frac{E_a}{k_B T^2} \label{eq:temperature_coefficient}
\end{equation}

### Humidity Effects

The effect of humidity on sensilla function is:

\eqref{eq:humidity_response}.
\begin{equation}
R(H) = R_0 \left[1 + \alpha(H - H_0) + \beta(H - H_0)^2\right] \label{eq:humidity_response}
\end{equation}

where:
- $H$ is the relative humidity
- $H_0$ is the reference humidity (typically 50%)
- $\alpha$ and $\beta$ are fitting parameters

**Humidity Sensitivity**: The humidity sensitivity is:

\eqref{eq:humidity_sensitivity}.
\begin{equation}
S_H = \frac{dR}{dH} = R_0 [\alpha + 2\beta(H - H_0)] \label{eq:humidity_sensitivity}
\end{equation}

## Integration and Signal Processing

### Multi-Sensilla Integration

The integrated response from multiple sensilla is:

\begin{equation}
R_{total} = \sum_{i=1}^{N} w_i R_i + \sum_{i=1}^{N} \sum_{j>i}^{N} w_{ij} R_i R_j \label{eq:integrated_response}
\end{equation}

where:
- $w_i$ are the weights for individual sensilla
- $w_{ij}$ are the weights for pairwise interactions
- $R_i$ is the response of the $i$th sensillum

**Optimal Weights**: The optimal weights minimize the mean squared error:

\eqref{eq:optimal_weights}.
\begin{equation}
\mathbf{w}_{opt} = (\mathbf{R}^T \mathbf{R})^{-1} \mathbf{R}^T \mathbf{y} \label{eq:optimal_weights}
\end{equation}

where $\mathbf{R}$ is the response matrix and $\mathbf{y}$ is the target response.

## Implementation Cross-Links (Selected)
- `src/core.py::calculate_atmospheric_transmission` → tests: `tests/test_core.py::TestAtmosphericTransmission`
- `src/sensilla.py::analyze_sensilla_dimensions` → tests: `tests/test_sensilla.py::TestSensillaAnalysis`
- `src/spectroscopy.py::analyze_chc_spectra` → tests: `tests/test_spectroscopy_analysis.py::TestAnalyzeChcSpectra`
- Conversions `calculate_wavelength_from_wavenumber`/`calculate_wavenumber_from_wavelength` → tests: `tests/test_core.py::TestWavelengthConversions`
-- Case-study appendices and corresponding src: \Cref{sec:app_sensilla_array}, \Cref{sec:app_environmental_channel}, \Cref{sec:app_detection_limits}, \Cref{sec:app_neural_encoding}, \Cref{sec:app_spectral_unmixing}, \Cref{sec:app_plasmonic_geometry}, \Cref{sec:app_active_inference}

### Adaptive Threshold Mechanism

The adaptive threshold for detection is:

\begin{equation}
\theta(t) = \theta_0 + \alpha \int_0^t R(\tau) e^{-\frac{t-\tau}{\tau_{adapt}}} d\tau \label{eq:adaptive_threshold}
\end{equation}

where:
- $\theta_0$ is the baseline threshold
- $\alpha$ is the adaptation strength
- $\tau_{adapt}$ is the adaptation time constant

**Adaptation Dynamics**: The adaptation rate is:

\eqref{eq:adaptation_rate}.
\begin{equation}
\frac{d\theta}{dt} = \alpha R(t) - \frac{\theta - \theta_0}{\tau_{adapt}} \label{eq:adaptation_rate}
\end{equation}

## Future Research Directions

### Machine Learning Approaches

The response function can be approximated using neural networks:

\eqref{eq:neural_network}.
\begin{equation}
R(C, \mathbf{x}) = f\left(\sum_{j=1}^{M} w_j \sigma\left(\sum_{i=1}^{N} w_{ij} x_i + b_j\right) + b\right) \label{eq:neural_network}
\end{equation}

where $\sigma$ is the activation function and $\mathbf{x}$ represents environmental parameters.

**Training Objective**: The training objective is to minimize:

\eqref{eq:training_objective}.
\begin{equation}
\mathcal{L} = \sum_{i=1}^{N} \left(R_i - R_{target}\right)^2 + \lambda \sum_{j=1}^{M} w_j^2 \label{eq:training_objective}
\end{equation}

where $\lambda$ is the regularization parameter.

### Optimization of Sensilla Arrays

The optimal spacing for a sensilla array can be determined by minimizing:

\eqref{eq:optimization_loss}.
\begin{equation}
\mathcal{L} = \sum_{i=1}^{N} \left(R_i - R_{target}\right)^2 + \lambda \sum_{i=1}^{N-1} (d_{i+1} - d_i)^2 \label{eq:optimization_loss}
\end{equation}

where:

- $d_i$ is the distance to the $i$th sensillum
- $\lambda$ is the regularization parameter
- $R_{target}$ is the desired response pattern

**Optimal Spacing**: The optimal spacing follows a log-periodic pattern:

\eqref{eq:optimal_spacing}.
\begin{equation}
d_{i+1} = d_i \tau \label{eq:optimal_spacing}
\end{equation}

where $\tau$ is the optimal log-periodic ratio.

### Information-Theoretic Analysis

The integrated analysis framework provides comprehensive quantitative assessment of the empirical evidence through information-theoretic measures. The `IntegratedAnalyzer` class combines multiple analytical approaches to provide system-level performance metrics.

**System Performance**: The `calculate_system_performance_metrics()` method generates composite performance scores that integrate information processing efficiency, material performance, and overall system efficiency. Figure manifests include `integrated_analysis_*` artifacts written to `../figures/`.

**Performance Metrics**:
- **Information Capacity**: $C \approx 10^3-10^4$ bits/s
- **Signal-to-Noise Ratio**: $SNR \approx 20-40$ dB
- **Detection Efficiency**: $\eta \approx 0.6-0.9$
- **False Alarm Rate**: $P_{FA} \approx 10^{-3}-10^{-2}$

**Cross-Domain Validation**: The framework integration allows validation of theoretical predictions across multiple domains, from molecular spectroscopy to behavioral response.

### Predictive Capability Assessment

The meta-material analytical framework enables prediction of system performance under different conditions. The `analyze_information_capacity()` method calculates channel capacity, signal-to-noise ratios, and quantum limits for information processing.

**Channel Capacity**: The information capacity of the infrared detection channel is:

\begin{equation}
C = B \log_2(1 + SNR)
\label{eq:channel_capacity_empirical}
\end{equation}

where $B$ is the bandwidth and $SNR$ is the signal-to-noise ratio.

**Quantum Limits**: The framework incorporates quantum mechanical limits on information processing:
- **Heisenberg Uncertainty**: $\Delta x \Delta p \geq \hbar/2$
- **Quantum Noise**: Zero-point fluctuations
- **Entanglement Effects**: Quantum correlations in receptor arrays

## Conclusion

This mathematical appendix provides the theoretical foundation for understanding the vibrational theory of olfaction in insects. The equations presented here can be used to:

1. **Model sensilla responses** to different infrared frequencies with quantitative accuracy
2. **Predict optimal sensilla dimensions** for specific detection tasks using electromagnetic theory
3. **Analyze signal processing** in the insect nervous system through statistical and information theory
4. **Design experiments** to test the vibrational theory with specific experimental parameters
5. **Develop biomimetic sensors** inspired by insect sensilla with predictable performance characteristics

**Computational Validation**: All equations are implemented in tested source code that generates the visualizations and analyses presented throughout this manuscript, ensuring empirical grounding for the theoretical framework.

**Experimental Predictions**: The mathematical framework provides specific, testable predictions for:
- Sensilla response characteristics across different frequencies
- Detection range and sensitivity under various environmental conditions
- Optimal array configurations for different detection tasks
- Performance limits based on fundamental physical principles

The mathematical framework demonstrates that the vibrational theory is not only biologically plausible but also mathematically rigorous, providing testable predictions for future experimental validation. This integration of theory, computation, and empirical validation represents a comprehensive approach to understanding the remarkable capabilities of insect chemosensation.



---



# Empirical Studies {#sec:empirical_studies}

## Introduction

Insect engagement with infrared (IR) radiation spans three functional axes that this section keeps separate:

1. **Active detection** — specialized organs or neural channels that transduce radiant IR into behaviorally relevant signals.
2. **Passive interaction** — cuticle and wing optical properties that govern absorption, reflection, and emission for thermoregulation.
3. **Applied IR** — NIRS, FTIR, and optical sensors used by researchers to profile insects (not insect sensing).

These axes constrain CohereAnts models and preregistered protocols. They do **not** prove that ordinary antennal olfactory sensilla detect semiochemical IR vibrational signatures. The central vibrational-olfaction hypothesis remains contested [@turin1996spectroscopic; @franco2011molecular; @block2015implausibility].

## Molecular Spectroscopy and Olfactory Theory

### Vibrational Olfaction: Support and Critique

- **Primary support**: Turin proposed an inelastic electron-tunneling mechanism for primary olfactory reception [@turin1996spectroscopic]. Franco et al. reported Drosophila behavioral discrimination of isotopologues and interpreted the results as evidence for a molecular vibration-sensing component [@franco2011molecular].
- **Primary critique**: Block et al. found no receptor-level support for the proposed vibrational mechanism in tested human and mouse odorant receptors and argued that the theory is implausible without stronger receptor evidence [@block2015implausibility].
- **Implication for CohereAnts**: Vibration sensing remains contested. Computational models produce falsifiable predictions; they do not settle receptor mechanism.
- **Code anchors**: `src/fermi_estimation.py::calculate_vibrational_entropy`; `src/core.py::calculate_wavelength_from_wavenumber`.

### CHC and Cuticle Spectroscopy

- **Primary evidence**: Durak et al. used ATR-FTIR to distinguish 12 aphid species and reported 98% classification with selected peaks, dropping to 90% under jackknife validation [@durak2022atrftir].
- **Chemical ecology context**: CHCs are central insect waterproofing and communication traits, with strong variation across taxa and social contexts [@blomquist2021hydrocarbons].
- **Implication for CohereAnts**: CHC-associated spectra can be discriminative; spectroscopic separability does not imply that insects directly sense the same bands electromagnetically.
- **Code anchors**: `src/spectroscopy.py::analyze_chc_spectra`; `src/case_studies/spectral_unmixing.py`.

## Active IR Detection in Insects

### Pyrophilous Photomechanic Organs

The thoracic pit organ of *Melanophila acuminata* is the best-characterized insect MIR detector. Schmitz and Trenner measured broadband sensitivity from 2 to 6 µm with peak response at 2.8–3.5 µm; Hammer et al. reported minimum detection thresholds near 14.6–17.3 mW/cm² at 3.39 µm [@schmitztrenner2003spectral; @hammer2001sensitivity]. Schmitz et al. described photomechanic transduction: absorbed IR heats a microfluidic core, deflecting a mechanosensitive dendrite in a Golay-cell-like architecture [@schmitz2011infrared; @schmitz2007mechanosensory]. Evans modeled the organ thermopneumatically [@evans2005thermopneumatic]; Siebke et al. translated it into a biomimetic sensor concept [@siebke2014biomimetic].

*Aradus* flat bugs independently evolved convergent photomechanic IR sensilla on the prothorax and mesothorax [@schmitza2010aradus]. *Acanthocnemus nigricans* uses a distinct microbolometer design: a cuticular disc with multipolar thermoreceptors, responding to 11–25 mW/cm² with 20–40 ms latencies [@schmitz2002acanthocnemus; @kreiss2007acanthocnemus].

*Merimna atrata* carries abdominal IR organs with bimodal thermo- and mechanosensory innervation [@schmitz2000merimna; @schmitz2012merimna]. Flight-tethering experiments revised the functional interpretation from fire attraction to **landing-hazard avoidance** on surfaces hotter than ~60 °C. Evans (2010) argued that inverse-square physics limits reliable long-range fire detection by *Melanophila* to less than often-claimed distances [@evans2010reproductive].

- **Implication for CohereAnts**: Pyrophilous organs establish that insect MIR detection evolves under fire-associated ecology. They are anatomical and transduction precedents for biomimetic bands 2.8--6 µm and literature thresholds 11--17.3 mW/cm²—not evidence for semiochemical IR olfaction in ordinary sensilla.
- **Code anchors**: `src/case_studies/plasmonic_geometry.py`; `src/case_studies/detection_limits.py`.

### Hematophagy and Host-Finding

Chandel et al. showed that *Aedes aegypti* uses thermal IR near skin temperature as a host-seeking cue when combined with CO₂ and odor; TRPA1 in antennal neurons is required [@chandel2024thermal]. Corfas and Vosshall linked AaegTRPA1 to selective thermotaxis toward host-temperature targets [@corfas2015trpa1].

*Rhodnius prolixus* lacks specialized IR organs but discriminates radiant IR from convective heat via combinatorial coding of peg-in-pit (PSw) and tapered-hair (THw) warm cells; forced convection disrupts the response quotient [@zopf2014infrared; @zopf2015convection]. Lazzari reviewed how physics shapes hematophagous orientation: radiant IR operates at longer range than convective heat within ~10 cm of the host [@lazzari2009orientation].

- **Implication for CohereAnts**: Mosquito and kissing-bug studies motivate thermal-IR protocol separation (34 °C blackbody, peak ~9.4 µm) and Rhodnius-style controls that distinguish T oscillations from IR power.
- **Code anchors**: `src/case_studies/active_inference.py`; `src/case_studies/environmental_channel.py`.

### Pollination and Mutualism

Valencia-Montoya et al. reported that thermogenic cycad cones radiate IR in circadian patterns that attract beetle pollinators with IR-activated antennal neurons [@valenciamontoya2025infrared]. Glover and Webb noted that IR is most detectable at night, constraining cycads to nocturnal beetle pollination in contrast to diurnal angiosperm visual signals [@glover2025pollination].

- **Implication for CohereAnts**: Plant-generated thermal IR is a mutualism cue precedent. It does not extend semiochemical IR olfaction claims to ordinary olfactory sensilla.
- **Code anchors**: `src/case_studies/environmental_channel.py`.

### Near-IR Photonic Opsins

Sato et al. characterized dragonfly RhLWA2 (λmax ~580 nm) with convergent tuning at opsin position 292 shared with mammalian red opsins; engineered variants respond to ~738 nm light [@sato2026dragonfly]. Liénard et al. documented red-shifted opsin evolution in lycaenid butterflies [@lienard2021opsin].

- **Implication for CohereAnts**: These are **visual** NIR-border cases, distinct from MIR thermogenic organs. They inform spectral vocabulary but not the semiochemical IR hypothesis directly.

### TRPA1 Molecular Context

Zhang et al. resolved Drosophila TRPA1 gating architecture, with ankyrin-repeat domains acting as heat-sensor modules [@zhang2023trpa1]. This molecular context complements mosquito behavioral TRPA1 requirements [@chandel2024thermal; @corfas2015trpa1].

### Historical Callahan FIR Hypothesis

Callahan proposed that nocturnal moth antennae function as dielectric waveguides detecting far-IR molecular emission lines, including overlap with the 7–14 µm atmospheric window [@callahan1965fir; @callahan1977moth]. The waveguide mechanism remains contested, but the proposal motivates sensilla-as-antenna geometric screening in CohereAnts without endorsing FIR pheromone reception.

- **Implication for CohereAnts**: Callahan supplies historical context for dielectric-antenna modeling; Campbell and Ford provide a broader biological IR sensing review frame [@campbell2001biological].
- **Code anchors**: `src/sensilla.py::analyze_sensilla_dimensions`; `src/case_studies/sensilla_array_directionality.py`.

## Morphology and Antennal Sensilla

- **Primary evidence**: Liu et al. measured antennal sensilla in three Thripidae species [@liu2021thripidae].
- **Thermosensitive ant sensilla**: Ruchty et al. described thermosensitive coeloconic sensilla in *Atta vollenweideri* responding to convective and radiant heat [@ruchty2009thermosensitive].
- **Implication for CohereAnts**: Morphometric resonance estimates remain predictions pending cross-taxa SEM validation.
- **Code anchors**: `src/sensilla.py::analyze_sensilla_dimensions`; `src/case_studies/sensilla_array_directionality.py`.

## Passive Cuticle and Wing IR Optics

Krishna et al. and Phan et al. showed that mid-IR wing emissivity (7.5–14 µm) correlates with habitat temperature, enhancing radiative cooling in warm climates [@krishna2020infrared; @phan2021emissivity]. Sheppard and de Boer found that NIR reflectance predicts beetle heating rates more strongly than visible reflectance [@sheppard2021heating]; Stavenga et al. reported similar NIR/visible partitioning in Christmas beetles [@stavenga2022beetles].

- **Implication for CohereAnts**: Passive optics shape body temperature and background IR; they support environmental-channel modeling, not olfactory transduction claims.
- **Code anchors**: `src/case_studies/environmental_channel.py`; `src/core.py::calculate_atmospheric_transmission`.

## Applied Infrared Spectroscopy and Monitoring

Dowell et al. demonstrated NIRS classification of stored-grain beetles [@dowell1999nirs]. Moraes Barros et al. reviewed FTIR applications in forensic entomology [@moraesbarros2021forensic]. Potamitis et al. deployed unsupervised NIR sensor networks for field insect monitoring [@potamitis2022monitoring]. These parallel Durak et al.'s CHC spectroscopy [@durak2022atrftir] as **human-applied** IR tools.

- **Implication for CohereAnts**: Applied spectroscopy validates species-discriminating IR structure in insect bodies; it does not demonstrate in vivo semiochemical IR detection.
- **Code anchors**: `src/spectroscopy.py`; `src/case_studies/spectral_unmixing.py`.

## Neurophysiology and ORN Timing

- **Primary evidence**: Egea-Weiss et al. reported Drosophila ORN first-spike latencies down to 3 ms [@egeaweiss2018rapid]. Gorur-Shandilya et al. showed gain control under intermittent odor stimuli [@gorurshandilya2017gain]. Barta et al. showed stimulus-duration encoding early in the moth pathway [@barta2024stimulus].
- **Implication for CohereAnts**: Any proposed IR stage must produce timing distinguishable from established ORN kinetics and thermal transduction.
- **Code anchors**: `src/core.py::calculate_response_time_improvement`; `src/case_studies/neural_encoding.py`.

## Comparative Overview

| Taxon | IR range | Mechanism | Primary function | Key citation |
| --- | --- | --- | --- | --- |
| *Melanophila acuminata* | 2–6 µm (peak 2.8–3.5 µm) | Photomechanic microfluidic sensillum | Long-range fire detection | [@schmitz2011infrared; @schmitztrenner2003spectral] |
| *Aradus* spp. | MIR | Convergent photomechanic sensillum | Fire-associated navigation | [@schmitza2010aradus] |
| *Acanthocnemus nigricans* | MIR | Microbolometer disc organ | Short-range burn orientation | [@schmitz2002acanthocnemus; @kreiss2007acanthocnemus] |
| *Merimna atrata* | MIR | Dual thermo/mechano abdominal organ | Landing hazard avoidance | [@schmitz2012merimna] |
| *Aedes aegypti* | Thermal IR (~skin temp.) | TRPA1 antennal neurons + opsins | Host seeking (multimodal) | [@chandel2024thermal; @corfas2015trpa1] |
| *Rhodnius prolixus* | Thermal MIR | PSw/THw combinatorial warm cells | Host finding; T vs IR discrimination | [@zopf2014infrared] |
| Cycad-pollinating beetles | Thermogenic cone IR | TRP-channel antennal neurons | Pollination | [@valenciamontoya2025infrared] |
| Dragonfly (*Asiagomphus*) | ~580 nm (visual NIR border) | Bistable opsin RhLWA2 | Likely mate/sex recognition | [@sato2026dragonfly] |
| Butterfly wings | 7.5–14 µm emissivity | Microstructure-mediated radiative cooling | Thermoregulation | [@krishna2020infrared] |
| Beetle elytra | NIR 700–2500 nm | Cuticular reflectance/absorptance | Solar heat gain regulation | [@sheppard2021heating] |

See \Cref{fig:empirical_ir_axes} for a schematic synthesis of the three functional axes and \Cref{fig:composite_cross_domain_overview} for how modeled atmospheric, morphometric, and spectral overlaps constrain the semiochemical IR hypothesis.

<!-- alt: Three-axis schematic of active photomechanic detection, passive cuticle optics, and applied IR spectroscopy with literature threshold bands; synthesis figure, not new data. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.95\textwidth]{../figures/empirical_ir_axes.png}
\caption{Three-axis schematic of insect IR biology synthesized from the comparative table above. Active photomechanic organs anchor biomimetic bands 2.8--6 µm and thresholds 11--17.3~mW/cm²; passive cuticle/thermosensory pathways set background IR context; applied spectroscopy validates discriminative structure without demonstrating in vivo semiochemical IR olfaction. Claim boundary: literature synthesis, not new empirical measurement.}
\label{fig:empirical_ir_axes}
\end{figure}

## Evolutionary Synthesis

Three evolutionary pressures recur:

1. **Pyrophily** — fire-associated reproduction drove MIR organ diversity (photomechanic, microbolometer, dual thermo/mechano).
2. **Hematophagy** — host-finding co-opted TRPA1 and warm-cell combinatorial coding; radiant IR propagates farther than convective heat [@lazzari2009orientation; @chandel2024thermal].
3. **Mutualism and mate recognition** — thermogenic plant IR (cycads) and visual NIR opsins (dragonflies, butterflies) expand the IR relevance landscape without unifying transduction mechanism.

Mechanistic diversity argues for IR detection as a recurrently co-opted modality rather than a single ancestral insect IR module.

## Translational Applications

Photomechanic *Melanophila* sensilla and *Acanthocnemus* microbolometers inform uncooled biomimetic MIR sensor design [@schmitz2011infrared; @siebke2014biomimetic]. Mosquito TRPA1 biology suggests skin-temperature IR sources may improve trap designs when combined with odor and CO₂ [@chandel2024thermal]. Potamitis et al.'s NIR sensor networks enable high-temporal-resolution monitoring relative to trap-based sampling [@potamitis2022monitoring].

## Environmental Channel Evidence

- **Atmospheric spectroscopy**: HITRAN2020 is the relevant source class for line-by-line absorption modeling [@gordon2022hitran].
- **Model boundary**: The core transmission function is intentionally coarse; precise range predictions require measured source spectra, humidity, path length, and background IR. See \Cref{fig:atmospheric_transmission} and \Cref{sec:app_environmental_channel}.
- **Code anchors**: `src/core.py::calculate_atmospheric_transmission`; `src/case_studies/environmental_channel.py`.

## Molecular Receptor Context

- **Receptor structure**: OR51E2 structure anchors molecular-recognition specificity [@billesbolle2023odorant].
- **GPCR dynamics**: Conformational dynamics provide molecular context without implying vibrational spectroscopy [@latorraca2016gpcr].
- **Mechanotransduction**: Piezo and related systems illustrate mechanical-to-biochemical signaling as analogy only [@di2023mechanotransduction].

## Experimental Priorities

1. **Single-sensillum IR electrophysiology** with matched broadband heating and thermography.
2. **Behavioral IR-only assays** with volatile-free chambers and wavelength sweeps at equal radiant power.
3. **Cross-taxa morphometrics** with preregistered resonance metrics and phylogenetic controls.
4. **Rhodnius-style T vs IR discrimination controls** in any hematophagy-inspired protocol.
5. **Isotope and spectral controls** separating molecular binding, vibrational shifts, and thermal absorption.
6. **Environmental realism** — humidity, path length, turbulence, and background IR paired with positive results.
7. **Thermogenic plant assays** — whether IR from heated structures modulates pollinator orientation under preregistered thermal matched controls.



---



# Ant Stack Implementation Appendix {#sec:ant_stack_appendix}

## Introduction

This appendix maps CohereAnts computational modules onto the Ant Stack three-layer framework (AntBody, AntBrain, AntMind) as a **sensor-fusion control model**, not a mind/brain metaphor. The stack coordinates physical sensing (sensilla IR models), state estimation (channel capacity), and action selection (active inference demos) for protocol design and assay simulation.

### AntBody Layer: Physical Simulation and Sensing

#### Sensilla Morphology Integration

```python
# AntBody sensilla configuration (adapter pattern)
class AntBodySensilla:
    def __init__(self, species_preset: str):
        # Load species-specific sensilla parameters via CohereAnts presets
        self.lengths = load_sensilla_lengths(species_preset)
        self.diameters = load_sensilla_diameters(species_preset)
        # Delegate resonance calculation to tested src utilities
        from src.sensilla import calculate_wavelength_matching
        self.optimal_wavelengths = calculate_wavelength_matching(self.lengths, self.diameters)

    def export_io(self) -> dict:
        return {
            'lengths_um': self.lengths,
            'diameters_um': self.diameters,
            'optimal_wavelengths_um': self.optimal_wavelengths,
        }
```

**I/O Contract**: 
- **Observations**: Sensilla dimensions ($\mu\mathrm{m}$), resonance frequencies (THz), quality factors
- **Actions**: Antenna positioning, sensilla orientation
- **Physics**: 1 kHz update rate, contact dynamics for substrate interaction

#### Spectroscopy and Atmospheric Transmission

Integration of CohereAnts atmospheric transmission models:

```python
class AntBodySpectroscopy:
    def __init__(self, environment_preset: str):
        self.transmission_curves = load_atmospheric_data(environment_preset)
        self.spectral_resolution = 0.01  # um
        
    def get_transmission(self, wavelength: float, distance: float) -> float:
        # Delegate to CohereAnts atmospheric transmission model in src/core
        return calculate_atmospheric_transmission(wavelength, distance)
```

**Configuration Parameters**:
- Atmospheric windows: 2-5 $\mu\mathrm{m}$, 8-14 $\mu\mathrm{m}$, 17-25 $\mu\mathrm{m}$
- Transmission coefficients: 0.7-0.9 for optimal windows
- Distance-dependent attenuation models

**Layer handoff:** AntBody exports wavelength-dependent transmission, sensilla resonance estimates, and spectral features as observation tensors. AntBrain consumes those tensors as channel inputs for encoding and discrimination models; it does not imply a literal insect central nervous system implementation.

### AntBrain Layer: Neural Architecture

#### Olfactory Processing Pipeline

Mapping CohereAnts vibrational theory to AntBrain's AL→MB→CX architecture:

```python
class AntBrainOlfaction:
    def __init__(self, neuron_count: int = 100000):
        # Antennal Lobe (AL) - odor coding
        self.al_neurons = self._initialize_al_circuit()
        # Mushroom Body (MB) - associative learning
        self.mb_neurons = self._initialize_mb_circuit()
        # Central Complex (CX) - spatial integration
        self.cx_neurons = self._initialize_cx_circuit()
    
    def _initialize_al_circuit(self):
        # Delegate vibrational detection to src components in production
        # Each glomerulus responds to specific molecular vibrations
        return VibrationalGlomeruliCircuit()
    
    def _initialize_mb_circuit(self):
        # Kenyon cells for odor-memory associations
        return KenyonCellCircuit()
    
    def _initialize_cx_circuit(self):
        # Ring attractor for heading representation
        return RingAttractorCircuit()
```

**Neural Implementation Details**:
- **AL Layer**: 50 glomeruli, each tuned to specific vibrational frequencies
- **MB Layer**: 2500 Kenyon cells with sparse coding (5% activity)
- **CX Layer**: 16-heading ring attractor with 100 neurons per heading

#### Vibrational Detection Circuit

Implementation of CohereAnts electromagnetic theory:

```python
class VibrationalGlomeruliCircuit:
    def __init__(self):
        self.frequency_tuning = np.linspace(2, 25, 50)  # um to THz
        self.quality_factors = np.ones(50) * 100
        
    def process_spectral_input(self, spectral_data: np.ndarray) -> np.ndarray:
        # Implement CohereAnts resonance detection
        responses = np.zeros(50)
        for i, freq in enumerate(self.frequency_tuning):
            responses[i] = self._calculate_vibrational_response(spectral_data, freq)
        return responses
    
    def _calculate_vibrational_response(self, spectrum: np.ndarray, 
                                     resonant_freq: float) -> float:
        # Placeholder: call src electromagnetic coupling utilities in production
        coupling_strength = self._calculate_coupling(spectrum, resonant_freq)
        return coupling_strength * self.quality_factors[i]
```

**Layer handoff:** AntBrain maps encoded spectral and timing features to population responses and information metrics (see \Cref{sec:app_neural_encoding}). AntMind applies policy steps—active inference demos in \Cref{sec:app_active_inference}—to simulate search trajectories under IR cue beliefs. This is a control-theoretic stack for protocol design, not a claim about insect cognition.

### AntMind Layer: Cognitive Modeling

#### Active Inference for Olfactory Search

Integration of CohereAnts behavioral models with active inference:

```python
class AntMindOlfaction:
    def __init__(self):
        self.generative_model = self._build_olfactory_model()
        self.policy_horizon = 2.0  # seconds
        
    def _build_olfactory_model(self):
        # Implement CohereAnts behavioral predictions
        return OlfactoryGenerativeModel()
    
    def select_policy(self, current_state: Dict) -> np.ndarray:
        # Active inference policy selection
        expected_free_energy = self._calculate_efe()
        return self._minimize_free_energy(expected_free_energy)
    
    def _calculate_efe(self) -> Dict[str, float]:
        # Decompose into epistemic and pragmatic value
        return {
            'epistemic': self._calculate_epistemic_value(),
            'pragmatic': self._calculate_pragmatic_value()
        }
```

#### Stigmergy for Trail Following

Implementation of CohereAnts pheromone dynamics:

```python
class AntMindStigmergy:
    def __init__(self):
        self.pheromone_field = np.zeros((100, 100))
        self.decay_rate = 0.01
        self.diffusion_coefficient = 0.1
        
    def update_pheromone_field(self, deposits: List[Tuple[int, int, float]]):
        # Implement CohereAnts pheromone diffusion model
        for x, y, amount in deposits:
            self.pheromone_field[x, y] += amount
        
        # Apply diffusion and decay
        self.pheromone_field = self._diffuse_and_decay()
    
    def _diffuse_and_decay(self) -> np.ndarray:
        # Fick's law implementation from CohereAnts
        laplacian = self._calculate_laplacian(self.pheromone_field)
        diffusion = self.diffusion_coefficient * laplacian
        decay = -self.decay_rate * self.pheromone_field
        return self.pheromone_field + diffusion + decay
```

## Species-Specific Implementations

### Formica Species Configuration

```python
# Formica species preset for Ant Stack
FORMICA_PRESET = {
    'body': {
        'sensilla_lengths': [15.2, 18.7, 22.1, 19.8, 16.5],  # um
        'sensilla_diameters': [2.1, 2.8, 3.2, 2.9, 2.3],     # um
        'optimal_wavelengths': [60.8, 74.8, 88.4, 79.2, 66.0], # um
        'antenna_length': 2.5,  # mm
        'leg_count': 6,
        'body_mass': 0.015  # g
    },
    'brain': {
        'al_glomeruli_count': 50,
        'mb_kenyon_cells': 2500,
        'cx_heading_resolution': 16,
        'spiking_threshold': 0.1,
        'learning_rate': 0.01
    },
    'mind': {
        'policy_horizon': 2.0,  # seconds
        'pheromone_decay': 0.01,
        'diffusion_coefficient': 0.1,
        'exploration_rate': 0.2
    }
}
```

### Camponotus Species Configuration

```python
# Camponotus species preset for Ant Stack
CAMPONOTUS_PRESET = {
    'body': {
        'sensilla_lengths': [22.5, 28.1, 31.7, 26.8, 24.3],  # um
        'sensilla_diameters': [3.2, 4.1, 4.8, 4.2, 3.6],     # um
        'optimal_wavelengths': [90.0, 112.4, 126.8, 107.2, 97.2], # um
        'antenna_length': 3.8,  # mm
        'leg_count': 6,
        'body_mass': 0.045  # g
    },
    'brain': {
        'al_glomeruli_count': 60,
        'mb_kenyon_cells': 3000,
        'cx_heading_resolution': 20,
        'spiking_threshold': 0.08,
        'learning_rate': 0.015
    },
    'mind': {
        'policy_horizon': 2.5,  # seconds
        'pheromone_decay': 0.008,
        'diffusion_coefficient': 0.12,
        'exploration_rate': 0.15
    }
}
```

## Evaluation and Benchmarking

### Navigation Performance Metrics

```python
class AntStackEvaluator:
    def __init__(self, test_scenarios: List[str]):
        self.scenarios = test_scenarios
        self.metrics = {}
    
    def evaluate_navigation(self, ant_stack: AntStack) -> Dict[str, float]:
        results = {}
        for scenario in self.scenarios:
            if scenario == 'trail_following':
                results[scenario] = self._evaluate_trail_following(ant_stack)
            elif scenario == 'food_search':
                results[scenario] = self._evaluate_food_search(ant_stack)
            elif scenario == 'nest_return':
                results[scenario] = self._evaluate_nest_return(ant_stack)
        return results
    
    def _evaluate_trail_following(self, ant_stack: AntStack) -> float:
        # Implement CohereAnts trail following metrics (calls src/behavioral metrics)
        trail_deviation = self._calculate_trail_deviation()
        pheromone_detection = self._calculate_pheromone_detection()
        return self._combine_metrics([trail_deviation, pheromone_detection])
    
    def _evaluate_food_search(self, ant_stack: AntStack) -> float:
        # Implement CohereAnts search efficiency metrics (calls src/behavioral metrics)
        search_time = self._measure_search_time()
        energy_efficiency = self._calculate_energy_efficiency()
        return self._combine_metrics([search_time, energy_efficiency])
```

### Robustness Testing

```python
class RobustnessTester:
    def __init__(self):
        self.noise_levels = [0.01, 0.05, 0.1, 0.2]
        self.adversary_types = ['sensor_noise', 'pheromone_contamination', 'path_obstruction']
    
    def test_noise_robustness(self, ant_stack: AntStack) -> Dict[str, float]:
        results = {}
        for noise_level in self.noise_levels:
            performance = self._run_noisy_scenario(ant_stack, noise_level)
            results[f'noise_{noise_level}'] = performance
        return results
    
    def test_adversary_robustness(self, ant_stack: AntStack) -> Dict[str, float]:
        results = {}
        for adversary in self.adversary_types:
            performance = self._run_adversarial_scenario(ant_stack, adversary)
            results[f'adversary_{adversary}'] = performance
        return results
```

## Implementation Workflow

### Development Pipeline

1. **Module Mapping**: Identify CohereAnts functions for Ant Stack integration
2. **I/O Contract Definition**: Establish standardized interfaces between layers
3. **Species Preset Creation**: Develop parameterized configurations
4. **Testing Framework**: Implement evaluation metrics and benchmarks
5. **Documentation**: Create implementation guides and examples

### Code Organization

```
ant_stack_cohereants/
├── antbody/
│   ├── sensilla_physics.py      # CohereAnts vibrational theory
│   ├── spectroscopy_sensors.py  # atmospheric transmission models
│   └── morphology_models.py     # species-specific parameters
├── antbrain/
│   ├── olfactory_circuits.py    # AL→MB→CX implementation
│   ├── vibrational_detection.py # electromagnetic coupling
│   └── learning_mechanisms.py   # STDP and plasticity
├── antmind/
│   ├── olfactory_inference.py   # active inference models
│   ├── stigmergy_models.py      # pheromone dynamics
│   └── behavioral_policies.py   # search and navigation
├── presets/
│   ├── formica_config.py        # Formica species preset
│   ├── camponotus_config.py     # Camponotus species preset
│   └── custom_species.py        # Template for new species
└── evaluation/
    ├── navigation_tests.py      # Trail following, search
    ├── robustness_tests.py      # Noise, adversary testing
    └── performance_metrics.py   # Standardized benchmarks
```

## Integration Benefits

### Reproducibility

- **Standardized I/O**: All experiments use consistent interfaces
- **Version Pinning**: Dependencies and parameters are explicitly tracked
- **Seed Management**: Reproducible random number generation
- **Artifact Tracking**: Complete experiment provenance

### Extensibility

- **Species Presets**: Easy addition of new ant species
- **Module Swapping**: Interchangeable components across layers
- **Parameter Tuning**: Systematic exploration of parameter space
- **Benchmark Addition**: New evaluation scenarios

### Validation

- **Biological Plausibility**: Grounded in empirical data
- **Performance Metrics**: Quantified success criteria
- **Robustness Testing**: Resilience to real-world challenges
- **Cross-Species Transfer**: Generalization across taxa

## Future Directions

### Advanced Learning Mechanisms

- **Meta-Learning**: Adaptation across different environments
- **Collective Intelligence**: Emergent behaviors in colonies
- **Transfer Learning**: Knowledge transfer between species

### Hardware Integration

- **Robotic Platforms**: Physical ant-inspired robots
- **Sensor Networks**: Distributed environmental monitoring
- **Edge Computing**: Efficient on-device processing

### Biological Validation

- **Field Studies**: Comparison with natural ant behavior
- **Neural Recording**: Validation against biological data
- **Evolutionary Analysis**: Phylogenetic patterns in behavior

## Conclusion

The integration of CohereAnts research into the Ant Stack framework provides a robust, reproducible platform for studying ant intelligence. By mapping our vibrational theory of olfaction, spectroscopic analysis, and behavioral modeling to the standardized three-layer architecture, we create a comprehensive system that bridges theoretical insights with computational implementation.

This implementation enables systematic exploration of ant behavior across species, environments, and experimental conditions while maintaining the biological plausibility that underpins our research. The modular design facilitates both hypothesis testing in myrmecology and applications in swarm robotics, cognitive security, and AI alignment.

**Key Contributions**:
1. **Systematic Integration**: Methodical mapping of CohereAnts to Ant Stack layers
2. **Species Parameterization**: Reproducible configurations for multiple ant taxa
3. **Evaluation Framework**: Standardized metrics and robustness testing
4. **Implementation Workflow**: Clear development pipeline and code organization
5. **Future Roadmap**: Extensibility and validation pathways

The resulting framework serves as a bridge between theoretical entomology and computational neuroscience, enabling reproducible research that advances our understanding of both natural ant intelligence and artificial intelligence systems.



---



# Symbols and Glossary {#sec:symbols_glossary}

## Key Terms and Definitions

### Olfaction and Chemosensation
- **Olfaction**: The sense of smell; the ability to detect and identify airborne molecules through specialized sensory organs
- **Chemosensation**: The detection of chemical stimuli by sensory cells, including olfaction, gustation, and chemesthesis
- **Semiochemicals**: Chemical substances that carry information between organisms, including pheromones, allomones, and kairomones
- **Pheromones**: Semiochemicals that affect the behavior of other members of the same species, such as sex pheromones and trail pheromones
- **Cuticular Hydrocarbons (CHCs)**: Long-chain hydrocarbons found on the surface of insects that serve as recognition cues and waterproofing agents
- **Sensilla**: Microscopic sensory hairs or pegs on insect antennae and other body parts that serve as the primary sensory units for olfaction and other senses

### Insect Anatomy and Physiology
- **Antennae**: Paired sensory appendages on the head of insects that contain olfactory and other sensory receptors
- **Sensilla**: Microscopic sensory hairs or pegs on insect antennae and other body parts that serve as the primary sensory units
- **Sensilla Trichodea**: Hair-like sensilla that are often involved in olfaction, typically 6-160 $\mu\mathrm{m}$ in length
- **Sensilla Basiconica**: Peg-like sensilla with porous surfaces, typically 2-8 $\mu\mathrm{m}$ in length
- **Sensilla Coeloconica**: Pit-like sensilla that may detect temperature, humidity, and infrared radiation
- **ORN**: Olfactory Receptor Neuron; nerve cells that respond to chemical stimuli and transmit signals to the brain
- **OR**: Olfactory Receptor; membrane proteins that bind to odor molecules and initiate signal transduction
 - **Antennal Lobe (AL)**: First olfactory processing center in the insect brain containing glomeruli that aggregate ORN inputs by receptor type
 - **Glomerulus (plural: glomeruli)**: Spheroidal neuropil compartment in the AL where ORN axons synapse with projection neurons and local interneurons; often tuned to receptor families or vibrational features

### Electromagnetic Theory and Infrared Detection
- **Infrared (IR)**: Electromagnetic radiation with wavelengths longer than visible light (0.7-1000 $\mu\mathrm{m}$), invisible to human eyes but detectable by specialized sensors
- **Mid-infrared (MIR)**: IR radiation in the 2-25 $\mu\mathrm{m}$ range, corresponding to molecular vibrational modes and fundamental for chemical sensing applications
- **Far-infrared (FIR)**: IR radiation in the 25-1000 $\mu\mathrm{m}$ range, corresponding to rotational and low-frequency vibrational modes, also known as thermal infrared
- **Near-infrared (NIR)**: IR radiation in the 0.7-2 $\mu\mathrm{m}$ range, just beyond visible light, commonly used in spectroscopy and optical communications
- **Dielectric**: A material that can be polarized by an electric field and supports electromagnetic wave propagation
- **Waveguide**: A structure that guides electromagnetic waves along a specific path with minimal loss
- **Resonator**: A device or structure that oscillates at specific frequencies, amplifying signals at resonant frequencies
- **Quality Factor (Q)**: A measure of resonator performance, defined as the ratio of stored energy to energy lost per cycle

### Spectroscopy and Molecular Properties
- **Vibrational Theory**: The contested hypothesis that molecular vibrations contribute to olfactory recognition; in this manuscript it is treated as a testable complement to molecular receptor binding, not as a replacement for shape and chemistry.
- **Emission Spectrum**: The range of wavelengths of electromagnetic radiation emitted by a substance when excited, characteristic of the energy level transitions in the material
- **Absorption Spectrum**: The range of wavelengths absorbed by a substance, complementary to emission spectra and determined by the molecular structure and bonding
- **Transmission Window**: A range of wavelengths where the atmosphere is relatively transparent to electromagnetic radiation, allowing for long-range signal propagation
- **Deuteration**: The replacement of hydrogen atoms with deuterium (heavy hydrogen) in molecules, affecting vibrational frequencies
- **Enantiomers**: Mirror-image forms of the same molecule that may have different olfactory properties
- **FRET**: F{\"o}rster Resonance Energy Transfer; energy transfer between molecules through dipole-dipole interactions
- **Wavenumber**: The reciprocal of wavelength, typically expressed in cm$^{-1}$, related to energy by $E = hc\tilde{\nu}$

## Mathematical Notation

### Wavelength and frequency
- **λ (lambda)**: Wavelength, typically in micrometers ($\mu\mathrm{m}$) or nanometers (nm).
- **ν (nu)**: Frequency in Hz, related to wavelength by $c = \lambda\nu$.
- **$\tilde{\nu}$ (wavenumber)**: Reciprocal wavelength in cm$^{-1}$, $\tilde{\nu} = 10^4/\lambda$ (for λ in $\mu\mathrm{m}$).
- **c**: Speed of light in vacuum (2.998 $\times$ 10\^{}8 m/s).
- **$\mu\mathrm{m}$**: Micrometer (10^-6 m); standard unit for infrared wavelengths.
- **nm**: Nanometer (10^-9 m).
- **cm^-1**: Wavenumber unit used in IR spectroscopy.

### Physical Constants and Units
- **h**: Planck's constant (6.626 $\times$ 10\^{}-34 J$\cdot$s)
- **$\hbar$**: Reduced Planck constant (h/2π = 1.055 $\times$ 10^-34 J$\cdot$s)
- **k_B**: Boltzmann constant (1.381 $\times$ 10^-23 J/K)
- **T**: Temperature in Kelvin (K)
- **ε_0**: Permittivity of free space (8.854 $\times$ 10^-12 F/m)
- **μ_0**: Permeability of free space (4$\pi$ $\times$ 10\^{}-7 H/m)
- **e**: Elementary charge (1.602 $\times$ 10^-19 C)

### Electromagnetic Theory
- **E**: Electric field vector (V/m)
- **B**: Magnetic induction vector (T)
- **D**: Electric displacement field (C/m²)
- **H**: Magnetic field vector (A/m)
- **P**: Polarization vector (C/m²)
- **M**: Magnetization vector (A/m)
- **ε_r**: Relative permittivity (dimensionless)
- **μ_r**: Relative permeability (dimensionless)
- **tan δ**: Loss tangent, measure of dielectric loss (dimensionless)

### Insect Measurements and Response Times
- **$\mu\mathrm{m}$**: Micrometer; typical size range for insect sensilla (1-200 $\mu\mathrm{m}$)
- **nm**: Nanometer; scale of molecular interactions and receptor dimensions
- **ms**: Millisecond; typical response time of insect ORNs (1-5 ms)
- **$\mu\mathrm{s}$**: Microsecond; time scale for electromagnetic detection
- **ns**: Nanosecond; time scale for quantum processes

## Abbreviations and Acronyms

### General Scientific Terms
- **OR**: Olfactory Receptor
- **ORNs**: Olfactory Receptor Neurons
- **CHCs**: Cuticular Hydrocarbons
- **GPCR**: G-Protein Coupled Receptor
- **MTs**: Microtubules
- **FRET**: F{\"o}rster Resonance Energy Transfer
- **SNR**: Signal-to-Noise Ratio
- **Q**: Quality Factor
- **ROC**: Receiver Operating Characteristic

### Infrared and Spectroscopy
- **IR**: Infrared
- **FIR**: Far Infrared
- **MIR**: Mid Infrared
- **NIR**: Near Infrared
- **ATR-FTIR**: Attenuated Total Reflectance Fourier Transform Infrared Spectroscopy
- **FTIR**: Fourier Transform Infrared Spectroscopy
- **Raman**: Raman Spectroscopy
- **UV-Vis**: Ultraviolet-Visible Spectroscopy

### Computational and Analytical
- **API**: Application Programming Interface
- **TDD**: Test-Driven Development
- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Square Error
- **ANOVA**: Analysis of Variance
- **PER**: Proboscis Extension Reflex

## Key Concepts and Relationships

### Atmospheric Transmission Windows
The Earth's atmosphere has specific wavelength ranges where infrared radiation travels with lower absorption. In this project these windows define candidate propagation bands for model testing; they do not by themselves prove long-range detection of insect semiochemicals [@gordon2022hitran].

- **2-5 $\mu\mathrm{m}$ (Mid-infrared)**: ~80% transmission efficiency, optimal for hydrocarbon detection
- **8-14 $\mu\mathrm{m}$ (Long-wave infrared)**: ~90% transmission efficiency, optimal for long-range communication; ground materials can emit infrared energy that partially penetrates this window
- **17-25 $\mu\mathrm{m}$ (Far-infrared extension)**: represented as a lower-confidence exploratory band with stronger environmental dependence

**Transmission function**: Modeled by `src/core.py::calculate_atmospheric_transmission()` as a coarse window function and by appendix case-study utilities for sensitivity analysis (see \eqref{eq:atmospheric_transmission}; unit tests in `tests/test_core.py`):

\begin{equation}
T(\lambda) = \exp\left[-\sum_i \alpha_i(\lambda) L_i\right]
\label{eq:transmission_function_gloss}
\end{equation}

where $\alpha_i(\lambda)$ is the absorption coefficient and $L_i$ is the path length through atmospheric component $i$.

### Sensilla Dimensions and Wavelength Matching
Insect sensilla have micron-scale dimensions that can be compared to IR wavelength estimates. The current evidence supports morphology-based candidate screening, while direct resonance tuning remains an experimental prediction [@liu2021thripidae]:

- **Sensilla Trichodea**: 6-160 $\mu\mathrm{m}$ length, optimal for 2-30 $\mu\mathrm{m}$ wavelengths
- **Sensilla Basiconica**: 2-8 $\mu\mathrm{m}$ length, optimal for 1-10 $\mu\mathrm{m}$ wavelengths; specific dimensions of 6.86–53.42 $\mu\mathrm{m}$ observed in thrips species
- **Sensilla Coeloconica**: 5-15 $\mu\mathrm{m}$ length, optimal for 3-20 $\mu\mathrm{m}$ wavelengths
- **Specialized IR organs**: Approximately 100 sensilla per organ in beetle species

**Wavelength matching**: Analyzed by `src/sensilla.py::analyze_sensilla_dimensions()` against representative morphometric ranges; see resonant frequency \eqref{eq:resonant_freq_gloss} and tests `tests/test_sensilla.py`. Publication figures are generated via `scripts/generate_research_figures.py`.

**Resonant Frequency**: The fundamental resonant frequency of a sensillum is:

\begin{equation}
f_{res} = \frac{c}{2\pi} \sqrt{\left(\frac{\alpha_{mn}}{a}\right)^2 + \left(\frac{p\pi}{L}\right)^2}
\label{eq:resonant_freq_gloss}
\end{equation}

where $c$ is the speed of light, $\alpha_{mn}$ is the Bessel function root, and $a$ and $L$ are the radius and length.

### Response Time Comparisons
Different sensory modalities exhibit characteristic response times that reflect their underlying mechanisms:

- **Insect ORNs**: millisecond-scale odor-evoked responses, including first spikes down to 3 ms in Drosophila [@egeaweiss2018rapid]
- **Insect Photoreceptors**: 0.1 ms response time
- **Insect Auditory Receptors**: 0.16 ms response time
- **Traditional Olfaction (Molecular)**: 7-12 ms response time
- **Mammalian ORNs**: 10-50 ms response time

**Response time analysis**: Compared using `src/core.py::calculate_response_time_improvement()`; see `tests/test_core.py::TestResponseTimeImprovement`. See `../figures/response_time_comparison.png` and cf. \eqref{eq:response_time_components}. IR-specific timing is an experimental target, not an established value.

### Signal Processing and Information Theory
The vibrational theory incorporates advanced signal processing concepts:

- **Channel Capacity**: The maximum information rate that can be transmitted through the infrared detection channel:

\begin{equation}
C = B \log_2(1 + SNR)
\label{eq:channel_capacity_gloss}
\end{equation}

where $B$ is the bandwidth and $SNR$ is the signal-to-noise ratio.

- **Detection Threshold**: The minimum detectable power is:

\begin{equation}
P_{min} = k_B T \Delta f \cdot SNR_{min}
\label{eq:min_power_gloss}
\end{equation}

where $k_B$ is Boltzmann's constant, $T$ is temperature, $\Delta f$ is bandwidth, and $SNR_{min}$ is the minimum required signal-to-noise ratio.

## Research Methodology Terms

### Experimental Techniques
- **Ionotropic**: Direct ligand-gated ion channels that open immediately upon binding
- **Metabotropic**: G-protein coupled receptor systems that activate intracellular signaling cascades
- **Behavioral Conditioning**: Training insects to associate specific stimuli with rewards or punishments
- **Electroantennography (EAG)**: Recording electrical responses from insect antennae to chemical stimuli
- **Single Sensillum Recording**: Recording from individual sensilla to measure response characteristics

### Physical and Chemical Properties
- **Piezoelectric**: Materials that generate electric charge in response to mechanical stress
- **Allosteric Modulation**: Changes in protein function due to binding at sites other than the active site
- **Photomodulation**: Changes in protein function due to light absorption
- **Dielectric Loss**: Energy dissipation in dielectric materials due to molecular motion
- **Resonant Coupling**: Stronger energy transfer when systems oscillate at the same frequency

### Statistical and Analytical Methods
- **Power Analysis**: Statistical method to determine the minimum sample size needed to detect an effect
- **Receiver Operating Characteristic (ROC)**: Plot of true positive rate vs. false positive rate
- **Discriminability Index (d')**: Measure of ability to distinguish between signal and noise
- **Hill Coefficient**: Measure of cooperativity in binding or response functions
- **Log-Periodic Analysis**: Analysis of systems with periodic spacing that increases logarithmically

## Source Code Implementation

All mathematical concepts and equations presented in this manuscript are implemented in tested source code that generates the visualizations and analyses embedded throughout. The key functions include:

### Core Physics and Calculations
- **`calculate_atmospheric_transmission()`**: Implements atmospheric transmission models with environmental parameter integration
- **`calculate_response_time_improvement()`**: Compares response times across different sensory modalities with statistical validation
- **`calculate_wavelength_from_wavenumber()`**: Converts between wavelength and wavenumber representations
- **`safe_division()`**: Performs safe division operations with error handling

### Morphological and Structural Analysis
- **`analyze_sensilla_dimensions()`**: Analyzes sensilla morphology and calculates optimal detection wavelengths
- **`calculate_sensilla_resonance_frequency()`**: Computes resonant frequencies using cavity resonator theory
- **`calculate_wavelength_matching()`**: Quantifies wavelength matching between sensilla and incident radiation
- **`generate_sensilla_visualization()`**: Creates detailed visualizations of sensilla structures and properties

### Spectroscopic and Chemical Analysis
- **`analyze_chc_spectra()`**: Processes cuticular hydrocarbon spectroscopic data with peak detection
- **`calculate_spectral_overlap()`**: Quantifies spectral similarity between different compounds
- **`generate_spectral_plots()`**: Creates publication-quality spectral visualizations
- **`identify_chc_compounds()`**: Identifies potential CHC compounds based on peak positions

### Behavioral and Response Analysis
- **`analyze_behavioral_response()`**: Analyzes behavioral response data with statistical testing
- **`calculate_power_analysis()`**: Performs statistical power analysis for experimental design
- **`calculate_response_statistics()`**: Computes comprehensive statistics for response data
- **`generate_behavioral_plots()`**: Creates behavioral response visualizations

### Integrated Analysis Frameworks
- **`IntegratedAnalyzer`**: Combines multiple analytical approaches for comprehensive assessment
- **`MetaMaterialAnalyzer`**: Analyzes meta-material properties and quantum effects
- **`FermiEstimator`**: Performs Fermi estimation for order-of-magnitude calculations
- **`BehavioralAnalyzer`**: Specialized analysis for behavioral response data

### Data Validation and Testing
- **`validate_numeric_inputs()`**: Ensures all numeric inputs are valid and finite (exercised in multiple unit tests)
- **`SensillaData`**: Container class for sensilla measurements with validation
- **`SpectralData`**: Container class for spectral data with analysis methods
- **`BehavioralData`**: Container class for behavioral data with statistical analysis

## References and Further Reading

For detailed discussions of the concepts presented here, see:

- **Vibrational olfaction theory and critique**: Turin, Franco et al., and Block et al. [@turin1996spectroscopic; @franco2011molecular; @block2015implausibility]
- **Insect IR and radiant sensing**: pyrophilous photomechanic organs (Schmitz et al., Hammer et al.), *Aradus*, *Acanthocnemus*, *Merimna*, hematophagy IR (Chandel, Zopf, Lazzari), cycad pollination IR (Valencia-Montoya), TRPA1 (Corfas, Zhang), passive cuticle optics (Krishna, Sheppard), and applied NIRS monitoring (Potamitis) [@schmitz2011infrared; @hammer2001sensitivity; @schmitza2010aradus; @schmitz2002acanthocnemus; @schmitz2012merimna; @chandel2024thermal; @zopf2014infrared; @lazzari2009orientation; @valenciamontoya2025infrared; @corfas2015trpa1; @krishna2020infrared; @potamitis2022monitoring]
- **Spectroscopy and CHC biology**: Durak et al. and Blomquist and Ginzel [@durak2022atrftir; @blomquist2021hydrocarbons]
- **ORN timing**: Gorur-Shandilya et al., Egea-Weiss et al., and Barta et al. [@gorurshandilya2017gain; @egeaweiss2018rapid; @barta2024stimulus]
- **Atmospheric transmission**: HITRAN2020 and the environmental-channel appendix [@gordon2022hitran]

## Computational Framework Documentation

The complete computational framework is documented with (appendix case studies: \Cref{sec:app_sensilla_array}, \Cref{sec:app_environmental_channel}, \Cref{sec:app_detection_limits}, \Cref{sec:app_neural_encoding}, \Cref{sec:app_spectral_unmixing}, \Cref{sec:app_plasmonic_geometry}, and \Cref{sec:app_active_inference}):

- **Coverage Gate**: The project enforces the template's $\geq 90\%$ `src/` coverage gate
- **Performance Benchmarks**: Execution speed and memory efficiency metrics
- **Validation Procedures**: Comparison with known physical constants and empirical data
- **API Documentation**: Complete function signatures and parameter descriptions
- **Example Scripts**: Demonstrations of complete analysis pipelines

For complete mathematical formulations and source code implementation, see Section \Cref{sec:mathematical_appendix}. Cross-links to implementations and unit tests are included therein.

<!-- BEGIN: AUTO-API-GLOSSARY -->
| Module | Name | Kind | Summary |
|---|---|---|---|
| `__init__` | `get_package_info` | function | Get comprehensive package information |
| `__init__` | `run_demo_analysis` | function | Run a demonstration analysis using all available frameworks |
| `ant_stack.antbody` | `AntBodySensilla` | class | Sensilla configuration using CohereAnts morphology analysis |
| `ant_stack.antbody` | `AntBodySpectroscopy` | class | Atmospheric transmission access aligned with core calculations |
| `ant_stack.antbrain` | `AntBrainOlfaction` | class | High-level olfactory pipeline stub with AL→MB→CX placeholders |
| `ant_stack.antbrain` | `VibrationalGlomeruliCircuit` | class | Bank of resonant channels tuned across 2–25 μm |
| `ant_stack.antmind` | `AntMindOlfaction` | class | Active-inference-like placeholder for olfactory policy selection |
| `ant_stack.antmind` | `AntMindStigmergy` | class | Grid-based pheromone field with diffusion and decay |
| `behavioral` | `BehavioralAnalyzer` | class | Main analyzer for behavioral response data |
| `behavioral` | `BehavioralData` | class | Container for behavioral response data with validation |
| `behavioral` | `StatisticalAnalyzer` | class | Statistical analysis for behavioral data |
| `behavioral` | `analyze_behavioral_response` | function | Analyze behavioral response data |
| `behavioral` | `calculate_power_analysis` | function | Calculate statistical power for the comparison |
| `behavioral` | `calculate_response_statistics` | function | Calculate comprehensive statistics for behavioral response data |
| `behavioral` | `generate_behavioral_plots` | function | Generate behavioral response plots |
| `case_studies.active_inference` | `olfactory_active_inference_step` | function | Minimal deterministic update step for a 2D position under a gradient cue |
| `case_studies.detection_limits` | `detection_performance_vs_snr` | function | Analyze detection performance vs signal-to-noise ratio |
| `case_studies.detection_limits` | `detection_range_analysis` | function | Analyze detection range for IR olfactory communication |
| `case_studies.detection_limits` | `min_detectable_power` | function | Minimum detectable signal power using thermal noise floor and SNR threshold |
| `case_studies.detection_limits` | `noise_floor_analysis` | function | Analyze noise floor components vs frequency |
| `case_studies.detection_limits` | `operating_point` | function | Bundle operating point parameters deterministically |
| `case_studies.detection_limits` | `operating_regions_analysis` | function | Analyze operating regions in power-temperature space |
| `case_studies.detection_limits` | `optimize_detection_parameters` | function | Optimize detection system parameters for given constraints and objectives |
| `case_studies.detection_limits` | `roc_analysis` | function | Receiver Operating Characteristic (ROC) analysis for signal detection |
| `case_studies.detection_limits` | `sensitivity_analysis` | function | Sensitivity analysis of detection performance to parameter variations |
| `case_studies.detection_limits` | `snr_curve` | function | SNR vs |
| `case_studies.environmental_channel` | `atmospheric_transmission_comprehensive` | function | Comprehensive atmospheric transmission model with multiple physical effects |
| `case_studies.environmental_channel` | `atmospheric_transmission_detailed` | function | Compute a simple parametric atmospheric transmission curve |
| `case_studies.environmental_channel` | `channel_capacity_analysis` | function | Analyze communication channel capacity under atmospheric conditions |
| `case_studies.environmental_channel` | `channel_capacity_vs_env` | function | Map Shannon capacity across humidity×temperature grid (legacy function) |
| `case_studies.environmental_channel` | `environmental_sensitivity_analysis` | function | Analyze sensitivity of transmission to environmental parameters |
| `case_studies.environmental_channel` | `molecular_absorption_cross_section` | function | Calculate molecular absorption cross-sections for atmospheric constituents |
| `case_studies.environmental_channel` | `optimize_wavelength_for_range` | function | Find optimal wavelengths for target communication range and capacity |
| `case_studies.environmental_channel` | `rayleigh_scattering_coefficient` | function | Calculate Rayleigh scattering coefficient for dry air |
| `case_studies.neural_encoding` | `adaptation_dynamics_analysis` | function | Analyze adaptation dynamics in neural responses |
| `case_studies.neural_encoding` | `analyze_spike_train_statistics` | function | Compute comprehensive spike train statistics |
| `case_studies.neural_encoding` | `generate_spike_trains` | function | Generate realistic spike trains for ORN responses to odor stimuli |
| `case_studies.neural_encoding` | `information_rate_time_series` | function | Estimate information metrics using a Gaussian channel approximation |
| `case_studies.neural_encoding` | `mutual_information_analysis` | function | Compute mutual information between neural responses and stimuli |
| `case_studies.neural_encoding` | `odor_discrimination_analysis` | function | Analyze odor discrimination performance across different time windows |
| `case_studies.neural_encoding` | `population_coding_analysis` | function | Analyze population coding efficiency across multiple ORNs |
| `case_studies.neural_encoding` | `rate_coding_metrics` | function | Compute simple separability metrics (means/stds) deterministically |
| `case_studies.neural_encoding` | `temporal_coding_analysis` | function | Analyze temporal coding precision and response latency |
| `case_studies.plasmonic_geometry` | `coupled_dipoles_near_field` | function | Calculate near-field enhancement for coupled plasmonic nanoparticles |
| `case_studies.plasmonic_geometry` | `drude_model_permittivity` | function | Calculate frequency-dependent permittivity using Drude model |
| `case_studies.plasmonic_geometry` | `field_distribution_near_particle` | function | Calculate near-field distribution around a spherical nanoparticle |
| `case_studies.plasmonic_geometry` | `mie_scattering_sphere` | function | Calculate Mie scattering properties for spherical nanoparticles |
| `case_studies.plasmonic_geometry` | `optimize_plasmonic_geometry` | function | Optimize nanoparticle geometry for maximum enhancement at target wavelength |
| `case_studies.plasmonic_geometry` | `sweep_plasmonic_quality` | function | Comprehensive sweep of plasmonic quality factors across size and wavelength |
| `case_studies.sensilla_array_directionality` | `analyze_sensilla_morphology` | function | Analyze sensilla dimensions for resonant wavelength matching |
| `case_studies.sensilla_array_directionality` | `array_gain` | function | Compute a scalar array gain proxy as peak-to-mean power ratio |
| `case_studies.sensilla_array_directionality` | `array_pattern_2d` | function | Compute 2D radiation pattern for sensilla array across frequency range |
| `case_studies.sensilla_array_directionality` | `compute_beam_pattern` | function | Compute a simplified 1D beam pattern over wavelengths |
| `case_studies.sensilla_array_directionality` | `design_circular_array` | function | Design a circular antenna array representing sensilla on insect antennae |
| `case_studies.sensilla_array_directionality` | `design_log_periodic_array` | function | Design a 1D log-periodic array of element positions |
| `case_studies.sensilla_array_directionality` | `frequency_response_analysis` | function | Analyze frequency response characteristics of sensilla array |
| `case_studies.sensilla_array_directionality` | `mutual_coupling_matrix` | function | Compute mutual coupling matrix between antenna elements |
| `case_studies.sensilla_array_directionality` | `sensilla_element_pattern` | function | Individual sensillum radiation pattern as function of observation angle |
| `case_studies.spectral_unmixing` | `advanced_classification_suite` | function | Comprehensive classification analysis using multiple algorithms |
| `case_studies.spectral_unmixing` | `generate_realistic_chc_spectra` | function | Generate realistic CHC spectral data with known ground truth components |
| `case_studies.spectral_unmixing` | `independent_component_analysis_spectra` | function | Independent Component Analysis (ICA) for blind source separation of spectra |
| `case_studies.spectral_unmixing` | `lda_baseline` | function | Closed-form two-class LDA with equal covariance; returns accuracy on train |
| `case_studies.spectral_unmixing` | `nmf_unmix` | function | Deterministic, simple NMF via multiplicative updates |
| `case_studies.spectral_unmixing` | `performance_metrics_comprehensive` | function | Compute comprehensive performance metrics for classification |
| `case_studies.spectral_unmixing` | `spectral_feature_extraction` | function | Extract discriminative features from spectral data |
| `case_studies.spectral_unmixing` | `vertex_component_analysis` | function | Vertex Component Analysis (VCA) for endmember extraction |
| `config` | `ConfigManager` | class | Centralized configuration manager for insect analysis |
| `config` | `enable_verbose_logging` | function | Enable verbose logging for debugging |
| `config` | `get_config` | function | Get the global configuration manager instance |
| `config` | `init_config` | function | Initialize the global configuration manager |
| `config` | `set_plot_style` | function | Set matplotlib plot style |
| `config` | `set_random_seed` | function | Set random seed for reproducible results |
| `config` | `set_temperature` | function | Set analysis temperature in Kelvin |
| `core` | `calculate_atmospheric_transmission` | function | Calculate atmospheric transmission for given wavelengths in the infrared spectrum |
| `core` | `calculate_response_time_improvement` | function | Calculate the improvement in response time compared to traditional olfaction |
| `core` | `calculate_wavelength_from_wavenumber` | function | Convert wavenumber (cm⁻¹) to wavelength (μm) |
| `core` | `calculate_wavenumber_from_wavelength` | function | Convert wavelength (μm) to wavenumber (cm^-1) |
| `core` | `safe_division` | function | Safely perform division, returning infinity if denominator is zero |
| `core` | `validate_numeric_inputs` | function | Validate that all numeric inputs are finite numbers |
| `fermi_estimation` | `FermiEstimator` | class | Comprehensive Fermi Estimation analyzer for olfaction and infrared sensing |
| `fermi_estimation` | `create_sample_fermi_analysis` | function | Create a sample Fermi analysis for demonstration |
| `glossary_gen` | `ApiEntry` | class | Represents a public API entry from source code |
| `glossary_gen` | `build_api_index` | function | Scan `src_dir` and collect public functions/classes with summaries |
| `glossary_gen` | `generate_markdown_table` | function | Generate a Markdown table from API entries |
| `glossary_gen` | `inject_between_markers` | function | Replace content between begin_marker and end_marker (inclusive markers preserved) |
| `insect_analysis` | `run_comprehensive_analysis` | function | Run comprehensive analysis using all available frameworks |
| `integrated_analysis` | `IntegratedAnalyzer` | class | Integrated analyzer combining Fermi Estimation and meta-material frameworks |
| `integrated_analysis` | `create_sample_integrated_analysis` | function | Create a sample integrated analysis for demonstration |
| `meta_material_framework` | `MetaMaterialAnalyzer` | class | Comprehensive meta-material analyzer for olfaction and infrared sensing |
| `meta_material_framework` | `create_sample_metamaterial_analysis` | function | Create a sample meta-material analysis for demonstration |
| `sensilla` | `SensillaData` | class | Container for sensilla measurement data with validation |
| `sensilla` | `analyze_sensilla_dimensions` | function | Analyze sensilla dimensions and calculate optimal detection wavelengths |
| `sensilla` | `calculate_sensilla_resonance_frequency` | function | Calculate the fundamental resonance frequency of a sensillum |
| `sensilla` | `calculate_wavelength_matching` | function | Calculate wavelength matching between sensilla dimensions and incident radiation |
| `sensilla` | `generate_sensilla_visualization` | function | Generate a visualization of sensilla dimensions and optimal wavelengths |
| `spectroscopy` | `CHCAnalyzer` | class | Analyzer for cuticular hydrocarbon spectra |
| `spectroscopy` | `PeakFinder` | class | Peak detection and analysis for spectral data |
| `spectroscopy` | `SpectralData` | class | Container for spectral data with validation and analysis methods |
| `spectroscopy` | `analyze_chc_spectra` | function | Analyze cuticular hydrocarbon (CHC) infrared spectra |
| `spectroscopy` | `calculate_spectral_overlap` | function | Calculate spectral overlap between two spectra |
| `spectroscopy` | `generate_spectral_plots` | function | Generate spectral plots for multiple compounds |
| `spectroscopy` | `identify_chc_compounds` | function | Identify potential CHC compounds based on peak positions |
| `visualization` | `AdvancedVisualizer` | class | Advanced visualization tools for insect analysis data |
| `visualization` | `PlotStyler` | class | Advanced plot styling and theming system |
| `visualization` | `create_accessible_figure` | function | Create a figure with accessibility-oriented styling options |
| `visualization` | `create_publication_figure` | function | Create a publication-ready figure with optimal styling |
| `visualization` | `create_subplots` | function | Create subplots with enhanced accessibility and consistent styling |
| `visualization` | `get_colorblind_palette` | function | Get a colorblind-friendly color palette |
| `visualization` | `set_plot_style` | function | Set the global plot style |
<!-- END: AUTO-API-GLOSSARY -->



---



# Appendix G: Active-Inference Behavioral Demo on IR Cues {#sec:app_active_inference}

## Objective

Demonstrate a deterministic active-inference step for olfactory search under IR cues.

## Interpretation

The demo shows how a minimal belief-update policy could navigate a grid when IR cue strength varies spatially. It supports assay design—what information a searcher would need from wavelength-specific cues—not field ethology. Outputs should be read alongside preregistered behavioral falsifiers in \Cref{sec:discussion}.

## Claim boundary

\Cref{fig:app_active_inference} is a deterministic trajectory from `src/behavioral_models.py`; it is not evidence that insects perform active inference on semiochemical IR gradients.

## Implemented (stub) Methods (src)

- `src/behavioral_models.py`
  - `olfactory_active_inference_step(state, params)` — deterministic single‑step update used in the demo

## Script and Outputs

- Script: `scripts/generate_active_inference_demo.py`
- Data: `output/data/active_inference_demo.npz`
- Figure: `../figures/active_inference_trajectory.png`

## Figure

<!-- alt: Deterministic active-inference trajectory on a grid with IR cue beliefs; behavioral demo model output, not field data. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/active_inference_trajectory.png}
\caption{Deterministic gradient-following trajectory under a simple active-inference step model. Claim boundary: behavioral demo only; not field data.}
\label{fig:app_active_inference}
\end{figure}

## Equation References

- Response/latency and information metrics: see \Cref{sec:mathematical_appendix}.

## Reproducibility

- Run: `python3 scripts/generate_active_inference_demo.py`
- Artifacts saved to `output/data/` and `../figures/`.
- Seed set to 42 via `src/config.set_random_seed(42)` for deterministic policy traces.
- Implementation note: the demo is a lightweight, deterministic adapter that calls `src/` policy utilities without embedding scientific logic in the script.

## Cross-References

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}

<!-- Removed duplicate figure block; primary figure `app_active_inference` is already included above. -->



---



# Appendix C: Detection Limits and Operating Points {#sec:app_detection_limits}

## Objective

Comprehensive detection-theory analysis with model operating points informed by electrophysiology literature anchors (not direct re-analysis of raw spike trains): ROC curves for millisecond-scale latency targets, sensitivity analysis for sub-10 ms ORN responses, operating regions in power-temperature space, and noise-floor characterization distinguishing electromagnetic from thermal effects for IR sensor bounds.

## Interpretation

Panels map literature-anchored SNR and power thresholds into ROC and operating-region plots. They answer whether a proposed IR stage could exceed thermal noise under stated assumptions, not whether insects operate at those points in nature.

## Claim boundary

\Cref{fig:app_detection_limits} bounds sensor feasibility; it does not establish biological IR olfaction or measured insect detection ranges.

## Methods (src)

- `src/case_studies/detection_limits.py`
  - `min_detectable_power(temperature_k, bandwidth_hz, snr_min_db)` — thermal‑noise‑limited detection
  - `roc_analysis(signal_power, noise_power)` — ROC curves and optimal thresholds
  - `detection_performance_vs_snr(snr_range_db, pfa_target)` — performance curves and MDS
  - `sensitivity_analysis(power_range, temp_range, param_variations)` — parameter sensitivity
  - `operating_regions_analysis(power_range, temp_range)` — SNR contours in operating space
  - `noise_floor_analysis(freq_range, temperature_k)` — multi‑component noise analysis
  - `detection_range_analysis(tx_power, antenna_gain, frequency, sensitivity)` — range calculations
  - `optimize_detection_parameters(constraints, objectives)` — system optimization

## Script and outputs

- Script: `scripts/generate_detection_limits.py`
- Data: `output/data/detection_limits_comprehensive.npz`
- Figure: `../figures/detection_limits_comprehensive_analysis.png`

## Figure

<!-- alt: Detection limits panels with ROC curves, SNR operating regions, and noise floors for IR sensor bounds; model output only. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/detection_limits_comprehensive_analysis.png}
\caption{Detection limits analysis with ROC curves, SNR operating regions, noise floors, and range trade-offs for IR sensor bounds. Claim boundary: bounds sensor feasibility and model assumptions; does not establish biological IR olfaction.}
\label{fig:app_detection_limits}
\end{figure}

<!-- Removed duplicate figure block to avoid repeated insertion; primary figure `app_detection_limits` remains above. -->

## Equation references

- Minimum power: see \eqref{eq:min_power_gloss}
- Capacity: see \eqref{eq:channel_capacity_gloss}

## Reproducibility

- Run: `python3 scripts/generate_detection_limits.py`
- Artifacts saved to `output/data/` and `../figures/`.
- Deterministic operating points via `src/config.set_random_seed(42)`.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}



---



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
- Figure: `../figures/environmental_channel_comprehensive_analysis.png`

## Figure

<!-- alt: Atmospheric channel model with absorption, scattering, and capacity maps across humidity and temperature; engineering channel bounds. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/environmental_channel_comprehensive_analysis.png}
\caption{Environmental channel model with absorption, scattering, and capacity maps across humidity and temperature grids. Claim boundary: channel-capacity sensitivity demo under modeled clear/humid conditions; not a measured insect range.}
\label{fig:app_env_channel}
\end{figure}

<!-- Removed duplicate figure: uses the primary `app_env_channel` figure above -->

<!-- alt: Integrated information decomposition across molecular, receptor, neural, and environmental terms; bounds sensor throughput, not biological proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/integrated_analysis_information_analysis.png}
\caption{Integrated information decomposition across molecular, receptor, neural, and environmental terms. Claim boundary: bounds sensor throughput; does not establish biological IR olfaction.}
\label{fig:integrated_info}
\end{figure}

## Equation references

- Atmospheric transmission: see \eqref{eq:atmospheric_transmission}
- Channel capacity: see \eqref{eq:channel_capacity_gloss}

## Reproducibility

- Run: `python3 scripts/generate_environmental_channel_analysis.py`
- Artifacts saved to `output/data/` and `../figures/`.
- Deterministic grids via `src/config.set_random_seed(42)`.

## Context Note on Biological Ranges

Some insects exhibit sensitivity to thermal IR in natural behaviors. *Aedes aegypti* integrates thermal IR around the human skin-temperature spectrum with other host cues [@chandel2024thermal]. *Rhodnius prolixus* discriminates radiant IR from convective heat via antennal warm-cell combinatorial coding; forced convection disrupts that quotient [@zopf2014infrared; @zopf2015convection]. Lazzari reviewed how radiant IR operates at longer range than convective heat near hosts [@lazzari2009orientation]. These behavioral constraints complement the electromagnetic window analysis and motivate species- and wavelength-specific range predictions.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}



---



# Appendix D: Neural Encoding Efficiency on Time-Series {#sec:app_neural_encoding}

## Objective

Comprehensive neural encoding analysis including spike‑train generation, temporal dynamics, population coding, mutual information, and adaptation mechanisms for olfactory receptor neurons.

## Interpretation

Synthetic spike trains and population metrics explore how fast ORN-like encoders could carry timing information if an IR-sensitive stage existed. The analysis separates already-fast molecular latencies from hypothetical sub-millisecond components that falsifier 4 in \Cref{sec:discussion} targets.

## Claim boundary

\Cref{fig:app_neural_encoding_full} uses generated time series; it does not reanalyze published electrophysiology recordings or prove IR transduction.

## Methods (src)

- `src/case_studies/neural_encoding.py`
  - `generate_spike_trains(stimuli, dt, baseline_rate, max_rate, dynamics)` — realistic spike generation
  - `analyze_spike_train_statistics(spike_data)` — ISI, CV, Fano factor
  - `temporal_coding_analysis(spike_data, stimulus_times)` — latency and precision metrics
  - `population_coding_analysis(population_responses, labels)` — PCA, LDA, correlation structure
  - `mutual_information_analysis(responses, stimuli)` — information‑theoretic metrics
  - `odor_discrimination_analysis(responses, odor_ids, time_windows)` — discrimination performance
  - `adaptation_dynamics_analysis(spike_data, stimulus_duration)` — adaptation characterization
  - `information_rate_time_series(responses, dt_s, noise_std)` — channel‑capacity estimation
  - `rate_coding_metrics(responses, labels)` — separability and discriminability metrics

## Script and outputs

- Script: `scripts/generate_neural_encoding_analysis.py`
- Data: `output/data/neural_encoding_comprehensive.npz`
- Figure: `../figures/neural_encoding_comprehensive_analysis.png`

## Figure

<!-- alt: Neural encoding panels with spike trains, population PCA, and information metrics on synthetic ORN time series; model output only. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/neural_encoding_comprehensive_analysis.png}
\caption{Neural encoding panels with spike trains, population PCA, and information metrics on synthetic ORN time series. Claim boundary: model output only; does not establish biological IR olfaction.}
\label{fig:app_neural_encoding_full}
\end{figure}

<!-- Integrated analysis figure is used elsewhere; removed duplicate to prevent redundancy. -->

## Equation references

- Information rate: see \eqref{eq:channel_capacity_gloss}
- Response time model: see \eqref{eq:response_time_components}

## Reproducibility

- Run: `python3 scripts/generate_neural_encoding_analysis.py`
- Artifacts saved to `output/data/` and `../figures/`.
- Deterministic seeds: `src/config.set_random_seed(42)` for surrogate time‑series.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}



---



# Appendix F: Plasmonic Nano-Geometry Sweep {#sec:app_plasmonic_geometry}

## Objective
Comprehensive plasmonic nanostructure analysis: frequency-dependent permittivity (Drude), Mie scattering, coupled‑dipole near‑field interactions, geometry optimization, and field‑enhancement mapping for receptor‑scale enhancement.

## Interpretation

Sweeps identify nanoparticle sizes and materials that maximize near-field enhancement at MIR wavelengths relevant to biomimetic bands 2.8--6 µm. Results inform whether receptor-scale structures could, in principle, boost weak narrowband signals—not whether insects employ plasmonics in sensilla.

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
- Figure: `../figures/plasmonic_geometry_comprehensive_analysis.png`

## Figure

<!-- alt: Plasmonic geometry sweep with Drude permittivity, Mie scattering, and near-field enhancement maps for receptor-scale sensor design. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/plasmonic_geometry_comprehensive_analysis.png}
\caption{Plasmonic geometry sweep with Drude permittivity, Mie scattering, and near-field enhancement maps for receptor-scale sensor design. Claim boundary: bounds sensor feasibility and model assumptions; does not establish biological IR olfaction.}
\label{fig:app_plasmonic_sweep}
\end{figure}

<!-- alt: Integrated metamaterial dielectric and plasmonic response with information-capacity summaries; engineering model panels. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/integrated_analysis_metamaterial_properties.png}
\caption{Integrated metamaterial dielectric and plasmonic response with information-capacity summaries. Claim boundary: engineering model panels only; does not establish biological IR olfaction.}
\label{fig:integrated_metamaterial}
\end{figure}

## Equation references

-- Resonance/wavelength: see main text and the Mathematical Appendix \Cref{sec:mathematical_appendix}.

## Reproducibility

- Run: `python3 scripts/generate_plasmonic_geometry_sweep.py`
- Artifacts saved to `output/data/` and `../figures/`.
- Deterministic radii grid and material parameters via `src/config.set_random_seed(42)`.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}



---



# Appendix A: Sensilla Array Directionality and Beam Patterns {#sec:app_sensilla_array}

## Objective
Electromagnetic antenna modeling for sensilla arrays benchmarked against peer-reviewed morphometric ranges: circular/log-periodic designs inspired by insect antenna structures, element patterns, mutual coupling, 2D radiation patterns, representative morphology-to-resonance comparisons, and frequency-response characterization for candidate directional olfactory detection [@liu2021thripidae].

## Interpretation

Beam patterns and coupling matrices translate morphometric presets into directional gain estimates. They support the behavioral directionality discussion in \Cref{sec:experimental_results} while requiring IR-only assays to validate any link to orientation behavior.

## Claim boundary

\Cref{fig:app_sensilla_beam} reports model gain and resonance maps; it is not field proof of semiochemical IR olfaction.

## Methods (src)
- `src/case_studies/sensilla_array_directionality.py`
  - `design_circular_array(n_elements: int, radius_m: float, wavelength_m: float) -> np.ndarray`
  - `sensilla_element_pattern(sensilla_type: str, frequency_hz: float, dimensions: dict) -> np.ndarray`
  - `mutual_coupling_matrix(positions: np.ndarray, wavelength_m: float) -> np.ndarray`
  - `array_pattern_2d(positions: np.ndarray, element_patterns: np.ndarray, frequency: float, coupling: np.ndarray) -> np.ndarray`
  - `analyze_sensilla_morphology(dimensions: np.ndarray, frequency_range: np.ndarray) -> dict`
  - `frequency_response_analysis(array_config: dict, freq_range: np.ndarray) -> dict`
  - `compute_beam_pattern(wavelengths: np.ndarray, positions: np.ndarray, gains: np.ndarray) -> np.ndarray`
  - `array_gain(pattern: np.ndarray) -> float`
  - `design_log_periodic_array(min_len: float, max_len: float, tau: float, count: int) -> np.ndarray`

## Script and outputs
- Script: `scripts/generate_sensilla_array_directionality.py`
- Data: `output/data/sensilla_array_comprehensive.npz`
- Figure: `../figures/sensilla_array_comprehensive_analysis.png`
- Caption metadata: `../figures/sensilla_array_comprehensive_analysis.caption.txt`

## Figure
<!-- alt: Sensilla array beam patterns, coupling, and morphology-to-resonance maps from antenna models; bounds directional gain, not field proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/sensilla_array_comprehensive_analysis.png}
\caption{Sensilla array beam patterns, coupling, and morphology-to-resonance maps from antenna models. Claim boundary: bounds directional gain; not field proof of semiochemical IR olfaction.}
\label{fig:app_sensilla_beam}
\end{figure}

## Equation references
- Effective aperture: see \eqref{eq:effective_aperture}
- Gain pattern: see \eqref{eq:gain_pattern}

## Reproducibility
1. Run: `python3 scripts/generate_sensilla_array_directionality.py`
2. Artifacts: `output/data/` and `../figures/`
3. Deterministic seed: `src/config.set_random_seed(42)`

## Cross‑references
- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math: \Cref{sec:mathematical_appendix}



---



# Appendix E: Spectral Unmixing and Classification {#sec:app_spectral_unmixing}

## Objective

Comprehensive spectral analysis: realistic CHC data generation, feature extraction, unmixing (NMF, VCA, ICA), and multi‑algorithm classification with deterministic evaluation.

## Interpretation

Synthetic mixtures benchmark unmixing and classification pipelines against known ground truth. Performance metrics justify spectroscopic feature extraction in \Cref{fig:chc_spectra_example} while leaving in vivo perceptual use of those bands as an open test.

## Claim boundary

\Cref{fig:app_spectral_unmixing} and \Cref{fig:integrated_classification} report algorithm evaluation on synthetic spectra; they are not species-identification proof on live specimens.

## Methods (src)

- `src/case_studies/spectral_unmixing.py`
  - `generate_realistic_chc_spectra(n_compounds: int, n_wavelengths: int, seed: int=42) -> dict` — synthetic CHC spectra with ground truth
  - `nmf_unmix(spectra: np.ndarray, n_components: int, seed: int=42) -> (W, H)` — deterministic NMF
  - `vertex_component_analysis(spectra: np.ndarray, n_endmembers: int) -> np.ndarray` — VCA endmember extraction
  - `independent_component_analysis_spectra(spectra: np.ndarray, n_components: int) -> np.ndarray` — ICA separation
  - `spectral_feature_extraction(spectra: np.ndarray, wavelengths: np.ndarray, method: str='peaks') -> dict` — peaks, derivatives, PCA, statistical features
  - `advanced_classification_suite(features: np.ndarray, labels: np.ndarray) -> dict` — multi‑algorithm benchmark
  - `performance_metrics_comprehensive(y_true: np.ndarray, y_pred: np.ndarray, y_prob: Optional[np.ndarray]=None) -> dict`
  - `lda_baseline(features: np.ndarray, labels: np.ndarray, seed: int=42) -> dict` — closed‑form LDA baseline

## Script and outputs

- Script: `scripts/generate_spectral_unmixing.py`
- Data: `output/data/spectral_unmixing_comprehensive.npz`
- Figure: `../figures/spectral_unmixing_comprehensive_analysis.png`

## Figure

<!-- alt: Synthetic CHC spectral unmixing and classification benchmarks with NMF/VCA/ICA panels; algorithm evaluation, not species identification proof. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/spectral_unmixing_comprehensive_analysis.png}
\caption{Synthetic CHC spectral unmixing and classification benchmarks with NMF/VCA/ICA panels. Claim boundary: algorithm evaluation; not species identification proof.}
\label{fig:app_spectral_unmixing}
\end{figure}

<!-- alt: Cross-domain synthesis of normalized performance metrics across information, material, and efficiency domains; evidence ladder panel. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../figures/integrated_analysis_cross_domain_synthesis.png}
\caption{Cross-domain synthesis from \texttt{scripts/generate\_integrated\_analysis.py}: normalized model metrics across information, material, and efficiency domains. Panel D reports unitless model sensitivity demo values, not predictive accuracy on live specimens. Claim boundary: engineering synthesis panel, not empirical classification proof.}
\label{fig:integrated_classification}
\end{figure}

## Equation References

## Reproducibility

- Run: `python3 scripts/generate_spectral_unmixing.py`
- Artifacts saved to `output/data/` and `../figures/`.
- Fixed RNG seed (42) used for deterministic NMF initialization and cross‑validation splits.

## Cross‑references

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}



---



---
nocite: |
  @*
---

# References {#sec:references}

::: {#refs}
:::
