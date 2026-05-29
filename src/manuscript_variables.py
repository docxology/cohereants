"""Manuscript variable generation for cohereants.

Reads analysis outputs under ``output/data/`` and protocol fixtures from
``src/manuscript_fixtures.py``. Returns flat ``dict[str, str]`` for
``{{TOKEN}}`` substitution via infrastructure manuscript injection.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

try:
    from .manuscript_fixtures import (
        BIOMIMETIC_IR_BAND_UM,
        BIOMIMETIC_RESPONSE_THRESHOLD_MW_CM2,
        FIRE_BLACKBODY_PEAK_UM,
        MOSQUITO_IR_PEAK_UM,
        MOSQUITO_IR_RANGE_M,
        MOSQUITO_IR_SOURCE_TEMP_C,
        PROTOCOL_IR_POWER_DENSITY_MW_CM2,
        PROTOCOL_MIN_PREREGISTERED_N,
        PROTOCOL_QCL_BANDS_UM,
        PROTOCOL_THERMAL_CONTROL_MATCHED_POWER,
        SKIN_BLACKBODY_PEAK_UM,
    )
except ImportError:  # pragma: no cover
    from manuscript_fixtures import (  # type: ignore[no-redef]
        BIOMIMETIC_IR_BAND_UM,
        BIOMIMETIC_RESPONSE_THRESHOLD_MW_CM2,
        FIRE_BLACKBODY_PEAK_UM,
        MOSQUITO_IR_PEAK_UM,
        MOSQUITO_IR_RANGE_M,
        MOSQUITO_IR_SOURCE_TEMP_C,
        PROTOCOL_IR_POWER_DENSITY_MW_CM2,
        PROTOCOL_MIN_PREREGISTERED_N,
        PROTOCOL_QCL_BANDS_UM,
        PROTOCOL_THERMAL_CONTROL_MATCHED_POWER,
        SKIN_BLACKBODY_PEAK_UM,
    )

try:
    from infrastructure.core.logging.utils import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging as _logging

    logger = _logging.getLogger(__name__)


def _load_npz(project_root: Path, name: str) -> dict[str, np.ndarray]:
    path = project_root / "output" / "data" / name
    if not path.exists():
        return {}
    with np.load(path, allow_pickle=True) as data:
        return {key: data[key] for key in data.files}


def _fmt_range(low: float, high: float, *, unit: str = "") -> str:
    return f"{low:g}--{high:g}{unit}"


def _load_config(project_root: Path) -> dict[str, Any]:
    config_path = project_root / "manuscript" / "config.yaml"
    if not config_path.exists():
        return {}
    with config_path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def generate_variables(project_root: Path, *, require_analysis_outputs: bool = False) -> dict[str, str]:
    """Build manuscript substitution tokens from measured outputs and fixtures."""
    project_root = project_root.resolve()
    missing: list[str] = []

    def require(path: Path, label: str) -> None:
        if require_analysis_outputs and not path.exists():
            missing.append(label)

    require(project_root / "output" / "data" / "response_time_comparison.npz", "response_time_comparison.npz")
    require(project_root / "output" / "data" / "detection_limits_comprehensive.npz", "detection_limits_comprehensive.npz")
    if missing:
        raise FileNotFoundError(
            "Missing analysis outputs required for manuscript variables: " + ", ".join(missing)
        )

    response_npz = _load_npz(project_root, "response_time_comparison.npz")
    detection_npz = _load_npz(project_root, "detection_limits_comprehensive.npz")
    sensilla_npz = _load_npz(project_root, "sensilla_data.npz")

    improvement_low, improvement_high = 2.3, 7.0
    if "improvement_factors" in response_npz:
        factors = np.asarray(response_npz["improvement_factors"], dtype=float)
        if factors.size:
            improvement_low = float(np.nanmin(factors))
            improvement_high = float(np.nanmax(factors))

    beam_width_low, beam_width_high = 15.0, 30.0
    if "beamwidth_deg" in sensilla_npz:
        bw = np.asarray(sensilla_npz["beamwidth_deg"], dtype=float)
        if bw.size:
            beam_width_low = float(np.nanmin(bw))
            beam_width_high = float(np.nanmax(bw))

    snr_operating_db = 10.0
    if "snr_db" in detection_npz:
        snr = np.asarray(detection_npz["snr_db"], dtype=float)
        if snr.size:
            snr_operating_db = float(np.nanmedian(snr))

    detection_spec_path = project_root / "output" / "data" / "detection_limits_spec.json"
    if detection_spec_path.exists():
        spec = json.loads(detection_spec_path.read_text(encoding="utf-8"))
        snr_operating_db = float(spec.get("snr_operating_db", snr_operating_db))

    config = _load_config(project_root)
    paper_title = str((config.get("paper") or {}).get("title", "cohereants"))
    random_seed = str((config.get("metadata") or {}).get("random_seed", 42))

    variables: dict[str, str] = {
        "PROJECT_TITLE": paper_title,
        "RANDOM_SEED": random_seed,
        "IMPROVEMENT_FACTOR_LOW": f"{improvement_low:g}",
        "IMPROVEMENT_FACTOR_HIGH": f"{improvement_high:g}",
        "BEAM_WIDTH_LOW_DEG": f"{beam_width_low:g}",
        "BEAM_WIDTH_HIGH_DEG": f"{beam_width_high:g}",
        "LOCALIZATION_ACCURACY_DEG": _fmt_range(beam_width_low, beam_width_high),
        "BIOMIMETIC_IR_BAND_UM": _fmt_range(*BIOMIMETIC_IR_BAND_UM, unit=" µm"),
        "BIOMIMETIC_THRESHOLD_MW_CM2": _fmt_range(*BIOMIMETIC_RESPONSE_THRESHOLD_MW_CM2),
        "PROTOCOL_QCL_BAND_UM": _fmt_range(*PROTOCOL_QCL_BANDS_UM, unit=" µm"),
        "PROTOCOL_POWER_DENSITY_MW_CM2": _fmt_range(*PROTOCOL_IR_POWER_DENSITY_MW_CM2),
        "PROTOCOL_MIN_N": str(PROTOCOL_MIN_PREREGISTERED_N),
        "PROTOCOL_THERMAL_CONTROL": "matched power deposition" if PROTOCOL_THERMAL_CONTROL_MATCHED_POWER else "unmatched",
        "SNR_OPERATING_DB": f"{snr_operating_db:g}",
        "MOSQUITO_IR_SOURCE_TEMP_C": str(MOSQUITO_IR_SOURCE_TEMP_C),
        "MOSQUITO_IR_PEAK_UM": f"{MOSQUITO_IR_PEAK_UM:g}",
        "MOSQUITO_IR_RANGE_M": f"{MOSQUITO_IR_RANGE_M:g}",
        "FIRE_BLACKBODY_PEAK_UM": f"{FIRE_BLACKBODY_PEAK_UM:g}",
        "SKIN_BLACKBODY_PEAK_UM": f"{SKIN_BLACKBODY_PEAK_UM:g}",
        "FIGURE_WIDTH_RESPONSE_TIME": "1.0",
        "FIGURE_WIDTH_COMPOSITE": "0.95",
        "GENERATED_AT_UTC": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return variables


def save_variables(variables: dict[str, str], output_path: Path) -> Path:
    """Persist variables JSON for render-time injection and evidence registry."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"variables": variables, "generated_at": variables.get("GENERATED_AT_UTC", "")}
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path
