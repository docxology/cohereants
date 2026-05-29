"""Statistical summary plotting helpers for AdvancedVisualizer."""

from __future__ import annotations

from typing import Any, Dict

import matplotlib.pyplot as plt
import numpy as np


def create_statistical_summary_plot(styler, data: Dict[str, Any], title: str = "Statistical Summary") -> plt.Figure:
    """
    Create a comprehensive statistical summary plot with enhanced accessibility.

    Args:
        styler: PlotStyler instance
        data: Dictionary containing statistical data to plot
        title: Overall figure title

    Returns:
        Matplotlib figure with statistical summaries
    """
    fig, axes = styler.create_figure_grid(2, 2, figsize=(12, 10))
    axes = axes.reshape(2, 2)

    colors = styler.get_colors(8, palette="high_contrast")

    if "distributions" in data:
        ax = axes[0, 0]
        for i, (name, values) in enumerate(data["distributions"].items()):
            if len(values) > 0:
                ax.hist(
                    values,
                    bins=20,
                    alpha=0.7,
                    color=colors[i],
                    label=f"{name}\nμ={np.mean(values):.2f}",
                    linewidth=1.5,
                )
        ax.set_xlabel("Value", fontweight="bold", fontsize=12)
        ax.set_ylabel("Frequency", fontweight="bold", fontsize=12)
        ax.set_title("Data Distributions", fontweight="bold", fontsize=13)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.4)

    if "boxplot_data" in data:
        ax = axes[0, 1]
        labels = list(data["boxplot_data"].keys())
        values = [data["boxplot_data"][label] for label in labels]
        bp = ax.boxplot(values, labels=labels, patch_artist=True)
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax.set_ylabel("Value", fontweight="bold", fontsize=12)
        ax.set_title("Box Plot Comparison", fontweight="bold", fontsize=13)
        ax.grid(True, alpha=0.4, axis="y")

    if "correlation_matrix" in data:
        ax = axes[1, 0]
        corr_matrix = data["correlation_matrix"]
        im = ax.imshow(corr_matrix, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_title("Correlation Matrix", fontweight="bold", fontsize=13)

        for i in range(corr_matrix.shape[0]):
            for j in range(corr_matrix.shape[1]):
                ax.text(j, i, f"{corr_matrix[i, j]:.2f}", ha="center", va="center", color="black", fontsize=10)

        plt.colorbar(im, ax=ax, shrink=0.8)

    if "summary_stats" in data:
        ax = axes[1, 1]
        ax.axis("off")
        stats = data["summary_stats"]

        table_data = []
        for key, values in stats.items():
            if isinstance(values, dict):
                for subkey, val in values.items():
                    table_data.append([f"{key}\n{subkey}", f"{val:.3f}"])
            else:
                table_data.append([key, f"{values:.3f}"])

        table = ax.table(
            cellText=table_data,
            colLabels=["Metric", "Value"],
            loc="center",
            cellLoc="center",
            colColours=["lightgray", "lightgray"],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        ax.set_title("Summary Statistics", fontweight="bold", fontsize=13, pad=20)

    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.95)
    plt.tight_layout()

    return fig
