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

- Biomimetic uncooled IR sensors informed by pit-organ and sensilla geometry (bands {{BIOMIMETIC_IR_BAND_UM}}, thresholds {{BIOMIMETIC_THRESHOLD_MW_CM2}} mW/cm²) [@siebke2014biomimetic].
- Pest-monitoring assay design with wavelength-specific stimulation and thermal controls.
- Channel-capacity and detection-limit estimates from `src/case_studies/environmental_channel.py` and `src/case_studies/detection_limits.py` as engineering upper bounds.

Quantum-coherence and broad quantum-biology claims remain out of scope; the framework focuses on measurable sensor bounds and preregistered protocols.

## Reproducibility

The Appendices and `src/` modules provide computational anchors for every figure label in the registry. Independent groups can regenerate artifacts via `./run.sh --project cohereants --core-only` or the documented script entry points, then validate outputs against `output/figures/figure_registry.json`.
