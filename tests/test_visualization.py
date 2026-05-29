"""
Real-data tests for the visualization module.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

try:
    import src.visualization as visualization
    from src.visualization import (
        AdvancedVisualizer,
        PlotStyler,
        create_publication_figure,
        create_subplots,
        get_colorblind_palette,
        set_plot_style,
    )
    from src.viz.plotly_helpers import plotly_title_text, plotly_trace_values
except ImportError:
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import src.visualization as visualization
    from src.visualization import (
        AdvancedVisualizer,
        PlotStyler,
        create_publication_figure,
        create_subplots,
        get_colorblind_palette,
        set_plot_style,
    )
    from src.viz.plotly_helpers import plotly_title_text, plotly_trace_values


class TestPlotStyler:
    """Test the PlotStyler class."""

    def test_initialization(self):
        styler = PlotStyler()
        assert styler.current_style == "default"

    def test_apply_style(self):
        styler = PlotStyler()
        styler.apply_style("default")
        assert styler.current_style == "default"

        for style in ["nature", "science", "ieee"]:
            styler.apply_style(style)
            assert styler.current_style == style

    def test_get_colors(self):
        styler = PlotStyler()
        colors = styler.get_colors(5, "colorblind")
        assert len(colors) == 5
        assert all(color.startswith("#") for color in colors)

        wrapped = styler.get_colors(15, "colorblind")
        assert len(wrapped) == 15
        assert wrapped[0] == styler.COLORBLIND_PALETTE[0]

    def test_format_axes(self):
        styler = PlotStyler()
        fig, ax = plt.subplots()

        formatted_ax = styler.format_axes(ax, xlabel="Test X Label", ylabel="Test Y Label", title="Test Title")

        assert formatted_ax is ax
        assert ax.get_xlabel() == "Test X Label"
        assert ax.get_ylabel() == "Test Y Label"
        assert ax.get_title() == "Test Title"
        plt.close("all")

    def test_create_figure_grid(self):
        styler = PlotStyler()

        fig, axes = styler.create_figure_grid(1, 1)
        assert axes.shape == (1,)
        assert hasattr(axes[0], "plot")
        plt.close(fig)

        fig, axes = styler.create_figure_grid(2, 2)
        assert axes.shape == (2, 2)
        plt.close(fig)

        fig, _ = styler.create_figure_grid(1, 1, figsize=(10, 8))
        assert fig.get_size_inches().tolist() == [10, 8]
        plt.close(fig)


class TestAdvancedVisualizer:
    """Test the AdvancedVisualizer class."""

    def test_initialization(self):
        visualizer = AdvancedVisualizer()
        assert isinstance(visualizer.styler, PlotStyler)
        assert visualizer.styler.current_style == "default"

    def test_plot_spectral_analysis(self):
        visualizer = AdvancedVisualizer()
        wavenumbers = np.linspace(2500, 3000, 100)
        intensities = np.exp(-((wavenumbers - 2900) / 100) ** 2)
        peaks = np.array([2900])

        fig = visualizer.plot_spectral_analysis(wavenumbers, intensities, peaks)

        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 2
        plt.close("all")

    def test_plot_correlation_matrix(self):
        visualizer = AdvancedVisualizer()
        rng = np.random.default_rng(42)
        data = {
            "var1": rng.normal(size=100),
            "var2": rng.normal(size=100),
            "var3": rng.normal(size=100),
        }

        fig = visualizer.plot_correlation_matrix(data, ["var1", "var2", "var3"])

        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) >= 2
        plt.close("all")

    def test_plot_multi_panel_analysis(self):
        visualizer = AdvancedVisualizer()
        data = {
            "Panel 1": {
                "x": np.linspace(0, 10, 100),
                "y": np.sin(np.linspace(0, 10, 100)),
                "xlabel": "Time",
                "ylabel": "Signal",
            },
            "Panel 2": {
                "histogram_data": np.random.default_rng(0).normal(size=1000),
                "xlabel": "Value",
            },
        }

        fig = visualizer.plot_multi_panel_analysis(data)

        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 2
        plt.close("all")

    def test_plot_multi_panel_single_panel(self):
        visualizer = AdvancedVisualizer()
        data = {
            "Only": {
                "x": np.linspace(0, 1, 5),
                "y": np.linspace(0, 1, 5),
                "xlabel": "X",
                "ylabel": "Y",
            }
        }
        fig = visualizer.plot_multi_panel_analysis(data)
        assert isinstance(fig, plt.Figure)
        assert len([ax for ax in fig.axes if ax.get_visible()]) == 1
        plt.close(fig)

    def test_create_interactive_plot_input_validation(self):
        visualizer = AdvancedVisualizer()
        with pytest.raises(ValueError, match="same length"):
            visualizer.create_interactive_plot(np.array([1, 2]), np.array([1]))

    def test_create_interactive_plot_real_branch(self):
        visualizer = AdvancedVisualizer()
        x_data = np.array([1, 2, 3])
        y_data = np.array([1, 4, 9])

        result = visualizer.create_interactive_plot(x_data, y_data, title="Quadratic")

        if isinstance(result, plt.Figure):
            assert len(result.axes) == 1
            assert result.axes[0].get_title() == "Quadratic"
            plt.close(result)
        else:
            as_json = result.to_plotly_json()
            assert plotly_title_text(as_json) == "Quadratic"
            x_vals = plotly_trace_values(as_json["data"][0], "x")
            if x_vals is not None:
                assert x_vals == [1.0, 2.0, 3.0]

    def test_save_figure_creates_directory_and_logs(self, tmp_path, caplog):
        import logging

        visualizer = AdvancedVisualizer()
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        output_path = tmp_path / "nested" / "figure.png"

        with caplog.at_level(logging.INFO):
            visualizer.save_figure(fig, str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 0
        assert any("Saved figure:" in record.message for record in caplog.records)
        plt.close("all")


def test_visualization_and_integrated_figures_moved():
    styler = PlotStyler()
    colors = styler.get_colors(4, palette="nonexistent_palette")
    assert len(colors) == 4

    fig, _ = styler.create_figure_grid(1, 1)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

    visualizer = AdvancedVisualizer()
    data_dict = {
        f"panel{i}": {"x": np.linspace(0, 1, 10), "y": np.linspace(i, i + 1, 10)}
        for i in range(5)
    }
    fig2 = visualizer.plot_multi_panel_analysis(data_dict)
    assert isinstance(fig2, plt.Figure)
    plt.close("all")


class TestUtilityFunctions:
    """Test utility functions."""

    def test_get_colorblind_palette(self):
        colors = get_colorblind_palette(5)
        assert len(colors) == 5
        assert all(color.startswith("#") for color in colors)

    def test_create_subplots(self):
        fig, axes = create_subplots(2, 2)
        assert isinstance(fig, plt.Figure)
        assert axes.shape == (2, 2)
        plt.close("all")

    def test_create_publication_figure(self):
        spectral_data = {
            "spectral_data": True,
            "wavenumbers": np.linspace(2500, 3000, 100),
            "intensities": np.random.default_rng(1).normal(size=100),
            "peaks": np.array([2900]),
            "title": "Test Spectrum",
        }
        fig = create_publication_figure(spectral_data, "default")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

        correlation_data = {
            "correlation_data": {
                "var1": np.random.default_rng(2).normal(size=50),
                "var2": np.random.default_rng(3).normal(size=50),
            },
            "variables": ["var1", "var2"],
            "title": "Test Correlation",
        }
        fig = create_publication_figure(correlation_data)
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_plot_spectral_analysis_auto_peak_detection(self):
        visualizer = AdvancedVisualizer()
        wavenumbers = np.linspace(2500, 3000, 500)
        intensities = np.exp(-((wavenumbers - 2700) / 10) ** 2) + 0.8 * np.exp(-((wavenumbers - 2900) / 8) ** 2)

        fig = visualizer.plot_spectral_analysis(wavenumbers, intensities, peaks=None)
        assert isinstance(fig, plt.Figure)
        assert len(fig.axes[0].texts) >= 1
        plt.close("all")

    def test_get_colors_with_cmap(self):
        styler = PlotStyler()
        colors = styler.get_colors(5, "viridis")
        assert len(colors) == 5
        assert all(isinstance(color, str) for color in colors)


class TestVizPanels:
    """Shared panel helpers."""

    def test_plot_correlation_heatmap(self):
        from src.viz.panels import plot_correlation_heatmap

        matrix = np.array([[1.0, 0.5], [0.5, 1.0]])
        fig, ax = plt.subplots()
        plot_correlation_heatmap(ax, matrix, ["a", "b"], title="Test")
        assert ax.get_title() == "Test"
        plt.close(fig)

    def test_receptor_specificity_curve(self):
        from src.viz.panels import receptor_specificity_curve

        receptor = {"specificity_index": 0.75}
        energies, values = receptor_specificity_curve(receptor)
        assert energies.size == values.size == 5
        assert values[-1] == pytest.approx(0.75)


class TestVisualizationEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_data_handling(self):
        visualizer = AdvancedVisualizer()
        fig = visualizer.plot_spectral_analysis(np.array([]), np.array([]))
        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1
        plt.close("all")

    def test_single_point_data(self):
        visualizer = AdvancedVisualizer()
        fig = visualizer.plot_spectral_analysis(np.array([2900]), np.array([1.0]))
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_invalid_style_handling(self):
        styler = PlotStyler()
        styler.apply_style("nonexistent_style")
        assert styler.current_style == "default"

    def test_large_color_request(self):
        styler = PlotStyler()
        colors = styler.get_colors(100, "colorblind")
        assert len(colors) == 100

    def test_correlation_matrix_edge_cases(self):
        visualizer = AdvancedVisualizer()

        fig = visualizer.plot_correlation_matrix({"var1": np.array([1, 2, 3, 4, 5])}, ["var1"])
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

        fig = visualizer.plot_correlation_matrix(
            {"var1": np.array([1, 1, 1, 1]), "var2": np.array([2, 2, 2, 2])},
            ["var1", "var2"],
        )
        assert isinstance(fig, plt.Figure)
        plt.close("all")

    def test_seaborn_unavailable(self):
        original = visualization.HAS_SEABORN
        try:
            visualization.HAS_SEABORN = False
            styler = PlotStyler()
            colors = styler.get_colors(5)
            assert len(colors) == 5
        finally:
            visualization.HAS_SEABORN = original

    def test_multi_panel_with_empty_data(self):
        visualizer = AdvancedVisualizer()
        fig = visualizer.plot_multi_panel_analysis(
            {
                "Empty Panel": {},
                "Another Panel": {"x": [], "y": []},
            }
        )
        assert isinstance(fig, plt.Figure)
        plt.close("all")

# --- merged from test_coverage_visualization.py ---

def test_plot_multi_panel_analysis_line_histogram_and_hidden_subplots():
    visualizer = AdvancedVisualizer("default")
    rng = np.random.default_rng(0)
    data = {
        "Line+Annotate": {
            "x": np.linspace(0.0, 1.0, 6),
            "y": np.linspace(0.0, 1.0, 6),
            "xlabel": "X",
            "ylabel": "Y",
            "annotate": True,
        },
        "Histogram": {
            "histogram_data": rng.normal(0.0, 1.0, 200),
            "xlabel": "Value",
        },
        "LargeLine": {
            "x": np.linspace(0.0, 1.0, 30),
            "y": np.sin(np.linspace(0.0, 1.0, 30)),
        },
        # A 4th panel forces a 2x3 grid -> the hidden-subplot loop runs for the
        # two unused axes.
        "SmallLine": {
            "x": np.linspace(0.0, 1.0, 5),
            "y": np.linspace(1.0, 0.0, 5),
        },
    }
    fig = visualizer.plot_multi_panel_analysis(
        data, title="Multi Panel", enhance_accessibility=True
    )
    assert hasattr(fig, "savefig")
    # 4 panels rounds up to a 2x3 grid (6 axes), two of which are hidden.
    assert len(fig.axes) == 6
    visible = [ax for ax in fig.axes if ax.get_visible()]
    assert len(visible) == 4
    plt.close(fig)


def test_create_statistical_summary_plot_all_panels():
    visualizer = AdvancedVisualizer("default")
    rng = np.random.default_rng(1)
    data = {
        "distributions": {
            "A": rng.normal(0.0, 1.0, 100),
            "B": rng.normal(1.0, 1.0, 100),
        },
        "boxplot_data": {
            "X": rng.normal(0.0, 1.0, 50),
            "Y": rng.normal(1.0, 1.0, 50),
        },
        "correlation_matrix": np.array([[1.0, 0.5], [0.5, 1.0]]),
        "summary_stats": {
            "metricA": 1.234,
            "group": {"sub1": 2.0, "sub2": 3.0},
        },
    }
    fig = visualizer.create_statistical_summary_plot(data, title="Summary")
    assert hasattr(fig, "savefig")
    assert len(fig.axes) >= 4
    plt.close(fig)


def test_annotate_top_peaks_and_guards():
    visualizer = AdvancedVisualizer("default")
    wavelengths = np.linspace(2.0, 25.0, 50)
    intensities = np.exp(-(((wavelengths - 10.0) / 2.0) ** 2))

    fig, ax = plt.subplots()
    visualizer.annotate_top_peaks(ax, wavelengths, intensities, num_peaks=3)
    # Three peak annotations were added as text artists.
    assert len(ax.texts) == 3
    plt.close(fig)

    # Guard branches: empty input and shape mismatch both return without raising.
    fig2, ax2 = plt.subplots()
    visualizer.annotate_top_peaks(ax2, np.array([]), np.array([]))
    visualizer.annotate_top_peaks(ax2, wavelengths, intensities[:-1])
    assert len(ax2.texts) == 0
    plt.close(fig2)


def test_create_publication_figure_correlation_path():
    data = {
        "correlation_data": {
            "a": np.arange(10.0),
            "b": np.arange(10.0) * 2.0,
        },
        "variables": ["a", "b"],
        "title": "Correlation",
    }
    fig = create_publication_figure(data, style="science")
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_set_plot_style_runs_without_error():
    set_plot_style("nature")
    # rcParams should reflect a non-default font size after applying the style.
    assert plt.rcParams["font.size"] == 12  # the "nature" style sets font.size=12
    set_plot_style("default")


def test_get_colors_colormap_and_invalid_palette_fallback():
    styler = PlotStyler("default")

    cmap_colors = styler.get_colors(5, palette="viridis")
    assert len(cmap_colors) == 5
    assert all(isinstance(color, str) and color.startswith("#") for color in cmap_colors)

    fallback_colors = styler.get_colors(3, palette="definitely_not_a_palette")
    assert len(fallback_colors) == 3
    # Fallback uses the colorblind palette.
    assert fallback_colors[0] == PlotStyler.COLORBLIND_PALETTE[0]
