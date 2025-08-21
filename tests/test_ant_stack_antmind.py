"""
Tests for Ant Stack AntMind layer classes.
"""

import numpy as np

try:
    from src.ant_stack.antmind import AntMindOlfaction, AntMindStigmergy
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.ant_stack.antmind import AntMindOlfaction, AntMindStigmergy


class TestAntMindOlfaction:
    def test_policy_selection_interface(self):
        mind = AntMindOlfaction(policy_horizon=2.0)
        current_state = {"position": np.array([0.0, 0.0]), "heading": 0.0}
        action = mind.select_policy(current_state)
        assert isinstance(action, np.ndarray)
        assert action.shape[-1] in (2, 3)


class TestAntMindStigmergy:
    def test_field_update_and_diffusion(self):
        sm = AntMindStigmergy(grid_shape=(32, 32), decay_rate=0.01, diffusion_coefficient=0.1)
        deposits = [(10, 10, 1.0), (20, 20, 0.5)]
        sm.update_pheromone_field(deposits)
        assert sm.pheromone_field[10, 10] > 0.0
        assert sm.pheromone_field[20, 20] > 0.0

        # After another update without deposits, total mass should decrease due to decay
        total_before = float(np.sum(sm.pheromone_field))
        sm.update_pheromone_field([])
        total_after = float(np.sum(sm.pheromone_field))
        assert total_after < total_before


