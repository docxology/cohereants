# Quick start

From the CohereAnts checkout, create a locked environment. Python 3.13 has wheels for the locked numerical dependencies. The repository's default interpreter file selects Python 3.15, which can require a Fortran toolchain to build SciPy.

```bash
uv sync --locked --python 3.13 --extra dev
MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  uv run --no-sync python -m pytest tests/ --cov=src --cov-fail-under=90 -q
```

These tests use finite arrays, local model fixtures, and, when present,
local render artifacts. They do not use field specimens, equipment, or
outside data services. See [testing](project/tests.md) for optional PDF cases.

For the paper, follow [the pinned build](rendering_pipeline.md).
The [output guide](output_conventions.md) describes the deposited files and
the local results a rebuild creates.
