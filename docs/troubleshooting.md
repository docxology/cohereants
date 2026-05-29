# Troubleshooting

Symptom-driven fixes for **cohereants** tests, analysis, and rendering. Commands use `--project cohereants` and the standardized lowercase project name.

## Literal `{{TOKEN}}` in the rendered PDF

**Cause:** Variable hydration did not run, failed, or the token is missing from `generate_variables()`.

**Fix:**

```bash
MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py
cat output/data/manuscript_variables.json | python -m json.tool | head
grep -r "{{" output/manuscript/ || echo "All resolved"
uv run python scripts/03_render_pdf.py --project cohereants   # from template root
```

Add missing keys in `src/manuscript_variables.py` and extend `tests/test_manuscript_variables.py`.

## `FileNotFoundError`: missing NPZ during variable hydration

**Cause:** Strict mode requires analysis outputs.

**Fix:**

```bash
MPLBACKEND=Agg .venv/bin/python scripts/generate_research_figures.py
MPLBACKEND=Agg .venv/bin/python scripts/run_all_case_studies.py
MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py
```

Draft-only:

```bash
MPLBACKEND=Agg .venv/bin/python scripts/z_generate_manuscript_variables.py --allow-draft
```

## Project not found / wrong tree used

**Cause:** Symlink missing or stale; pipeline looking at empty `projects/cohereants`.

**Fix:**

```bash
# From template root
uv run python -m infrastructure.orchestration link-projects --dry-run
ls -la projects_in_progress/cohereants
uv run python -c "
from pathlib import Path
from infrastructure.project.discovery import resolve_project_root
print(resolve_project_root(Path('.'), 'cohereants'))
"
```

Canonical source: `path/to/cohereants/`

## Coverage gate fails (under 90%)

```bash
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-report=term-missing -v
```

Add tests for uncovered branches in `src/case_studies/` or orchestration paths. Do not lower `fail_under`.

## Tests report PASSED but 0 collected

**Cause:** Stale or empty `.venv` when invoked via aggregate runner.

**Fix:**

```bash
cd path/to/cohereants
uv sync --extra dev
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-fail-under=90 -q
```

Never trust exit code alone — verify collected count and coverage percentage.

## `ModuleNotFoundError: No module named 'src'`

**Cause:** pytest run without project `conftest.py` path setup or wrong CWD.

**Fix:** Run from project root with project interpreter, or use template orchestrator:

```bash
uv run python scripts/01_run_tests.py --project cohereants --project-only
```

## Figure reference unresolved (`??` in PDF log)

**Cause:** `\label{fig:…}` missing, PNG absent, or label not in `figure_registry.json`.

**Fix:**

```bash
ls output/figures/response_time_comparison.png
python -c "import json; print(list(json.load(open('output/figures/figure_registry.json')).keys()))"
MPLBACKEND=Agg .venv/bin/python scripts/generate_research_figures.py
```

Align `\label{fig:response_time_comparison}` in manuscript with `src/figure_registry_builder.py`.

## `??` references, partial PDF, or `\mathrm` LaTeX errors

**Cause:** xelatex emergency-stopped before BibTeX/multi-pass resolution. Common triggers in this project:

- `FIGURE_WIDTH_*` token included `\textwidth` while the manuscript also appends `\textwidth` → `0.8\textwidth\textwidth`
- `<!-- alt: ... -->` inside `\begin{figure}` environments
- `\(...\)` inline math in Markdown list items (Pandoc emits text-mode `\mathrm`)
- LaTeX commands such as `\mu\mathrm{m}` injected into prose without math delimiters

**Diagnose:**

```bash
grep -E 'mathrm allowed only|textwidth.*invalid|Emergency stop|ended by \\\\end\{document\}' \
  output/pdf/_combined_manuscript.log
grep 'textwidth\\textwidth' output/pdf/_combined_manuscript.tex
grep -n '<!-- alt:' output/pdf/_combined_manuscript.tex | head
pdfinfo output/pdf/cohereants_combined.pdf | grep Pages
```

A healthy combined build is on the order of **~69 pages** (not ~10). After fixing sources, re-run hydration and render:

```bash
cd path/to/cohereants
MPLBACKEND=Agg uv run python scripts/z_generate_manuscript_variables.py
cd path/to/template
uv run python scripts/03_render_pdf.py --project cohereants
uv run python scripts/05_copy_outputs.py --project cohereants
uv run python -m infrastructure.validation.cli pdf output/cohereants/pdf/cohereants_combined.pdf
```

Project tests: `tests/test_manuscript_latex_safety.py`, `tests/test_pdf_compile_smoke.py`.

## Appendix figure bundles / registry validation

Appendix generators write PNG plus sidecar files via `scripts/_utils.write_figure_bundle_from_script()`:

- `output/figures/<stem>.caption.txt` — LaTeX caption text
- `output/figures/<stem>.alt.txt` — accessibility alt text (≥40 characters)

Registry entries are built by `src/figure_registry_builder.py`. Validate after analysis:

```bash
cd path/to/cohereants
MPLBACKEND=Agg .venv/bin/python scripts/run_all_case_studies.py
# From template root:
uv run python -m infrastructure.validation.content.figure_validator projects_in_progress/cohereants/output/figures
```

`integrated_analysis_system_performance.png` is an auxiliary integrated-analysis panel and is **not** registered in `figure_registry.json` (non-manuscript diagnostic output).

## Combined PDF missing manuscript sections

The combined PDF includes **18** discoverable top-level sections (`00_`–`16_` plus `99_references.md`). Excluded by design: `preamble.md`, `AGENTS.md`, `config.yaml`, `references.bib`. Introduction opens without an H1 (prose lead-in).

Contract test: `tests/test_manuscript_combined_inclusion.py`. After render, confirm the log lists 18 sections and inspect `output/pdf/_combined_manuscript.md` or the validation CLI:

```bash
uv run python scripts/03_render_pdf.py --project cohereants
uv run python -m infrastructure.validation.cli pdf output/cohereants/pdf/cohereants_combined.pdf
```


```bash
npx --yes puppeteer browsers install chrome-headless-shell
uv run python scripts/03_render_pdf.py --project cohereants
```

## numpy 2.x: `trapz` removed

Use `np.trapezoid` or project shims (`getattr(np, "trapezoid", None) or getattr(np, "trapz")`) in modules that integrate spectra.

## Evidence / claim validation failures

Numeric manuscript claims must align with `data/claim_ledger.yaml` and generated artifacts. Regenerate analysis before re-running stage 7 validation:

```bash
uv run python scripts/04_validate_output.py --project cohereants
```

## See Also

- [`rendering_pipeline.md`](rendering_pipeline.md)
- [`output_conventions.md`](output_conventions.md)
- [`faq.md`](faq.md)
