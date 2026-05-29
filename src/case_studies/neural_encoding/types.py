"""Typed analysis contract."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NeuralEncodingAnalysis:
    time_axis: object
    stimuli: object
    stimulus_labels: object
    n_neurons: object
    population_spike_data: object
    population_responses: object
    spike_stats: object
    temporal_results: object
    pop_results: object
    mi_results: object
    discrimination_results: object
    adaptation_results: object

    def as_dict(self) -> dict[str, Any]:
        return {
            "time_axis": self.time_axis,
            "stimuli": self.stimuli,
            "stimulus_labels": self.stimulus_labels,
            "n_neurons": self.n_neurons,
            "population_spike_data": self.population_spike_data,
            "population_responses": self.population_responses,
            "spike_stats": self.spike_stats,
            "temporal_results": self.temporal_results,
            "pop_results": self.pop_results,
            "mi_results": self.mi_results,
            "discrimination_results": self.discrimination_results,
            "adaptation_results": self.adaptation_results
        }
