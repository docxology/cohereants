"""
Comprehensive tests for visualization edge cases and error handling.

This file tests visualization edge cases, error conditions, and alternative code paths
to ensure robust error handling and fallback mechanisms.
"""

import importlib.util
import sys
import types

import matplotlib.pyplot as plt
import numpy as np
import pytest
import warnings

from src.visualization import HAS_SEABORN, AdvancedVisualizer, PlotStyler
from src.viz.plotly_helpers import plotly_title_text


class TestVisualizationStyleHandling:
    """Test visualization style error handling."""

    def test_plotstyler_get_colors_fallback(self):
        """Invalid palette names fall back to colorblind colors."""
        styler = PlotStyler()
        colors = styler.get_colors(5, palette="nonexistent_palette")
        assert len(colors) == 5
        assert all(isinstance(c, str) for c in colors)

    def test_apply_style_handles_rcparams_update_keyerror(self, monkeypatch):
        """Simulate plt.rcParams.update raising KeyError and ensure apply_style falls back."""
        styler = PlotStyler()

        def raise_keyerror(_):
            raise KeyError("invalid param")

        monkeypatch.setattr(plt.rcParams, "update", raise_keyerror)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            styler.apply_style("nature")
            assert any("Some style parameters may be invalid" in str(x.message) for x in w)

    def test_visualization_style_handling(self):
        """Unknown matplotlib style names fall back to default."""
        styler = PlotStyler()
        styler.apply_style("nonexistent_style")
        assert styler.current_style == "default"


class TestInteractivePlotting:
    """Test interactive plotting functionality."""

    def test_plotly_helpers(self):
        from src.viz.plotly_helpers import plotly_title_text, plotly_trace_values

        assert plotly_title_text({"layout": {"title": {"text": "Hi"}}}) == "Hi"
        assert plotly_title_text({"layout": {"title": "Plain"}}) == "Plain"
        assert plotly_trace_values({"x": [1.0, 2.0]}, "x") == [1.0, 2.0]
        assert plotly_trace_values({"x": {"bdata": "abc"}}, "x") is None

    def test_create_interactive_plot_with_plotly(self, monkeypatch):
        """Provide a fake plotly module to exercise the interactive plotting branch."""
        go = types.SimpleNamespace()

        class FakeFigure:
            def __init__(self, *args, **kwargs):
                self.data = args
                self._title = ""

            def update_layout(self, *a, **k):
                self._title = k.get("title", "")

            def to_plotly_json(self):
                return {
                    "layout": {"title": {"text": self._title}},
                    "data": [{"x": [1, 2, 3], "y": [1, 4, 9]}],
                }

        def FakeScatter(x, y, mode):
            return ("scatter", x, y, mode)

        go.Figure = FakeFigure
        go.Scatter = FakeScatter

        monkeypatch.setitem(sys.modules, "plotly", types.ModuleType("plotly"))
        monkeypatch.setitem(sys.modules, "plotly.graph_objects", go)
        monkeypatch.setattr("src.visualization._plotly_available", lambda: True)

        visualizer = AdvancedVisualizer()
        fig = visualizer.create_interactive_plot(np.array([1, 2, 3]), np.array([1, 4, 9]), title="Test")
        assert fig is not None
        assert plotly_title_text(fig.to_plotly_json()) == "Test"

    def test_create_interactive_plot_fallback(self, monkeypatch):
        """Test interactive plot fallback when plotly unavailable."""
        monkeypatch.setitem(sys.modules, "plotly", None)
        monkeypatch.delitem(sys.modules, "plotly.graph_objects", raising=False)
        visualizer = AdvancedVisualizer()
        fig = visualizer.create_interactive_plot(np.array([1, 2, 3]), np.array([1, 4, 9]))
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestSpectralAnalysisEdgeCases:
    """Test spectral analysis edge cases."""

    def test_plot_spectral_analysis_empty_and_mismatch(self):
        """Empty arrays return a figure; mismatched lengths raise."""
        visualizer = AdvancedVisualizer()
        fig_empty = visualizer.plot_spectral_analysis(np.array([]), np.array([]))
        assert isinstance(fig_empty, plt.Figure)
        plt.close(fig_empty)

        with pytest.raises(ValueError):
            visualizer.plot_spectral_analysis(np.linspace(100, 200, 10), np.linspace(0, 1, 5))

    def test_annotate_top_peaks_invalid_shapes(self):
        visualizer = AdvancedVisualizer()
        fig, ax = plt.subplots()
        visualizer.annotate_top_peaks(ax, np.array([[1, 2]]), np.array([1, 2]))
        plt.close(fig)

    def test_plot_spectral_analysis_find_peaks_exception(self, monkeypatch):
        """Force scipy.signal.find_peaks to raise to exercise exception branch."""
        visualizer = AdvancedVisualizer()
        from scipy import signal

        def fake_find_peaks(*args, **kwargs):
            raise RuntimeError("boom")

        monkeypatch.setattr(signal, "find_peaks", fake_find_peaks)

        wavenumbers = np.linspace(2500, 3000, 100)
        intensities = np.exp(-((wavenumbers - 2900) / 100) ** 2)

        fig = visualizer.plot_spectral_analysis(wavenumbers, intensities, peaks=None)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestSeabornAvailability:
    """Test optional seaborn detection without runpy reload."""

    def test_has_seaborn_matches_find_spec(self):
        assert HAS_SEABORN == (importlib.util.find_spec("seaborn") is not None)

    def test_has_seaborn_false_when_find_spec_blocked(self, monkeypatch):
        real_find_spec = importlib.util.find_spec

        def blocked_find_spec(name, package=None):
            if name == "seaborn":
                return None
            return real_find_spec(name, package)

        monkeypatch.setattr(importlib.util, "find_spec", blocked_find_spec)
        monkeypatch.delitem(sys.modules, "src.visualization", raising=False)
        reloaded = importlib.import_module("src.visualization")
        assert reloaded.HAS_SEABORN is False
