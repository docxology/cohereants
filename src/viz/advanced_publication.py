"""Publication-level figure helpers built on AdvancedVisualizer."""

from __future__ import annotations

from typing import Any, Dict

import matplotlib.pyplot as plt

from .advanced import AdvancedVisualizer


def create_publication_figure(data: Dict[str, Any], style: str = "nature") -> plt.Figure:
    """
    Create a publication-ready figure with optimal styling.

    Args:
        data: Dictionary containing figure data
        style: Publication style ('nature', 'science', 'ieee')

    Returns:
        Matplotlib figure optimized for publication
    """
    visualizer = AdvancedVisualizer(style)

    if "spectral_data" in data:
        return visualizer.plot_spectral_analysis(
            data["wavenumbers"], data["intensities"], data.get("peaks"), data.get("title", "Spectral Analysis")
        )
    if "correlation_data" in data:
        return visualizer.plot_correlation_matrix(
            data["correlation_data"], data["variables"], data.get("title", "Correlation Analysis")
        )
    return visualizer.plot_multi_panel_analysis(data, data.get("title", "Analysis Figure"))


def create_accessible_figure(
    data_dict: Dict[str, Dict], title: str = "Analysis Figure", style: str = "science"
) -> plt.Figure:
    """
    Create an accessible figure with enhanced features for better understanding.

    Args:
        data_dict: Dictionary containing plot data for each panel
        title: Overall figure title
        style: Plot style to use

    Returns:
        Matplotlib figure optimized for accessibility
    """
    visualizer = AdvancedVisualizer(style)
    return visualizer.plot_multi_panel_analysis(data_dict, title, enhance_accessibility=True)
