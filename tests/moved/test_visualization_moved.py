import matplotlib.pyplot as plt
import numpy as np
from src.visualization import PlotStyler, AdvancedVisualizer


def test_visualization_and_integrated_figures(tmp_path):
    styler = PlotStyler()
    colors = styler.get_colors(4, palette='nonexistent_palette')
    assert len(colors) == 4

    fig, axes = styler.create_figure_grid(1, 1)
    assert fig is not None
    plt.close(fig)

    visualizer = AdvancedVisualizer()
    data_dict = {f'panel{i}': {'x': np.linspace(0, 1, 10), 'y': np.linspace(i, i+1, 10)} for i in range(5)}
    fig2 = visualizer.plot_multi_panel_analysis(data_dict)
    assert fig2 is not None
    plt.close(fig2)


