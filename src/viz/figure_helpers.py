"""Shared helpers for figure generation, captions, and registry metadata."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from src.core import calculate_response_time_improvement
from src.manuscript_fixtures import (
    BIOMIMETIC_IR_BAND_UM,
    BIOMIMETIC_RESPONSE_THRESHOLD_MW_CM2,
    FIRE_BLACKBODY_PEAK_UM,
    RESPONSE_TIME_AUDITORY_MS,
    RESPONSE_TIME_INSECT_ORN_MS,
    RESPONSE_TIME_MODEL_IR_TARGET_MS,
    RESPONSE_TIME_SLOW_COMPARATOR_MS,
    RESPONSE_TIME_VISUAL_MS,
    SKIN_BLACKBODY_PEAK_UM,
)

DEFAULT_CLAIM_BOUNDARY = (
    "Bounds sensor feasibility and model assumptions; does not establish biological IR olfaction."
)

FIGURE_CLAIM_BOUNDARIES: dict[str, str] = {
    "fig:atmospheric_transmission": (
        "Marks atmospheric window opportunity only; not a measured insect communication range."
    ),
    "fig:sensilla_wavelength_matching": (
        "Quarter- and half-wave estimates are model probes, not measured receptor tuning curves."
    ),
    "fig:chc_spectra_example": (
        "Synthetic CHC-band fixture for feature extraction; not a measured ant spectrum."
    ),
    "fig:response_time_comparison": (
        "Timing constraint map; hatched bars are model targets, not measurements."
    ),
    "fig:composite_cross_domain_overview": (
        "Hypothesis evidence ladder; direct semiochemical IR olfaction remains unproven."
    ),
    "fig:empirical_ir_axes": (
        "Schematic synthesis of published IR biology axes; not new empirical measurement."
    ),
    "fig:integrated_classification": (
        "Cross-domain model synthesis panel; not a classification benchmark on live specimens."
    ),
    "fig:integrated_info": DEFAULT_CLAIM_BOUNDARY,
    "fig:integrated_metamaterial": DEFAULT_CLAIM_BOUNDARY,
    "fig:integrated_summary": DEFAULT_CLAIM_BOUNDARY,
    "fig:app_env_channel": (
        "Channel-capacity sensitivity demo under modeled clear/humid conditions."
    ),
    "fig:app_detection_limits": DEFAULT_CLAIM_BOUNDARY,
    "fig:app_neural_encoding_full": (
        "Model output only; does not establish biological IR olfaction."
    ),
    "fig:app_plasmonic_sweep": DEFAULT_CLAIM_BOUNDARY,
    "fig:app_sensilla_beam": (
        "Bounds directional gain; not field proof of semiochemical IR olfaction."
    ),
    "fig:app_spectral_unmixing": (
        "Algorithm evaluation; not species identification proof."
    ),
    "fig:app_active_inference": (
        "Behavioral demo only; not field data."
    ),
}

FIGURE_ALT_TEXT: dict[str, str] = {
    "fig:atmospheric_transmission": (
        "Atmospheric transmission versus wavelength with shaded mid-IR, long-wave, and far-IR windows "
        "and a biomimetic 2.8–6 µm band; coarse model scope, not a range proof."
    ),
    "fig:sensilla_wavelength_matching": (
        "Representative sensilla dimensions and modeled quarter- and half-wave resonance estimates "
        "plotted against atmospheric windows; geometry screening, not receptor tuning proof."
    ),
    "fig:chc_spectra_example": (
        "Synthetic cuticular-hydrocarbon infrared spectrum with C-H stretch and bend regions annotated; "
        "fixture for spectral feature extraction, not a measured ant spectrum."
    ),
    "fig:response_time_comparison": (
        "Bar chart comparing visual, auditory, insect ORN, model IR-stage, and slow-comparator response "
        "times in milliseconds; engineering timing bounds, not biological proof."
    ),
    "fig:composite_cross_domain_overview": (
        "Four-panel evidence map linking atmospheric windows, sensilla geometry, CHC bands, and evidence "
        "status; hypothesis ladder, not an experimental setup."
    ),
    "fig:empirical_ir_axes": (
        "Three-axis schematic of active photomechanic detection, passive cuticle optics, and applied IR "
        "spectroscopy with literature threshold bands; synthesis figure, not new data."
    ),
    "fig:integrated_classification": (
        "Cross-domain synthesis of normalized model metrics across information and material domains; "
        "sensitivity demo, not predictive accuracy on live insects."
    ),
    "fig:integrated_info": (
        "Integrated Fermi information decomposition across molecular, receptor, neural, and environmental terms; "
        "bounds sensor throughput, not biological proof."
    ),
    "fig:integrated_metamaterial": (
        "Integrated metamaterial dielectric and plasmonic response with information-capacity summaries; "
        "engineering model panels only."
    ),
    "fig:integrated_summary": (
        "Composite summary of dielectric response and normalized integrated performance metrics; "
        "engineering bounds panel."
    ),
    "fig:app_detection_limits": (
        "Detection limits panels with ROC curves, SNR operating regions, and noise floors for IR sensor bounds; "
        "model output only."
    ),
    "fig:app_env_channel": (
        "Atmospheric channel model with absorption, scattering, and capacity maps across humidity and temperature; "
        "engineering channel bounds."
    ),
    "fig:app_neural_encoding_full": (
        "Neural encoding panels with spike trains, population PCA, and information metrics on synthetic ORN time series; "
        "model output only."
    ),
    "fig:app_plasmonic_sweep": (
        "Plasmonic geometry sweep with Drude permittivity, Mie scattering, and near-field enhancement maps for "
        "receptor-scale sensor design."
    ),
    "fig:app_sensilla_beam": (
        "Sensilla array beam patterns, coupling, and morphology-to-resonance maps from antenna models; "
        "bounds directional gain, not field proof."
    ),
    "fig:app_spectral_unmixing": (
        "Synthetic CHC spectral unmixing and classification benchmarks with NMF/VCA/ICA panels; "
        "algorithm evaluation, not species identification proof."
    ),
    "fig:app_active_inference": (
        "Deterministic active-inference trajectory on a grid with IR cue beliefs; behavioral demo model output, "
        "not field data."
    ),
}


APPENDIX_CAPTION_TEMPLATES: dict[str, str] = {
    "fig:app_spectral_unmixing": (
        "Comprehensive spectral unmixing and classification analysis: Analysis of "
        "{n_spectra} CHC spectra with {n_components} components. "
        "{best_unmixing} achieved best reconstruction (MSE: {best_mse:.4f}) "
        "while {best_classifier} achieved best classification accuracy "
        "({best_accuracy:.3f}). Analysis includes NMF and VCA unmixing with "
        "comprehensive feature extraction and multi-algorithm classification validation."
    ),
    "fig:app_detection_limits": (
        "Detection limits analysis: best ROC AUC {best_auc:.3f}, "
        "minimum detectable SNR {mds_snr_db:.1f} dB, maximum range {max_range_km:.1f} km."
    ),
    "fig:app_neural_encoding_full": (
        "Neural encoding analysis: classification accuracy {classification_accuracy:.1%}, "
        "mutual information {mutual_information_bits:.2f} bits, temporal precision "
        "{temporal_precision:.1f}, and mean adaptation index {mean_adaptation_index:.2f}."
    ),
    "fig:app_env_channel": (
        "Environmental channel analysis: clear-sky capacity {clear_capacity_mbps:.2e} Mbps and "
        "humid capacity {humid_capacity_mbps:.2e} Mbps."
    ),
    "fig:app_plasmonic_sweep": (
        "Plasmonic geometry sweep: max gold enhancement {max_gold_enhancement:.2f} and "
        "field max enhancement {field_max_enhancement:.2f}."
    ),
    "fig:app_sensilla_beam": (
        "Sensilla array directionality: log-periodic gain {log_gain:.2f}, morphology correlation "
        "{morph_correlation:.3f}, and 3 dB bandwidth {bandwidth_3db_thz:.2f} THz."
    ),
}


def format_appendix_caption(label: str, metrics: dict[str, float], **extra: object) -> str:
    """Format registry appendix caption from label template and metrics."""
    template = APPENDIX_CAPTION_TEMPLATES.get(label)
    if template is None:
        parts = ", ".join(f"{key}={value}" for key, value in sorted(metrics.items()))
        return f"Appendix figure ({label}): {parts}."
    payload = {**metrics, **extra}
    try:
        return template.format(**payload)
    except KeyError:
        return template.format_map(_SafeFormatDict(payload))


class _SafeFormatDict(dict):
    def __missing__(self, key: str) -> str:
        return "N/A"


def format_display_metric(value: float, *, unit: str = "", precision: int = 1) -> str:
    """Format numeric metrics for captions, guarding nan/inf/zero."""
    if value is None or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return "N/A (fixture)"
    if abs(value) < 1e-12:
        return "N/A (fixture)"
    formatted = f"{value:.{precision}f}"
    return f"{formatted} {unit}".strip()


def build_chc_fixture_spectrum() -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Return wavenumbers, intensities, and analyze_chc_spectra results for figure generation."""
    from src.spectroscopy import analyze_chc_spectra

    wavenumbers = np.linspace(1200, 3400, 1200)
    ch_peak = 2900.0
    ch_bend_peak = 1465.0
    intensities = np.exp(-((wavenumbers - ch_peak) / 50.0) ** 2)
    intensities += 0.8 * np.exp(-((wavenumbers - (ch_peak - 30.0)) / 40.0) ** 2)
    intensities += 0.4 * np.exp(-((wavenumbers - (ch_peak - 60.0)) / 35.0) ** 2)
    intensities += 0.6 * np.exp(-((wavenumbers - ch_bend_peak) / 35.0) ** 2)
    intensities += 0.3 * np.exp(-((wavenumbers - (ch_bend_peak + 30.0)) / 30.0) ** 2)
    rng = np.random.default_rng(42)
    intensities += 0.02 * rng.standard_normal(len(intensities))
    intensities = np.maximum(0.0, intensities)
    analysis = analyze_chc_spectra(wavenumbers, intensities, species="fixture", input_type="wavenumbers")
    return wavenumbers, intensities, analysis


def build_response_time_series() -> tuple[list[str], np.ndarray, list[str], np.ndarray, np.ndarray]:
    """Build response-time figure data grounded in fixtures and core.py."""
    modalities = [
        "Visual\nbenchmark",
        "Auditory\nbenchmark",
        "Insect ORN\nanchor",
        "Model IR-stage\ntarget",
        "Slow odor-plume\ncomparator",
    ]
    response_times = np.array(
        [
            RESPONSE_TIME_VISUAL_MS,
            RESPONSE_TIME_AUDITORY_MS,
            RESPONSE_TIME_INSECT_ORN_MS,
            RESPONSE_TIME_MODEL_IR_TARGET_MS,
            RESPONSE_TIME_SLOW_COMPARATOR_MS,
        ],
        dtype=float,
    )
    source_status = [
        "literature benchmark",
        "literature benchmark",
        "olfactory neurophysiology anchor",
        "model target",
        "slow-comparator scenario",
    ]
    is_model_target = np.array([False, False, False, True, False])
    improvement_factors = np.array(
        [
            calculate_response_time_improvement(RESPONSE_TIME_SLOW_COMPARATOR_MS, RESPONSE_TIME_INSECT_ORN_MS),
            calculate_response_time_improvement(RESPONSE_TIME_SLOW_COMPARATOR_MS, RESPONSE_TIME_MODEL_IR_TARGET_MS),
            calculate_response_time_improvement(RESPONSE_TIME_INSECT_ORN_MS, RESPONSE_TIME_MODEL_IR_TARGET_MS),
        ],
        dtype=float,
    )
    return modalities, response_times, source_status, is_model_target, improvement_factors


def add_panel_letter(ax: Any, letter: str) -> None:
    """Add accessible panel letter badge."""
    ax.text(
        0.02,
        0.98,
        letter,
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.92, edgecolor="black"),
    )


def add_source_badge(ax: Any, text: str, *, y: float = 0.04) -> None:
    """Add source-tier badge to a panel."""
    ax.text(
        0.02,
        y,
        text,
        transform=ax.transAxes,
        fontsize=9,
        va="bottom",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.9),
    )


def biomimetic_band_annotation() -> tuple[float, float]:
    """Return biomimetic IR band endpoints in µm."""
    return BIOMIMETIC_IR_BAND_UM


def empirical_axes_panel_data() -> dict[str, Any]:
    """Structured data for the three-axis empirical IR figure."""
    return {
        "active": {
            "title": "Active photomechanic",
            "taxa": ["Melanophila", "Aradus", "Acanthocnemus"],
            "band_um": BIOMIMETIC_IR_BAND_UM,
            "threshold_mw_cm2": BIOMIMETIC_RESPONSE_THRESHOLD_MW_CM2,
            "peak_um": FIRE_BLACKBODY_PEAK_UM,
        },
        "passive": {
            "title": "Passive cuticle / thermosensory",
            "taxa": ["Merimna", "Rhodnius", "cycad pollinators"],
            "peak_um": SKIN_BLACKBODY_PEAK_UM,
        },
        "applied": {
            "title": "Applied / remote IR",
            "taxa": ["NIRS grain beetles", "FTIR forensics", "field NIR nets"],
        },
    }
