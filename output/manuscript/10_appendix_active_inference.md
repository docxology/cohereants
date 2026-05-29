# Appendix G: Active-Inference Behavioral Demo on IR Cues {#sec:app_active_inference}

## Objective

Demonstrate a deterministic active-inference step for olfactory search under IR cues.

## Interpretation

The demo shows how a minimal belief-update policy could navigate a grid when IR cue strength varies spatially. It supports assay design—what information a searcher would need from wavelength-specific cues—not field ethology. Outputs should be read alongside preregistered behavioral falsifiers in \Cref{sec:discussion}.

## Claim boundary

\Cref{fig:app_active_inference} is a deterministic trajectory from `src/behavioral_models.py`; it is not evidence that insects perform active inference on semiochemical IR gradients.

## Implemented (stub) Methods (src)

- `src/behavioral_models.py`
  - `olfactory_active_inference_step(state, params)` — deterministic single‑step update used in the demo

## Script and Outputs

- Script: `scripts/generate_active_inference_demo.py`
- Data: `output/data/active_inference_demo.npz`
- Figure: `output/figures/active_inference_trajectory.png`

## Figure

<!-- alt: Deterministic active-inference trajectory on a grid with IR cue beliefs; behavioral demo model output, not field data. -->
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/active_inference_trajectory.png}
\caption{Deterministic gradient-following trajectory under a simple active-inference step model. Claim boundary: behavioral demo only; not field data.}
\label{fig:app_active_inference}
\end{figure}

## Equation References

- Response/latency and information metrics: see \Cref{sec:mathematical_appendix}.

## Reproducibility

- Run: `python3 scripts/generate_active_inference_demo.py`
- Artifacts saved to `output/data/` and `output/figures/`.
- Seed set to 42 via `src/config.set_random_seed(42)` for deterministic policy traces.
- Implementation note: the demo is a lightweight, deterministic adapter that calls `src/` policy utilities without embedding scientific logic in the script.

## Cross-References

- Methods: \Cref{sec:methodology}
- Symbols: \Cref{sec:symbols_glossary}
- Math appendix: \Cref{sec:mathematical_appendix}

<!-- Removed duplicate figure block; primary figure `app_active_inference` is already included above. -->
