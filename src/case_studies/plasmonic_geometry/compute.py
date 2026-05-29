"""Case study orchestration for plasmonic_geometry."""
from __future__ import annotations

from .core import *
from .types import PlasmonicGeometryAnalysis

def compute_plasmonic_geometry_analysis(seed: int = 42) -> PlasmonicGeometryAnalysis:
    """Compute plasmonic sweeps, optimization, coupling, and near-field artifacts."""
    _ = seed  # reserved for future stochastic extensions
    radii_nm = np.linspace(5, 100, 50)
    wavelengths_um = np.linspace(2.0, 25.0, 200)
    ir_wavelengths = np.array([3.0, 5.0, 10.0, 15.0, 20.0])

    sweep_gold = sweep_plasmonic_quality(radii_nm, wavelengths_um, "gold", 2.25)
    sweep_silver = sweep_plasmonic_quality(radii_nm, wavelengths_um, "silver", 2.25)

    optimized_geometries: Dict[str, list] = {"gold": [], "silver": []}
    for material in ("gold", "silver"):
        for wl in ir_wavelengths:
            optimized_geometries[material].append(
                optimize_plasmonic_geometry(wl, "sphere", material, 2.25, (5.0, 100.0))
            )

    gold_epsilon = drude_model_permittivity(wavelengths_um, 0.138, 27.0)
    silver_epsilon = drude_model_permittivity(wavelengths_um, 0.137, 17.0)

    positions_nm = np.array([[0, 0, 0], [30, 0, 0], [15, 26, 0]])
    gold_eps_at_10um = drude_model_permittivity(np.array([10.0]), 0.138, 27.0)[0]
    coupling_analysis = coupled_dipoles_near_field(positions_nm, 25.0, 10.0, gold_eps_at_10um, 2.25)

    optimal_radius = optimized_geometries["gold"][2]["optimal_size_nm"]
    field_dist = field_distribution_near_particle(optimal_radius, 10.0, gold_eps_at_10um, 2.25, 300.0, 80)

    return PlasmonicGeometryAnalysis(
        radii_nm=radii_nm,
        wavelengths_um=wavelengths_um,
        ir_wavelengths=ir_wavelengths,
        sweep_gold=sweep_gold,
        sweep_silver=sweep_silver,
        optimized_geometries=optimized_geometries,
        gold_epsilon=gold_epsilon,
        silver_epsilon=silver_epsilon,
        positions_nm=positions_nm,
        coupling_analysis=coupling_analysis,
        optimal_radius=optimal_radius,
        field_dist=field_dist,
    )

