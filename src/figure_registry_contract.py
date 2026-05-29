"""Figure registry metadata and caption contracts for validation."""

from __future__ import annotations

from typing import Any

FIGURE_VALIDATION_NOTE = (
    "Registry metadata records the generation method, source artifact, and claim boundary for validation."
)

_FIGURE_METHODS: dict[str, str] = {
    "fig:atmospheric_transmission": "Coarse window model from src.core.calculate_atmospheric_transmission().",
    "fig:sensilla_wavelength_matching": "Representative sensilla inputs via src.sensilla.analyze_sensilla_dimensions().",
    "fig:chc_spectra_example": "Fixture spectrum analyzed with src.spectroscopy.analyze_chc_spectra().",
    "fig:response_time_comparison": "Timing constraint map from src.viz.figure_helpers.build_response_time_series().",
    "fig:composite_cross_domain_overview": "Evidence ladder panel linking empirical IR organs, model assumptions, and protocols.",
    "fig:empirical_ir_axes": "Three-axis schematic from src.figures.generate_empirical_ir_axes() and manuscript fixtures.",
    "fig:integrated_info": "IntegratedAnalyzer Fermi + information panels via src.integrated_figures.",
    "fig:integrated_metamaterial": "IntegratedAnalyzer metamaterial sweep via src.integrated_figures.",
    "fig:integrated_classification": "Cross-domain synthesis panel via src.integrated_figures.create_cross_domain_synthesis_figure().",
    "fig:integrated_summary": "Composite summary via src.integrated_figures.create_composite_summary_figure().",
    "fig:app_detection_limits": "ROC/SNR operating points from src.case_studies.detection_limits.",
    "fig:app_env_channel": "Channel-capacity sensitivity from environmental_channel case study.",
    "fig:app_neural_encoding_full": "Information-rate model from neural_encoding case study.",
    "fig:app_plasmonic_sweep": "Geometry sweep aligned with biomimetic pit-organ precedents.",
    "fig:app_sensilla_beam": "Array directionality beam patterns from sensilla_array case study.",
    "fig:app_spectral_unmixing": "Spectral unmixing fixture from spectral_unmixing case study.",
    "fig:app_active_inference": "Active-inference control trajectory demo.",
}


def figure_method(label: str) -> str:
    """Return concise generation method for a figure label."""
    return _FIGURE_METHODS.get(label, "Deterministic figure generated from local project artifacts.")


def caption_with_contract(caption: str, method: str) -> str:
    """Attach method sentence and validation note to a caption."""
    if FIGURE_VALIDATION_NOTE in caption:
        return caption
    return f"{caption} Generation method: {method} {FIGURE_VALIDATION_NOTE}"


def finalize_figure_registry(records: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    """Add method and validation metadata to registry records."""
    for label, record in records.items():
        method = figure_method(label)
        record["caption"] = caption_with_contract(str(record.get("caption", "")), method)
        metadata = _metadata(record)
        metadata["method"] = method
        metadata["validated_by"] = "Stage 04 output validation and figure registry validation."
        record["metadata"] = metadata
    return records


def _metadata(record: dict[str, object]) -> dict[str, Any]:
    metadata = record.get("metadata")
    return metadata if isinstance(metadata, dict) else {}
