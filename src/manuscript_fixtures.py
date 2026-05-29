"""Shared manuscript figure fixtures and protocol constants."""

from __future__ import annotations

from typing import Any, Sequence, Tuple

import numpy as np

# Atmospheric windows used by the coarse transmission model (μm).
IR_WINDOWS: Sequence[tuple[float, float, str, str]] = (
    (2.0, 5.0, "2-5 μm mid-IR", "higher-confidence window"),
    (8.0, 14.0, "8-14 μm long-wave IR", "primary atmospheric window"),
    (17.0, 25.0, "17-25 μm far-IR", "lower-confidence model band"),
)

# Representative sensilla morphometric inputs (class, length μm, diameter μm).
SENSILLA_SAMPLES: Sequence[tuple[str, float, float]] = (
    ("coeloconica", 5.0, 1.0),
    ("coeloconica", 9.0, 1.3),
    ("coeloconica", 14.0, 1.8),
    ("basiconica", 18.0, 2.2),
    ("basiconica", 32.0, 3.0),
    ("trichodea", 55.0, 3.5),
    ("trichodea", 95.0, 4.8),
    ("trichodea", 150.0, 6.0),
)

# Experimental protocol defaults (engineering deliverable).
PROTOCOL_QCL_BANDS_UM = (2.0, 25.0)
PROTOCOL_THERMAL_CONTROL_MATCHED_POWER = True
PROTOCOL_MIN_PREREGISTERED_N = 50
PROTOCOL_IR_POWER_DENSITY_MW_CM2 = (0.1, 2.0)

# Literature-anchored sensor precedents (Melanophila electrophysiology; Schmitz & Trenner 2003; Hammer 2001).
BIOMIMETIC_IR_BAND_UM = (2.8, 6.0)
BIOMIMETIC_RESPONSE_THRESHOLD_MW_CM2 = (11.0, 17.3)

# Blackbody peak wavelengths for protocol context (Wien displacement; engineering fixtures).
FIRE_BLACKBODY_PEAK_UM = 3.0
SKIN_BLACKBODY_PEAK_UM = 9.4

# Chandel et al. thermal-IR host-seeking assay parameters (engineering protocol separation).
MOSQUITO_IR_SOURCE_TEMP_C = 34
MOSQUITO_IR_PEAK_UM = 9.4
MOSQUITO_IR_RANGE_M = 0.7

# Response-time anchors for fig:response_time_comparison (milliseconds).
RESPONSE_TIME_VISUAL_MS = 0.1
RESPONSE_TIME_AUDITORY_MS = 0.16
RESPONSE_TIME_INSECT_ORN_MS = 3.0
RESPONSE_TIME_SLOW_COMPARATOR_MS = 10.0
RESPONSE_TIME_MODEL_IR_TARGET_MS = 2.5


def default_olfactory_fixtures(
    seed: int = 42,
) -> Tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return canonical demo inputs for integrated olfactory analysis."""
    odorant_properties = {
        "molecular_weight": 150.0,
        "symmetry_number": 2,
        "vibrational_modes": 15,
    }
    receptor_properties = {
        "binding_energies": np.array([-25.0, -20.0, -15.0, -10.0, -5.0]),
        "response_amplitudes": np.random.default_rng(seed).normal(1.0, 0.3, 100),
        "epsilon_inf": 2.0,
        "omega_p": 5e15,
        "gamma": 1e13,
        "particle_radius": 50e-9,
        "metal_dielectric": -10.0 + 1j,
        "medium_dielectric": 1.5,
        "frequency_bandwidth": 1e12,
        "signal_power": 1e-6,
    }
    environmental_conditions = {
        "temperature_range": (273.15, 313.15),
        "humidity_range": (0.3, 0.8),
        "pressure_range": (101000, 102000),
        "noise_temperature": 300.0,
    }
    return odorant_properties, receptor_properties, environmental_conditions
