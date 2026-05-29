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

Model outputs indicate improvement factors of $\approx {{IMPROVEMENT_FACTOR_LOW}}\text{--}{{IMPROVEMENT_FACTOR_HIGH}}\times$ when the hypothetical IR-detection term is set below slower diffusion-dominated terms. This is a sensitivity result: it identifies the timing regime an IR pathway would need to occupy, rather than proving that the pathway exists.

See \Cref{fig:response_time_comparison} for the comparison.

<!-- alt: Response-time constraint map comparing insect ORN latencies, slower model terms, and a hypothetical IR-stage target; engineering bounds, not biological proof. -->
\begin{figure}[h]
\centering
\includegraphics[width={{FIGURE_WIDTH_RESPONSE_TIME}}\textwidth]{../output/figures/response_time_comparison.png}
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
- **Beam Width**: {{BEAM_WIDTH_LOW_DEG}}--{{BEAM_WIDTH_HIGH_DEG}}$^{\circ}$ half-power beamwidth
- **Front-to-Back Ratio**: 10-20 dB directional selectivity
- **Gain Pattern**: Maximum sensitivity in the forward direction

**Behavioral validation**: Experimental studies show localization accuracy of $\pm 15\text{--}30^{\circ}$ in wind-tunnel assays, which is consistent with antenna-like gain patterns having 15-30$^{\circ}$ half-power beamwidths. However, these studies used chemical gradients, so controlled IR-only assays are required to disambiguate electromagnetic detection from volatile plume structure. See array directionality case study in \Cref{sec:app_sensilla_array}. We provide minimal falsifiers in the Discussion.

### Specialized Infrared Sensors

Pyrophilous beetles provide the clearest insect precedent for specialized IR organs. Schmitz et al. described photomechanic Golay-cell transduction in *Melanophila acuminata*; Evans modeled the organ thermopneumatically; Siebke et al. translated it into a biomimetic sensor concept [@schmitz2011infrared; @evans2005thermopneumatic; @siebke2014biomimetic]. Convergent photomechanic sensilla occur in *Aradus* flat bugs [@schmitza2010aradus], while *Acanthocnemus nigricans* uses a microbolometer disc organ [@schmitz2002acanthocnemus; @kreiss2007acanthocnemus]. *Merimna atrata* abdominal organs were reinterpreted as landing-hazard avoidance sensors rather than fire attractors [@schmitz2012merimna].

**Sensor Characteristics** (plasmonic/geometry links in \Cref{sec:app_plasmonic_geometry}):

- **Species**: *Melanophila acuminata*, *Acanthocnemus nigricans*, *Aradus* spp., *Merimna atrata*
- **Evolutionary Origin**: Mechanosensory or thermosensory sensilla modified for radiant-energy detection (photomechanic or microbolometer)
- **Detection Range**: {{BIOMIMETIC_IR_BAND_UM}} infrared wavelengths (literature-anchored *Melanophila* band)
- **Response Threshold**: ${{BIOMIMETIC_THRESHOLD_MW_CM2}}\,\mathrm{mW}/\mathrm{cm}^2$ (electrophysiology literature range)
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
\includegraphics[width={{FIGURE_WIDTH_COMPOSITE}}\textwidth]{../output/figures/composite_cross_domain_overview.png}
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
