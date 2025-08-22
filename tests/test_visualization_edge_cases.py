"""
Comprehensive tests for visualization edge cases and error handling.

This file tests visualization edge cases, error conditions, and alternative code paths
to ensure robust error handling and fallback mechanisms.
"""

import sys
import types
import numpy as np
import matplotlib.pyplot as plt
import warnings
from unittest.mock import patch

from src.visualization import PlotStyler, AdvancedVisualizer


class TestVisualizationStyleHandling:
    """Test visualization style error handling."""

    def test_apply_style_handles_rcparams_update_keyerror(self, monkeypatch):
        """Simulate plt.rcParams.update raising KeyError and ensure apply_style falls back."""
        styler = PlotStyler()

        def raise_keyerror(_):
            raise KeyError("invalid param")

        monkeypatch.setattr(plt.rcParams, 'update', raise_keyerror)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            # Should not raise
            styler.apply_style('nature')
            assert any('Some style parameters may be invalid' in str(x.message) for x in w)

    def test_visualization_style_handling(self):
        """Test visualization style error handling."""
        styler = PlotStyler()

        # Test with invalid style - should not raise
        styler.apply_style('nonexistent_style')
        assert styler.current_style == 'nonexistent_style'


class TestInteractivePlotting:
    """Test interactive plotting functionality."""

    def test_create_interactive_plot_with_plotly(self, monkeypatch):
        """Provide a fake plotly module to exercise the interactive plotting branch."""
        # Create minimal fake plotly.graph_objects
        go = types.SimpleNamespace()

        class FakeFigure:
            def __init__(self, *args, **kwargs):
                self.data = args

            def update_layout(self, *a, **k):
                pass

        def FakeScatter(x, y, mode):
            return ('scatter', x, y, mode)

        go.Figure = FakeFigure
        go.Scatter = FakeScatter

        px = types.SimpleNamespace()

        sys.modules['plotly'] = types.SimpleNamespace()
        sys.modules['plotly.graph_objects'] = go
        sys.modules['plotly.express'] = px

        visualizer = AdvancedVisualizer()
        fig = visualizer.create_interactive_plot(np.array([1,2,3]), np.array([1,4,9]), title='Test')
        assert fig is not None

        # Clean up inserted modules
        del sys.modules['plotly.graph_objects']
        del sys.modules['plotly.express']
        if 'plotly' in sys.modules:
            del sys.modules['plotly']

    def test_create_interactive_plot_fallback(self, monkeypatch):
        """Test interactive plot fallback when plotly unavailable."""
        monkeypatch.setitem(sys.modules, 'plotly', None)
        visualizer = AdvancedVisualizer()
        fig = visualizer.create_interactive_plot(np.array([1,2,3]), np.array([1,4,9]))
        # Fallback returns a matplotlib Figure
        assert isinstance(fig, plt.Figure)
        if hasattr(fig, 'close'):
            plt.close(fig)


class TestSpectralAnalysisEdgeCases:
    """Test spectral analysis edge cases."""

    def test_plot_spectral_analysis_find_peaks_exception(self, monkeypatch):
        """Force scipy.signal.find_peaks to raise to exercise exception branch."""
        visualizer = AdvancedVisualizer()

        # Ensure we have scipy.signal available
        from scipy import signal

        def fake_find_peaks(*args, **kwargs):
            raise RuntimeError("boom")

        monkeypatch.setattr(signal, 'find_peaks', fake_find_peaks)

        wavenumbers = np.linspace(2500, 3000, 100)
        intensities = np.exp(-((wavenumbers - 2900) / 100)**2)

        # Should not raise even though find_peaks raises
        fig = visualizer.plot_spectral_analysis(wavenumbers, intensities, peaks=None)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestVisualizationReloadTests:
    """Test visualization module reloading under different import conditions."""

    def test_reload_with_seaborn_and_config_missing(self, tmp_path, monkeypatch):
        """Run the visualization module with seaborn present and src.config missing."""
        vis_path = 'src/visualization.py'

        # Ensure seaborn present
        fake_seaborn = types.ModuleType('seaborn')
        sys.modules['seaborn'] = fake_seaborn

        # Ensure src.config cannot be imported
        if 'src.config' in sys.modules:
            monkeypatch.delitem(sys.modules, 'src.config', raising=False)

        # Execute module in fresh namespace
        import runpy
        ns = runpy.run_path(vis_path)

        # HAS_SEABORN should be True in the executed namespace
        assert ns.get('HAS_SEABORN', False) is True

    def test_reload_without_seaborn_and_with_config(self, tmp_path, monkeypatch):
        """Run the visualization module with seaborn absent and real src.config available."""
        vis_path = 'src/visualization.py'

        # Ensure seaborn absent
        monkeypatch.setitem(sys.modules, 'seaborn', None)
        if 'seaborn' in sys.modules:
            del sys.modules['seaborn']

        # Execute module and ensure HAS_SEABORN is False
        import runpy
        ns = runpy.run_path(vis_path)
        assert ns.get('HAS_SEABORN', False) is False
