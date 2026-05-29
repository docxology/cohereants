# Quick Start

Minimal path to run tests and regenerate figures for **cohereants**. The project is **passive / WIP**: it lives in the private repo and is symlinked under `template/projects_in_progress/cohereants` for pipeline work. It is not in default `./run.sh` discovery until promoted to `active/`.

## Prerequisites

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) at the template repo root
- Symlink synced: `./run.sh` or `uv run python -m infrastructure.orchestration link-projects --dry-run`
- Project-local venv with scientific extras

## One-Time Setup

```bash
# Private repo (canonical)
cd path/to/cohereants
uv sync --extra dev

# Or from template checkout via symlink
cd /path/to/template/projects_in_progress/cohereants
uv sync --extra dev
```

## Run Tests (90% Gate)

From **template root** (authoritative for CI parity):

```bash
uv run python scripts/01_run_tests.py --project cohereants --project-only
```

From **project directory**:

```bash
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-fail-under=90 -v
```

Confirm **tests collected > 0** and coverage ≥ 90%.

## Generate Core Figures

```bash
cd path/to/cohereants
MPLBACKEND=Agg .venv/bin/python scripts/generate_research_figures.py
```

Each script prints output paths to stdout for manifest collection.

## Hydrate Manuscript Variables

Requires analysis NPZ files unless drafting:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py
# Early draft without full analysis:
MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py --allow-draft
```

## Core-Only Pipeline (Template Root)

```bash
cd /path/to/template
uv run python scripts/execute_pipeline.py --project cohereants --core-only
```

Uses `resolve_project_root()` to find `projects_in_progress/cohereants`.

## View Results

| Artifact | Path |
| --- | --- |
| Combined PDF | `output/pdf/cohereants_combined.pdf` |
| Figure registry | `output/figures/figure_registry.json` |
| Variable map | `output/data/manuscript_variables.json` |
| Test report | `output/reports/test_results.json` |

## Command Reference

| Task | Command |
| --- | --- |
| Project tests | `uv run python scripts/01_run_tests.py --project cohereants --project-only` |
| Core figures | `MPLBACKEND=Agg .venv/bin/python scripts/generate_research_figures.py` |
| Case studies | `MPLBACKEND=Agg .venv/bin/python scripts/run_all_case_studies.py` |
| Variables | `MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py` |
| Render PDF | `uv run python scripts/03_render_pdf.py --project cohereants` |
| Clean outputs | `rm -rf output/` |

## Next Steps

- Read [`docs/agent_instructions.md`](agent_instructions.md) before editing code
- Read [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) before editing prose
- See [`../ISA.md`](../ISA.md) for remediation backlog and ideal state

## See Also

- [`docs/README.md`](README.md) — Full documentation hub
- [`troubleshooting.md`](troubleshooting.md) — Common failures
