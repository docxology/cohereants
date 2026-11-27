# Output directory

The checkout tracks the published PDF, HTML, resolved sections, and numerical
and figure artifacts under `output/`. Build logs, validation reports, and
checkpoints are local. Use a disposable checkout for a rebuild and preserve the
tracked snapshots in normal source edits.

| Path | Contents |
| --- | --- |
| `output/data/` | Finite numerical model NPZ arrays and resolved variables |
| `output/figures/` | PNGs, captions, alt text, and figure registry |
| `output/manuscript/` | Generated copies of the canonical sources |
| `output/pdf/` and `output/web/` | Combined manuscript and web sections |
| `output/reports/` | Local checks and generated provenance |

The registry pairs each figure's filename with its label, description,
generation method, and claim boundary. The data and figures used by the
[offline build](rendering_pipeline.md) are retained artifacts from the same
revision. Numerical interpretation belongs to the [manuscript](manuscript/README.md).
