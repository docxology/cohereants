"""Appendix F: Plasmonic nano-geometry sweep.

Comprehensive electromagnetic modeling of plasmonic nanostructures in insect sensilla,
including resonance analysis, field enhancement calculations, and geometry optimization.
Models localized surface plasmons (LSPs) and their role in IR detection enhancement.
"""

from __future__ import annotations

from typing import Dict, Tuple, Union, Optional
import numpy as np
from scipy.optimize import minimize_scalar


def drude_model_permittivity(
    wavelengths_um: np.ndarray,
    plasma_wavelength_um: float = 0.138,  # Gold plasma wavelength
    collision_time_fs: float = 27.0,  # Gold collision time
    epsilon_inf: float = 1.0,
) -> np.ndarray:
    """
    Calculate frequency-dependent permittivity using Drude model.

    Args:
        wavelengths_um: Wavelengths in micrometers
        plasma_wavelength_um: Plasma wavelength in micrometers
        collision_time_fs: Collision time in femtoseconds
        epsilon_inf: High-frequency permittivity

    Returns:
        Complex permittivity array
    """
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    if np.any(wavelengths <= 0):
        raise ValueError("All wavelengths must be positive")

    # Convert to angular frequency (rad/s)
    c_um_per_s = 2.998e14  # Speed of light in μm/s
    omega = 2 * np.pi * c_um_per_s / wavelengths

    # Plasma frequency
    omega_p = 2 * np.pi * c_um_per_s / plasma_wavelength_um

    # Collision frequency
    gamma = 1.0 / (collision_time_fs * 1e-15)

    # Drude permittivity
    epsilon = epsilon_inf - (omega_p**2) / (omega**2 + 1j * omega * gamma)

    return epsilon


def mie_scattering_sphere(
    wavelengths_um: np.ndarray,
    radius_nm: float,
    epsilon_particle: Union[complex, np.ndarray],
    epsilon_medium: float = 2.25,  # Typical insect cuticle
) -> Dict[str, np.ndarray]:
    """
    Calculate Mie scattering properties for spherical nanoparticles.

    Args:
        wavelengths_um: Wavelengths in micrometers
        radius_nm: Particle radius in nanometers
        epsilon_particle: Complex permittivity of particle material
        epsilon_medium: Real permittivity of surrounding medium

    Returns:
        Dict with scattering cross-sections, efficiency factors, and field enhancement
    """
    wavelengths = np.asarray(wavelengths_um, dtype=float)
    n_wavelengths = len(wavelengths)

    if np.isscalar(epsilon_particle):
        epsilon_p = np.full(n_wavelengths, epsilon_particle, dtype=complex)
    else:
        epsilon_p = np.asarray(epsilon_particle, dtype=complex)
        if len(epsilon_p) != n_wavelengths:
            raise ValueError("epsilon_particle array size must match wavelengths")

    # Size parameter
    k_medium = 2 * np.pi * np.sqrt(epsilon_medium) / wavelengths  # Wave vector in medium
    x = k_medium * (radius_nm * 1e-3)  # Convert nm to μm

    # Relative permittivity
    m_squared = epsilon_p / epsilon_medium

    # Dipole approximation (valid for x << 1)
    alpha_normalized = 3 * (m_squared - 1) / (m_squared + 2)  # Polarizability

    # Cross sections (using dipole approximation)
    geometric_cross_section = np.pi * (radius_nm * 1e-3) ** 2  # μm²

    C_ext = 4 * np.pi * k_medium * (radius_nm * 1e-3) ** 3 * np.imag(alpha_normalized)
    C_sca = (8 * np.pi / 3) * k_medium**4 * (radius_nm * 1e-3) ** 6 * np.abs(alpha_normalized) ** 2
    C_abs = C_ext - C_sca

    # Efficiency factors
    Q_ext = C_ext / geometric_cross_section
    Q_sca = C_sca / geometric_cross_section
    Q_abs = C_abs / geometric_cross_section

    # Field enhancement at particle surface (dipole approximation)
    enhancement = np.abs(1 + 2 * alpha_normalized) ** 2

    # Quality factor (resonance sharpness)
    q_factor = np.abs(alpha_normalized.real) / (2 * np.abs(alpha_normalized.imag) + 1e-12)

    return {
        "wavelengths_um": wavelengths,
        "size_parameter": x,
        "extinction_cross_section": C_ext,
        "scattering_cross_section": C_sca,
        "absorption_cross_section": C_abs,
        "extinction_efficiency": Q_ext,
        "scattering_efficiency": Q_sca,
        "absorption_efficiency": Q_abs,
        "field_enhancement": enhancement,
        "quality_factor": q_factor,
        "polarizability": alpha_normalized,
    }


def coupled_dipoles_near_field(
    positions_nm: np.ndarray,
    radius_nm: float,
    wavelength_um: float,
    epsilon_particle: complex,
    epsilon_medium: float = 2.25,
    incident_field_strength: float = 1.0,
) -> Dict[str, np.ndarray]:
    """
    Calculate near-field enhancement for coupled plasmonic nanoparticles.

    Args:
        positions_nm: Particle positions in nanometers, shape (N, 3)
        radius_nm: Particle radius in nanometers
        wavelength_um: Wavelength in micrometers
        epsilon_particle: Complex permittivity of particles
        epsilon_medium: Real permittivity of medium
        incident_field_strength: Incident field amplitude

    Returns:
        Dict with near-field enhancement factors and coupling strengths
    """
    positions = np.asarray(positions_nm, dtype=float) * 1e-3  # Convert to μm
    if positions.ndim != 2 or positions.shape[1] != 3:
        raise ValueError("Positions must be (N, 3) array")

    n_particles = positions.shape[0]

    # Wave vector in medium
    k = 2 * np.pi * np.sqrt(epsilon_medium) / wavelength_um

    # Individual particle polarizability (from Mie theory)
    single_particle = mie_scattering_sphere(np.array([wavelength_um]), radius_nm, epsilon_particle, epsilon_medium)
    alpha_0 = single_particle["polarizability"][0]

    # Distance matrix between particles
    distances = np.zeros((n_particles, n_particles))
    for i in range(n_particles):
        for j in range(i + 1, n_particles):
            r_ij = np.linalg.norm(positions[i] - positions[j])
            distances[i, j] = distances[j, i] = r_ij

    # Dipole-dipole interaction matrix
    G = np.eye(n_particles, dtype=complex)

    for i in range(n_particles):
        for j in range(n_particles):
            if i != j:
                r = distances[i, j]
                if r > 0:
                    # Simplified dipole-dipole interaction (retarded case)
                    G[i, j] = alpha_0 * (np.exp(1j * k * r) / r**3) * (1 - 1j * k * r)

    # Solve for induced dipole moments: (I - G) * p = alpha_0 * E_0
    try:
        I_minus_G = np.eye(n_particles) - G
        E_incident = np.ones(n_particles) * incident_field_strength
        dipole_moments = np.linalg.solve(I_minus_G, alpha_0 * E_incident)
    except np.linalg.LinAlgError:
        # Fallback to individual particles if coupling matrix is singular
        dipole_moments = alpha_0 * E_incident

    # Enhancement factors
    individual_enhancement = np.abs(alpha_0 * incident_field_strength) ** 2
    coupled_enhancement = np.abs(dipole_moments) ** 2
    enhancement_ratio = coupled_enhancement / (individual_enhancement + 1e-12)

    # Coupling strength metric
    coupling_eigenvalues = np.linalg.eigvals(G)
    max_coupling = np.max(np.abs(coupling_eigenvalues - 1))

    return {
        "positions_um": positions,
        "distances_um": distances,
        "dipole_moments": dipole_moments,
        "individual_enhancement": individual_enhancement,
        "coupled_enhancement": coupled_enhancement,
        "enhancement_ratio": enhancement_ratio,
        "coupling_strength": max_coupling,
        "coupling_eigenvalues": coupling_eigenvalues,
    }


def optimize_plasmonic_geometry(
    target_wavelength_um: float,
    geometry_type: str = "sphere",
    material: str = "gold",
    medium_permittivity: float = 2.25,
    size_range_nm: Tuple[float, float] = (5.0, 100.0),
) -> Dict[str, Union[float, complex]]:
    """
    Optimize nanoparticle geometry for maximum enhancement at target wavelength.

    Args:
        target_wavelength_um: Target wavelength for optimization
        geometry_type: 'sphere', 'cylinder', or 'ellipsoid'
        material: Material type ('gold', 'silver', 'aluminum')
        medium_permittivity: Permittivity of surrounding medium
        size_range_nm: Size optimization range in nanometers

    Returns:
        Optimized geometry parameters and performance metrics
    """
    # Material parameters (simplified)
    material_params = {
        "gold": {"plasma_wl": 0.138, "collision_time": 27.0},
        "silver": {"plasma_wl": 0.137, "collision_time": 17.0},
        "aluminum": {"plasma_wl": 0.105, "collision_time": 12.0},
    }

    if material not in material_params:
        raise ValueError(f"Unknown material: {material}")

    params = material_params[material]
    epsilon_particle = drude_model_permittivity(
        np.array([target_wavelength_um]), params["plasma_wl"], params["collision_time"]
    )[0]

    def objective(size_nm):
        """Objective function to maximize field enhancement."""
        if geometry_type == "sphere":
            result = mie_scattering_sphere(
                np.array([target_wavelength_um]), size_nm, epsilon_particle, medium_permittivity
            )
            return -result["field_enhancement"][0]  # Negative for minimization
        else:
            # Simplified for other geometries
            return -(size_nm / 50.0)  # Placeholder

    # Optimize size
    optimization_result = minimize_scalar(objective, bounds=size_range_nm, method="bounded")

    optimal_size = optimization_result.x
    max_enhancement = -optimization_result.fun

    # Calculate properties at optimal size
    if geometry_type == "sphere":
        optimal_properties = mie_scattering_sphere(
            np.array([target_wavelength_um]), optimal_size, epsilon_particle, medium_permittivity
        )
        resonance_quality = optimal_properties["quality_factor"][0]
    else:
        resonance_quality = 10.0  # Placeholder

    return {
        "optimal_size_nm": optimal_size,
        "max_enhancement": max_enhancement,
        "resonance_quality": resonance_quality,
        "target_wavelength_um": target_wavelength_um,
        "material_permittivity": epsilon_particle,
        "geometry_type": geometry_type,
        "material": material,
    }


def sweep_plasmonic_quality(
    radii_nm: np.ndarray,
    wavelengths_um: "Optional[np.ndarray]" = None,
    material: str = "gold",
    medium_epsilon_real: float = 2.25,
    metal_epsilon_imag: "Optional[float]" = None,
) -> Dict[str, np.ndarray]:
    """
    Comprehensive sweep of plasmonic quality factors across size and wavelength.

    Args:
        radii_nm: Particle radii in nanometers
        wavelengths_um: Wavelengths in micrometers
        material: Material type
        medium_epsilon_real: Real part of medium permittivity

    Returns:
        Quality factors and enhancement factors as 2D arrays
    """

    radii = np.asarray(radii_nm, dtype=float)
    # Allow caller to omit wavelengths; use a sensible default sweep if so
    if wavelengths_um is None:
        wavelengths = np.linspace(2.0, 25.0, 100)
    else:
        wavelengths = np.asarray(wavelengths_um, dtype=float)

    if radii.ndim != 1 or wavelengths.ndim != 1:
        raise ValueError("Radii and wavelengths must be 1D arrays")

    n_radii = len(radii)
    n_wavelengths = len(wavelengths)

    # Calculate material permittivity
    material_params = {
        "gold": {"plasma_wl": 0.138, "collision_time": 27.0},
        "silver": {"plasma_wl": 0.137, "collision_time": 17.0},
        "aluminum": {"plasma_wl": 0.105, "collision_time": 12.0},
    }

    if material not in material_params:
        raise ValueError(f"Unknown material: {material}")

    params = material_params[material]
    epsilon_material = drude_model_permittivity(wavelengths, params["plasma_wl"], params["collision_time"])
    # Allow callers to manually inject an imaginary component for material loss
    if metal_epsilon_imag is not None:
        epsilon_material = epsilon_material + 1j * float(metal_epsilon_imag)

    # Output arrays
    q_factors = np.zeros((n_radii, n_wavelengths))
    enhancements = np.zeros((n_radii, n_wavelengths))
    resonance_wavelengths = np.zeros(n_radii)
    max_enhancements = np.zeros(n_radii)

    for i, radius in enumerate(radii):
        # Calculate properties across wavelength range
        mie_result = mie_scattering_sphere(wavelengths, radius, epsilon_material, medium_epsilon_real)

        q_factors[i, :] = mie_result["quality_factor"]
        enhancements[i, :] = mie_result["field_enhancement"]

        # Find resonance wavelength (max enhancement)
        max_idx = np.argmax(enhancements[i, :])
        resonance_wavelengths[i] = wavelengths[max_idx]
        max_enhancements[i] = enhancements[i, max_idx]

    # Provide a simple 1D proxy for quality factor across radii for downstream checks
    q_factor_proxy = np.max(np.abs(q_factors), axis=1)

    return {
        "radii_nm": radii,
        "wavelengths_um": wavelengths,
        "q_factors_2d": q_factors,
        "enhancements_2d": enhancements,
        "resonance_wavelengths": resonance_wavelengths,
        "max_enhancements": max_enhancements,
        "material_permittivity": epsilon_material,
        "q_factor_proxy": q_factor_proxy,
    }


def field_distribution_near_particle(
    particle_radius_nm: float,
    wavelength_um: float,
    epsilon_particle: complex,
    epsilon_medium: float = 2.25,
    grid_extent_nm: float = 200.0,
    grid_points: int = 50,
) -> Dict[str, np.ndarray]:
    """
    Calculate near-field distribution around a spherical nanoparticle.

    Args:
        particle_radius_nm: Particle radius in nanometers
        wavelength_um: Wavelength in micrometers
        epsilon_particle: Complex permittivity of particle
        epsilon_medium: Real permittivity of medium
        grid_extent_nm: Spatial extent of calculation grid in nanometers
        grid_points: Number of grid points per dimension

    Returns:
        Near-field intensity and phase distributions
    """
    # Create spatial grid
    x_nm = np.linspace(-grid_extent_nm / 2, grid_extent_nm / 2, grid_points)
    y_nm = np.linspace(-grid_extent_nm / 2, grid_extent_nm / 2, grid_points)
    X_nm, Y_nm = np.meshgrid(x_nm, y_nm)

    # Distance from center
    R_nm = np.sqrt(X_nm**2 + Y_nm**2)

    # Wave vector in medium
    k = 2 * np.pi * np.sqrt(epsilon_medium) / wavelength_um

    # Polarizability (dipole approximation)
    alpha = 3 * (epsilon_particle - epsilon_medium) / (epsilon_particle + 2 * epsilon_medium)

    # Initialize field arrays
    E_field = np.zeros_like(X_nm, dtype=complex)

    # Calculate field at each point
    for i in range(grid_points):
        for j in range(grid_points):
            r_nm = R_nm[i, j]
            r_um = r_nm * 1e-3  # Convert to micrometers

            if r_nm > particle_radius_nm:
                # Outside particle - scattered field
                if r_um > 0:
                    # Dipole field contribution
                    kr = k * r_um
                    dipole_field = alpha * (np.exp(1j * kr) / kr**3) * (kr**2 + 1j * kr - 1)
                    E_field[i, j] = 1.0 + dipole_field  # Incident + scattered
                else:
                    E_field[i, j] = 1.0  # Only incident field at origin
            else:
                # Inside particle - transmitted field
                transmission_coeff = 3 * epsilon_medium / (epsilon_particle + 2 * epsilon_medium)
                E_field[i, j] = transmission_coeff

    # Calculate intensity and phase
    intensity = np.abs(E_field) ** 2
    phase = np.angle(E_field)

    # Find enhancement hot spots
    max_intensity = np.max(intensity)
    enhancement_factor = max_intensity / 1.0  # Relative to incident field

    return {
        "x_nm": x_nm,
        "y_nm": y_nm,
        "X_nm": X_nm,
        "Y_nm": Y_nm,
        "R_nm": R_nm,
        "E_field_complex": E_field,
        "intensity": intensity,
        "phase": phase,
        "max_enhancement": enhancement_factor,
        "particle_radius_nm": particle_radius_nm,
    }
