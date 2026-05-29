"""Typed analysis contract."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlasmonicGeometryAnalysis:
    radii_nm: object
    wavelengths_um: object
    ir_wavelengths: object
    sweep_gold: object
    sweep_silver: object
    optimized_geometries: object
    gold_epsilon: object
    silver_epsilon: object
    positions_nm: object
    coupling_analysis: object
    optimal_radius: object
    field_dist: object

    def as_dict(self) -> dict[str, Any]:
        return {
            "radii_nm": self.radii_nm,
            "wavelengths_um": self.wavelengths_um,
            "ir_wavelengths": self.ir_wavelengths,
            "sweep_gold": self.sweep_gold,
            "sweep_silver": self.sweep_silver,
            "optimized_geometries": self.optimized_geometries,
            "gold_epsilon": self.gold_epsilon,
            "silver_epsilon": self.silver_epsilon,
            "positions_nm": self.positions_nm,
            "coupling_analysis": self.coupling_analysis,
            "optimal_radius": self.optimal_radius,
            "field_dist": self.field_dist
        }
