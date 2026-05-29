from __future__ import annotations

import os
import time
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from src.figure_artifacts import save_figure_bundle
from src.figure_registry_builder import build_figure_registry
from src.manuscript_fixtures import BIOMIMETIC_IR_BAND_UM, IR_WINDOWS, SENSILLA_SAMPLES
from src.viz.figure_helpers import (
    FIGURE_ALT_TEXT,
    FIGURE_CLAIM_BOUNDARIES,
    add_panel_letter,
    add_source_badge,
    build_chc_fixture_spectrum,
    build_response_time_series,
    empirical_axes_panel_data,
)
from src.viz.styling import PlotStyler, get_colorblind_palette

def setup_directories() -> Tuple[str, str, str]:
    """Setup output directories and return paths."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(repo_root, "output")
    data_dir = os.path.join(output_dir, "data")
    figure_dir = os.path.join(output_dir, "figures")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figure_dir, exist_ok=True)
    
    return output_dir, data_dir, figure_dir


# Note: The convergence plot from the previous template is intentionally
# omitted to keep figures domain-relevant for insect IR sensing.


# Removed legacy experimental_setup figure generation (template holdover)


