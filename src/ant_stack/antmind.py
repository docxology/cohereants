"""
Ant Stack - AntMind layer components.

Implements minimal cognitive interfaces for policy selection and stigmergic
pheromone field dynamics with diffusion and decay.
"""

from typing import Dict, List, Tuple
import numpy as np


class AntMindOlfaction:
    """
    Active-inference-like placeholder for olfactory policy selection.

    Args:
        policy_horizon: planning horizon in seconds
    """

    def __init__(self, policy_horizon: float = 2.0):
        if policy_horizon <= 0:
            raise ValueError("policy_horizon must be positive")
        self.policy_horizon = float(policy_horizon)

    def select_policy(self, current_state: Dict) -> np.ndarray:
        """
        Select a simple movement policy based on current state.
        Returns an action vector (dx, dy) or (v, omega).
        """
        # Minimal deterministic behavior: small forward step
        return np.array([0.1, 0.0], dtype=float)


class AntMindStigmergy:
    """
    Grid-based pheromone field with diffusion and decay.

    Args:
        grid_shape: (H, W)
        decay_rate: exponential decay rate per update
        diffusion_coefficient: diffusion strength
    """

    def __init__(self, grid_shape=(100, 100), decay_rate: float = 0.01, diffusion_coefficient: float = 0.1):
        h, w = int(grid_shape[0]), int(grid_shape[1])
        if h <= 0 or w <= 0:
            raise ValueError("grid_shape must be positive")
        if decay_rate < 0 or diffusion_coefficient < 0:
            raise ValueError("rates must be non-negative")
        self.pheromone_field = np.zeros((h, w), dtype=float)
        self.decay_rate = float(decay_rate)
        self.diffusion_coefficient = float(diffusion_coefficient)

    def update_pheromone_field(self, deposits: List[Tuple[int, int, float]]):
        for x, y, amount in deposits:
            if 0 <= x < self.pheromone_field.shape[0] and 0 <= y < self.pheromone_field.shape[1]:
                self.pheromone_field[x, y] += float(amount)
        self.pheromone_field = self._diffuse_and_decay(self.pheromone_field)

    def _diffuse_and_decay(self, field: np.ndarray) -> np.ndarray:
        laplacian = (
            -4 * field
            + np.roll(field, 1, axis=0)
            + np.roll(field, -1, axis=0)
            + np.roll(field, 1, axis=1)
            + np.roll(field, -1, axis=1)
        )
        diffusion = self.diffusion_coefficient * laplacian
        decay = -self.decay_rate * field
        return field + diffusion + decay
