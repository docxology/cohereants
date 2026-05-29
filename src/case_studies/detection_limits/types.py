"""Typed analysis contract."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DetectionLimitsAnalysis:
    roc_results: object
    snr_levels: object
    detection_perf: object
    operating_regions: object
    noise_analysis: object
    range_analysis: object

    def as_dict(self) -> dict[str, Any]:
        return {
            "roc_results": self.roc_results,
            "snr_levels": self.snr_levels,
            "detection_perf": self.detection_perf,
            "operating_regions": self.operating_regions,
            "noise_analysis": self.noise_analysis,
            "range_analysis": self.range_analysis
        }
