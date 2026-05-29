# Rendering Pipeline: Manuscript → PDF

The `manuscript/` tree is a multi-section engineering monograph on insect IR perception and biomimetic sensor design. The template rendering infrastructure compiles it to PDF, HTML, and slides when the project is invoked with `--project cohereants`.

## WIP Path Resolution

While **cohereants** remains **passive**, the canonical source lives in the private repo and is symlinked for template work:

| Context | Path |
| --- | --- |
| Private canonical | `path/to/cohereants/` |
| Template WIP symlink | `template/projects_in_progress/cohereants` |
| Pipeline resolution | `infrastructure.project.discovery.resolve_project_root(repo_root, "cohereants")` |

`resolve_project_root()` prefers `projects/cohereants` when that tree has `src/`, `tests/`, `scripts/`, and `manuscript/`. Otherwise it uses `projects_in_progress/cohereants` when the symlink exists. Rendering and validation therefore operate on the WIP tree without promoting the project to active discovery.

**Passive implication:** `./run.sh` does not list cohereants until promoted to `active/` in the private lifecycle repo. Targeted runs still work:

```bash
uv run python scripts/execute_pipeline.py --project cohereants --core-only
```

## Prerequisite: Mermaid and Chrome

Manuscript sections may embed ```mermaid``` blocks. Combined PDF rendering uses `mmdc`, which requires `chrome-headless-shell`:

```bash
npx --yes puppeteer browsers install chrome-headless-shell
```

If slides render but the combined PDF fails with "Could not find Chrome", install the headless shell and re-run stage 6. See [`troubleshooting.md`](troubleshooting.md).

## Four Phases

### 1. Analysis (figures and data)

**Scripts:** `scripts/generate_research_figures.py`, `scripts/run_all_case_studies.py`, individual `scripts/generate_*.py`

**Outputs:**

- `output/figures/` — PNG figures and `figure_registry.json`
- `output/data/` — NPZ arrays, JSON specs
- Caption sidecars `*.caption.txt`

### 2. Manuscript variables

**Script:** `scripts/z_generate_manuscript_variables.py`

**Logic:** `src/manuscript_variables.py::generate_variables(project_root, require_analysis_outputs=...)`

**Default strict inputs:**

- `output/data/response_time_comparison.npz`
- `output/data/detection_limits_comprehensive.npz`

**Outputs:**

- `output/data/manuscript_variables.json`
- `output/manuscript/*.md` — token-substituted section copies

Use `--allow-draft` only for early drafts that may omit analysis outputs.

### 3. PDF render

**Script (template root):** `uv run python scripts/03_render_pdf.py --project cohereants`

**Inputs:** Resolved markdown under `output/manuscript/`, plus `manuscript/config.yaml`, `preamble.md`, `references.bib`

**Outputs:**

- `output/pdf/cohereants_combined.pdf`
- `output/web/` HTML sections
- LaTeX intermediates and `_combined_manuscript.log`

Manuscript prose uses LaTeX `\Cref{fig:…}` / `\label{fig:…}` for figures (see [`syntax_guide.md`](syntax_guide.md)).

### 4. Copy deliverables

**Script:** `uv run python scripts/05_copy_outputs.py --project cohereants`

Copies working artifacts to template root `output/cohereants/` for CI artifacts and archival stages.

## config.yaml Controls

| Key area | Consumed by |
| --- | --- |
| `paper.title`, `authors`, `keywords` | PDF front matter, `{{PROJECT_TITLE}}` |
| `metadata.random_seed` | `{{RANDOM_SEED}}`, deterministic runs |
| `publication.doi` | Title page (when set) |
| `llm.*` | Optional LLM stages (skipped in `--core-only`) |

Experiment-specific bounds also live in `src/manuscript_fixtures.py` (protocol QCL bands, biomimetic thresholds).

## Troubleshooting Quick Links

| Symptom | Doc section |
| --- | --- |
| Literal `{{TOKEN}}` in PDF | [`troubleshooting.md`](troubleshooting.md) |
| Missing NPZ during hydration | [`troubleshooting.md`](troubleshooting.md) |
| Figure `\Cref` unresolved | [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) |
| Chrome / mmdc failure | [`troubleshooting.md`](troubleshooting.md) |

## See Also

- [`output_conventions.md`](output_conventions.md) — Artifact inventory
- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — Figure and claim protocol
