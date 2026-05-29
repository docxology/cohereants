"""Tests for shared appendix grid renderer."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from src.viz.appendix_grid import PanelSpec, render_analysis_grid, render_labeled_grid, summarize_metrics


def test_render_labeled_grid_shape() -> None:
    panels = [
        PanelSpec("A", plot=lambda ax, _: ax.plot([0, 1], [0, 1])),
        PanelSpec("B", plot=lambda ax, _: ax.bar(["x"], [1])),
    ]
    fig = render_labeled_grid(panels, nrows=1, ncols=2, figsize=(6, 3))
    assert len(fig.axes) == 2
    plt.close(fig)


def test_render_analysis_grid_passes_analysis() -> None:
    analysis = {"values": np.array([1.0, 2.0, 3.0])}

    def _plot(ax, data):
        ax.plot(data["values"])

    panels = [PanelSpec("Series", plot=_plot)]
    fig = render_analysis_grid(analysis, panels, nrows=1, ncols=1, figsize=(4, 3))
    assert len(fig.axes) == 1
    plt.close(fig)


def test_summarize_metrics_rules() -> None:
    analysis = {"a": 2.0, "b": 3.0}
    metrics = summarize_metrics(analysis, {"sum": lambda d: float(d["a"] + d["b"])})
    assert metrics["sum"] == 5.0
