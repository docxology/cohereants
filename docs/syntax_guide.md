# Syntax Guide

Manuscript syntax for **cohereants**: `{{TOKEN}}` variable injection, LaTeX figure cross-references, and registry-backed validation.

---

## 1. Variable Injection (`{{TOKEN}}`)

Dynamic numeric or typeset values use doubled-brace tokens. Values come from `src/manuscript_variables.py::generate_variables()` and are written to:

- `output/data/manuscript_variables.json`
- `output/manuscript/*.md` (substituted copies)

**BAD:** The operating SNR was 10 dB.  
**GOOD:** The operating SNR was {{SNR_OPERATING_DB}} dB.

Never hard-code values that change when analysis outputs or `manuscript/config.yaml` change.

### Authoritative token list

Treat **`generate_variables()`** as source of truth. Illustrative tokens:

| Token | Description | Source |
| --- | --- | --- |
| `{{PROJECT_TITLE}}` | Paper title | `manuscript/config.yaml` |
| `{{RANDOM_SEED}}` | Reproducibility seed | `metadata.random_seed` |
| `{{IMPROVEMENT_FACTOR_LOW}}` | Response-time improvement lower bound | `output/data/response_time_comparison.npz` |
| `{{IMPROVEMENT_FACTOR_HIGH}}` | Response-time improvement upper bound | same |
| `{{BEAM_WIDTH_LOW_DEG}}` | Sensilla beam width lower bound | `sensilla_data.npz` or defaults |
| `{{BEAM_WIDTH_HIGH_DEG}}` | Sensilla beam width upper bound | same |
| `{{LOCALIZATION_ACCURACY_DEG}}` | Formatted degree range | derived |
| `{{BIOMIMETIC_IR_BAND_UM}}` | Biomimetic IR band (µm) | `src/manuscript_fixtures.py` |
| `{{BIOMIMETIC_THRESHOLD_MW_CM2}}` | Response threshold range | fixtures |
| `{{PROTOCOL_QCL_BAND_UM}}` | QCL band protocol range | fixtures |
| `{{PROTOCOL_POWER_DENSITY_MW_CM2}}` | IR power density protocol | fixtures |
| `{{PROTOCOL_MIN_N}}` | Minimum pre-registered N | fixtures |
| `{{PROTOCOL_THERMAL_CONTROL}}` | Thermal control wording | fixtures |
| `{{SNR_OPERATING_DB}}` | Operating SNR | NPZ + `detection_limits_spec.json` |
| `{{FIGURE_WIDTH_RESPONSE_TIME}}` | LaTeX width **fraction** for timing figure (manuscript appends `\textwidth`) | constants (`1.0`) |
| `{{FIGURE_WIDTH_COMPOSITE}}` | LaTeX width **fraction** for composite figure | constants (`0.95`) |
| `{{GENERATED_AT_UTC}}` | ISO timestamp | generated at run time |

### Adding a token

1. Add key in `generate_variables()` in `src/manuscript_variables.py`.
2. Add assertion in `tests/test_manuscript_variables.py`.
3. Reference as `{{NEW_TOKEN}}` in `manuscript/*.md`.
4. Run `scripts/z_generate_manuscript_variables.py`.

### Detect unresolved tokens

```bash
grep -r "{{" output/manuscript/ 2>/dev/null && echo "UNRESOLVED" || echo "OK"
```

---

## 2. Figure Cross-References

cohereants manuscript sections use **LaTeX** figure environments embedded in markdown, not Pandoc `[@fig:label]` syntax.

**Pattern in manuscript:**

```markdown
<!-- alt: One-sentence accessibility description; claim boundary. -->
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/response_time_comparison.png}
\caption{...}
\label{fig:response_time_comparison}
\end{figure}
```

**Width tokens:** manuscript uses `\includegraphics[width={{FIGURE_WIDTH_COMPOSITE}}\textwidth]{...}`. Tokens supply only the numeric fraction (`0.95`), not `\textwidth`.

**Alt text:** place `<!-- alt: ... -->` **immediately before** `\begin{figure}`. HTML comments inside `\begin{figure}...\end{figure}` pass through to `.tex` and break xelatex.

**Inline math in Markdown lists:** use `$...$`, not `\(...\)`, in `- **Label**: ...` list items. Pandoc converts `\(...\)` in lists to broken text-mode `\mathrm` and triggers `\mathrm allowed only in math mode`.

**Prose unit tokens:** `{{PROTOCOL_QCL_BAND_UM}}` and `{{BIOMIMETIC_IR_BAND_UM}}` resolve to Unicode µm ranges (e.g. `2--25 µm`) safe outside math mode.

**Prose reference:** `\Cref{fig:response_time_comparison}` (requires `cleveref` in `preamble.md`).

Do not hard-code "Figure 3" — use `\Cref{fig:…}` so numbering stays correct.

---

## 3. Figure Label Registry

`output/figures/figure_registry.json` maps each `\label{fig:…}` to a PNG and generation method. Labels registered in `src/figure_registry_builder.py`:

| Label | PNG file (under `output/figures/`) |
| --- | --- |
| `fig:atmospheric_transmission` | `atmospheric_transmission.png` |
| `fig:sensilla_wavelength_matching` | `sensilla_wavelength_matching.png` |
| `fig:chc_spectra_example` | `chc_spectra_example.png` |
| `fig:response_time_comparison` | `response_time_comparison.png` |
| `fig:empirical_ir_axes` | `empirical_ir_axes.png` |
| `fig:composite_cross_domain_overview` | `composite_cross_domain_overview.png` |
| `fig:app_detection_limits` | `detection_limits_comprehensive_analysis.png` |
| `fig:app_env_channel` | `environmental_channel_comprehensive_analysis.png` |
| `fig:integrated_info` | `integrated_analysis_information_analysis.png` |
| `fig:app_neural_encoding_full` | `neural_encoding_comprehensive_analysis.png` |
| `fig:app_plasmonic_sweep` | `plasmonic_geometry_comprehensive_analysis.png` |
| `fig:integrated_metamaterial` | `integrated_analysis_metamaterial_properties.png` |
| `fig:app_sensilla_beam` | `sensilla_array_comprehensive_analysis.png` |
| `fig:app_spectral_unmixing` | `spectral_unmixing_comprehensive_analysis.png` |
| `fig:integrated_classification` | `integrated_analysis_cross_domain_synthesis.png` |
| `fig:integrated_summary` | `integrated_analysis_summary.png` |
| `fig:app_active_inference` | `active_inference_trajectory.png` |

Generation methods are documented in `src/figure_registry_contract.py::_FIGURE_METHODS`.

---

## 4. Citations

Use Pandoc citekeys `[@authorYearKeyword]` with entries in `manuscript/references.bib`. Prefer primary entomology, spectroscopy, and olfaction literature — the upstream manuscript was rebuilt with DOI-verified sources.

---

## 5. Section Anchors

Unnumbered sections use `{#sec:…}` on headings, e.g. `# Abstract {#sec:abstract}`, and `\Cref{sec:methodology}` in prose.

---

## 6. Markdown Links

Use descriptive link text. Internal references to code should name the module path: `` `src/sensilla.py` ``.

---

## See Also

- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — Figure tokens, VAR policy, claims
- [`rendering_pipeline.md`](rendering_pipeline.md) — Hydration and render order
- [`output_conventions.md`](output_conventions.md) — Registry file location
