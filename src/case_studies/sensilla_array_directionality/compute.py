"""Case study orchestration for sensilla_array_directionality."""
from __future__ import annotations

from .core import *
from .morphology import *
from .types import SensillaArrayDirectionalityAnalysis

def compute_sensilla_array_analysis(seed: int = 42) -> SensillaArrayDirectionalityAnalysis:
    """Compute array geometries, morphology, frequency response, and coupling artifacts."""
    rng = np.random.default_rng(seed)
    wavelengths = np.linspace(2.0, 25.0, 200)
    ir_wavelengths = np.array([2.5, 5.0, 10.0, 15.0, 20.0])

    log_positions = design_log_periodic_array(min_len_um=1.0, max_len_um=200.0, tau=1.3, count=8)
    log_pattern = compute_beam_pattern(wavelengths, log_positions, np.ones_like(log_positions))
    log_gain = array_gain(log_pattern["pattern"])

    circular_array = design_circular_array(radius_um=50.0, count=12, phase_center=True)
    circ_positions = np.column_stack([circular_array["x_positions"], circular_array["y_positions"]])

    n_sensilla = 50
    sensilla_lengths = rng.lognormal(mean=2.5, sigma=0.6, size=n_sensilla)
    sensilla_diameters = sensilla_lengths * rng.uniform(0.1, 0.3, n_sensilla)
    morphology_analysis = analyze_sensilla_morphology(sensilla_lengths, sensilla_diameters, ir_wavelengths)

    array_geometry = {"positions": circ_positions}
    freq_response = frequency_response_analysis(
        array_geometry,
        frequency_range_thz=(10, 150),
        n_frequencies=150,
        medium_permittivity=2.3,
    )

    angles = np.linspace(0, 180, 181)
    dipole_pattern = sensilla_element_pattern(angles, 10.0, 10.0, "dipole")
    monopole_pattern = sensilla_element_pattern(angles, 10.0, 10.0, "monopole")
    patch_pattern = sensilla_element_pattern(angles, 10.0, 10.0, "patch")
    coupling_matrix = mutual_coupling_matrix(circ_positions, 10.0, coupling_strength=0.2)

    morph_correlation = float(
        np.corrcoef(morphology_analysis["sensilla_lengths_um"], morphology_analysis["best_wavelength_matches"])[0, 1]
    )

    return SensillaArrayDirectionalityAnalysis(
        wavelengths=wavelengths,
        log_positions=log_positions,
        log_pattern=log_pattern,
        log_gain=log_gain,
        circ_positions=circ_positions,
        n_sensilla=n_sensilla,
        morphology_analysis=morphology_analysis,
        freq_response=freq_response,
        angles=angles,
        dipole_pattern=dipole_pattern,
        monopole_pattern=monopole_pattern,
        patch_pattern=patch_pattern,
        coupling_matrix=coupling_matrix,
        morph_correlation=morph_correlation,
    )

