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
