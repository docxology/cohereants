"""Tests for manuscript variable generation."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.manuscript_variables import generate_variables, save_variables


def _minimal_project(tmp_path: Path) -> Path:
    (tmp_path / "output" / "data").mkdir(parents=True)
    np.savez(
        tmp_path / "output" / "data" / "response_time_comparison.npz",
        improvement_factors=np.array([2.3, 5.0, 7.0]),
    )
    np.savez(tmp_path / "output" / "data" / "sensilla_data.npz", beamwidth_deg=np.array([15.0, 22.0, 30.0]))
    np.savez(tmp_path / "output" / "data" / "detection_limits_comprehensive.npz", snr_db=np.array([8.0, 10.0, 12.0]))
    (tmp_path / "output" / "data" / "detection_limits_spec.json").write_text(
        json.dumps({"snr_operating_db": 11.0}), encoding="utf-8"
    )
    (tmp_path / "manuscript").mkdir()
    (tmp_path / "manuscript" / "config.yaml").write_text("paper:\n  title: Test\nmetadata:\n  random_seed: 42\n")
    return tmp_path


def test_generate_variables_from_outputs(tmp_path: Path) -> None:
    root = _minimal_project(tmp_path)
    variables = generate_variables(root, require_analysis_outputs=True)
    assert variables["IMPROVEMENT_FACTOR_LOW"] == "2.3"
    assert variables["IMPROVEMENT_FACTOR_HIGH"] == "7"
    assert variables["BEAM_WIDTH_LOW_DEG"] == "15"
    assert variables["SNR_OPERATING_DB"] == "11"
    assert variables["FIRE_BLACKBODY_PEAK_UM"] == "3"
    assert variables["SKIN_BLACKBODY_PEAK_UM"] == "9.4"
    assert variables["BIOMIMETIC_IR_BAND_UM"] == "2.8--6 µm"
    assert variables["PROTOCOL_QCL_BAND_UM"] == "2--25 µm"
    assert variables["BIOMIMETIC_THRESHOLD_MW_CM2"] == "11--17.3"
    out = save_variables(variables, root / "output" / "data" / "manuscript_variables.json")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "variables" in payload


def test_figure_width_tokens_are_fractions_only(tmp_path: Path) -> None:
    variables = generate_variables(_minimal_project(tmp_path))
    for key in ("FIGURE_WIDTH_RESPONSE_TIME", "FIGURE_WIDTH_COMPOSITE"):
        assert "\\textwidth" not in variables[key]
        assert variables[key] in {"1.0", "0.95"}


def test_no_double_textwidth_in_includegraphics_pattern(tmp_path: Path) -> None:
    variables = generate_variables(_minimal_project(tmp_path))
    for key in ("FIGURE_WIDTH_RESPONSE_TIME", "FIGURE_WIDTH_COMPOSITE"):
        line = f"\\includegraphics[width={variables[key]}\\textwidth]{{../output/figures/example.png}}"
        assert "\\textwidth\\textwidth" not in line
