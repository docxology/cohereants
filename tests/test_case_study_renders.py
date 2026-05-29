"""In-process tests for case-study compute/render pairs."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pytest

from src.case_studies.detection_limits import (
    compute_detection_limits_analysis,
    render_comprehensive_figure,
)
from src.case_studies.environmental_channel import (
    compute_environmental_channel_analysis,
    render_comprehensive_figure as render_environmental_figure,
)
from src.case_studies.neural_encoding import (
    compute_neural_encoding_analysis,
    render_comprehensive_figure as render_neural_figure,
)
from src.case_studies.plasmonic_geometry import (
    compute_plasmonic_geometry_analysis,
    render_comprehensive_figure as render_plasmonic_figure,
)
from src.case_studies.sensilla_array_directionality import (
    compute_sensilla_array_analysis,
    render_comprehensive_figure as render_sensilla_figure,
)
from src.case_studies.spectral_unmixing import (
    compute_spectral_unmixing_analysis,
    render_comprehensive_figure as render_spectral_figure,
)

CASE_STUDY_RENDER_CASES = [
    ("detection_limits", compute_detection_limits_analysis, render_comprehensive_figure, {"best_auc", "mds_snr_db"}),
    (
        "environmental_channel",
        compute_environmental_channel_analysis,
        render_environmental_figure,
        {"clear_capacity_mbps", "humid_capacity_mbps"},
    ),
    (
        "spectral_unmixing",
        compute_spectral_unmixing_analysis,
        render_spectral_figure,
        {"best_accuracy", "best_mse"},
    ),
    (
        "sensilla_array",
        compute_sensilla_array_analysis,
        render_sensilla_figure,
        {"log_gain", "morph_correlation"},
    ),
    (
        "plasmonic_geometry",
        compute_plasmonic_geometry_analysis,
        render_plasmonic_figure,
        {"max_gold_enhancement", "field_max_enhancement"},
    ),
    (
        "neural_encoding",
        compute_neural_encoding_analysis,
        render_neural_figure,
        {"classification_accuracy", "mutual_information_bits"},
    ),
]


@pytest.mark.parametrize(
    "name,compute_fn,render_fn,metric_keys",
    CASE_STUDY_RENDER_CASES,
    ids=[case[0] for case in CASE_STUDY_RENDER_CASES],
)
def test_case_study_compute_render_pair(
    name: str,
    compute_fn,
    render_fn,
    metric_keys: set[str],
) -> None:
    analysis = compute_fn()
    if hasattr(analysis, "as_dict"):
        assert analysis.as_dict()
    else:
        assert isinstance(analysis, dict) and analysis

    fig, metrics = render_fn(analysis)
    assert fig is not None
    assert metrics.keys() >= metric_keys
    for key in metric_keys:
        assert metrics[key] == metrics[key]  # not NaN
        assert isinstance(metrics[key], (int, float))

    axes = fig.get_axes()
    assert len(axes) >= 4, f"{name} figure should have multiple panels"
    fig.clf()
