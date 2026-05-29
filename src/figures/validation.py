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

def validate_outputs(figure_dir: str, data_dir: str) -> tuple[bool, list[str]]:
    """Validate that all expected outputs were generated correctly."""
    missing = []
    
    expected_figures = [
        "atmospheric_transmission.png",
        "sensilla_wavelength_matching.png", 
        "chc_spectra_example.png",
        "response_time_comparison.png",
        "composite_cross_domain_overview.png",
        "empirical_ir_axes.png",
    ]
    
    expected_data = [
        "atmospheric_transmission.npz",
        "sensilla_data.npz",
        "response_time_comparison.npz",
        "chc_spectra.npz",
    ]
    
    expected_captions = [
        "atmospheric_transmission.caption.txt",
        "sensilla_wavelength_matching.caption.txt",
        "chc_spectra_example.caption.txt", 
        "response_time_comparison.caption.txt",
        "composite_cross_domain_overview.caption.txt",
        "empirical_ir_axes.caption.txt",
    ]
    
    # Check figures
    for fig in expected_figures:
        path = os.path.join(figure_dir, fig)
        if not os.path.exists(path):
            missing.append(f"Figure: {fig}")
        elif os.path.getsize(path) == 0:
            missing.append(f"Empty figure: {fig}")
    
    # Check data files  
    for data in expected_data:
        path = os.path.join(data_dir, data)
        if not os.path.exists(path):
            missing.append(f"Data: {data}")
        elif os.path.getsize(path) == 0:
            missing.append(f"Empty data: {data}")
            
    # Check captions
    for caption in expected_captions:
        path = os.path.join(figure_dir, caption)
        if not os.path.exists(path):
            missing.append(f"Caption: {caption}")
        elif os.path.getsize(path) == 0:
            missing.append(f"Empty caption: {caption}")
    
    return len(missing) == 0, missing


