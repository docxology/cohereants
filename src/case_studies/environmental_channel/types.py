"""Typed analysis contract."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EnvironmentalChannelAnalysis:
    wavelengths_um: object
    transmission_results: object
    capacity_results: object

    def as_dict(self) -> dict[str, Any]:
        return {
            "wavelengths_um": self.wavelengths_um,
            "transmission_results": self.transmission_results,
            "capacity_results": self.capacity_results
        }
