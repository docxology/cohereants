"""
Meta-Material Analytical Framework Module

This module implements a comprehensive meta-material analytical framework for the
vibrational theory of olfaction and infrared sensing in insects. It provides:

- Multi-scale material property analysis
- Electromagnetic field interactions
- Quantum mechanical coupling models
- Information-theoretic material characterization
- Integration with Fermi Estimation analysis

The framework serves as the theoretical foundation for connecting empirical evidence
with quantitative predictions and analysis.
"""

import numpy as np
from typing import Dict, Optional
from scipy import constants


class MetaMaterialAnalyzer:
    """
    Comprehensive meta-material analyzer for olfaction and infrared sensing.

    Implements multi-scale analysis of material properties and their
    relationship to sensory function in insects.
    """

    def __init__(self):
        """Initialize the meta-material analyzer with physical constants."""
        self.epsilon_0 = constants.epsilon_0  # Vacuum permittivity
        self.mu_0 = constants.mu_0  # Vacuum permeability
        self.c = constants.c  # Speed of light
        self.h = constants.h  # Planck's constant
        self.hbar = constants.hbar  # Reduced Planck's constant
        self.k_B = constants.k  # Boltzmann constant
        self.e = constants.e  # Elementary charge

    def calculate_dielectric_response(
        self, frequency: np.ndarray, epsilon_inf: float = 1.0, omega_p: float = 1e15, gamma: float = 1e12
    ) -> Dict[str, np.ndarray]:
        """
        Calculate Drude-Lorentz dielectric response for meta-materials.

        Args:
            frequency: Frequency array (Hz)
            epsilon_inf: High-frequency dielectric constant
            omega_p: Plasma frequency (rad/s)
            gamma: Damping frequency (rad/s)

        Returns:
            Dictionary with dielectric properties
        """
        omega = 2 * np.pi * frequency

        # Drude model for free electrons
        epsilon_drude = epsilon_inf - (omega_p**2) / (omega**2 + 1j * omega * gamma)

        # Real and imaginary parts
        epsilon_real = np.real(epsilon_drude)
        epsilon_imag = np.imag(epsilon_drude)

        # Refractive index
        n = np.sqrt(epsilon_real + np.sqrt(epsilon_real**2 + epsilon_imag**2))
        k = np.sqrt(-epsilon_real + np.sqrt(epsilon_real**2 + epsilon_imag**2))

        # Absorption coefficient
        alpha = 2 * omega * k / self.c

        return {
            "epsilon_real": epsilon_real,
            "epsilon_imag": epsilon_imag,
            "refractive_index": n,
            "extinction_coefficient": k,
            "absorption_coefficient": alpha,
            "frequency": frequency,
        }

    def analyze_plasmonic_resonance(
        self, particle_radius: float, metal_dielectric: float, medium_dielectric: float = 1.0
    ) -> Dict[str, float]:
        """
        Analyze plasmonic resonance in metallic nanoparticles.

        Args:
            particle_radius: Radius of nanoparticle (m)
            metal_dielectric: Dielectric constant of metal
            medium_dielectric: Dielectric constant of surrounding medium

        Returns:
            Dictionary with plasmonic properties
        """
        # Mie theory for spherical particles (quasi-static approximation)
        # For small particles, only dipole mode is important

        # Plasmon resonance condition
        epsilon_resonance = -2 * medium_dielectric

        # Resonance frequency (approximate)
        omega_resonance = np.sqrt(4 * np.pi * self.e**2 * self.c**2 / (3 * particle_radius * self.hbar))

        # Quality factor
        Q_factor = np.abs(epsilon_resonance) / np.imag(metal_dielectric)

        # Local field enhancement
        field_enhancement = (3 * medium_dielectric) / (metal_dielectric + 2 * medium_dielectric)

        return {
            "resonance_frequency_hz": omega_resonance / (2 * np.pi),
            "resonance_wavelength_m": 2 * np.pi * self.c / omega_resonance,
            "quality_factor": Q_factor,
            "field_enhancement": np.abs(field_enhancement),
            "epsilon_resonance": epsilon_resonance,
        }

    def calculate_quantum_coupling(
        self, energy_levels: np.ndarray, coupling_strength: float, temperature: float = 300.0
    ) -> Dict[str, np.ndarray]:
        """
        Calculate quantum mechanical coupling between energy levels.

        Args:
            energy_levels: Array of energy levels (J)
            coupling_strength: Coupling strength (J)
            temperature: Temperature (K)

        Returns:
            Dictionary with quantum coupling properties
        """
        # Boltzmann distribution
        boltzmann_weights = np.exp(-energy_levels / (self.k_B * temperature))
        boltzmann_weights = boltzmann_weights / np.sum(boltzmann_weights)

        # Coupling matrix elements
        n_levels = len(energy_levels)
        coupling_matrix = np.zeros((n_levels, n_levels))

        for i in range(n_levels):
            for j in range(n_levels):
                if i != j:
                    # Off-diagonal coupling
                    energy_diff = abs(energy_levels[i] - energy_levels[j])
                    coupling_matrix[i, j] = coupling_strength * np.exp(-energy_diff / (self.k_B * temperature))

        # Eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(coupling_matrix)

        # Transition rates (Fermi's golden rule)
        transition_rates = []
        for i in range(n_levels):
            for j in range(i + 1, n_levels):
                rate = (2 * np.pi / self.hbar) * coupling_matrix[i, j] ** 2 * boltzmann_weights[i]
                transition_rates.append(rate)

        return {
            "coupling_matrix": coupling_matrix,
            "eigenvalues": eigenvalues,
            "eigenvectors": eigenvectors,
            "transition_rates": np.array(transition_rates),
            "boltzmann_weights": boltzmann_weights,
        }

    def analyze_information_capacity(
        self,
        material_properties: Dict,
        frequency_bandwidth: float,
        signal_power: float,
        noise_temperature: float = 300.0,
    ) -> Dict[str, float]:
        """
        Analyze information capacity of meta-material systems.

        Args:
            material_properties: Output from calculate_dielectric_response
            frequency_bandwidth: Frequency bandwidth (Hz)
            signal_power: Signal power (W)
            noise_temperature: Noise temperature (K)

        Returns:
            Dictionary with information capacity measures
        """
        # Average refractive index
        avg_refractive_index = np.mean(material_properties["refractive_index"])

        # Group velocity
        group_velocity = self.c / avg_refractive_index

        # Signal energy
        signal_energy = signal_power / frequency_bandwidth

        # Noise power (Johnson-Nyquist)
        noise_power = self.k_B * noise_temperature * frequency_bandwidth

        # Signal-to-noise ratio
        snr = signal_power / noise_power

        # Shannon capacity
        channel_capacity = frequency_bandwidth * np.log2(1 + snr)

        # Information density
        info_density = channel_capacity / (signal_energy * group_velocity)

        # Quantum limit
        quantum_limit = frequency_bandwidth * np.log2(1 + signal_energy / (self.hbar * frequency_bandwidth))

        return {
            "channel_capacity_bits_per_sec": channel_capacity,
            "signal_to_noise_ratio": snr,
            "information_density_bits_per_joule_meter": info_density,
            "quantum_limit_bits_per_sec": quantum_limit,
            "group_velocity_m_per_sec": group_velocity,
            "noise_power_watts": noise_power,
        }

    def calculate_metamaterial_figure_of_merit(
        self,
        epsilon_real: np.ndarray,
        epsilon_imag: np.ndarray,
        mu_real: Optional[np.ndarray] = None,
        mu_imag: Optional[np.ndarray] = None,
    ) -> Dict[str, np.ndarray]:
        """
        Calculate figure of merit for meta-materials.

        Args:
            epsilon_real: Real part of permittivity
            epsilon_imag: Imaginary part of permittivity
            mu_real: Real part of permeability (optional)
            mu_imag: Imaginary part of permeability (optional)

        Returns:
            Dictionary with figure of merit measures
        """
        # Default permeability (non-magnetic)
        if mu_real is None:
            mu_real = np.ones_like(epsilon_real)
        if mu_imag is None:
            mu_imag = np.zeros_like(epsilon_imag)

        # Refractive index
        n = np.sqrt(epsilon_real * mu_real)

        # Impedance - handle division by zero element-wise
        epsilon_safe = np.where(np.abs(epsilon_real) < 1e-12, 1e-12, epsilon_real)
        z = np.sqrt(mu_real / epsilon_safe)

        # Figure of merit (FOM) for epsilon-near-zero materials
        fom_enz = np.abs(epsilon_real) / (np.abs(epsilon_imag) + 1e-12)

        # Figure of merit for negative index materials
        fom_nim = np.abs(n) / (np.abs(epsilon_imag) + np.abs(mu_imag) + 1e-12)

        # Loss tangent
        loss_tangent = np.abs(epsilon_imag) / (np.abs(epsilon_real) + 1e-12)

        # Quality factor
        quality_factor = 1.0 / (loss_tangent + 1e-12)

        return {
            "refractive_index": n,
            "impedance": z,
            "figure_of_merit_enz": fom_enz,
            "figure_of_merit_nim": fom_nim,
            "loss_tangent": loss_tangent,
            "quality_factor": quality_factor,
        }

    def analyze_multi_scale_properties(
        self, length_scales: np.ndarray, property_values: np.ndarray, scaling_exponent: float = 1.0
    ) -> Dict[str, np.ndarray]:
        """
        Analyze multi-scale material properties using scaling laws.

        Args:
            length_scales: Array of length scales (m)
            property_values: Array of corresponding property values
            scaling_exponent: Expected scaling exponent

        Returns:
            Dictionary with multi-scale analysis results
        """
        # Log-log scaling analysis
        log_lengths = np.log10(length_scales)
        log_properties = np.log10(property_values)

        # Linear fit
        coeffs = np.polyfit(log_lengths, log_properties, 1)
        slope = coeffs[0]
        intercept = coeffs[1]

        # Predicted values
        predicted = 10 ** (slope * log_lengths + intercept)

        # Residuals
        residuals = property_values - predicted

        # R-squared
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((property_values - np.mean(property_values)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # Fractal dimension (if applicable)
        fractal_dimension = -slope if slope < 0 else None

        return {
            "scaling_slope": slope,
            "scaling_intercept": intercept,
            "r_squared": r_squared,
            "fractal_dimension": fractal_dimension,
            "predicted_values": predicted,
            "residuals": residuals,
            "scaling_deviation": abs(slope - scaling_exponent),
        }

    def generate_metamaterial_report(
        self, dielectric_data: Dict, plasmonic_data: Dict, quantum_data: Dict, info_capacity_data: Dict
    ) -> str:
        """
        Generate comprehensive meta-material analysis report.

        Args:
            dielectric_data: Output from calculate_dielectric_response
            plasmonic_data: Output from analyze_plasmonic_resonance
            quantum_data: Output from calculate_quantum_coupling
            info_capacity_data: Output from analyze_information_capacity

        Returns:
            Formatted report string
        """
        report = []
        report.append("=== COMPREHENSIVE META-MATERIAL ANALYSIS ===\n")

        # Dielectric properties
        report.append("DIELECTRIC PROPERTIES:")
        report.append(
            f"  Frequency range: {dielectric_data['frequency'][0] / 1e12:.2f} - {dielectric_data['frequency'][-1] / 1e12:.2f} THz"
        )
        report.append(f"  Average refractive index: {np.mean(dielectric_data['refractive_index']):.3f}")
        report.append(
            f"  Absorption coefficient range: {np.min(dielectric_data['absorption_coefficient']):.2e} - {np.max(dielectric_data['absorption_coefficient']):.2e} m⁻¹\n"
        )

        # Plasmonic properties
        report.append("PLASMONIC PROPERTIES:")
        report.append(f"  Resonance frequency: {plasmonic_data['resonance_frequency_hz'] / 1e12:.2f} THz")
        report.append(f"  Resonance wavelength: {plasmonic_data['resonance_wavelength_m'] * 1e6:.2f} μm")
        report.append(f"  Quality factor: {plasmonic_data['quality_factor']:.2f}")
        report.append(f"  Field enhancement: {plasmonic_data['field_enhancement']:.2f}\n")

        # Quantum properties
        report.append("QUANTUM COUPLING:")
        report.append(f"  Number of energy levels: {len(quantum_data['eigenvalues'])}")
        report.append(f"  Average transition rate: {np.mean(quantum_data['transition_rates']):.2e} s⁻¹")
        report.append(f"  Coupling matrix size: {quantum_data['coupling_matrix'].shape}\n")

        # Information capacity
        report.append("INFORMATION CAPACITY:")
        report.append(f"  Channel capacity: {info_capacity_data['channel_capacity_bits_per_sec']:.2e} bits/s")
        report.append(f"  Signal-to-noise ratio: {info_capacity_data['signal_to_noise_ratio']:.2f}")
        report.append(
            f"  Information density: {info_capacity_data['information_density_bits_per_joule_meter']:.2e} bits/(J·m)"
        )
        report.append(f"  Quantum limit: {info_capacity_data['quantum_limit_bits_per_sec']:.2e} bits/s\n")

        return "\n".join(report)


def create_sample_metamaterial_analysis():
    """
    Create a sample meta-material analysis for demonstration.

    Returns:
        MetaMaterialAnalyzer instance with sample analysis
    """
    analyzer = MetaMaterialAnalyzer()

    # Sample frequency range (near-infrared to mid-infrared)
    frequency = np.logspace(13, 15, 100)  # 10 THz to 1000 THz

    # Sample dielectric response
    dielectric_data = analyzer.calculate_dielectric_response(
        frequency=frequency, epsilon_inf=2.0, omega_p=5e15, gamma=1e13
    )

    # Sample plasmonic analysis
    plasmonic_data = analyzer.analyze_plasmonic_resonance(
        particle_radius=50e-9,  # 50 nm
        metal_dielectric=-10.0 + 1j,
        medium_dielectric=1.5,
    )

    # Sample quantum coupling
    energy_levels = np.array([0, 1e-20, 2e-20, 3e-20])  # J
    quantum_data = analyzer.calculate_quantum_coupling(
        energy_levels=energy_levels,
        coupling_strength=1e-21,  # J
        temperature=300.0,
    )

    # Sample information capacity
    info_capacity_data = analyzer.analyze_information_capacity(
        material_properties=dielectric_data,
        frequency_bandwidth=1e12,  # 1 THz
        signal_power=1e-6,  # 1 μW
        noise_temperature=300.0,
    )

    return analyzer, dielectric_data, plasmonic_data, quantum_data, info_capacity_data


if __name__ == "__main__":
    # Example usage
    analyzer, dielec_data, plasm_data, quant_data, info_data = create_sample_metamaterial_analysis()

    report = analyzer.generate_metamaterial_report(dielec_data, plasm_data, quant_data, info_data)
    print(report)
