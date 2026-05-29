"""Typed analysis contract."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SensillaArrayDirectionalityAnalysis:
    wavelengths: object
    log_positions: object
    log_pattern: object
    log_gain: object
    circ_positions: object
    n_sensilla: object
    morphology_analysis: object
    freq_response: object
    angles: object
    dipole_pattern: object
    monopole_pattern: object
    patch_pattern: object
    coupling_matrix: object
    morph_correlation: object

    def as_dict(self) -> dict[str, Any]:
        return {
            "wavelengths": self.wavelengths,
            "log_positions": self.log_positions,
            "log_pattern": self.log_pattern,
            "log_gain": self.log_gain,
            "circ_positions": self.circ_positions,
            "n_sensilla": self.n_sensilla,
            "morphology_analysis": self.morphology_analysis,
            "freq_response": self.freq_response,
            "angles": self.angles,
            "dipole_pattern": self.dipole_pattern,
            "monopole_pattern": self.monopole_pattern,
            "patch_pattern": self.patch_pattern,
            "coupling_matrix": self.coupling_matrix,
            "morph_correlation": self.morph_correlation
        }
