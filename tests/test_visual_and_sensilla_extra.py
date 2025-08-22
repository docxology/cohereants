import os
import numpy as np
import matplotlib.pyplot as plt

from src.visualization import (
    PlotStyler,
    AdvancedVisualizer,
    create_publication_figure,
    create_subplots,
    get_colorblind_palette,
)

from src.case_studies.sensilla_array_directionality import (
    sensilla_element_pattern,
    mutual_coupling_matrix,
    array_pattern_2d,
    design_circular_array,
)


def test_plotstyler_and_advanced_visualizer(tmp_path):
    styler = PlotStyler()
    # invalid style should fallback without exception
    styler.apply_style('nonexistent_style')

    colors = styler.get_colors(12, palette='viridis')
    assert len(colors) == 12

    fig, axes = create_subplots(1, 1)
    assert fig is not None

    av = AdvancedVisualizer()
    # small spectral arrays -> empty-spectrum branch handled
    fig_empty = av.plot_spectral_analysis(np.array([]), np.array([]))
    assert fig_empty is not None

    # create_publication_figure generic branch
    fig2 = create_publication_figure({'panel1': {'x': [0, 1], 'y': [0, 1]}}, style='nature')
    assert fig2 is not None

    # save a figure to tmp
    out = tmp_path / "test_fig.png"
    av.save_figure(fig2, str(out))
    assert out.exists()


def test_sensilla_element_and_array_patterns():
    theta = np.linspace(0, 180, 37)
    # dipole
    p = sensilla_element_pattern(theta, 10.0, 5.0, element_type='dipole')
    assert p.shape == theta.shape

    # monopole and patch
    m = sensilla_element_pattern(theta, 8.0, 4.0, element_type='monopole')
    q = sensilla_element_pattern(theta, 12.0, 6.0, element_type='patch')
    assert np.all(m >= 0) and np.all(q >= 0)

    # mutual coupling with 1D positions
    Z = mutual_coupling_matrix(np.array([0.0, 10.0, 20.0]), 5.0)
    assert Z.shape == (3, 3)

    # array_pattern_2d with include_coupling False
    circ = design_circular_array(5.0, 4)
    positions = np.column_stack([circ['x_positions'], circ['y_positions']])
    ap = array_pattern_2d(np.array([5.0]), positions, np.ones(positions.shape[0]), include_coupling=False)
    assert 'patterns' in ap


