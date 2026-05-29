# Scripts — CohereAnts thin orchestrators

Business logic lives in `src/`. Each script imports tested functions, writes figures/data under
`output/`, and prints paths for the template pipeline manifest.

## Core orchestrators

| Script | `src/` entry | Outputs |
| --- | --- | --- |
| `generate_research_figures.py` | `src/figures/` | Core manuscript figures + registry refresh |
| `generate_integrated_analysis.py` | `src/integrated_figures.py` | Integrated panels + `integrated_analysis.npz` |
| `z_generate_manuscript_variables.py` | `src/manuscript_variables.py` | `output/data/manuscript_variables.json` |
| `run_all_case_studies.py` | (subprocess, parallel pool) | All appendix generators |

Appendix scripts follow the same thin pattern: `compute_*` → `render_comprehensive_figure` →
`format_appendix_caption(label, metrics)` → `write_figure_bundle_from_script`. Typed analysis
objects expose `.as_dict()` for NPZ sidecars via `scripts/_utils.analysis_as_dict`.

## Appendix generators (A–G)

| Script | Appendix |
| --- | --- |
| `generate_sensilla_array_directionality.py` | A — beam patterns |
| `generate_environmental_channel_analysis.py` | B — atmospheric channel |
| `generate_detection_limits.py` | C — detection limits |
| `generate_neural_encoding_analysis.py` | D — neural encoding |
| `generate_spectral_unmixing.py` | E — spectral unmixing |
| `generate_plasmonic_geometry_sweep.py` | F — plasmonic geometry |
| `generate_active_inference_demo.py` | G — active inference demo |

## Template integration

- Run tests: `uv run python scripts/01_run_tests.py --project cohereants --project-only` (from template root).
- Render PDF: `uv run python scripts/03_render_pdf.py --project cohereants`.
- Full pipeline: `uv run python scripts/execute_pipeline.py --project cohereants --core-only`.

Set `MPLBACKEND=Agg` for headless matplotlib. Use `uv run python scripts/...` from the project directory.
