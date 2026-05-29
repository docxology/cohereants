# Frequently Asked Questions

## Project lifecycle

### Why is cohereants passive?

The project is stored under `projects/passive/cohereants` in the private lifecycle repo. Passive projects symlink into `template/projects_in_progress/` for inspection and targeted pipeline runs but are **not** auto-discovered like `active/` projects. Promote to `active/` when default rendering and menu discovery are desired.

### Where do I commit changes?

Commit in `path/to/cohereants/`, not in the public `template/` repository. The public repo must never track `projects/cohereants/`.

### How does the pipeline find the project?

`resolve_project_root(template_root, "cohereants")` returns `projects_in_progress/cohereants` when the symlink exists and `projects/cohereants` is absent or lacks source markers. Commands always use `--project cohereants`.

## Architecture

### What is the thin orchestrator pattern?

`scripts/` import computation from `src/`, set `MPLBACKEND=Agg`, write PNG/NPZ under `output/`, and print paths. They do not implement atmospheric models, sensilla antenna math, or ROC logic inline.

### Can `src/` import from `infrastructure/`?

Orchestration modules (`manuscript_variables.py`, figure registry writers) may import template utilities behind try/except. Core biophysics modules should stay importable with only numpy/scipy/sklearn/matplotlib for unit tests.

### Why is the vibrational theory described as contested?

Empirical receptor-level evidence remains disputed. The codebase is a **falsification framework** for IR-associated olfactory hypotheses, not a proof of biological IR olfaction. See [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) for claim policy.

## Testing

### Why zero mocks?

Mocks certify call wiring, not whether `calculate_atmospheric_transmission()` or detection-limit ROC code returns correct arrays. New tests use real computation.

### What about legacy mock tests?

Upstream port debt — see [`ISA.md`](../ISA.md). Refactor over time; do not extend mock usage.

### Can I lower the 90% coverage gate?

No. Add tests for uncovered `src/` lines instead.

## Manuscript and outputs

### What are `{{TOKEN}}` variables?

Placeholders like `{{SNR_OPERATING_DB}}` substituted by `scripts/z_generate_manuscript_variables.py` from `src/manuscript_variables.py`. Never hard-code values that change when analysis re-runs.

### Where is the token list defined?

Authoritative: `src/manuscript_variables.py::generate_variables()`. Reference table: [`syntax_guide.md`](syntax_guide.md).

### How do figures work?

Manuscript uses LaTeX `\includegraphics` + `\label{fig:…}` and `\Cref{fig:…}`. `output/figures/figure_registry.json` maps labels to PNG paths and generation methods for validation.

### Where does the PDF live?

Working copy: `output/pdf/cohereants_combined.pdf` under the project tree. After copy stage: `template/output/cohereants/pdf/`.

## Common pitfalls

### I edited `output/figures/*.png` by hand

Changes are lost on the next pipeline run. Edit `src/figures.py` or the relevant case study module.

### I used "CohereAnts" in a script flag

Standardize on **`cohereants`** for `--project`, directory names, and documentation commands.

### Analysis ran but registry validation failed

Re-run figure generation so `figure_registry.json` includes every `\label{fig:…}` used in manuscript appendices. Update `src/figure_registry_builder.py` when adding labels.

## See Also

- [`quickstart.md`](quickstart.md)
- [`troubleshooting.md`](troubleshooting.md)
- [`architecture.md`](architecture.md)
