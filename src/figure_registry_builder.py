"""Build complete figure_registry.json from output artifacts."""

from __future__ import annotations

from pathlib import Path

from src.figure_artifacts import write_figure_registry
from src.figure_registry_contract import FIGURE_VALIDATION_NOTE, figure_method
from src.viz.figure_helpers import DEFAULT_CLAIM_BOUNDARY, FIGURE_ALT_TEXT, FIGURE_CLAIM_BOUNDARIES

_LABEL_TO_FILE: dict[str, str] = {
    "fig:atmospheric_transmission": "atmospheric_transmission.png",
    "fig:sensilla_wavelength_matching": "sensilla_wavelength_matching.png",
    "fig:chc_spectra_example": "chc_spectra_example.png",
    "fig:response_time_comparison": "response_time_comparison.png",
    "fig:composite_cross_domain_overview": "composite_cross_domain_overview.png",
    "fig:empirical_ir_axes": "empirical_ir_axes.png",
    "fig:app_detection_limits": "detection_limits_comprehensive_analysis.png",
    "fig:app_env_channel": "environmental_channel_comprehensive_analysis.png",
    "fig:integrated_info": "integrated_analysis_information_analysis.png",
    "fig:app_neural_encoding_full": "neural_encoding_comprehensive_analysis.png",
    "fig:app_plasmonic_sweep": "plasmonic_geometry_comprehensive_analysis.png",
    "fig:integrated_metamaterial": "integrated_analysis_metamaterial_properties.png",
    "fig:app_sensilla_beam": "sensilla_array_comprehensive_analysis.png",
    "fig:app_spectral_unmixing": "spectral_unmixing_comprehensive_analysis.png",
    "fig:integrated_classification": "integrated_analysis_cross_domain_synthesis.png",
    "fig:integrated_summary": "integrated_analysis_summary.png",
    "fig:app_active_inference": "active_inference_trajectory.png",
}


def _resolve_alt_text(label: str, caption: str, figure_dir: Path, filename: str) -> str:
    alt_path = figure_dir / f"{Path(filename).stem}.alt.txt"
    if alt_path.exists():
        return alt_path.read_text(encoding="utf-8").strip()
    if label in FIGURE_ALT_TEXT:
        return FIGURE_ALT_TEXT[label]
    first_sentence = caption.split(".")[0].strip()
    return first_sentence if first_sentence else label


def build_figure_registry(project_root: Path) -> Path:
    """Write figure_registry.json covering all manuscript figure labels."""
    figure_dir = project_root / "output" / "figures"
    records: dict[str, dict[str, object]] = {}
    for label, filename in _LABEL_TO_FILE.items():
        figure_path = figure_dir / filename
        caption_path = figure_dir / f"{Path(filename).stem}.caption.txt"
        caption = ""
        if caption_path.exists():
            caption = caption_path.read_text(encoding="utf-8")
        elif not caption:
            caption = f"Figure generated for {label}. Generation method: {figure_method(label)} {FIGURE_VALIDATION_NOTE}"
        claim_boundary = FIGURE_CLAIM_BOUNDARIES.get(label, DEFAULT_CLAIM_BOUNDARY)
        alt_text = _resolve_alt_text(label, caption, figure_dir, filename)
        # Store a project-root-relative path so the registry is portable and never
        # leaks an absolute home-directory path into the published artifact.
        try:
            rel_path = figure_path.relative_to(project_root).as_posix()
        except ValueError:
            rel_path = figure_path.as_posix()
        records[label] = {
            "path": rel_path,
            "caption": caption,
            "filename": filename,
            "label": label,
            "metadata": {
                "claim_boundary": claim_boundary,
                "source_artifact": filename,
                "alt_text": alt_text,
            },
        }
    return write_figure_registry(figure_dir, records)
