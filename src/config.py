"""
Configuration system for insect analysis research.

This module provides a centralized configuration system for managing analysis
parameters, visualization settings, and computational options. It supports
environment variables, configuration files, and programmatic overrides.

Key Features:
- Environment variable integration
- JSON/YAML configuration file support
- Runtime configuration updates
- Validation and type checking
- Default parameter sets for different analysis types
"""

import os
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path
import warnings


class ConfigManager:
    """
    Centralized configuration manager for insect analysis.

    Manages analysis parameters, visualization settings, and computational
    options with support for multiple configuration sources.

    Examples:
        >>> config = ConfigManager()
        >>> print(f"Temperature: {config.get('temperature')}K")
        Temperature: 298.15K

        >>> config.set('temperature', 310.15)
        >>> config.save('my_config.json')
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Optional path to JSON configuration file
        """
        self._config = self._get_defaults()
        self._config_file = config_file

        # Load from file if provided
        if config_file and Path(config_file).exists():
            self.load(config_file)

        # Override with environment variables
        self._load_from_environment()

        # Validate configuration
        self._validate_config()

    def _get_defaults(self) -> Dict[str, Any]:
        """
        Get default configuration values.

        Returns:
            Dictionary with default configuration
        """
        return {
            # Physical constants
            'temperature': 298.15,  # K (25°C)
            'boltzmann_constant': 1.380649e-23,  # J/K
            'plancks_constant': 6.62607015e-34,  # J⋅s
            'speed_of_light': 2.99792458e8,  # m/s

            # Analysis parameters
            'frequency_range': [1e12, 1e15],  # Hz
            'wavenumber_range': [500, 4000],  # cm⁻¹
            'wavelength_range': [2.5, 25],  # μm

            # Visualization settings
            'plot_dpi': 300,
            'plot_format': 'png',
            'colormap': 'viridis',
            'figure_size': [12, 8],

            # Computational settings
            'max_iterations': 1000,
            'convergence_threshold': 1e-6,
            'random_seed': 42,
            'parallel_processing': True,

            # Output settings
            'output_directory': 'output',
            'save_intermediate_results': True,
            'verbose_logging': False,

            # Analysis-specific defaults
            'analysis': {
                'fermi_estimation': {
                    'vibrational_modes': 15,
                    'binding_energy_range': [-30, 10],  # kJ/mol
                    'signal_to_noise_ratio': 10.0
                },
                'meta_material': {
                    'particle_radius': 50e-9,  # m
                    'plasma_frequency': 5e15,  # Hz
                    'damping_rate': 1e13,  # Hz
                    'refractive_index_medium': 1.5
                },
                'behavioral': {
                    'alpha': 0.05,  # significance level
                    'bootstrap_samples': 1000,
                    'response_time_bins': 50
                }
            }
        }

    def _load_from_environment(self) -> None:
        """
        Load configuration from environment variables.

        Environment variables should be prefixed with 'INSECT_' and use
        uppercase with underscores (e.g., INSECT_TEMPERATURE=310.15)
        """
        env_prefix = 'INSECT_'

        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()

                # Convert string values to appropriate types
                if value.isdigit():
                    converted_value = int(value)
                elif value.replace('.', '').replace('-', '').isdigit():
                    converted_value = float(value)
                elif value.lower() in ('true', 'false'):
                    converted_value = value.lower() == 'true'
                elif value.startswith('[') and value.endswith(']'):
                    # Simple list parsing
                    try:
                        converted_value = json.loads(value)
                    except json.JSONDecodeError:
                        converted_value = value
                else:
                    converted_value = value

                self.set(config_key, converted_value)

    def _validate_config(self) -> None:
        """
        Validate configuration values.

        Raises:
            ValueError: If configuration contains invalid values
        """
        # Temperature validation
        if self._config['temperature'] <= 0:
            raise ValueError("Temperature must be positive")

        # Range validations
        if self._config['frequency_range'][0] >= self._config['frequency_range'][1]:
            raise ValueError("Frequency range must be increasing")

        if self._config['wavenumber_range'][0] >= self._config['wavenumber_range'][1]:
            raise ValueError("Wavenumber range must be increasing")

        if self._config['wavelength_range'][0] >= self._config['wavelength_range'][1]:
            raise ValueError("Wavelength range must be increasing")

        # Positive value checks
        if self._config['plot_dpi'] <= 0:
            raise ValueError("Plot DPI must be positive")

        if self._config['max_iterations'] <= 0:
            raise ValueError("Max iterations must be positive")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get('temperature')
            298.15

            >>> config.get('analysis.fermi_estimation.vibrational_modes')
            15
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            value: Value to set

        Examples:
            >>> config.set('temperature', 310.15)
            >>> config.set('analysis.fermi_estimation.vibrational_modes', 20)
        """
        keys = key.split('.')
        config = self._config

        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

        # Re-validate configuration
        self._validate_config()

    def load(self, filename: str) -> None:
        """
        Load configuration from JSON file.

        Args:
            filename: Path to JSON configuration file

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        with open(filename, 'r') as f:
            loaded_config = json.load(f)

        # Merge with current configuration
        self._merge_dicts(self._config, loaded_config)

        # Re-validate
        self._validate_config()

    def save(self, filename: str) -> None:
        """
        Save current configuration to JSON file.

        Args:
            filename: Path to save configuration file
        """
        # Create directory if it doesn't exist
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        with open(filename, 'w') as f:
            json.dump(self._config, f, indent=2, sort_keys=True)

    def _merge_dicts(self, base: Dict, update: Dict) -> None:
        """
        Recursively merge update dictionary into base dictionary.

        Args:
            base: Base dictionary to update
            update: Dictionary with updates
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = self._get_defaults()
        self._load_from_environment()
        self._validate_config()

    def get_analysis_config(self, analysis_type: str) -> Dict[str, Any]:
        """
        Get configuration specific to an analysis type.

        Args:
            analysis_type: Type of analysis ('fermi_estimation', 'meta_material', 'behavioral')

        Returns:
            Dictionary with analysis-specific configuration
        """
        return self._config.get('analysis', {}).get(analysis_type, {})

    def update_analysis_config(self, analysis_type: str, updates: Dict[str, Any]) -> None:
        """
        Update configuration for a specific analysis type.

        Args:
            analysis_type: Type of analysis to update
            updates: Dictionary with configuration updates
        """
        if 'analysis' not in self._config:
            self._config['analysis'] = {}

        if analysis_type not in self._config['analysis']:
            self._config['analysis'][analysis_type] = {}

        self._config['analysis'][analysis_type].update(updates)
        self._validate_config()


# Global configuration instance
_config_manager = None

def get_config() -> ConfigManager:
    """
    Get the global configuration manager instance.

    Returns:
        Global ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def init_config(config_file: Optional[str] = None) -> ConfigManager:
    """
    Initialize the global configuration manager.

    Args:
        config_file: Optional path to configuration file

    Returns:
        Global ConfigManager instance
    """
    global _config_manager
    _config_manager = ConfigManager(config_file)
    return _config_manager


# Convenience functions for common operations
def set_temperature(temp: float) -> None:
    """Set analysis temperature in Kelvin."""
    get_config().set('temperature', temp)

def set_plot_style(style: str = 'seaborn-v0_8') -> None:
    """Set matplotlib plot style."""
    import matplotlib.pyplot as plt
    try:
        plt.style.use(style)
    except OSError:
        warnings.warn(f"Plot style '{style}' not found, using default")

def enable_verbose_logging() -> None:
    """Enable verbose logging for debugging."""
    get_config().set('verbose_logging', True)

def set_random_seed(seed: int) -> None:
    """Set random seed for reproducible results."""
    get_config().set('random_seed', seed)
    import numpy as np
    np.random.seed(seed)

