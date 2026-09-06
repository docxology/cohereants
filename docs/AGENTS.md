# docs/ — Agent-Facing Documentation Hub

## Overview

Technical guide for `docs/` inside **cohereants** — the operational rulebook for AI agents and developers working on biomimetic IR sensor engineering and insect infra-red perception models. Every document in this directory is a hard constraint, not a suggestion.

**Project name (commands):** `cohereants` — always lowercase, never `cohereants` or `CohereAnts` in CLI flags or `--project` arguments.

## File Inventory

| File | Purpose | Status |
| --- | --- | --- |
| `README.md` | Hub index and navigation | Current |
| `AGENTS.md` | This index | Current |
| `agent_instructions.md` | Behavioral constraints (read-first) | Comprehensive |
| `architecture.md` | Domain module map, dependency direction | Comprehensive |
| `testing_philosophy.md` | Zero-mock policy, 90% gate, mock-debt note | Comprehensive |
| `rendering_pipeline.md` | Four-phase pipeline; WIP `resolve_project_root` | Comprehensive |
| `style_guide.md` | Understated engineering prose; code rules | Comprehensive |
| `syntax_guide.md` | `{{TOKEN}}` and figure cross-reference syntax | Comprehensive |
| `output_conventions.md` | `output/` layout, registries, regeneration | Comprehensive |
| `troubleshooting.md` | Symptom-driven recipes | Comprehensive |
| `quickstart.md` | Passive/WIP quick start | Comprehensive |
| `faq.md` | Recurring questions | Comprehensive |

## Key Conventions

**Read-first protocol:** Agents must read `agent_instructions.md` before modifying project files. Skipping it tends to produce mocks in tests, algorithms in `scripts/`, or hard-coded engineering numbers in manuscript prose.

**Thin orchestrator:** Domain physics and biophysics live in `src/`. `scripts/` coordinate figure generation, case studies, and manuscript variable hydration — they print output paths for manifest collection.

**Zero-mock target:** New tests use real numpy/scipy data. Upstream cohereants tests may still contain `unittest.mock`; treat that as debt to remove, not a pattern to copy (see `ISA.md`).

**Contested hypothesis:** The vibrational/IR theory of olfaction is presented as a **testable hypothesis**, not established fact. Numeric claims in prose must bind to generated artifacts or `data/claim_ledger.yaml`.

## Reading Order

1. **`agent_instructions.md`** — Rules and verification checklist
2. **`architecture.md`** — Module map before touching structure
3. **`testing_philosophy.md`** — Before writing or editing tests
4. **`rendering_pipeline.md`** — Before manuscript or output changes
5. **`style_guide.md`** — Before source edits
6. **`syntax_guide.md`** — Before manuscript token or figure edits

## Verification Commands

```bash
# From template root (symlink present under projects_in_progress/)
uv run python scripts/01_run_tests.py --project cohereants --project-only

# From project root (private repo or symlink)
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-fail-under=90 -q

# Mock audit (new tests must stay clean; legacy debt may still fail grep)
grep -r "unittest.mock\|MagicMock\|@patch" tests/ || echo "Clean"
```

## REQUIRED vs AESTHETIC

| Path | Status | Enforcing gate |
| --- | --- | --- |
| `src/core.py`, `src/spectroscopy.py`, … case studies | REQUIRED | 90% coverage on `src/` |
| `src/manuscript_variables.py` | REQUIRED | `tests/test_manuscript_variables.py` |
| `src/figure_registry_builder.py`, `figure_registry_contract.py` | REQUIRED | Figure validation stage |
| `scripts/generate_research_figures.py` | REQUIRED | Core figure outputs |
| `scripts/z_generate_manuscript_variables.py` | REQUIRED | PDF variable hydration |
| `docs/manuscript/config.yaml`, `*.md`, `references.bib` | REQUIRED | Render pipeline |
| `data/claim_ledger.yaml` | REQUIRED | Evidence-registry gates |
| `docs/*.md` | AESTHETIC | No automated parser — keep aligned manually |
| `ISA.md` | AESTHETIC (load-bearing) | Human/agent system of record |

## Cross-References

- [`README.md`](README.md) — Hub navigation
- [`../AGENTS.md`](../AGENTS.md) — Project root agent guide
- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — Manuscript protocol
- [`../pyproject.toml`](../pyproject.toml) — Coverage and pytest config
- [`../domain_profile.yaml`](../domain_profile.yaml) — Advisory validation gates
