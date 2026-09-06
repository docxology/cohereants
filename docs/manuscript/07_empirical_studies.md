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

- **Implication for CohereAnts**: Pyrophilous organs establish that insect MIR detection evolves under fire-associated ecology. They are anatomical and transduction precedents for biomimetic bands {{BIOMIMETIC_IR_BAND_UM}} and literature thresholds {{BIOMIMETIC_THRESHOLD_MW_CM2}} mW/cm²—not evidence for semiochemical IR olfaction in ordinary sensilla.
- **Code anchors**: `src/case_studies/plasmonic_geometry.py`; `src/case_studies/detection_limits.py`.

### Hematophagy and Host-Finding

Chandel et al. showed that *Aedes aegypti* uses thermal IR near skin temperature as a host-seeking cue when combined with CO₂ and odor; TRPA1 in antennal neurons is required [@chandel2024thermal]. Corfas and Vosshall linked AaegTRPA1 to selective thermotaxis toward host-temperature targets [@corfas2015trpa1].

*Rhodnius prolixus* lacks specialized IR organs but discriminates radiant IR from convective heat via combinatorial coding of peg-in-pit (PSw) and tapered-hair (THw) warm cells; forced convection disrupts the response quotient [@zopf2014infrared; @zopf2015convection]. Lazzari reviewed how physics shapes hematophagous orientation: radiant IR operates at longer range than convective heat within ~10 cm of the host [@lazzari2009orientation].

- **Implication for CohereAnts**: Mosquito and kissing-bug studies motivate thermal-IR protocol separation ({{MOSQUITO_IR_SOURCE_TEMP_C}} °C blackbody, peak ~{{MOSQUITO_IR_PEAK_UM}} µm) and Rhodnius-style controls that distinguish T oscillations from IR power.
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
\includegraphics[width=0.95\textwidth]{../output/figures/empirical_ir_axes.png}
\caption{Three-axis schematic of insect IR biology synthesized from the comparative table above. Active photomechanic organs anchor biomimetic bands {{BIOMIMETIC_IR_BAND_UM}} and thresholds {{BIOMIMETIC_THRESHOLD_MW_CM2}}~mW/cm²; passive cuticle/thermosensory pathways set background IR context; applied spectroscopy validates discriminative structure without demonstrating in vivo semiochemical IR olfaction. Claim boundary: literature synthesis, not new empirical measurement.}
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
