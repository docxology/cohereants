# CohereAnts

**When do bugs see (infra)red? On the Visual and Infra-red in the Insect Perceptual Apparatus**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20450880.svg)](https://doi.org/10.5281/zenodo.20450880)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Computational research on insect IR sensing and olfaction modeling — engineering bounds and
protocol design, not biological proof of IR olfaction.

![CohereAnts evidence map: what is modeled, anchored, and still untested across atmospheric, geometric, spectral and evidence-status panels](output/figures/composite_cross_domain_overview.png)

**Cite this work** via the concept DOI [10.5281/zenodo.20450880](https://doi.org/10.5281/zenodo.20450880)
(always resolves to the latest version). The v1.0.0 deposit is
[10.5281/zenodo.20450970](https://doi.org/10.5281/zenodo.20450970). See [`CITATION.cff`](CITATION.cff).

| Context | Name |
| --- | --- |
| Display name (this README, manuscript title) | **CohereAnts** |
| Pipeline CLI / folder / `pyproject.toml` | `cohereants` |
| Canonical repository | [`github.com/docxology/cohereants`](https://github.com/docxology/cohereants) |

Authors: **Tucker Chambers** (Independent Researcher) and **Daniel A. Friedman** (Active Inference
Institute). License: Apache-2.0.

Built on the [Research Project Template](https://github.com/docxology/template) two-layer
architecture. Structure, tests, registry, and documentation follow `template_code_project`;
science modules use numpy-2 shims and thin orchestrators.

## Domain modules

| Domain | Module(s) |
| --- | --- |
| Atmospheric IR transmission | `src/core.py` |
| CHC spectroscopy | `src/spectroscopy.py` |
| Sensilla morphology | `src/sensilla.py` |
| Behavioral statistics | `src/behavioral.py` |
| Fermi estimation | `src/fermi_estimation.py` |
| Metamaterial framework | `src/meta_material_framework.py` |
| Integrated analysis | `src/integrated_analysis.py`, `src/integrated_figures.py` |
| Figure registry / variables | `src/figures/`, `src/manuscript_variables.py` |
| Visualization | `src/visualization.py`, `src/viz/styling.py` |
| Case studies (appendices) | `src/case_studies/` |

## Documentation

The package requires Python 3.11 or later. The [offline reproduction guide](docs/quickstart.md) selects Python 3.13 for its locked verification environment.

Use the [documentation index](docs/README.md) for setup, architecture, and
verification. The [quick start](docs/quickstart.md) runs the offline tests.
The [manuscript](docs/manuscript/README.md) and
[pinned PDF and HTML build](docs/rendering_pipeline.md) describe the canonical
sources and the tracked release artifacts.

## Citation

If you use this work, please cite it via [`CITATION.cff`](CITATION.cff). The archived release
(PDF + source) is deposited on Zenodo with a concept DOI (stable, always-latest) and a per-version
DOI; see the badges/links at the top of the GitHub release notes and `docs/manuscript/config.yaml`
(`publication.doi` = concept DOI, `publication.version_doi` = this deposit).

See [`AGENTS.md`](AGENTS.md), [`docs/README.md`](docs/README.md), and [`ISA.md`](docs/project/ISA.md).
