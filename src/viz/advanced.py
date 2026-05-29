"""
Advanced visualization capabilities for insect analysis research.

This module provides enhanced plotting capabilities, interactive visualizations,
and publication-quality figure generation with better styling and customization
options.

Key Features:
- Publication-quality plots with consistent styling
- Interactive plotting support
- Advanced figure layouts and annotations
- Statistical visualization helpers
- Colorblind-friendly palettes
"""

import importlib.util
import logging
import numpy as np
import matplotlib.pyplot as plt

HAS_SEABORN = importlib.util.find_spec("seaborn") is not None

from typing import Dict, List, Optional, Tuple, Any, Union
import warnings

logger = logging.getLogger(__name__)

from src.config import get_config
from src.viz.panels import plot_correlation_heatmap
from src.viz.advanced_summary import create_statistical_summary_plot as build_statistical_summary_plot
from src.viz.styling import (
    PlotStyler,
    create_subplots,
    flatten_axes,
    get_colorblind_palette,
    set_plot_style,
)


def _plotly_available() -> bool:
    """Return True when plotly is installed and importable."""
    try:
        if importlib.util.find_spec("plotly") is None:
            return False
        if importlib.util.find_spec("plotly.graph_objects") is None:
            return False
        import plotly.graph_objects as go

        return hasattr(go, "Figure")
    except (ImportError, ModuleNotFoundError, ValueError, AttributeError):
        return False


def _validate_xy_arrays(x_data: np.ndarray, y_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Validate and coerce 1-D x/y arrays for plotting."""
    if x_data is None or y_data is None:
        raise ValueError("x_data and y_data must be provided")
    x_arr = np.asarray(x_data)
    y_arr = np.asarray(y_data)
    if x_arr.ndim != 1 or y_arr.ndim != 1:
        raise ValueError("x_data and y_data must be 1D arrays")
    if x_arr.size != y_arr.size:
        raise ValueError("x_data and y_data must have the same length")
    return x_arr, y_arr


class AdvancedVisualizer:
    """
    Advanced visualization tools for insect analysis data.

    Provides specialized plotting functions for different types of analysis
    with enhanced styling and publication-quality output.

    Examples:
        >>> visualizer = AdvancedVisualizer()
        >>> fig = visualizer.plot_spectral_analysis(wavenumbers, intensities)
        >>> visualizer.save_figure(fig, 'spectral_analysis.png')
    """

    def __init__(self, style: str = "default"):
        """
        Initialize advanced visualizer.

        Args:
            style: Plot style to use
        """
        self.styler = PlotStyler(style)
        self.config = get_config()

    def plot_spectral_analysis(
        self,
        wavenumbers: np.ndarray,
        intensities: np.ndarray,
        peaks: Optional[np.ndarray] = None,
        title: str = "Spectral Analysis",
    ) -> plt.Figure:
        """
        Create an advanced spectral analysis plot.

        Args:
            wavenumbers: Wavenumber array
            intensities: Intensity array
            peaks: Optional array of peak positions
            title: Plot title

        Returns:
            Matplotlib figure
        """
        # Basic validation
        if wavenumbers is None or intensities is None:
            raise ValueError("wavenumbers and intensities must be provided")
        if not isinstance(wavenumbers, np.ndarray):
            wavenumbers = np.asarray(wavenumbers)
        if not isinstance(intensities, np.ndarray):
            intensities = np.asarray(intensities)
        if wavenumbers.ndim != 1 or intensities.ndim != 1:
            raise ValueError("wavenumbers and intensities must be 1D arrays")
        if wavenumbers.size != intensities.size:
            raise ValueError("wavenumbers and intensities must have the same length")
        if wavenumbers.size == 0:
            # Return an informative empty figure
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(
                0.5, 0.5, "Empty spectrum", ha="center", va="center", transform=ax.transAxes, fontsize=12, color="gray"
            )
            ax.axis("off")
            return fig

        fig, axes = self.styler.create_figure_grid(2, 1, figsize=(12, 10))
        ax1, ax2 = axes[0], axes[1]

        # Main spectrum plot
        colors = self.styler.get_colors(2)
        ax1.plot(wavenumbers, intensities, color=colors[0], linewidth=2, label="Spectrum")

        if peaks is not None:
            peak_intensities = np.interp(peaks, wavenumbers, intensities)
            ax1.scatter(peaks, peak_intensities, color=colors[1], s=100, marker="v", label="Peaks", zorder=5)

        self.styler.format_axes(ax1, xlabel="Wavenumber (cm⁻¹)", ylabel="Intensity (a.u.)", title=title)

        # Derivative plot for peak detection and confidence interval shading
        if len(intensities) > 5:
            from scipy import signal

            derivative = np.gradient(intensities)
            # Estimate a simple moving standard deviation as a proxy for variability
            window = min(7, max(3, len(intensities) // 20))
            pad = window // 2
            mov_std = np.array(
                [
                    np.std(intensities[max(0, i - pad) : min(len(intensities), i + pad + 1)])
                    for i in range(len(intensities))
                ]
            )

            ax2.plot(wavenumbers, derivative, color=colors[1], linewidth=1.5, label="Derivative")
            # Shade +/- 1 std around derivative to show confidence region
            ax2.fill_between(wavenumbers, derivative - mov_std, derivative + mov_std, color=colors[1], alpha=0.2)
            ax2.axhline(y=0, color="black", linestyle="--", alpha=0.5)
            self.styler.format_axes(
                ax2, xlabel="Wavenumber (cm⁻¹)", ylabel="Derivative", title="First Derivative (with local std)"
            )

            # If peaks not provided, try to detect using SciPy's find_peaks
            if peaks is None:
                try:
                    peaks_idx, _ = signal.find_peaks(intensities, prominence=(np.max(intensities) * 0.05))
                    peaks = wavenumbers[peaks_idx]
                    peak_vals = intensities[peaks_idx]
                    # annotate peaks on main axis
                    for x, y in zip(peaks, peak_vals):
                        ax1.annotate(
                            f"{x:.1f}", xy=(x, y), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8
                        )
                except Exception:
                    peaks = None

        plt.tight_layout()
        return fig

    @staticmethod
    def annotate_top_peaks(ax: plt.Axes, wavenumbers: np.ndarray, intensities: np.ndarray, num_peaks: int = 5) -> None:
        """
        Annotate the top-N peaks by intensity on an axes.

        Args:
            ax: Target matplotlib Axes
            wavenumbers: 1D array of wavenumbers (cm⁻¹)
            intensities: 1D array of intensities
            num_peaks: Number of peaks to annotate
        """
        if wavenumbers.ndim != 1 or intensities.ndim != 1 or wavenumbers.size != intensities.size:
            return
        if wavenumbers.size == 0:
            return
        try:
            idx = np.argsort(intensities)[-num_peaks:][::-1]
            for i in idx:
                ax.annotate(
                    f"{wavenumbers[i]:.1f}",
                    xy=(wavenumbers[i], intensities[i]),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )
        except Exception:
            # Best-effort: do not raise in visualization helper
            pass

    def plot_correlation_matrix(
        self, data: Dict[str, np.ndarray], variables: List[str], title: str = "Correlation Analysis"
    ) -> plt.Figure:
        """
        Create a correlation matrix visualization.

        Args:
            data: Dictionary of variable arrays
            variables: List of variable names to correlate
            title: Plot title

        Returns:
            Matplotlib figure
        """
        # Create correlation matrix
        n_vars = len(variables)
        corr_matrix = np.zeros((n_vars, n_vars))

        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if var1 in data and var2 in data:
                    corr_matrix[i, j] = np.corrcoef(data[var1], data[var2])[0, 1]

        fig, ax = plt.subplots(figsize=(10, 8))
        plot_correlation_heatmap(ax, corr_matrix, variables, title=title)
        plt.tight_layout()
        return fig

    def plot_multi_panel_analysis(
        self, data_dict: Dict[str, Dict], title: str = "Multi-Panel Analysis", enhance_accessibility: bool = True
    ) -> plt.Figure:
        """
        Create a comprehensive multi-panel analysis figure with enhanced accessibility.

        Args:
            data_dict: Dictionary containing analysis data for each panel
            title: Overall figure title
            enhance_accessibility: Whether to apply accessibility enhancements

        Returns:
            Matplotlib figure
        """
        n_panels = len(data_dict)
        if n_panels <= 3:
            rows, cols = 1, n_panels
        else:
            rows = int(np.ceil(n_panels / 3))
            cols = min(n_panels, 3)

        fig, axes = self.styler.create_figure_grid(rows, cols, figsize=(5 * cols, 4 * rows))
        axes_flat = flatten_axes(axes)

        colors = self.styler.get_colors(n_panels, palette="high_contrast" if enhance_accessibility else "colorblind")

        for i, (panel_name, panel_data) in enumerate(data_dict.items()):
            ax = axes_flat[i]

            # Plot based on data type with enhanced styling
            if "x" in panel_data and "y" in panel_data:
                line = ax.plot(
                    panel_data["x"],
                    panel_data["y"],
                    color=colors[i],
                    linewidth=2.5,
                    marker="o" if len(panel_data["x"]) < 20 else None,
                    markersize=4 if len(panel_data["x"]) < 20 else None,
                )
                if "xlabel" in panel_data:
                    ax.set_xlabel(panel_data["xlabel"], fontweight="bold", fontsize=12)
                if "ylabel" in panel_data:
                    ax.set_ylabel(panel_data["ylabel"], fontweight="bold", fontsize=12)

                # Add data point annotations for small datasets
                if len(panel_data["x"]) <= 10 and "annotate" in panel_data and panel_data["annotate"]:
                    for j, (x_val, y_val) in enumerate(zip(panel_data["x"], panel_data["y"])):
                        ax.annotate(
                            f"({x_val:.1f}, {y_val:.1f})",
                            (x_val, y_val),
                            textcoords="offset points",
                            xytext=(0, 8),
                            ha="center",
                            fontsize=9,
                            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
                        )

            elif "histogram_data" in panel_data:
                data = panel_data["histogram_data"]
                n, bins, patches = ax.hist(data, bins=30, alpha=0.8, color=colors[i], edgecolor="black", linewidth=1.5)
                if "xlabel" in panel_data:
                    ax.set_xlabel(panel_data["xlabel"], fontweight="bold", fontsize=12)

                # Add statistics annotation
                if len(data) > 0:
                    mean_val = np.mean(data)
                    std_val = np.std(data)
                    ax.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"μ={mean_val:.2f}")
                    ax.text(
                        0.02,
                        0.98,
                        f"μ={mean_val:.2f}\nσ={std_val:.2f}",
                        transform=ax.transAxes,
                        verticalalignment="top",
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9),
                        fontsize=10,
                        fontweight="bold",
                    )

            # Enhanced title and formatting
            ax.set_title(f"{panel_name}", fontweight="bold", fontsize=13, pad=10)

            # Apply accessibility formatting
            if enhance_accessibility:
                ax.grid(True, alpha=0.4, linewidth=0.8)
                ax.tick_params(axis="both", which="major", labelsize=11)

        # Hide unused subplots
        for i in range(n_panels, len(axes_flat)):
            axes_flat[i].set_visible(False)

        # Enhanced main title with better spacing
        fig.suptitle(title, fontsize=16, fontweight="bold", y=0.95)

        # Add metadata annotation
        if enhance_accessibility:
            fig.text(
                0.02,
                0.02,
                f"Generated with enhanced accessibility features | {len(data_dict)} panels",
                fontsize=8,
                style="italic",
                alpha=0.7,
            )

        plt.tight_layout()
        return fig

    def create_interactive_plot(
        self, x_data: np.ndarray, y_data: np.ndarray, title: str = "Interactive Plot"
    ) -> Union[Any, plt.Figure]:
        """
        Create an interactive plot if plotly is available.

        Args:
            x_data: X-axis data
            y_data: Y-axis data
            title: Plot title

        Returns:
            Plotly figure or matplotlib figure if plotly unavailable
        """
        x_arr, y_arr = _validate_xy_arrays(x_data, y_data)

        from importlib import import_module

        viz = import_module("src.visualization")
        if viz._plotly_available():
            try:
                import plotly.graph_objects as go

                fig = go.Figure(data=go.Scatter(x=x_arr, y=y_arr, mode="lines+markers"))
                fig.update_layout(
                    title=title, xaxis_title="X Values", yaxis_title="Y Values", template="plotly_white"
                )
                if not hasattr(fig, "to_plotly_json"):
                    raise AttributeError("plotly figure missing to_plotly_json")
                return fig
            except Exception:
                warnings.warn("Plotly unavailable or broken, falling back to matplotlib")

        warnings.warn("Plotly not available, falling back to matplotlib")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_arr, y_arr, "b-", linewidth=2)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        return fig

    def create_statistical_summary_plot(self, data: Dict[str, Any], title: str = "Statistical Summary") -> plt.Figure:
        """Create a comprehensive statistical summary plot with enhanced accessibility."""
        return build_statistical_summary_plot(self.styler, data, title=title)

    def save_figure(
        self,
        fig: plt.Figure,
        filename: str,
        dpi: int = None,
        format: str = None,
        enhance_for_accessibility: bool = True,
    ) -> None:
        """
        Save figure with optimal settings for publication and accessibility.

        Args:
            fig: Matplotlib figure to save
            filename: Output filename
            dpi: Resolution (uses high DPI for accessibility if None)
            format: File format (inferred from extension if None)
            enhance_for_accessibility: Whether to use high DPI for better accessibility
        """
        if dpi is None:
            dpi = 600 if enhance_for_accessibility else self.config.get("plot_dpi", 300)

        if format is None:
            format = filename.split(".")[-1].lower()

        # Ensure output directory exists
        import os

        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)

        # Save with enhanced settings for accessibility
        fig.savefig(
            filename, dpi=dpi, format=format, bbox_inches="tight", facecolor="white", edgecolor="none", pad_inches=0.1
        )

        logger.info(
            "Saved figure: %s (DPI: %s, Format: %s, Accessibility: %s)",
            filename,
            dpi,
            format,
            enhance_for_accessibility,
        )


from .advanced_publication import create_accessible_figure, create_publication_figure

__all__ = [
    "HAS_SEABORN",
    "AdvancedVisualizer",
    "_plotly_available",
    "_validate_xy_arrays",
    "create_accessible_figure",
    "create_publication_figure",
]
