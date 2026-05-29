"""Reusable matplotlib panel builders for domain and manuscript figures."""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np

from .styling import PlotStyler, get_colorblind_palette


def plot_correlation_heatmap(
    ax: plt.Axes,
    matrix: np.ndarray,
    labels: Sequence[str],
    *,
    title: str = "Correlation Matrix",
    cmap: str = "RdBu_r",
    styler: Optional[PlotStyler] = None,
    show_colorbar: bool = True,
    colorbar_label: str = "Correlation Coefficient",
    annotate: bool = True,
    fontweight: str = "normal",
) -> plt.Axes:
    """Draw a labeled correlation heatmap on ``ax``."""
    matrix = np.asarray(matrix)
    n_vars = len(labels)
    im = ax.imshow(matrix, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(np.arange(n_vars))
    ax.set_yticks(np.arange(n_vars))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    if annotate:
        for i in range(n_vars):
            for j in range(n_vars):
                ax.text(
                    j,
                    i,
                    f"{matrix[i, j]:.2f}",
                    ha="center",
                    va="center",
                    color="black",
                    fontweight=fontweight,
                )

    if show_colorbar:
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(colorbar_label)

    if styler is not None:
        styler.format_axes(ax, title=title, legend=False)
    else:
        ax.set_title(title, fontweight="bold", pad=20)

    return ax


def plot_behavioral_time_series(
    ax: plt.Axes,
    time_points: np.ndarray,
    response_data: np.ndarray,
    *,
    stimulus_times: Optional[List[float]] = None,
    styler: Optional[PlotStyler] = None,
    colors: Optional[List[str]] = None,
) -> plt.Axes:
    """Plot behavioral response over time with optional stimulus markers."""
    palette = colors or get_colorblind_palette(4)
    ax.plot(time_points, response_data, color=palette[0], linewidth=2, label="Response")

    if stimulus_times:
        for stim_time in stimulus_times:
            ax.axvline(
                x=stim_time,
                color=palette[2],
                linestyle="--",
                alpha=0.7,
                label="Stimulus" if stim_time == stimulus_times[0] else "",
            )

    if styler is not None:
        styler.format_axes(
            ax,
            xlabel="Time (s)",
            ylabel="Response Amplitude",
            title="Behavioral Response Over Time",
        )
    return ax


def plot_behavioral_histogram(
    ax: plt.Axes,
    response_data: np.ndarray,
    *,
    bins: int = 30,
    styler: Optional[PlotStyler] = None,
    colors: Optional[List[str]] = None,
) -> plt.Axes:
    """Plot response amplitude distribution with mean and median markers."""
    palette = colors or get_colorblind_palette(4)
    ax.hist(response_data, bins=bins, alpha=0.7, color=palette[1], edgecolor="black")
    ax.axvline(
        np.mean(response_data),
        color=palette[2],
        linestyle="--",
        linewidth=2,
        label=f"Mean: {np.mean(response_data):.2f}",
    )
    ax.axvline(
        np.median(response_data),
        color=palette[3],
        linestyle="--",
        linewidth=2,
        label=f"Median: {np.median(response_data):.2f}",
    )

    if styler is not None:
        styler.format_axes(
            ax,
            xlabel="Response Amplitude",
            ylabel="Frequency",
            title="Response Amplitude Distribution",
        )
    return ax


def receptor_specificity_curve(
    receptor_analysis: dict,
    binding_energies: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Derive illustrative specificity-vs-energy curve from Fermi receptor output."""
    if binding_energies is None:
        binding_energies = np.array([-25.0, -20.0, -15.0, -10.0, -5.0], dtype=float)
    base_spec = float(receptor_analysis["specificity_index"])
    specificity_values = np.linspace(base_spec * 0.6, base_spec, binding_energies.size)
    return binding_energies, specificity_values


def plot_receptor_specificity_curve(
    ax: plt.Axes,
    receptor_analysis: dict,
    *,
    binding_energies: Optional[np.ndarray] = None,
    styler: Optional[PlotStyler] = None,
    color: Optional[str] = None,
) -> plt.Axes:
    """Plot receptor binding specificity vs binding energy from analysis output."""
    energies, specificity = receptor_specificity_curve(receptor_analysis, binding_energies)
    line_color = color or get_colorblind_palette(1)[0]
    ax.plot(energies, specificity, color=line_color, marker="o", linewidth=2, markersize=8)

    if styler is not None:
        styler.format_axes(
            ax,
            xlabel="Binding Energy (kJ/mol)",
            ylabel="Specificity Index",
            title="Receptor Binding Specificity vs Energy",
            legend=False,
        )
    return ax
