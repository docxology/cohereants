# Render and validate the CohereAnts manuscript

The eighteen numbered files in [`docs/manuscript/`](manuscript/) are the maintained sources. The
same directory owns the publication metadata, bibliography, and LaTeX preamble.
`output/manuscript/` contains a historical resolved snapshot. Rebuild in a
separate clean checkout to preserve the original tracked deposit. Its physical
directory must be named `cohereants` so Stage 04 can locate the combined PDF.

## Prepare the resolved sources

Use the tracked finite model arrays in `output/data/` and corresponding figures
in `output/figures/` from the same revision. The default hydration requires the
response-time and detection-limit arrays. It resolves manuscript quantities using
the existing numerical values and fixture configuration. It does not rerun case
studies or collect observations. Draft mode allows unavailable values and is
intended for editing previews.

Set `cohereants_checkout` and `template_checkout` to absolute paths. Check out
[Template revision `87704feae0a4490ef7dad9c931d268e8c30273c2`](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2).
Use compatible Pandoc and pandoc-crossref versions, XeLaTeX and BibTeX, and the
[Template prerequisites](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md).

```bash
cd "$cohereants_checkout"
uv sync --locked --python 3.13 --extra dev
TEMPLATE_ROOT="$template_checkout" MPLBACKEND=Agg \
  uv run --no-sync python scripts/z_generate_manuscript_variables.py
```

## Build and check both formats

From the Template checkout, register the disposable project in an unused working slot.

```bash
cd "$template_checkout"
uv sync --locked --no-dev
mkdir -p projects/working
ln -s "$cohereants_checkout" projects/working/cohereants
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/cohereants --skip-manuscript-hydration
python "$cohereants_checkout/scripts/link_web_references.py" "$cohereants_checkout/output"
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/cohereants
```

The reference step reads the combined PDF's numbered equation and figure
records and the matching generated HTML. It links equations and figures in the
combined and chapter readers. In aligned math, the link selects the
corresponding number below the shared display. It leaves formulas and the PDF
untouched. Rerun it on the same Stage 03 output after an interruption.

Open `output/pdf/cohereants_combined.pdf`, `output/web/index.html`, and
`output/reports/validation_report.json` in the CohereAnts checkout. The format
checks cover the render and the available numerical, citation, and figure
bindings. The manuscript discusses the scope of the empirical literature and
the unresolved biological hypothesis.
