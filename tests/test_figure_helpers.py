"""Tests for src.viz.figure_helpers utilities."""

from __future__ import annotations

import math

import numpy as np

from src.spectroscopy import analyze_chc_spectra
from src.viz.figure_helpers import (
    build_chc_fixture_spectrum,
    build_response_time_series,
    format_display_metric,
)


def test_format_display_metric_nan_and_zero() -> None:
    assert format_display_metric(float("nan")) == "N/A (fixture)"
    assert format_display_metric(float("inf")) == "N/A (fixture)"
    assert format_display_metric(0.0) == "N/A (fixture)"
    assert format_display_metric(1.234, unit="dB", precision=2) == "1.23 dB"


def test_build_chc_fixture_spectrum_matches_analyze_chc_spectra() -> None:
    wavenumbers, intensities, analysis = build_chc_fixture_spectrum()
    direct = analyze_chc_spectra(wavenumbers, intensities, species="fixture", input_type="wavenumbers")
    assert len(analysis["peak_wavenumbers"]) == len(direct["peak_wavenumbers"])
    assert np.allclose(analysis["peak_intensities"], direct["peak_intensities"])
    assert analysis["species"] == direct["species"]


def test_build_response_time_series_ordering() -> None:
    modalities, times, _, is_model, _ = build_response_time_series()
    assert len(modalities) == 5
    assert len(times) == 5
    assert is_model[3]
    assert all(not math.isnan(value) for value in times)
