"""Shared multi-panel appendix figure grid renderer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

import matplotlib.pyplot as plt

from src.viz.warnings_util import suppress_plot_warnings

PlotFn = Callable[[object, Mapping[str, object]], None]


@dataclass(frozen=True)
class PanelSpec:
    """Single panel in an appendix comprehensive figure."""

    title: str
    plot: PlotFn
    xlabel: str = ""
    ylabel: str = ""


def render_labeled_grid(
    panels: Sequence[PanelSpec],
    *,
    nrows: int,
    ncols: int,
    figsize: tuple[float, float] = (16.0, 12.0),
    suptitle: str | None = None,
) -> plt.Figure:
    """Render a labeled grid of appendix panels from shared specs."""
    if len(panels) > nrows * ncols:
        raise ValueError(f"Panel count {len(panels)} exceeds grid capacity {nrows * ncols}")

    with suppress_plot_warnings():
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
        flat_axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for index, panel in enumerate(panels):
            ax = flat_axes[index]
            panel.plot(ax, {})
            ax.set_title(panel.title)
            if panel.xlabel:
                ax.set_xlabel(panel.xlabel)
            if panel.ylabel:
                ax.set_ylabel(panel.ylabel)
            ax.grid(True, alpha=0.3)

        for ax in flat_axes[len(panels) :]:
            ax.axis("off")

        if suptitle:
            fig.suptitle(suptitle)
        fig.tight_layout()
    return fig


def render_analysis_grid(
    analysis: Mapping[str, object],
    panels: Sequence[PanelSpec],
    *,
    nrows: int,
    ncols: int,
    figsize: tuple[float, float] = (16.0, 12.0),
    suptitle: str | None = None,
) -> plt.Figure:
    """Render appendix panels with analysis dict passed to each plot callable."""
    if len(panels) > nrows * ncols:
        raise ValueError(f"Panel count {len(panels)} exceeds grid capacity {nrows * ncols}")

    with suppress_plot_warnings():
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
        flat_axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for index, panel in enumerate(panels):
            ax = flat_axes[index]
            panel.plot(ax, analysis)
            ax.set_title(panel.title)
            if panel.xlabel:
                ax.set_xlabel(panel.xlabel)
            if panel.ylabel:
                ax.set_ylabel(panel.ylabel)
            ax.grid(True, alpha=0.3)

        for ax in flat_axes[len(panels) :]:
            ax.axis("off")

        if suptitle:
            fig.suptitle(suptitle)
        fig.tight_layout()
    return fig


def summarize_metrics(
    analysis: Mapping[str, object],
    rules: Mapping[str, Callable[[Mapping[str, object]], float]],
) -> dict[str, float]:
    """Extract summary metrics from analysis using named rule callables."""
    return {name: float(rule(analysis)) for name, rule in rules.items()}
