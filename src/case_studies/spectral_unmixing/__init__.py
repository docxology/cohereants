"""Spectral unmixing case study package."""
from .classifiers import advanced_classification_suite, lda_baseline, performance_metrics_comprehensive
from .compute import compute_spectral_unmixing_analysis
from .core import generate_realistic_chc_spectra, independent_component_analysis_spectra, nmf_unmix, vertex_component_analysis
from .features import spectral_feature_extraction
from .figures import render_comprehensive_figure
from .types import SpectralUnmixingAnalysis
