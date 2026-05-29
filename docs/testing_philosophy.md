# Testing Philosophy: Zero-Mock Standard

**cohereants** follows the Research Project Template contract: tests exercise real numpy/scipy/matplotlib code paths with no mock frameworks.

## Why Zero Mocks?

Insect IR models combine atmospheric transmission, sensilla geometry, and neural timing constraints. Tests must call real `src/` functions so regressions in unit handling, window models, or ROC construction surface immediately.

**Rule of thumb:** If you reach for `MagicMock`, move I/O to `scripts/` and test the pure function in `src/` with real arrays.

## Coverage Gate

| Setting | Value |
| --- | --- |
| Target | `src/` |
| Minimum | **90%** (`fail_under = 90` in `pyproject.toml`) |
| Branch coverage | Enabled |
| Runner | Project env via `uv run` (template) or project `.venv` (direct) |

**Authoritative gate from template root** (uses `uv run --directory` for project deps such as `scikit-learn`):

```bash
uv run python scripts/01_run_tests.py --project cohereants --project-only
```

**Direct gate (project directory):**

```bash
cd /path/to/cohereants
uv sync
MPLBACKEND=Agg uv run pytest tests/ --cov=src --cov-fail-under=90 --cov-report=term-missing
```

A green exit with **0 tests collected** is not a pass. Confirm collected count > 0 and coverage ≥ 90%.

## Domain Test Layout

Coverage is organized by domain module, not `test_coverage_*` shards:

| Area | Primary test modules |
| --- | --- |
| Case-study appendices | `tests/test_case_studies.py`, `tests/test_case_study_renders.py` |
| Integrated analysis | `tests/test_integration.py` |
| Visualization | `tests/test_visualization.py`, `tests/test_visualization_edge_cases.py` |
| Sensilla / array | `tests/test_sensilla.py` |
| Behavioral | `tests/test_behavioral_analysis.py` |
| Insect pipeline | `tests/test_insect_analysis.py` |
| Glossary generation | `tests/test_glossary_gen_parse.py`, `tests/test_glossary_gen_output.py` |

Appendix compute/render contracts are parametrized in `test_case_study_typed_compute_contract` (typed dataclass + `.as_dict()` export).

## Audit Commands

```bash
# No mocks in src/ or tests/
rg -n 'unittest\.mock|MagicMock|mocker\.patch' src/ tests/ --glob '!tests/README.md'

# Module size bar (src/)
find src -name '*.py' -exec wc -l {} + | awk '$1>500'
```

## Test Environment

`tests/conftest.py` must:

- Set `MPLBACKEND=Agg` before matplotlib import
- Add project `src/` to `sys.path`
- Resolve paths from `__file__`, not process CWD (template runs pytest from repo root)

## Zero-Mock Checklist

Before submitting a test:

- [ ] Uses real numpy/scipy arrays or on-disk fixtures under `tests/` or `output/data/`
- [ ] Calls `src/` functions directly
- [ ] Asserts numerical or structural properties, not call counts
- [ ] No `unittest.mock`, `MagicMock`, `@patch`, or fake return injection
- [ ] Timing assertions use bounds, not exact wall-clock values

## Structural Rule

| Code location | Testing approach |
| --- | --- |
| `src/case_studies/*/compute.py`, core modules | Unit tests with analytic or fixture inputs |
| `src/figures/`, integrated pipelines | Integration tests; write to `tmp_path` when needed |
| `scripts/*.py` | Subprocess or import-and-run smoke with real small configs |

## Running Subsets

```bash
# Fast iteration on one module
MPLBACKEND=Agg uv run pytest tests/test_core.py -v

# Skip slow integration if marked
MPLBACKEND=Agg uv run pytest tests/ -m "not slow" -q
```

## See Also

- [`troubleshooting.md`](troubleshooting.md) — Coverage failures and 0-test false positives
- [`agent_instructions.md`](agent_instructions.md) — Rule 2 (coverage gate)
- [`../pyproject.toml`](../pyproject.toml) — `[tool.coverage.*]` settings
