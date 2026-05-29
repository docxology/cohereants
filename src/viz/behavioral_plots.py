"""Behavioral response figure generation."""

from __future__ import annotations

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np

from .panels import plot_behavioral_histogram, plot_behavioral_time_series
from .styling import PlotStyler, get_colorblind_palette


def generate_behavioral_plots(
    response_data: np.ndarray,
    time_points: np.ndarray,
    stimulus_times: Optional[List[float]] = None,
    plot_type: str = "time_series",
) -> plt.Figure:
    """
    Generate behavioral response plots.

    Args:
        response_data: Array of response amplitudes over time
        time_points: Array of time points corresponding to responses
        stimulus_times: Optional list of stimulus presentation times
        plot_type: Type of plot ('time_series', 'histogram', 'both')

    Returns:
        Matplotlib figure with behavioral plots
    """
    styler = PlotStyler("science")
    colors = get_colorblind_palette(4)

    if plot_type == "time_series":
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        plot_behavioral_time_series(
            ax,
            time_points,
            response_data,
            stimulus_times=stimulus_times,
            styler=styler,
            colors=colors,
        )

    elif plot_type == "histogram":
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        plot_behavioral_histogram(ax, response_data, styler=styler, colors=colors)

    elif plot_type == "both":
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        plot_behavioral_time_series(
            ax1,
            time_points,
            response_data,
            stimulus_times=stimulus_times,
            styler=styler,
            colors=colors,
        )
        plot_behavioral_histogram(ax2, response_data, styler=styler, colors=colors)

    else:
        raise ValueError("plot_type must be 'time_series', 'histogram', or 'both'")

    plt.tight_layout()
    return fig
