# AI Agent Instructions — cohereants

Read this file before modifying **cohereants**. Pair with [`../AGENTS.md`](../AGENTS.md), [`../ISA.md`](../ISA.md), and the template root agent docs when running pipeline stages.

---

## Rule 1: Read the Hub First

| Document | Governs |
| --- | --- |
| **This file** | All modifications |
| [`architecture.md`](architecture.md) | Module boundaries |
| [`testing_philosophy.md`](testing_philosophy.md) | Tests and coverage |
| [`rendering_pipeline.md`](rendering_pipeline.md) | Manuscript and PDF |
| [`style_guide.md`](style_guide.md) | Code and prose tone |
| [`syntax_guide.md`](syntax_guide.md) | `{{TOKEN}}` and figures |
| [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) | Claims and registry |

---

## Rule 2: Coverage Gate — ≥90% on `src/`

Enforced by `pyproject.toml` and `scripts/01_run_tests.py --project cohereants --project-only`.

After any `src/` change:

```bash
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-fail-under=90 --cov-report=term-missing -q
```

Do not delete tests to satisfy the gate.

---

## Rule 3: Thin Orchestrator — `scripts/` vs `src/`

- **`src/`** — Atmospheric transmission, CHC spectra, sensilla models, case studies, figures, manuscript variables.
- **`scripts/`** — Invoke `src/`, save outputs, print paths.

If spectroscopy, ROC logic, or antenna geometry appears in a script, move it to `src/` and test it.

---

## Rule 4: No New Mocks

Never add `unittest.mock`, `MagicMock`, or `@patch`. Legacy upstream mock tests are debt — refactor toward real arrays when touching those files.

---

## Rule 5: Engineering Claims and Hypothesis Framing

The vibrational/IR olfaction hypothesis is **contested**. Manuscript and code comments must:

- Present IR/vibrational sensing as testable, not proven
- Bind numeric claims to `{{TOKEN}}` substitution or `data/claim_ledger.yaml`
- Respect `metadata.claim_boundary` strings in `figure_registry.json`

Do not strengthen prose beyond what generated artifacts support.

---

## Rule 6: Passive / WIP Workflow

- Canonical git tree: `path/to/cohereants/`
- Template symlink: `projects_in_progress/cohereants`
- Pipeline flag: **`--project cohereants`** (never `cohereants`)
- Do not commit under public `template/projects/cohereants/`

---

## Rule 7: `output/` Is Disposable

Edit generators (`src/figures.py`, case studies) and manuscript templates — not `output/figures/*.png` or resolved `output/manuscript/*.md`.

Regeneration order: figures → case studies → `z_generate_manuscript_variables.py` → `03_render_pdf.py`.

---

## Rule 8: numpy 2.x Compatibility

Use `np.trapezoid` or project `_trapezoid` shims — not bare `np.trapz`.

---

## Verification Checklist

```bash
# 1. Tests + coverage
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-fail-under=90 -q

# 2. No new mocks in touched test files
grep -n "unittest.mock\|MagicMock\|@patch" tests/test_*.py  # inspect hits — legacy allowed only in known debt files

# 3. Figure registry present after figure work
test -f output/figures/figure_registry.json && echo "registry ok"

# 4. Variables (when manuscript changed)
MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py --allow-draft
test -f output/data/manuscript_variables.json && echo "variables ok"
```

---

## See Also

- [`../ISA.md`](../ISA.md) — Ideal state and remediation backlog
- [`quickstart.md`](quickstart.md) — Run commands
