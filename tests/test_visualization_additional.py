"""
Additional tests to increase visualization coverage by exercising alternate code paths.
"""
import sys
import types
import numpy as np
import matplotlib.pyplot as plt
import warnings

from src.visualization import PlotStyler, AdvancedVisualizer


def test_apply_style_handles_rcparams_update_keyerror(monkeypatch):
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


def test_create_interactive_plot_with_plotly(monkeypatch):
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


def test_plot_spectral_analysis_find_peaks_exception(monkeypatch):
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


