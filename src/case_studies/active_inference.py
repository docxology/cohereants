"""Appendix G: Active-inference behavioral demo on IR cues."""

from __future__ import annotations

from typing import Dict
import numpy as np


def olfactory_active_inference_step(state: Dict[str, float], params: Dict[str, float]) -> Dict[str, float]:
    """
    Minimal deterministic update step for a 2D position under a gradient cue.

    Args:
        state: {'x': float, 'y': float}
        params: {'step': float, 'gain': float}

    Returns:
        New state dict with updated 'x','y'.
    """
    x = float(state.get("x", 0.0))
    y = float(state.get("y", 0.0))
    step = float(params.get("step", 0.1))
    gain = float(params.get("gain", 1.0))

    # Deterministic gradient toward origin (as proxy cue)
    grad_x = -gain * x
    grad_y = -gain * y
    norm = np.hypot(grad_x, grad_y) + 1e-12
    dx = step * grad_x / norm
    dy = step * grad_y / norm
    return {"x": x + dx, "y": y + dy}
