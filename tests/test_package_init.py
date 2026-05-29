"""
Real-data tests for the src package initialization surface.
"""

import importlib
import numpy as np
import pytest

try:
    import src
    from src import get_package_info, run_demo_analysis
except ImportError:
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import src
    from src import get_package_info, run_demo_analysis


class TestPackageInit:
    """Test package exports and metadata."""

    def test_version_info(self):
        assert src.__version__ == "3.0.0"
        assert isinstance(src.__author__, str)
        assert len(src.__author__) > 0

    def test_all_exports(self):
        assert isinstance(src.__all__, list)
        assert "get_package_info" in src.__all__
        assert "run_demo_analysis" in src.__all__

    def test_core_functions_exported(self):
        for func_name in [
            "calculate_wavelength_from_wavenumber",
            "calculate_wavenumber_from_wavelength",
            "calculate_atmospheric_transmission",
            "calculate_response_time_improvement",
        ]:
            assert hasattr(src, func_name)
            assert callable(getattr(src, func_name))

    def test_analysis_classes_exported(self):
        for class_name in ["FermiEstimator", "MetaMaterialAnalyzer", "IntegratedAnalyzer"]:
            assert hasattr(src, class_name)
            assert class_name in src.__all__

    def test_module_functions_exported(self):
        for func_name in ["analyze_sensilla_dimensions", "analyze_chc_spectra", "analyze_behavioral_response"]:
            assert hasattr(src, func_name)
            assert callable(getattr(src, func_name))


class TestGetPackageInfo:
    """Test the get_package_info function."""

    def test_get_package_info_structure(self):
        info = get_package_info()

        assert info["name"] == "CohereAnts"
        assert info["pipeline_id"] == "cohereants"
        assert info["version"] == src.__version__
        assert info["author"] == src.__author__
        assert isinstance(info["modules"], list)
        assert isinstance(info["frameworks"], list)

    def test_get_package_info_modules(self):
        info = get_package_info()
        assert len(info["modules"]) == 8
        assert all("—" in module for module in info["modules"])

    def test_get_package_info_counts(self):
        info = get_package_info()
        assert len(info["modules"]) == 8
        assert len(info["frameworks"]) == 3


class TestRunDemoAnalysis:
    """Test the real demo analysis path."""

    def test_run_demo_analysis_basic(self, capsys):
        np.random.seed(0)
        result = run_demo_analysis()

        captured = capsys.readouterr()
        assert isinstance(result, dict)
        assert set(result) == {"analysis_results", "performance_metrics", "comprehensive_report"}
        assert "Demo analysis completed successfully!" in captured.out
        assert "Generated 9 performance metrics" in captured.out
        assert result["performance_metrics"]["system_efficiency"] >= 0.0
        assert "INTEGRATED ANALYSIS SUMMARY" in result["comprehensive_report"]

    def test_run_demo_analysis_result_contents(self):
        np.random.seed(1)
        result = run_demo_analysis()

        metrics = result["performance_metrics"]
        molecular = result["analysis_results"]["fermi_analysis"]["molecular"]

        # Real physical/structural properties of the deterministic pipeline:
        # - average_refractive_index is a real index of refraction, so >= 1.
        # - material_performance_score is positive in this configuration.
        # - molecular total_bits == sum of its three component entropies (identity).
        # - information_processing_score is NEGATIVE here because it equals
        #   total_info_content * receptor_specificity * neural_efficiency and
        #   total_info_content inherits the negative total_bits from the src
        #   3/2*log2(molecular_mass_in_kg)+15 translational-entropy model (see
        #   report). We assert the real sign and real identity, not a guessed sign.
        assert metrics["average_refractive_index"] >= 1.0
        assert metrics["material_performance_score"] > 0.0
        component_sum = (
            molecular["translational_bits"]
            + molecular["rotational_bits"]
            + molecular["vibrational_bits"]
        )
        assert np.isclose(molecular["total_bits"], component_sum)
        assert molecular["total_bits"] < 0.0
        assert metrics["information_processing_score"] < 0.0


class TestPackageImports:
    """Test package import functionality."""

    def test_direct_imports_work(self):
        from src import FermiEstimator, calculate_wavelength_from_wavenumber

        assert FermiEstimator is not None
        assert callable(calculate_wavelength_from_wavenumber)

    def test_module_level_access(self):
        assert callable(src.calculate_wavelength_from_wavenumber)
        assert src.FermiEstimator is not None

    def test_all_listed_items_importable(self):
        for item_name in src.__all__:
            assert hasattr(src, item_name), f"{item_name} not found in module"
            assert getattr(src, item_name) is not None

    def test_imports_dont_raise_exceptions(self):
        reloaded = importlib.reload(src)
        assert reloaded.__version__ == src.__version__


class TestPackageCompatibility:
    """Test package compatibility and edge cases."""

    def test_version_format(self):
        parts = src.__version__.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)

    def test_module_docstring(self):
        assert src.__doc__ is not None
        assert "CohereAnts" in src.__doc__

    def test_no_private_items_in_all(self):
        assert all(not item.startswith("_") for item in src.__all__)

    def test_edge_case_imports_and_fallbacks(self):
        for module_name in ["src.behavioral", "src.spectroscopy", "src.integrated_analysis"]:
            module = importlib.import_module(module_name)
            assert module.__name__ == module_name
