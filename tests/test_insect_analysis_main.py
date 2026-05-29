"""
Real execution and integration tests for the insect_analysis module.
"""

import importlib
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

import src.insect_analysis as insect_analysis
from src.insect_analysis import run_comprehensive_analysis

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run_script(script_path: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    env["MPLBACKEND"] = "Agg"
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / script_path)],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    return result


class TestInsectAnalysisModule:
    def test_module_imports(self):
        expected_names = [
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
            "MetaMaterialAnalyzer",
            "IntegratedAnalyzer",
        ]

        for name in expected_names:
            assert hasattr(insect_analysis, name)
            assert name in insect_analysis.__all__

    def test_run_comprehensive_analysis_real_structure_and_stdout(self, capsys):
        np.random.seed(0)
        result = run_comprehensive_analysis()
        captured = capsys.readouterr()

        assert "Running comprehensive insect analysis..." in captured.out
        assert set(result) == {"analysis_results", "performance_metrics", "comprehensive_report"}
        assert set(result["analysis_results"]) == {"fermi_analysis", "metamaterial_analysis"}
        assert result["analysis_results"]["fermi_analysis"]["molecular"]["total_bits"] < 0.0
        assert result["performance_metrics"]["information_processing_score"] < 0.0
        assert result["performance_metrics"]["material_performance_score"] > 0.0
        assert result["performance_metrics"]["system_efficiency"] == 0.0
        assert "INTEGRATED ANALYSIS SUMMARY" in result["comprehensive_report"]

    def test_run_comprehensive_analysis_parameter_contract_via_real_results(self):
        np.random.seed(0)
        result = run_comprehensive_analysis()
        analysis = result["analysis_results"]
        dielectric = analysis["metamaterial_analysis"]["dielectric"]
        neural = analysis["fermi_analysis"]["neural"]

        assert analysis["fermi_analysis"]["receptor"]["specificity_index"] >= 0.0
        assert analysis["fermi_analysis"]["receptor"]["specificity_index"] <= 1.0
        assert dielectric["frequency"].shape == dielectric["refractive_index"].shape
        assert neural["channel_capacity_bits"] > 0.0

    def test_module_reload_keeps_public_api(self):
        reloaded = importlib.reload(insect_analysis)
        assert hasattr(reloaded, "IntegratedAnalyzer")
        assert hasattr(reloaded, "run_comprehensive_analysis")

    def test_related_modules_remain_importable(self):
        for module_name in ["src.behavioral", "src.spectroscopy", "src.integrated_analysis"]:
            module = importlib.import_module(module_name)
            assert module.__name__ == module_name


class TestInsectAnalysisMainExecution:
    def test_main_block_executes_successfully(self, tmp_path):
        result = _run_script("src/insect_analysis.py", cwd=tmp_path)

        assert "Insect Analysis Module - Comprehensive Analysis" in result.stdout
        assert "Analysis completed successfully!" in result.stdout
        assert "Key Performance Metrics:" in result.stdout
