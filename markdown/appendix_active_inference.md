# Appendix G: Active-Inference Behavioral Demo on IR Cues {#sec:app_active_inference}

## Objective
Demonstrate a deterministic active-inference step for olfactory search under IR cues.

## Planned Methods (src)
- `src/behavioral_models.py`
  - `olfactory_active_inference_step(state, params)`

## Planned Script and Outputs
- Script: `scripts/generate_active_inference_demo.py`
- Data: `output/data/active_inference_demo.npz`
- Figure: `output/figures/active_inference_trajectory.png`

## Figure
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{../output/figures/active_inference_trajectory.png}
\caption{Planned trajectories and belief updates for IR-guided search in a deterministic grid environment.}
\label{fig:app_active_inference}
\end{figure}

## Equation References
- Response/latency and information metrics: see \cref{sec:mathematical_appendix}.

## Reproducibility
- Run: `python3 scripts/generate_active_inference_demo.py`
- Artifacts saved to `output/data/` and `output/figures/`.

## Cross-References
- Methods: \cref{sec:methodology}
- Symbols: \cref{sec:symbols_glossary}
- Math appendix: \cref{sec:mathematical_appendix}
