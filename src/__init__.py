"""
CohereAnts analysis package (pipeline id: cohereants).

Lightweight exports load eagerly; case-study and visualization symbols load on demand.
"""

from __future__ import annotations

from typing import Any

__version__ = "3.0.0"
__author__ = "Tucker Chambers, Daniel A. Friedman"

from src.behavioral import analyze_behavioral_response, calculate_response_statistics, generate_behavioral_plots
from src.config import (
    ConfigManager,
    enable_verbose_logging,
    get_config,
    init_config,
    set_plot_style,
    set_random_seed,
    set_temperature,
)
from src.core import (
    calculate_atmospheric_transmission,
    calculate_response_time_improvement,
    calculate_wavelength_from_wavenumber,
    calculate_wavenumber_from_wavelength,
)
from src.fermi_estimation import FermiEstimator, create_sample_fermi_analysis
from src.integrated_analysis import IntegratedAnalyzer, create_sample_integrated_analysis
from src.meta_material_framework import MetaMaterialAnalyzer, create_sample_metamaterial_analysis
from src.sensilla import analyze_sensilla_dimensions, calculate_wavelength_matching, generate_sensilla_visualization
from src.spectroscopy import analyze_chc_spectra, calculate_spectral_overlap, generate_spectral_plots

_LAZY_EXPORTS: dict[str, tuple[str, str]] = {
    "run_comprehensive_analysis": ("src.insect_analysis", "run_comprehensive_analysis"),
    "AdvancedVisualizer": ("src.visualization", "AdvancedVisualizer"),
    "PlotStyler": ("src.visualization", "PlotStyler"),
    "create_publication_figure": ("src.visualization", "create_publication_figure"),
    "get_colorblind_palette": ("src.visualization", "get_colorblind_palette"),
    "create_subplots": ("src.visualization", "create_subplots"),
    "compute_beam_pattern": ("src.case_studies.sensilla_array_directionality", "compute_beam_pattern"),
    "array_gain": ("src.case_studies.sensilla_array_directionality", "array_gain"),
    "design_log_periodic_array": ("src.case_studies.sensilla_array_directionality", "design_log_periodic_array"),
    "atmospheric_transmission_detailed": ("src.case_studies.environmental_channel", "atmospheric_transmission_detailed"),
    "channel_capacity_vs_env": ("src.case_studies.environmental_channel", "channel_capacity_vs_env"),
    "min_detectable_power": ("src.case_studies.detection_limits", "min_detectable_power"),
    "snr_curve": ("src.case_studies.detection_limits", "snr_curve"),
    "operating_point": ("src.case_studies.detection_limits", "operating_point"),
    "information_rate_time_series": ("src.case_studies.neural_encoding", "information_rate_time_series"),
    "rate_coding_metrics": ("src.case_studies.neural_encoding", "rate_coding_metrics"),
    "nmf_unmix": ("src.case_studies.spectral_unmixing", "nmf_unmix"),
    "lda_baseline": ("src.case_studies.spectral_unmixing", "lda_baseline"),
    "sweep_plasmonic_quality": ("src.case_studies.plasmonic_geometry", "sweep_plasmonic_quality"),
    "olfactory_active_inference_step": (
        "src.case_studies.active_inference",
        "olfactory_active_inference_step",
    ),
}

__all__ = [
    "calculate_wavelength_from_wavenumber",
    "calculate_wavenumber_from_wavelength",
    "calculate_atmospheric_transmission",
    "calculate_response_time_improvement",
    "analyze_sensilla_dimensions",
    "generate_sensilla_visualization",
    "calculate_wavelength_matching",
    "analyze_chc_spectra",
    "calculate_spectral_overlap",
    "generate_spectral_plots",
    "analyze_behavioral_response",
    "calculate_response_statistics",
    "generate_behavioral_plots",
    "FermiEstimator",
    "create_sample_fermi_analysis",
    "MetaMaterialAnalyzer",
    "create_sample_metamaterial_analysis",
    "IntegratedAnalyzer",
    "create_sample_integrated_analysis",
    "run_comprehensive_analysis",
    "ConfigManager",
    "get_config",
    "init_config",
    "set_temperature",
    "set_plot_style",
    "enable_verbose_logging",
    "set_random_seed",
    "AdvancedVisualizer",
    "PlotStyler",
    "create_publication_figure",
    "get_colorblind_palette",
    "create_subplots",
    "compute_beam_pattern",
    "array_gain",
    "design_log_periodic_array",
    "atmospheric_transmission_detailed",
    "channel_capacity_vs_env",
    "min_detectable_power",
    "snr_curve",
    "operating_point",
    "information_rate_time_series",
    "rate_coding_metrics",
    "nmf_unmix",
    "lda_baseline",
    "sweep_plasmonic_quality",
    "olfactory_active_inference_step",
    "get_package_info",
    "run_demo_analysis",
]


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_path, attr = _LAZY_EXPORTS[name]
    import importlib

    module = importlib.import_module(module_path)
    value = getattr(module, attr)
    globals()[name] = value
    return value


def get_package_info() -> dict[str, Any]:
    """Return package metadata for tooling and demos."""
    return {
        "name": "CohereAnts",
        "pipeline_id": "cohereants",
        "version": __version__,
        "author": __author__,
        "description": "Engineering bounds for insect-inspired IR sensing and olfaction modeling",
        "modules": [
            "core — physical conversions and atmospheric windows",
            "sensilla — morphology and wavelength matching",
            "spectroscopy — CHC spectral analysis",
            "behavioral — response statistics",
            "fermi_estimation — order-of-magnitude bounds",
            "meta_material_framework — dielectric/plasmonic models",
            "integrated_analysis — cross-domain synthesis",
            "insect_analysis — comprehensive orchestration entry",
        ],
        "frameworks": [
            "Fermi Estimation Analysis",
            "Meta-Material Analytical Framework",
            "Integrated Cross-Domain Analysis",
        ],
    }


def run_demo_analysis() -> dict | None:
    """Run demonstration comprehensive analysis."""
    from src.insect_analysis import run_comprehensive_analysis

    print("CohereAnts — demo analysis")
    result = run_comprehensive_analysis()
    print("Demo analysis completed successfully!")
    print(f"Generated {len(result['performance_metrics'])} performance metrics")
    return result


if __name__ == "__main__":
    info = get_package_info()
    print(f"{info['name']} v{info['version']}")
    print(f"Author: {info['author']}")
    print(f"Description: {info['description']}")
    print("\nAvailable modules:")
    for module in info["modules"]:
        print(f"  - {module}")
    print("\nAnalytical frameworks:")
    for framework in info["frameworks"]:
        print(f"  - {framework}")
    print("\nRunning demo analysis...")
    run_demo_analysis()
