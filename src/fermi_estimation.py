"""
Fermi Estimation Analysis Module

This module implements comprehensive Fermi Estimation type analysis for the vibrational theory
of olfaction and infrared sensing in insects. It provides quantitative estimation of:
- Syntactic information content (bits)
- Semantic information content (bits)
- Gaussian variational mean/variance estimates
- Information-theoretic measures for olfaction

The module integrates with the meta-material analytical framework to provide
quantitative grounding for empirical studies.
"""

import numpy as np
from typing import Dict, Tuple, Optional
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")


class FermiEstimator:
    """
    Comprehensive Fermi Estimation analyzer for olfaction and infrared sensing.

    Implements information-theoretic approaches to quantify:
    - Molecular vibrational information content
    - Receptor binding specificity
    - Neural response encoding
    - Environmental signal processing
    """

    def __init__(self):
        """Initialize the Fermi estimator with default parameters."""
        self.boltzmann_constant = 1.380649e-23  # J/K
        self.temperature = 298.15  # K (25°C)
        self.plancks_constant = 6.62607015e-34  # J⋅s

    def calculate_vibrational_entropy(
        self, frequencies: np.ndarray, occupation_numbers: Optional[np.ndarray] = None
    ) -> float:
        """
        Calculate vibrational entropy from frequency spectrum.

        Args:
            frequencies: Array of vibrational frequencies (cm^-1)
            occupation_numbers: Array of occupation numbers (default: Boltzmann distribution)

        Returns:
            Entropy in bits
        """
        if occupation_numbers is None:
            # Use Boltzmann distribution
            energy_levels = self.plancks_constant * frequencies * 3e10  # Convert to J
            occupation_numbers = np.exp(-energy_levels / (self.boltzmann_constant * self.temperature))
            occupation_numbers = occupation_numbers / np.sum(occupation_numbers)

        # Calculate entropy in bits
        entropy = -np.sum(occupation_numbers * np.log2(occupation_numbers + 1e-12))
        return entropy

    def estimate_molecular_information_content(
        self, molecular_weight: float, symmetry_number: int = 1, vibrational_modes: int = 3
    ) -> Dict[str, float]:
        """
        Estimate total information content of a molecule.

        Args:
            molecular_weight: Molecular weight in g/mol
            symmetry_number: Symmetry number for rotational entropy
            vibrational_modes: Number of vibrational degrees of freedom

        Returns:
            Dictionary with various information measures
        """
        # Translational entropy (3D ideal gas)
        molecular_mass = molecular_weight * 1.66e-27
        translational_entropy = 3 / 2 * np.log2(molecular_mass) + 15.0 if molecular_mass > 0 else 0.0

        # Rotational entropy
        rotational_entropy = np.log2(symmetry_number) + 2.0

        # Vibrational entropy (approximate)
        vibrational_entropy = vibrational_modes * 2.0

        # Total information content
        total_information = translational_entropy + rotational_entropy + vibrational_entropy

        return {
            "translational_bits": translational_entropy,
            "rotational_bits": rotational_entropy,
            "vibrational_bits": vibrational_entropy,
            "total_bits": total_information,
            "total_bytes": total_information / 8.0,
        }

    def calculate_receptor_specificity(
        self, binding_energies: np.ndarray, background_energy: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate receptor binding specificity using information theory.

        Args:
            binding_energies: Array of binding energies (kJ/mol)
            background_energy: Background/reference energy level

        Returns:
            Dictionary with specificity measures
        """
        # Convert to J/mol
        energies_j = binding_energies * 1000

        # Calculate Boltzmann weights
        weights = np.exp(-energies_j / (8.314 * self.temperature))
        weights = weights / np.sum(weights)

        # Information content of binding
        binding_entropy = -np.sum(weights * np.log2(weights + 1e-12))

        # Specificity index (lower entropy = higher specificity)
        specificity_index = 1.0 / (1.0 + binding_entropy)

        # Signal-to-noise ratio
        signal_energy = np.max(energies_j)
        noise_energy = np.std(energies_j)
        snr = signal_energy / (noise_energy + 1e-12)

        return {
            "binding_entropy_bits": binding_entropy,
            "specificity_index": specificity_index,
            "signal_to_noise_ratio": snr,
            "energy_range_kj_mol": np.ptp(binding_energies),
            "mean_binding_energy_kj_mol": np.mean(binding_energies),
        }

    def estimate_neural_encoding_efficiency(
        self, response_amplitudes: np.ndarray, noise_level: float = 0.1
    ) -> Dict[str, float]:
        """
        Estimate neural encoding efficiency for olfactory responses.

        Args:
            response_amplitudes: Array of neural response amplitudes
            noise_level: Standard deviation of noise

        Returns:
            Dictionary with encoding efficiency measures
        """
        # Handle empty array case
        if len(response_amplitudes) == 0:
            return {
                "signal_power": 0.0,
                "noise_power": noise_level**2,
                "signal_to_noise_ratio": 0.0,
                "channel_capacity_bits": 0.0,
                "information_rate_bits": 0.0,
                "encoding_efficiency_bits_per_energy": 0.0,
            }

        # Signal power
        signal_power = np.var(response_amplitudes)

        # Noise power
        noise_power = noise_level**2

        # Signal-to-noise ratio
        snr = signal_power / (noise_power + 1e-12)

        # Channel capacity (Shannon's formula)
        channel_capacity = 0.5 * np.log2(1 + snr)

        # Information rate (bits per response)
        information_rate = channel_capacity * len(response_amplitudes)

        # Encoding efficiency (information per unit energy)
        total_energy = np.sum(response_amplitudes**2)
        encoding_efficiency = information_rate / (total_energy + 1e-12)

        return {
            "signal_power": signal_power,
            "noise_power": noise_power,
            "signal_to_noise_ratio": snr,
            "channel_capacity_bits": channel_capacity,
            "information_rate_bits": information_rate,
            "encoding_efficiency_bits_per_energy": encoding_efficiency,
        }

    def gaussian_variational_analysis(self, data: np.ndarray, n_components: int = 3) -> Dict[str, np.ndarray]:
        """
        Perform Gaussian variational analysis on data.

        Args:
            data: Input data array
            n_components: Number of Gaussian components

        Returns:
            Dictionary with variational parameters
        """
        # Fit Gaussian mixture model
        from sklearn.mixture import GaussianMixture

        gmm = GaussianMixture(n_components=n_components, random_state=42)
        gmm.fit(data.reshape(-1, 1))

        # Extract parameters
        means = gmm.means_.flatten()
        variances = gmm.covariances_.flatten()
        weights = gmm.weights_

        # Calculate information content of each component
        entropies = []
        for mean, var in zip(means, variances):
            # Gaussian entropy: 0.5 * log(2πeσ²)
            entropy = 0.5 * np.log2(2 * np.pi * np.e * var)
            entropies.append(entropy)

        return {
            "means": means,
            "variances": variances,
            "weights": weights,
            "entropies_bits": np.array(entropies),
            "total_entropy_bits": np.sum(weights * entropies),
        }

    def calculate_environmental_information_content(
        self,
        temperature_range: Tuple[float, float],
        humidity_range: Tuple[float, float],
        pressure_range: Tuple[float, float],
    ) -> Dict[str, float]:
        """
        Calculate information content of environmental parameters.

        Args:
            temperature_range: (min, max) temperature in K
            humidity_range: (min, max) relative humidity (0-1)
            pressure_range: (min, max) pressure in Pa

        Returns:
            Dictionary with environmental information measures
        """
        # Temperature information (assuming uniform distribution)
        temp_diff = temperature_range[1] - temperature_range[0]
        temp_info = np.log2(temp_diff / 0.1) if temp_diff > 0.1 else 0.0  # 0.1K resolution

        # Humidity information
        humidity_diff = humidity_range[1] - humidity_range[0]
        humidity_info = np.log2(humidity_diff / 0.01) if humidity_diff > 0.01 else 0.0  # 1% resolution

        # Pressure information
        pressure_diff = pressure_range[1] - pressure_range[0]
        pressure_info = np.log2(pressure_diff / 100) if pressure_diff > 100 else 0.0  # 100 Pa resolution

        total_info = temp_info + humidity_info + pressure_info

        return {
            "temperature_bits": temp_info,
            "humidity_bits": humidity_info,
            "pressure_bits": pressure_info,
            "total_environmental_bits": total_info,
        }

    def generate_fermi_analysis_report(
        self, molecular_data: Dict, receptor_data: Dict, neural_data: Dict, environmental_data: Dict
    ) -> str:
        """
        Generate comprehensive Fermi analysis report.

        Args:
            molecular_data: Output from estimate_molecular_information_content
            receptor_data: Output from calculate_receptor_specificity
            neural_data: Output from estimate_neural_encoding_efficiency
            environmental_data: Output from calculate_environmental_information_content

        Returns:
            Formatted report string
        """
        report = []
        report.append("=== COMPREHENSIVE FERMI ESTIMATION ANALYSIS ===\n")

        # Molecular information
        report.append("MOLECULAR INFORMATION CONTENT:")
        report.append(f"  Total: {molecular_data['total_bits']:.2f} bits ({molecular_data['total_bytes']:.2f} bytes)")
        report.append(f"  Translational: {molecular_data['translational_bits']:.2f} bits")
        report.append(f"  Rotational: {molecular_data['rotational_bits']:.2f} bits")
        report.append(f"  Vibrational: {molecular_data['vibrational_bits']:.2f} bits\n")

        # Receptor specificity
        report.append("RECEPTOR BINDING SPECIFICITY:")
        report.append(f"  Binding entropy: {receptor_data['binding_entropy_bits']:.2f} bits")
        report.append(f"  Specificity index: {receptor_data['specificity_index']:.3f}")
        report.append(f"  Signal-to-noise ratio: {receptor_data['signal_to_noise_ratio']:.2f}\n")

        # Neural encoding
        report.append("NEURAL ENCODING EFFICIENCY:")
        report.append(f"  Channel capacity: {neural_data['channel_capacity_bits']:.2f} bits")
        report.append(f"  Information rate: {neural_data['information_rate_bits']:.2f} bits")
        report.append(f"  Encoding efficiency: {neural_data['encoding_efficiency_bits_per_energy']:.4f} bits/energy\n")

        # Environmental factors
        report.append("ENVIRONMENTAL INFORMATION:")
        report.append(f"  Total environmental bits: {environmental_data['total_environmental_bits']:.2f} bits")
        report.append(f"  Temperature: {environmental_data['temperature_bits']:.2f} bits")
        report.append(f"  Humidity: {environmental_data['humidity_bits']:.2f} bits")
        report.append(f"  Pressure: {environmental_data['pressure_bits']:.2f} bits\n")

        # Summary statistics
        total_system_info = (
            molecular_data["total_bits"]
            + receptor_data["binding_entropy_bits"]
            + neural_data["information_rate_bits"]
            + environmental_data["total_environmental_bits"]
        )

        report.append("SYSTEM SUMMARY:")
        report.append(f"  Total system information: {total_system_info:.2f} bits")
        report.append(f"  Information density: {total_system_info / 1000:.3f} bits/kJ")

        return "\n".join(report)


def create_sample_fermi_analysis():
    """
    Create a sample Fermi analysis for demonstration.

    Returns:
        FermiEstimator instance with sample analysis
    """
    estimator = FermiEstimator()

    # Sample molecular data
    molecular_data = estimator.estimate_molecular_information_content(
        molecular_weight=150.0,  # Typical odorant
        symmetry_number=2,
        vibrational_modes=15,
    )

    # Sample receptor data
    binding_energies = np.array([-25.0, -20.0, -15.0, -10.0, -5.0])  # kJ/mol
    receptor_data = estimator.calculate_receptor_specificity(binding_energies)

    # Sample neural data
    response_amplitudes = np.random.normal(1.0, 0.3, 100)
    neural_data = estimator.estimate_neural_encoding_efficiency(response_amplitudes)

    # Sample environmental data
    environmental_data = estimator.calculate_environmental_information_content(
        temperature_range=(273.15, 313.15),  # 0-40°C
        humidity_range=(0.3, 0.8),  # 30-80%
        pressure_range=(101000, 102000),  # 1 atm ± 100 Pa
    )

    return estimator, molecular_data, receptor_data, neural_data, environmental_data


if __name__ == "__main__":
    # Example usage
    estimator, mol_data, rec_data, neu_data, env_data = create_sample_fermi_analysis()

    report = estimator.generate_fermi_analysis_report(mol_data, rec_data, neu_data, env_data)
    print(report)
