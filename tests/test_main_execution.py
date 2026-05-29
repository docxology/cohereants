"""
Real execution tests for module entrypoints and sample factories.
"""

import importlib
import os
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np

from src.fermi_estimation import create_sample_fermi_analysis
from src.insect_analysis import run_comprehensive_analysis
from src.integrated_analysis import create_sample_integrated_analysis
from src.meta_material_framework import create_sample_metamaterial_analysis

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_script(script_path: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = _PROJECT_ROOT
    env.setdefault("MPLBACKEND", "Agg")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        cwd=_PROJECT_ROOT,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    return result


class TestMainExecutionBlocks:
    """Test main execution blocks for real scripts."""

    def test_fermi_estimation_main_block(self):
        result = _run_script("src/fermi_estimation.py")
        assert "COMPREHENSIVE FERMI ESTIMATION ANALYSIS" in result.stdout

    def test_meta_material_framework_main_block(self):
        result = _run_script("src/meta_material_framework.py")
        assert "COMPREHENSIVE META-MATERIAL ANALYSIS" in result.stdout
        assert "DIELECTRIC PROPERTIES:" in result.stdout

    def test_integrated_analysis_main_block(self):
        result = _run_script("src/integrated_analysis.py")
        assert "INTEGRATED ANALYSIS SUMMARY" in result.stdout
        assert "Analysis complete! Check output/figures/" in result.stdout

    def test_insect_analysis_main_block(self):
        result = _run_script("src/insect_analysis.py")
        assert "Insect Analysis Module - Comprehensive Analysis" in result.stdout
        assert "Analysis completed successfully!" in result.stdout

    def test_package_init_main_block(self):
        result = _run_script("src/__init__.py")
        assert "CohereAnts v3.0.0" in result.stdout
        assert "Running demo analysis..." in result.stdout


class TestSampleFactories:
    """Test the real sample factory functions."""

    def test_fermi_estimation_factory(self):
        estimator, molecular, receptor, neural, environmental = create_sample_fermi_analysis()

        assert estimator is not None
        # Real structural identity: total_bits is exactly the sum of the three
        # component entropies. (total_bits is NEGATIVE here because the src model
        # uses 3/2*log2(molecular_mass_in_kg)+15 for translational entropy, which
        # is deeply negative for realistic masses — a questionable physical model,
        # but consistent and deterministic; see report. We assert the real identity,
        # not a guessed sign.)
        expected_molecular_total = (
            molecular["translational_bits"]
            + molecular["rotational_bits"]
            + molecular["vibrational_bits"]
        )
        assert np.isclose(molecular["total_bits"], expected_molecular_total)
        assert np.isclose(molecular["total_bytes"], molecular["total_bits"] / 8.0)
        assert 0.0 <= receptor["specificity_index"] <= 1.0
        assert neural["channel_capacity_bits"] > 0.0
        expected_env_total = (
            environmental["temperature_bits"]
            + environmental["humidity_bits"]
            + environmental["pressure_bits"]
        )
        assert np.isclose(environmental["total_environmental_bits"], expected_env_total)

    def test_meta_material_factory(self):
        analyzer, dielectric, plasmonic, quantum, info_capacity = create_sample_metamaterial_analysis()

        assert analyzer is not None
        assert dielectric["frequency"].shape == dielectric["refractive_index"].shape
        assert plasmonic["quality_factor"] > 0.0
        assert quantum["coupling_matrix"].shape == (4, 4)
        assert info_capacity["channel_capacity_bits_per_sec"] > 0.0

    def test_integrated_analysis_factory(self):
        analyzer, results = create_sample_integrated_analysis()
        figures = analyzer.create_visualization_figures(results)

        assert set(results) == {"fermi_analysis", "metamaterial_analysis"}
        assert set(figures) == {
            "information_breakdown",
            "metamaterial_properties",
            "system_performance",
        }
        assert all(isinstance(fig, plt.Figure) for fig in figures.values())
        plt.close("all")

    def test_run_comprehensive_analysis_real(self):
        np.random.seed(0)
        result = run_comprehensive_analysis()

        assert set(result) == {"analysis_results", "performance_metrics", "comprehensive_report"}
        assert result["performance_metrics"]["system_efficiency"] >= 0.0
        assert "INTEGRATED ANALYSIS SUMMARY" in result["comprehensive_report"]


class TestImportsAndReloads:
    """Test module imports and reloads without substitutes."""

    def test_reload_keeps_integrated_analyzer_export(self):
        module = importlib.import_module("src.integrated_analysis")
        reloaded = importlib.reload(module)
        assert hasattr(reloaded, "IntegratedAnalyzer")

    def test_reload_keeps_insect_analysis_export(self):
        module = importlib.import_module("src.insect_analysis")
        reloaded = importlib.reload(module)
        assert hasattr(reloaded, "run_comprehensive_analysis")

    def test_edge_case_imports_and_fallbacks(self):
        for module_name in ["src.behavioral", "src.spectroscopy", "src.integrated_analysis"]:
            module = importlib.import_module(module_name)
            assert module.__name__ == module_name
