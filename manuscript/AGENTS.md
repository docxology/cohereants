---
title: "Manuscript directory: cohereants"
type: "manuscript_guide"
version: "1.0"
---

# Manuscript (`manuscript/`)

Agent rules for the **cohereants** engineering monograph on insect infra-red perception and biomimetic sensor design. Repository-wide constraints: [`../docs/agent_instructions.md`](../docs/agent_instructions.md).

## Scope

The manuscript presents the vibrational/IR olfaction hypothesis as **under investigation**, integrates comparative entomology and spectroscopy literature, and documents computational artifacts (figures, protocols, appendices). It does not claim biological IR olfaction is established.

## File Inventory (pattern)

| Pattern | Role |
| --- | --- |
| `00_abstract.md` | Abstract, keywords, reproducibility pointer |
| `01_introduction.md` | Hypothesis framing, literature context |
| `02_methodology.md` | Models, sensilla, atmospheric channels |
| `03_experimental_results.md` | Core results figures (`fig:response_time_comparison`, `fig:composite_cross_domain_overview`) |
| `04_discussion.md` | Interpretation with claim boundaries |
| `05_conclusion.md` | Falsifiable predictions |
| `06_mathematical_appendix.md` | Equations |
| `07_empirical_studies.md` | Empirical anchor summary |
| `08_ant_stack.md` | Layered ant model narrative |
| `09_symbols_glossary.md` | Notation |
| `10_appendix_active_inference.md` … `16_appendix_spectral_unmixing.md` | Case-study appendices |
| `config.yaml` | Title, authors, metadata, LLM flags |
| `preamble.md` | LaTeX packages (`cleveref`, math, figures) |
| `references.bib` | DOI-verified bibliography |

**Combined PDF:** `discover_manuscript_files()` includes **18** top-level section files (`00_`–`16_`, `99_references.md`). Not in the combined body: `preamble.md` (LaTeX preamble injection), `AGENTS.md`, `config.yaml`, `references.bib`. `01_introduction.md` opens with prose (no H1).

## {{VAR}} / `{{TOKEN}}` Protocol

Numeric or protocol-bound prose must use **`{{TOKEN}}`** syntax resolved by:

1. `scripts/z_generate_manuscript_variables.py`
2. `src/manuscript_variables.py::generate_variables()`
3. `output/data/manuscript_variables.json`
4. `output/manuscript/*.md` substituted copies consumed by PDF render

### VAR tokens (registry)

Authoritative list: **`src/manuscript_variables.py::generate_variables()`**. See [`../docs/syntax_guide.md`](../docs/syntax_guide.md) for the reference table.

**Policy:**

- Config- and fixture-derived tokens (`{{PROTOCOL_*}}`, `{{BIOMIMETIC_*}}`) may use defaults when `--allow-draft` is set.
- Measurement tokens (`{{SNR_OPERATING_DB}}`, `{{IMPROVEMENT_FACTOR_*}}`) must come from analysis NPZ/JSON when publishing.
- Do not hand-edit substituted files under `output/manuscript/`.

**Adding a VAR token:**

1. Implement in `generate_variables()`.
2. Test in `tests/test_manuscript_variables.py`.
3. Use in manuscript as `{{NEW_TOKEN}}`.
4. Re-run hydration script.

## Citation policy

- **`references.bib`**: DOI-verified primary sources only; cite via `[@citekey]` in manuscript markdown.
- **§07 empirical studies**: three-axis IR framework (active detection, passive cuticle, applied spectroscopy); expanded 2026-05-26 scholarship integration (~45 citekeys).
- **Press releases**: prefer peer-reviewed follow-ups (e.g. *Merimna* hazard avoidance → `@schmitz2012merimna`, not news pages alone).
- **Claim boundaries**: pyrophilous/MIR organs, mosquito thermal IR, and cycad pollination IR are radiant-cue precedents—not proof of semiochemical IR olfaction in ordinary sensilla.

## Figure Protocol

Figures use LaTeX `\includegraphics` + `\label{fig:…}` + `\Cref{fig:…}` in prose.

### LaTeX / Pandoc rules

1. **Alt text before figures:** `<!-- alt: ... -->` on the line immediately above `\begin{figure}` — never between `\begin{figure}` and `\includegraphics`.
2. **List math:** in Markdown bullet lists, use `$...$` for micrometers and units; `\(...\)` breaks under Pandoc and yields `\mathrm` outside math mode in the PDF.
3. **Figure width tokens:** `{{FIGURE_WIDTH_*}}` values are fractions only (`1.0`, `0.95`); the manuscript template appends `\textwidth`.
4. **Page geometry:** `\usepackage[margin=0.2in]{geometry}` in `preamble.md` overrides the Layer 1 default 0.75in injection.
5. **Code fences:** use plain `um` in Python comment lines, not `\(\mu\mathrm{m}\)`.

Regression tests: `tests/test_manuscript_latex_safety.py`, `tests/test_manuscript_variables.py`, and `@pytest.mark.requires_latex` checks in `tests/test_pdf_compile_smoke.py`.

### Figure tokens (labels)

Each manuscript figure label must appear in **`output/figures/figure_registry.json`**, built by `src/figure_registry_builder.py`.

| Label | Typical section | Generator domain |
| --- | --- | --- |
| `fig:atmospheric_transmission` | Methodology / results | `src/core.py`, `src/figures.py` |
| `fig:sensilla_wavelength_matching` | Methodology | `src/sensilla.py` |
| `fig:chc_spectra_example` | Methodology | `src/spectroscopy.py` |
| `fig:response_time_comparison` | `03_experimental_results.md` | `src/core.py` timing maps |
| `fig:composite_cross_domain_overview` | Results | `src/figures.py` evidence ladder |
| `fig:empirical_ir_axes` | `07_empirical_studies.md` | `src/figures.py` three-axis synthesis |
| `fig:app_detection_limits` | Appendix detection limits | `src/case_studies/detection_limits` |
| `fig:app_env_channel` | Appendix environmental channel | environmental case study |
| `fig:integrated_info` | Appendix | integrated analysis |
| `fig:app_neural_encoding_full` | Appendix neural encoding | neural encoding case study |
| `fig:app_plasmonic_sweep` | Appendix plasmonic | plasmonic geometry |
| `fig:integrated_metamaterial` | Appendix | integrated metamaterial panel |
| `fig:app_sensilla_beam` | Appendix sensilla array | sensilla array case study |
| `fig:app_spectral_unmixing` | Appendix spectral unmixing | spectral unmixing |
| `fig:integrated_classification` | Appendix spectral unmixing | `integrated_analysis_cross_domain_synthesis.png` |
| `fig:integrated_summary` | Integrated analysis bundle | `integrated_analysis_summary.png` |
| `fig:app_active_inference` | Appendix active inference | active inference demo |

Captions include a **generation method** sentence and validation note per `src/figure_registry_contract.py`. Generators call `src.figure_artifacts.save_figure_bundle()` (core/integrated) or `scripts/_utils.write_figure_bundle_from_script()` (appendix thin orchestrators) with `label`, `claim_boundary`, and `alt_text`. Core manuscript figures render at **600 DPI**; appendix case-study scripts use **300 DPI**. Registry `metadata.alt_text` stores full WCAG-oriented alt strings from `.alt.txt` sidecars.

### Adding a figure

1. Implement generator in `src/figures.py` or `src/case_studies/`.
2. Wire thin script under `scripts/`.
3. Add label → filename mapping in `src/figure_registry_builder.py` and methods/alt text in `figure_registry_contract.py` / `viz/figure_helpers.py`.
4. Add LaTeX figure block and `\Cref{fig:…}` references in manuscript.
5. Regenerate figures and registry; run output validation.

## Engineering Claim Policy

1. **Hypothesis, not fact.** Wording must remain consistent with `domain_profile.yaml` `llm_prompt_guidance` and the abstract's contested-framing.
2. **Registry-backed numbers.** Quantitative claims in results sections use `{{TOKEN}}` or cite generated tables/figures — not literals copied from older drafts.
3. **Claim ledger.** Structured numeric claims for evidence validation live in `data/claim_ledger.yaml`. New binding claims require ledger entries with `artifact_path` and `source_tier`.
4. **Figure boundaries.** Registry metadata includes `claim_boundary` (e.g. sensor feasibility vs biological proof). Do not override in prose.
5. **Understated tone.** Avoid promotional adjectives; state what the model assumes and what would falsify it.
6. **Building on prior work.** Related work extends and juxtaposes citations; avoid oppositional "against" framing unless reviewing specific evidence.

## Section Modification Workflow

1. Edit source `manuscript/*.md` (not `output/manuscript/`).
2. Update `src/` and tests if models change.
3. Regenerate figures: `scripts/generate_research_figures.py`, case-study scripts.
4. Hydrate variables: `scripts/z_generate_manuscript_variables.py`.
5. Verify: `grep -r "{{" output/manuscript/ || echo OK`
6. Render from template root: `uv run python scripts/03_render_pdf.py --project cohereants`.
7. Validate: `uv run python scripts/04_validate_output.py --project cohereants`.

## Passive / WIP Note

While the project stays in `passive/`, manuscript work commits to the private repo. Pipeline rendering uses `projects_in_progress/cohereants` via `resolve_project_root()` when symlinked.

## See Also

- [`../docs/syntax_guide.md`](../docs/syntax_guide.md) — Full token and label tables
- [`../docs/rendering_pipeline.md`](../docs/rendering_pipeline.md) — PDF pipeline
- [`../docs/style_guide.md`](../docs/style_guide.md) — Prose tone
- [`../data/claim_ledger.yaml`](../data/claim_ledger.yaml) — Evidence bindings
- [`../domain_profile.yaml`](../domain_profile.yaml) — Validation gates
