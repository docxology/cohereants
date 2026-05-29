"""Plot styling utilities for publication-quality figures."""

from __future__ import annotations

import warnings
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


def flatten_axes(axes) -> np.ndarray:
    """Return a 1-D array of matplotlib Axes regardless of grid shape."""
    if isinstance(axes, np.ndarray):
        return axes.flatten()
    return np.array([axes])


class PlotStyler:
    """
    Advanced plot styling and theming system.

    Provides consistent, publication-quality styling with support for
    colorblind-friendly palettes and academic journal requirements.

    Examples:
        >>> styler = PlotStyler()
        >>> styler.apply_style('nature')
        >>> fig, ax = plt.subplots()
        >>> styler.format_axes(ax, xlabel='Wavenumber (cm⁻¹)', ylabel='Absorbance')
    """

    # Enhanced colorblind-friendly color palettes with better contrast
    COLORBLIND_PALETTE = [
        "#0072B2",  # Blue
        "#E69F00",  # Orange
        "#009E73",  # Green
        "#CC79A7",  # Pink
        "#56B4E9",  # Light blue
        "#D55E00",  # Red
        "#F0E442",  # Yellow
        "#000000",  # Black
    ]

    # High contrast palette for accessibility
    HIGH_CONTRAST_PALETTE = [
        "#000000",  # Black
        "#004488",  # Dark blue
        "#DDAA33",  # Yellow
        "#BB5566",  # Red
        "#000000",  # Black (duplicate for more options)
        "#004488",  # Dark blue
        "#DDAA33",  # Yellow
        "#BB5566",  # Red
    ]

    ACADEMIC_STYLES = {
        # Enhanced accessibility styles with larger fonts and better contrast
        "nature": {
            "font.family": "sans-serif",
            "font.size": 12,  # Increased from 7 for better readability
            "font.weight": "normal",
            "axes.linewidth": 1.0,  # Thicker lines for better visibility
            "xtick.major.size": 4,  # Larger ticks
            "ytick.major.size": 4,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.labelsize": 11,  # Explicit tick label size
            "ytick.labelsize": 11,
            "axes.labelsize": 12,  # Larger axis labels
            "axes.titlesize": 14,  # Larger titles
            "legend.fontsize": 11,  # Larger legend text
            "grid.alpha": 0.4,  # More visible grid
            "figure.dpi": 600,
            "lines.linewidth": 2.0,  # Thicker plot lines
            "lines.markersize": 6,  # Larger markers
        },
        "science": {
            "font.family": "sans-serif",
            "font.size": 13,  # Increased from 8
            "font.weight": "normal",
            "axes.linewidth": 1.2,  # Thicker lines
            "xtick.major.size": 5,  # Larger ticks
            "ytick.major.size": 5,
            "xtick.major.width": 1.2,
            "ytick.major.width": 1.2,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "axes.labelsize": 13,
            "axes.titlesize": 15,
            "legend.fontsize": 12,
            "grid.alpha": 0.5,
            "figure.dpi": 600,
            "lines.linewidth": 2.5,
            "lines.markersize": 7,
        },
        "ieee": {
            "font.family": "serif",
            "font.size": 12,  # Increased from 8
            "font.weight": "normal",
            "axes.linewidth": 1.0,
            "xtick.major.size": 4,
            "ytick.major.size": 4,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 14,
            "legend.fontsize": 11,
            "grid.alpha": 0.4,
            "figure.dpi": 300,
            "lines.linewidth": 2.0,
            "lines.markersize": 6,
        },
    }

    def __init__(self, style: str = "default"):
        """
        Initialize plot styler.

        Args:
            style: Initial style to apply ('default', 'nature', 'science', 'ieee')
        """
        self.current_style = style
        self.apply_style(style)

    def apply_style(self, style: str) -> None:
        """
        Apply a predefined style to matplotlib.

        Args:
            style: Style name to apply
        """
        if style == "default":
            # Reset to matplotlib defaults with some improvements
            try:
                plt.style.use("default")
            except Exception as e:
                warnings.warn(f"Failed to apply base style 'default': {e}")
            plt.rcParams.update(
                {
                    "font.size": 10,
                    "font.family": "sans-serif",
                    "axes.linewidth": 0.8,
                    "axes.grid": True,
                    "grid.alpha": 0.3,
                    "figure.dpi": 150,
                }
            )
        elif style in self.ACADEMIC_STYLES:
            try:
                plt.style.use("default")
            except Exception:
                # If applying the default style fails, continue and attempt to update rcParams
                warnings.warn("Could not apply default style; continuing with rcParams update")
            settings = self.ACADEMIC_STYLES[style]
            try:
                plt.rcParams.update(settings)
            except Exception as e:
                # Handle invalid matplotlib parameters gracefully (KeyError or other)
                warnings.warn(f"Some style parameters may be invalid or update failed: {e}")
                # Update only valid parameters where possible
                try:
                    valid_settings = {k: v for k, v in settings.items() if k in plt.rcParams}
                    if valid_settings:
                        try:
                            plt.rcParams.update(valid_settings)
                        except Exception as e2:
                            warnings.warn(f"Failed to update partial rcParams: {e2}")
                except Exception:
                    # In case plt.rcParams is not subscriptable or other failure
                    pass
        else:
            try:
                plt.style.use(style)
                self.current_style = style
            except OSError:
                warnings.warn(f"Style '{style}' not found, using default")
                self.apply_style("default")
                return

        if style in ("default",) or style in self.ACADEMIC_STYLES:
            self.current_style = style

    def get_colors(self, n: int, palette: str = "colorblind") -> List[str]:
        """
        Get a list of colors from a predefined palette with enhanced accessibility.

        Args:
            n: Number of colors needed
            palette: Palette name ('colorblind', 'high_contrast', 'viridis', 'plasma', 'tab10')

        Returns:
            List of color hex codes optimized for accessibility
        """
        if palette == "colorblind":
            colors = self.COLORBLIND_PALETTE
        elif palette == "high_contrast":
            colors = self.HIGH_CONTRAST_PALETTE
        else:
            try:
                cmap = plt.get_cmap(palette)
                colors = [cmap(i / n) for i in range(n)]
                colors = [plt.matplotlib.colors.to_hex(c) for c in colors]
            except ValueError:
                warnings.warn(f"Palette '{palette}' not found, using colorblind")
                colors = self.COLORBLIND_PALETTE

        # Cycle through colors if n > palette size
        return [colors[i % len(colors)] for i in range(n)]

    def format_axes(
        self,
        ax: plt.Axes,
        xlabel: str = None,
        ylabel: str = None,
        title: str = None,
        legend: bool = True,
        enhance_accessibility: bool = True,
    ) -> plt.Axes:
        """
        Format axes with enhanced accessibility and consistent styling.

        Args:
            ax: Matplotlib axes to format
            xlabel: X-axis label
            ylabel: Y-axis label
            title: Plot title
            legend: Whether to show legend if present
            enhance_accessibility: Whether to apply accessibility enhancements

        Returns:
            Formatted axes object
        """
        if xlabel:
            ax.set_xlabel(xlabel, fontweight="bold", fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontweight="bold", fontsize=12)
        if title:
            ax.set_title(title, fontweight="bold", pad=15, fontsize=14)

        # Enhanced tick formatting for accessibility
        if enhance_accessibility:
            ax.tick_params(axis="both", which="major", labelsize=11, width=1.0, length=4)
            # Ensure minimum tick spacing for readability
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            ax.yaxis.set_major_locator(plt.MaxNLocator(6))

        # Add more visible grid for better data reading
        ax.grid(True, alpha=0.4, linestyle="-", linewidth=0.8, color="gray")

        # Remove top and right spines for cleaner look (but keep bottom/left thicker)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_linewidth(1.2)
        ax.spines["left"].set_linewidth(1.2)

        if legend and ax.get_legend_handles_labels()[1]:
            legend_obj = ax.legend(frameon=True, fancybox=True, shadow=False, framealpha=0.9, loc="best", fontsize=11)
            # Make legend frame more visible
            legend_obj.get_frame().set_linewidth(1.5)

        # Add subtle background color for better contrast
        if enhance_accessibility:
            ax.set_facecolor("#FAFAFA")

        return ax

    def create_figure_grid(
        self, rows: int, cols: int, figsize: Tuple[float, float] = None, **kwargs
    ) -> Tuple[plt.Figure, np.ndarray]:
        """
        Create a figure with a grid layout optimized for academic publishing.

        Args:
            rows: Number of subplot rows
            cols: Number of subplot columns
            figsize: Figure size tuple (width, height)
            **kwargs: Additional arguments for plt.subplots

        Returns:
            Tuple of (figure, axes_array)
        """
        if figsize is None:
            # Auto-scale figure size based on grid dimensions
            base_size = 4
            figsize = (base_size * cols, base_size * rows)

        fig, axes = plt.subplots(rows, cols, figsize=figsize, **kwargs)
        if rows == 1 and cols == 1:
            axes_array: np.ndarray = np.array([axes])
        else:
            axes_array = np.asarray(axes)

        for ax in flatten_axes(axes_array):
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig, axes_array


def set_plot_style(style: str) -> None:
    """Set the global plot style."""
    PlotStyler().apply_style(style)


def get_colorblind_palette(n_colors: int = 8) -> List[str]:
    """Get a colorblind-friendly color palette."""
    return PlotStyler().get_colors(n_colors, "colorblind")


def create_subplots(
    n_rows: int,
    n_cols: int,
    style: str = "science",
    figsize: Tuple[float, float] | None = None,
    enhance_accessibility: bool = True,
) -> Tuple[plt.Figure, np.ndarray]:
    """Create subplots with enhanced accessibility and consistent styling."""
    _ = enhance_accessibility
    return PlotStyler(style).create_figure_grid(n_rows, n_cols, figsize)
