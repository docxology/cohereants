# AGENTS.md — `cohereants/scripts`

Thin-orchestrator contract for this directory. Read with the repo-root
[`AGENTS.md`](../AGENTS.md) and [`ISA.md`](../ISA.md).

## Contract

`scripts/` holds **thin orchestrators only**: argparse where needed, path bootstrap,
progress prints, and delegated calls into `src/` entrypoints.

- **No business/data/plot/analysis logic here.** Algorithms live in `src/` and are tested
  there (`tests/`, zero-mock, coverage ≥90% on `src/` per `pyproject.toml`).
- Reuse the shared helpers in [`_utils.py`](_utils.py) — `ensure_src_on_path`,
  `setup_paths`, `set_mpl_backend`, `write_figure_bundle_from_script`,
  `analysis_as_dict`. Do not re-implement path/bootstrap logic locally.
- Scripts must run headless and deterministically: call `set_mpl_backend()`;
  `tests/test_figure_outputs.py` executes every generator via subprocess and asserts its
  outputs, so keep runtime bounded and outputs stable.

## Inventory

| Script | Delegates to |
| --- | --- |
| `generate_research_figures.py` | `src.figures.generate_core_manuscript_figures` |
| `generate_integrated_analysis.py` | `src.integrated_figures.generate_integrated_analysis_figures` |
| `z_generate_manuscript_variables.py` | `src/manuscript_variables.py` + template-root `infrastructure.rendering.manuscript_injection` |
| `run_all_case_studies.py` | subprocess pool over the seven appendix generators |
| `generate_sensilla_array_directionality.py` | `src.case_studies.sensilla_array_directionality` |
| `generate_environmental_channel_analysis.py` | `src.case_studies.environmental_channel` |
| `generate_detection_limits.py` | `src.case_studies.detection_limits` (+ `src.visualization.set_plot_style`) |
| `generate_neural_encoding_analysis.py` | `src.case_studies.neural_encoding` |
| `generate_spectral_unmixing.py` | `src.case_studies.spectral_unmixing` |
| `generate_plasmonic_geometry_sweep.py` | `src.case_studies.plasmonic_geometry` |
| `generate_active_inference_demo.py` | `src.case_studies.olfactory_active_inference_step` |
| `_utils.py` | shared helpers; lazy-imports `src.figure_artifacts`, `src.viz.figure_helpers` |

## Gotchas

- This directory is part of the tracked repo (origin `github.com/docxology/cohereants`);
  commit here normally. The template-root pipeline scripts (`01_run_tests.py`,
  `03_render_pdf.py`, `execute_pipeline.py`) are external — never present them as living
  in this `scripts/`.
- Every script bootstraps its own `sys.path` (script dir for `_utils`, repo root for
  `src.*`); run them from the project directory with `uv run python scripts/...`.
- `MPLBACKEND=Agg` (or `set_mpl_backend()`) is required for headless rendering.
- Figure sidecar contract: `.png` + `.caption.txt` + `.alt.txt` under `output/figures/`,
  indexed by `figure_registry.json`; NPZ payloads under `output/data/`.
- `z_generate_manuscript_variables.py` imports `infrastructure.rendering` from the
  template root; pass `--allow-draft` when analysis outputs are missing.
- `generate_detection_limits.py` pulls `src.visualization.set_plot_style` (deprecated shim
  re-exporting `viz.styling`) — keep it working until that shim is retired repo-wide.
