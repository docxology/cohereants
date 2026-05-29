# Style Guide

Coding and prose style for **cohereants** — biomimetic IR sensor engineering with understated, evidence-bound language.

---

## 1. Zero-Mock Policy (New Tests)

Forbidden in **new** test code:

- `unittest.mock`, `MagicMock`, `@patch`, `create_autospec`

Legacy upstream tests may still contain mocks; do not copy them. See [`testing_philosophy.md`](testing_philosophy.md).

**Correct pattern:**

```python
def test_atmospheric_transmission_window():
    from src.core import calculate_atmospheric_transmission
    wavelengths = np.linspace(8.0, 14.0, 50)
    transmission = calculate_atmospheric_transmission(wavelengths)
    assert transmission.shape == wavelengths.shape
    assert np.all(transmission >= 0.0)
```

---

## 2. Thin Orchestrator Pattern

`scripts/generate_research_figures.py` imports `generate_core_manuscript_figures()` from `src/figures.py` — it does not plot sensilla matching inline.

**Decision rule:** If a line computes physics or statistics that define a scientific result, it belongs in `src/` with tests.

---

## 3. Infrastructure Delegation

| Layer | May import |
| --- | --- |
| `src/core.py`, `src/spectroscopy.py`, … | numpy, scipy, sklearn, stdlib |
| `src/manuscript_variables.py` | `infrastructure.*` (optional, guarded) |
| `scripts/*.py` | `src.*`, `infrastructure.core.logging` |

---

## 4. Understated Engineering Prose

Manuscript and docs describe mechanisms and limits without hype.

**Avoid:** "novel enhanced real-world breakthrough sensor"

**Prefer:** "The coarse window model in `src/core.calculate_atmospheric_transmission()` estimates transmission factors; it is not a line-by-line radiative-transfer substitute."

**Avoid:** "Proves insects use IR olfaction"

**Prefer:** "Motivates a falsifiable protocol with matched thermal controls (@cite sources)."

Avoid adjectives that do not change meaning (`enhanced`, `real`, `new`) unless they distinguish two defined artifacts.

---

## 5. Show, Not Tell

Link claims to code paths and artifacts.

| Vague | Concrete |
| --- | --- |
| "Fast neural responses were modeled." | "`src.case_studies.neural_encoding` produces information-rate curves written to `output/data/` and cited in Appendix neural encoding." |
| "Detection limits were analyzed." | "`{{SNR_OPERATING_DB}}` is read from `output/data/detection_limits_spec.json` after `scripts/generate_detection_limits.py` runs." |

---

## 6. Explicit Paths

When documenting from the private repo, anchor paths at the project root:

| Artifact | Path |
| --- | --- |
| Atmospheric model | `src/core.py` |
| Variable generator | `src/manuscript_variables.py` |
| Figure registry | `output/figures/figure_registry.json` |
| Claim ledger | `data/claim_ledger.yaml` |

From the template checkout, prefix with `projects_in_progress/cohereants/` when citing symlink locations.

---

## 7. Type Hints and Errors

- Public functions in `src/` require type hints and docstrings.
- `ValueError` messages include actual shapes or parameter values:

```python
raise ValueError(f"wavelengths must be 1D, got shape {wavelengths.shape}")
```

---

## 8. Naming

- Project and CLI: **`cohereants`** (lowercase)
- Figure labels: `fig:response_time_comparison` (snake_case after prefix)
- Tokens: `SCREAMING_SNAKE` in `{{TOKEN}}` form

Historical prose may say "CohereAnts" as the research name; commands and paths use `cohereants` only.

## See Also

- [`agent_instructions.md`](agent_instructions.md)
- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — Claim policy
