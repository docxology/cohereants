"""Tests for manuscript variables and figure registry builders."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_build_figure_registry(tmp_path: Path) -> None:
    from src.figure_registry_builder import build_figure_registry

    figure_dir = tmp_path / "output" / "figures"
    figure_dir.mkdir(parents=True)
    for name in (
        "atmospheric_transmission.png",
        "composite_cross_domain_overview.png",
        "detection_limits_comprehensive_analysis.png",
    ):
        (figure_dir / name).write_bytes(b"png")
        (figure_dir / f"{name.replace('.png', '.caption.txt')}").write_text("Caption.", encoding="utf-8")

    registry_path = build_figure_registry(tmp_path)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert "fig:app_detection_limits" in registry
    assert "fig:experimental_setup" not in registry


def test_build_figure_registry_integrated_classification_mapping(tmp_path: Path) -> None:
    from src.figure_registry_builder import _LABEL_TO_FILE, build_figure_registry

    assert _LABEL_TO_FILE["fig:integrated_classification"] == "integrated_analysis_cross_domain_synthesis.png"
    figure_dir = tmp_path / "output" / "figures"
    figure_dir.mkdir(parents=True)
    for name in _LABEL_TO_FILE.values():
        (figure_dir / name).write_bytes(b"png")
        (figure_dir / f"{Path(name).stem}.caption.txt").write_text("Caption.", encoding="utf-8")
    registry = json.loads(build_figure_registry(tmp_path).read_text(encoding="utf-8"))
    assert registry["fig:integrated_classification"]["filename"] == "integrated_analysis_cross_domain_synthesis.png"
    assert registry["fig:empirical_ir_axes"]["filename"] == "empirical_ir_axes.png"
    assert len(registry["fig:integrated_classification"]["metadata"]["alt_text"]) > 20


def test_registry_labels_have_alt_sidecars_or_dict() -> None:
    from src.figure_registry_builder import _LABEL_TO_FILE, build_figure_registry

    build_figure_registry(PROJECT_ROOT)
    registry = json.loads((PROJECT_ROOT / "output" / "figures" / "figure_registry.json").read_text(encoding="utf-8"))
    figure_dir = PROJECT_ROOT / "output" / "figures"
    for label, filename in _LABEL_TO_FILE.items():
        alt_path = figure_dir / f"{Path(filename).stem}.alt.txt"
        alt_text = str(registry[label]["metadata"]["alt_text"])
        assert alt_path.exists() or len(alt_text) >= 40
        assert not alt_text[-1].isdigit()


def test_syntax_guide_label_table_matches_registry() -> None:
    from src.figure_registry_builder import _LABEL_TO_FILE

    syntax_guide = (PROJECT_ROOT / "docs" / "syntax_guide.md").read_text(encoding="utf-8")
    for label, filename in _LABEL_TO_FILE.items():
        assert f"`{label}`" in syntax_guide
        assert filename in syntax_guide


def test_build_response_time_series_uses_core_improvement() -> None:
    from src.core import calculate_response_time_improvement
    from src.manuscript_fixtures import RESPONSE_TIME_INSECT_ORN_MS, RESPONSE_TIME_SLOW_COMPARATOR_MS
    from src.viz.figure_helpers import build_response_time_series

    _, times, _, is_model, factors = build_response_time_series()
    assert is_model[3]
    expected = calculate_response_time_improvement(
        RESPONSE_TIME_SLOW_COMPARATOR_MS, RESPONSE_TIME_INSECT_ORN_MS
    )
    assert float(factors[0]) == expected
    assert float(times[2]) == RESPONSE_TIME_INSECT_ORN_MS


def test_generate_core_manuscript_figures_smoke() -> None:
    from src.figures import generate_core_manuscript_figures

    paths = generate_core_manuscript_figures(PROJECT_ROOT)
    assert len(paths) >= 6
    registry = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    assert registry.exists()
