# Tests — CohereAnts

Pytest suite over `src/` with **no mocks**. Configuration and the ≥90% coverage gate live in
`pyproject.toml` (`pythonpath`, `coverage.source = ["src"]`, `fail_under = 90`).

## Run

```bash
# Template root (authoritative):
uv run python scripts/01_run_tests.py --project cohereants --project-only

# Project directory:
cd path/to/cohereants
MPLBACKEND=Agg uv run pytest tests/ --cov=src --cov-report=term-missing
```

## Layout

- `conftest.py` — shared fixtures (real numpy data, temp paths)
- `test_insect_analysis.py` — facade + comprehensive analysis integration
- `test_case_studies.py`, `test_case_study_renders.py` — appendix compute/render contracts
- `test_integration.py`, `test_visualization.py`, `test_sensilla.py`, … — domain coverage
- `test_glossary_gen_parse.py`, `test_glossary_gen_output.py` — glossary generation
- `test_figure_outputs.py`, `test_manuscript_registry.py` — registry and artifact contracts

## Policy

- Use `tmp_path` for file I/O; fixed seeds for deterministic numerics.
- Do not add `unittest.mock`, `patch`, or conftest coverage-theater classes.
- Target ≥90% on `src/`; add real edge-case tests in the domain module that owns the behavior.
