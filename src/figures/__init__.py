"""Core manuscript figure builders for cohereants."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from src.figure_registry_builder import build_figure_registry

from .atmosphere import generate_atmospheric_transmission_plot
from .chc_spectra import generate_chc_spectra_example
from .composite import generate_composite_multipanel
from .empirical_axes import generate_empirical_ir_axes
from .response_time import generate_response_time_comparison
from .sensilla_match import generate_sensilla_wavelength_matching
from .validation import validate_outputs

def generate_core_manuscript_figures(project_root: Path | None = None) -> list[Path]:
    """Generate core manuscript figures and return output PNG paths."""
    os.environ.setdefault("MPLBACKEND", "Agg")
    root = project_root or Path(__file__).resolve().parent.parent
    output_dir = root / "output"
    data_dir = str(output_dir / "data")
    figure_dir = str(output_dir / "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figure_dir, exist_ok=True)

    try:
        from src.config import set_random_seed
        from src.visualization import set_plot_style

        set_random_seed(42)
        set_plot_style("science")
    except ImportError:
        np.random.seed(42)

    paths = [
        generate_atmospheric_transmission_plot(figure_dir, data_dir),
        generate_sensilla_wavelength_matching(figure_dir, data_dir),
        generate_chc_spectra_example(figure_dir, data_dir),
        generate_response_time_comparison(figure_dir, data_dir),
        generate_composite_multipanel(figure_dir),
        generate_empirical_ir_axes(figure_dir, data_dir),
    ]
    figure_paths = [Path(p) for p in paths if p]
    build_figure_registry(root)
    is_valid, missing = validate_outputs(figure_dir, data_dir)
    if not is_valid:
        raise RuntimeError(f"Figure generation incomplete: {missing}")
    return figure_paths
