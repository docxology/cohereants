"""Subprocess smoke tests for figure generation scripts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GENERATE_SCRIPTS: list[tuple[str, list[str]]] = [
    (
        "scripts/generate_research_figures.py",
        [
            "atmospheric_transmission",
            "sensilla_wavelength_matching",
            "chc_spectra_example",
            "response_time_comparison",
            "composite_cross_domain_overview",
            "empirical_ir_axes",
        ],
    ),
    (
        "scripts/generate_integrated_analysis.py",
        [
            "integrated_analysis_information_analysis",
            "integrated_analysis_metamaterial_properties",
            "integrated_analysis_system_performance",
            "integrated_analysis_cross_domain_synthesis",
            "integrated_analysis_summary",
        ],
    ),
    ("scripts/generate_detection_limits.py", ["detection_limits_comprehensive_analysis"]),
    ("scripts/generate_environmental_channel_analysis.py", ["environmental_channel_comprehensive_analysis"]),
    ("scripts/generate_neural_encoding_analysis.py", ["neural_encoding_comprehensive_analysis"]),
    ("scripts/generate_plasmonic_geometry_sweep.py", ["plasmonic_geometry_comprehensive_analysis"]),
    ("scripts/generate_sensilla_array_directionality.py", ["sensilla_array_comprehensive_analysis"]),
    ("scripts/generate_spectral_unmixing.py", ["spectral_unmixing_comprehensive_analysis"]),
    ("scripts/generate_active_inference_demo.py", ["active_inference_trajectory"]),
]


def test_generate_integrated_analysis_figures_inprocess() -> None:
    from src.integrated_figures import generate_integrated_analysis_figures

    paths = generate_integrated_analysis_figures(PROJECT_ROOT)
    assert len(paths) >= 5
    for path in paths:
        assert path.exists() and path.stat().st_size > 0
    npz = PROJECT_ROOT / "output" / "data" / "integrated_analysis.npz"
    assert npz.exists() and npz.stat().st_size > 0
    registry = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    assert registry.exists() and registry.stat().st_size > 0


@pytest.mark.parametrize("script,expected_stems", GENERATE_SCRIPTS)
def test_figure_script_generates_outputs(script: str, expected_stems: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, script],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    figure_dir = PROJECT_ROOT / "output" / "figures"
    for stem in expected_stems:
        png = figure_dir / f"{stem}.png"
        caption = figure_dir / f"{stem}.caption.txt"
        alt = figure_dir / f"{stem}.alt.txt"
        assert png.exists() and png.stat().st_size > 0
        assert caption.exists() and caption.read_text(encoding="utf-8").strip()
        assert alt.exists() and len(alt.read_text(encoding="utf-8").strip()) >= 40
    registry = figure_dir / "figure_registry.json"
    assert registry.exists() and registry.stat().st_size > 0


def test_registry_alt_text_not_truncated() -> None:
    from src.figure_registry_builder import _LABEL_TO_FILE, build_figure_registry

    build_figure_registry(PROJECT_ROOT)
    registry = json.loads((PROJECT_ROOT / "output" / "figures" / "figure_registry.json").read_text(encoding="utf-8"))
    for label in _LABEL_TO_FILE:
        alt_text = str(registry[label]["metadata"]["alt_text"])
        assert len(alt_text) >= 40, f"{label} alt text too short: {alt_text!r}"
        assert not alt_text[-1].isdigit(), f"{label} alt text looks truncated: {alt_text!r}"
