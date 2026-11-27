# AGENTS.md — CohereAnts

Agent guide for **CohereAnts** (display name). Pipeline / folder id: `cohereants`.
Read with the workspace-level `AGENTS.md` one directory above this repository.

## Naming

| Context | Value |
| --- | --- |
| Display name | CohereAnts (Cohere + Ants) |
| Pipeline / folder / pyproject id | `cohereants` |
| Upstream provenance | [`github.com/docxology/cohereants`](https://github.com/docxology/cohereants) |

## What this is

Engineering remediation of the cohereants science codebase into the template two-layer
structure. Business logic in `src/`; thin `scripts/` orchestrators; manuscript with
registry-backed `{{TOKEN}}` injection and `data/claim_ledger.yaml`. Ideal-State Artifact:
[`ISA.md`](docs/project/ISA.md). Documentation hub: [`docs/`](docs/).

## Invariants

- **Thin orchestrator.** Algorithms only in `src/`. Scripts coordinate I/O and print paths.
- **No mocks** in tests (`unittest.mock`, `patch`, etc. forbidden).
- **Coverage ≥90%** on `src/` (`pyproject.toml` `fail_under = 90`).
- **numpy 2.x:** use `np.trapezoid` or module `_trapezoid` shims.
- **CWD-independence:** resolve paths from `__file__` / project root in tests.
- **Local rendering:** register a disposable checkout as `projects/working/cohereants` in the pinned Template checkout.

## Run

```bash
# From the CohereAnts checkout:
uv sync --locked --python 3.13 --extra dev
MPLBACKEND=Agg uv run pytest tests/ --cov=src --cov-report=term-missing

# Manuscript variables (allow draft when outputs missing):
uv run python scripts/z_generate_manuscript_variables.py --allow-draft
```

## Layout

```
src/                 domain modules (core, figures, integrated_figures, viz/, case_studies/, …)
tests/               zero-mock pytest over src/
scripts/             generate_*.py, run_all_case_studies.py, z_generate_manuscript_variables.py
docs/manuscript/          NN_*.md + config.yaml + AGENTS.md
data/claim_ledger.yaml   evidence registry numeric claims
docs/                maintained guides and manuscript
ISA.md               verification block + phase status
```

## Visualization

| Module | Role |
| --- | --- |
| `src/viz/styling.py` | `PlotStyler`, palette helpers, `set_plot_style` |
| `src/viz/panels.py` | Shared panel builders (correlation, receptor specificity, behavioral panels) |
| `src/viz/appendix_grid.py` | Shared 12-panel appendix renderer (`PanelSpec`, `render_labeled_grid`) |
| `src/viz/figure_helpers.py` | Registry metadata + `format_appendix_caption` templates |
| `src/viz/advanced.py` | `AdvancedVisualizer`, `create_publication_figure` (canonical advanced plotting) |
| `src/visualization.py` | Deprecated shim re-exporting `viz.advanced` + `viz.styling` |
| `src/figures/` | Manuscript figure package (`generate_core_manuscript_figures`) |
| `src/integrated_analyzer_figures.py` | Matplotlib-only `IntegratedAnalyzer` figure builders |
| `src/integrated_figures.py` | Manuscript integrated-analysis figure orchestration |
| `src/case_studies/*/figures.py` | Appendix-specific panel specs (compute stays in `core.py` / `compute.py`) |

- **Case studies:** each appendix is a package (`compute.py`, `types.py`, `figures.py`, optional split `core.py` helpers).
- **Scripts:** call `compute_*` → `render_comprehensive_figure` → `format_appendix_caption` → `write_figure_bundle_from_script`.
- **Integrated analysis:** `IntegratedAnalyzer` is numpy/report only; plotting delegates to `integrated_analyzer_figures`.

## Scripts (current)

| Script | Role |
| --- | --- |
| `generate_research_figures.py` | Core figures via `src/figures/` + registry |
| `generate_integrated_analysis.py` | Integrated panels via `src/integrated_figures.py` |
| `generate_*` (appendices A–G) | Case-study orchestrators; `write_figure_bundle_from_script()` writes `.caption.txt` + `.alt.txt` |
| `run_all_case_studies.py` | Runs appendix generators |
| `z_generate_manuscript_variables.py` | Writes `output/data/manuscript_variables.json` |

Use the [pinned rendering guide](docs/rendering_pipeline.md) for PDF and HTML.
