# Troubleshooting local verification

- **Dependency build fails.** Use the explicit `--python 3.13` in the
  [quick start](quickstart.md) to select the supported wheel environment.
- **Hydration cannot import `infrastructure`.** Set `TEMPLATE_ROOT` to the pinned
  Template checkout before running the project script.
- **An input array is missing.** Restore the corresponding tracked artifact from
  the same revision. Strict hydration requires the files in the [render guide](rendering_pipeline.md).
- **A token remains literal.** Check the source key against
  [the syntax guide](syntax_guide.md). Hydrate again before rendering.
- **A figure is missing.** Check `output/figures/figure_registry.json` and the
  exact cited filename in the disposable checkout.
- **Validation reports a missing or unsupported value.** Inspect
  `output/reports/validation_report.json` and the
  [claim ledger](../data/claim_ledger.yaml). For LaTeX failures, read
  `output/pdf/_combined_manuscript.log` in the disposable checkout.
