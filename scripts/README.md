# Scripts — CohereAnts thin orchestrators

Business logic lives in `src/`. Each script here is orchestration only: path bootstrap, a
delegated call into a `src/` entrypoint, and writing figure/data artifacts under `output/`.
Contract details: [AGENTS.md](AGENTS.md).

## Inventory

| Script | Purpose | Delegates to | Run command |
| --- | --- | --- | --- |
| `generate_research_figures.py` | Core manuscript figures + registry refresh | `src.figures.generate_core_manuscript_figures` | `uv run python scripts/generate_research_figures.py` |
| `generate_integrated_analysis.py` | Integrated-analysis panels + `integrated_analysis.npz` | `src.integrated_figures.generate_integrated_analysis_figures` | `uv run python scripts/generate_integrated_analysis.py` |
| `z_generate_manuscript_variables.py` | Registry-backed `{{TOKEN}}` variables → `output/data/manuscript_variables.json` | `src/manuscript_variables.py` + template-root `infrastructure.rendering.manuscript_injection` | `uv run python scripts/z_generate_manuscript_variables.py --allow-draft` |
| `run_all_case_studies.py` | Runs all seven appendix generators (parallel pool) | subprocess over the appendix scripts below | `uv run python scripts/run_all_case_studies.py` |
| `generate_sensilla_array_directionality.py` | Appendix A — sensilla beam patterns | `src.case_studies.sensilla_array_directionality` | `uv run python scripts/generate_sensilla_array_directionality.py` |
| `generate_environmental_channel_analysis.py` | Appendix B — atmospheric channel | `src.case_studies.environmental_channel` | `uv run python scripts/generate_environmental_channel_analysis.py` |
| `generate_detection_limits.py` | Appendix C — detection limits | `src.case_studies.detection_limits` (+ `src.visualization.set_plot_style`) | `uv run python scripts/generate_detection_limits.py` |
| `generate_neural_encoding_analysis.py` | Appendix D — neural encoding | `src.case_studies.neural_encoding` | `uv run python scripts/generate_neural_encoding_analysis.py` |
| `generate_spectral_unmixing.py` | Appendix E — spectral unmixing | `src.case_studies.spectral_unmixing` | `uv run python scripts/generate_spectral_unmixing.py` |
| `generate_plasmonic_geometry_sweep.py` | Appendix F — plasmonic geometry | `src.case_studies.plasmonic_geometry` | `uv run python scripts/generate_plasmonic_geometry_sweep.py` |
| `generate_active_inference_demo.py` | Appendix G — active-inference demo | `src.case_studies.olfactory_active_inference_step` | `uv run python scripts/generate_active_inference_demo.py` |
| `_utils.py` | Shared helpers: path bootstrap, backend, figure bundles, NPZ dicts | lazy-imports `src.figure_artifacts`, `src.viz.figure_helpers` | imported, never run |

Appendix pattern: `compute_*()` → `render_comprehensive_figure()` →
`format_appendix_caption(label, metrics)` → `write_figure_bundle_from_script()`. Typed
analysis objects expose `.as_dict()` for NPZ sidecars via `scripts/_utils.analysis_as_dict`.

## Outputs

- `output/figures/` — `*.png` + `.caption.txt` + `.alt.txt` sidecars, indexed by `figure_registry.json`.
- `output/data/` — `*.npz` payloads, `manuscript_variables.json`.

## Tests

```bash
# From this project directory:
MPLBACKEND=Agg uv run pytest tests/ --cov=src --cov-report=term-missing
```

`tests/test_figure_outputs.py` runs every generator above via subprocess and asserts its
PNG + caption + alt sidecars are non-empty.

## Template integration (external)

The two-layer pipeline scripts referenced by the repo root live in the **template root**,
a sibling checkout — not in this repository's `scripts/`. From the template root only:

- Tests: `uv run python scripts/01_run_tests.py --project cohereants --project-only`
- PDF: `uv run python scripts/03_render_pdf.py --project cohereants`
- Full pipeline: `uv run python scripts/execute_pipeline.py --project cohereants --core-only`

Set `MPLBACKEND=Agg` for headless matplotlib; run scripts with `uv run python scripts/...`
from the project directory.
