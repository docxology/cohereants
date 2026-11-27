# Source modules

The numerical and figure code lives in [`src/`](../../src/).
[Architecture](../architecture.md) explains the dependency boundaries.
The [scripts guide](scripts.md) describes the entry points.

| Directory | Responsibility |
| --- | --- |
| [`ant_stack/`](../../src/ant_stack/) | Layered model of perception, policy, and action |
| [`case_studies/`](../../src/case_studies/) | Finite computational appendix models |
| [`figures/`](../../src/figures/) | Core manuscript figures |
| [`viz/`](../../src/viz/) | Shared plotting and metadata utilities |

`src/manuscript_variables.py` reads the existing response-time and detection
arrays during strict hydration. `src/manuscript_fixtures.py` holds configured
model and protocol assumptions. The [manuscript guide](../manuscript/README.md)
describes the distinction between modeled quantities and empirical sources.
