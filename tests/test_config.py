"""
Comprehensive tests for the configuration system.

This test suite ensures high code coverage for the ConfigManager class
and related configuration functionality.
"""

import pytest
import tempfile
import os
import json
import warnings
import matplotlib.pyplot as plt

# Import the module under test
try:
    from src.config import ConfigManager, get_config, init_config, set_temperature
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.config import ConfigManager, get_config, init_config, set_temperature


class TestConfigManager:
    """Test the ConfigManager class."""

    def test_default_initialization(self):
        """Test initialization with default values."""
        config = ConfigManager()
        assert config.get('temperature') == 298.15
        assert config.get('boltzmann_constant') > 0
        assert config.get('plot_dpi') == 300

    def test_custom_config_file(self):
        """Test loading configuration from file."""
        # Create temporary config file
        config_data = {
            'temperature': 310.15,
            'plot_dpi': 600,
            'custom_setting': 'test_value'
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        try:
            config = ConfigManager(temp_file)
            assert config.get('temperature') == 310.15
            assert config.get('plot_dpi') == 600
            assert config.get('custom_setting') == 'test_value'
            # Default values should still be present
            assert config.get('boltzmann_constant') > 0
        finally:
            os.unlink(temp_file)

    def test_environment_variable_override(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv('INSECT_TEMPERATURE', '315.0')
        monkeypatch.setenv('INSECT_PLOT_DPI', '450')

        config = ConfigManager()
        assert config.get('temperature') == 315.0
        assert config.get('plot_dpi') == 450

    def test_get_method(self):
        """Test the get method with various scenarios."""
        config = ConfigManager()

        # Test existing key
        assert config.get('temperature') == 298.15

        # Test non-existing key with default
        assert config.get('nonexistent', 'default') == 'default'

        # Test non-existing key without default
        assert config.get('nonexistent') is None

        # Test nested key access
        config.set('nested.key', 'value')
        assert config.get('nested.key') == 'value'

    def test_set_method(self):
        """Test the set method."""
        config = ConfigManager()

        # Test setting new value
        config.set('temperature', 300.0)
        assert config.get('temperature') == 300.0

        # Test setting nested value
        config.set('analysis.fermi_estimation.vibrational_modes', 20)
        assert config.get('analysis.fermi_estimation.vibrational_modes') == 20

    def test_validation(self):
        """Test configuration validation."""
        config = ConfigManager()

        # Test invalid temperature
        with pytest.raises(ValueError):
            config.set('temperature', -100)

        # Test invalid range
        with pytest.raises(ValueError):
            config.set('frequency_range', [100, 50])  # min > max

    def test_load_method(self):
        """Test loading configuration from file."""
        config_data = {'temperature': 305.0, 'plot_dpi': 400}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        try:
            config = ConfigManager()
            config.load(temp_file)
            assert config.get('temperature') == 305.0
            assert config.get('plot_dpi') == 400
        finally:
            os.unlink(temp_file)

    def test_save_method(self):
        """Test saving configuration to file."""
        config = ConfigManager()
        config.set('temperature', 307.0)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            config.save(temp_file)

            # Load and verify
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            assert saved_data['temperature'] == 307.0
        finally:
            os.unlink(temp_file)

    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        config = ConfigManager()
        original_temp = config.get('temperature')

        # Modify configuration
        config.set('temperature', 400.0)
        assert config.get('temperature') == 400.0

        # Reset to defaults
        config.reset_to_defaults()
        assert config.get('temperature') == original_temp

    def test_analysis_config_methods(self):
        """Test analysis-specific configuration methods."""
        config = ConfigManager()

        # Test getting analysis config
        fermi_config = config.get_analysis_config('fermi_estimation')
        assert 'vibrational_modes' in fermi_config

        # Test updating analysis config
        config.update_analysis_config('fermi_estimation', {'vibrational_modes': 25})
        updated_config = config.get_analysis_config('fermi_estimation')
        assert updated_config['vibrational_modes'] == 25


class TestGlobalConfigFunctions:
    """Test global configuration functions."""

    def test_get_config(self):
        """Test get_config function."""
        config = get_config()
        assert isinstance(config, ConfigManager)

    def test_init_config(self):
        """Test init_config function."""
        config_data = {'temperature': 303.0}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        try:
            config = init_config(temp_file)
            assert config.get('temperature') == 303.0
        finally:
            os.unlink(temp_file)

    def test_set_temperature(self):
        """Test set_temperature convenience function."""
        from src.config import get_config

        # Use the global config instance
        global_config = get_config()
        original_temp = global_config.get('temperature')

        set_temperature(305.0)
        assert global_config.get('temperature') == 305.0

        # Reset
        set_temperature(original_temp)

    def test_convenience_functions(self):
        """Test convenience functions with real matplotlib + config state."""
        from src import config as config_module
        config = init_config()
        original_verbose = config.get('verbose_logging')
        original_seed = config.get('random_seed')

        from src.config import set_plot_style

        # Real call: 'default' is a valid matplotlib style and resets rcParams.
        # Perturb a parameter, then assert set_plot_style actually changed it back.
        plt.rcParams['lines.linewidth'] = 99.0
        set_plot_style('default')
        assert plt.rcParams['lines.linewidth'] != 99.0
        assert plt.rcParams['lines.linewidth'] == plt.rcParamsDefault['lines.linewidth']

        # Real except-OSError branch: an unknown style warns and does NOT raise.
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            set_plot_style('this_style_does_not_exist_12345')
        assert any("not found" in str(w.message) for w in caught)

        from src.config import enable_verbose_logging
        enable_verbose_logging()
        assert config_module.get_config().get('verbose_logging') is True

        from src.config import set_random_seed
        set_random_seed(123)
        assert config_module.get_config().get('random_seed') == 123

        config_module.get_config().set('verbose_logging', original_verbose)
        config_module.get_config().set('random_seed', original_seed)


class TestConfigManagerEdgeCases:
    """Test edge cases and error conditions."""

    def test_invalid_json_file(self):
        """Test loading invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content')
            temp_file = f.name

        try:
            config = ConfigManager()
            with pytest.raises(json.JSONDecodeError):
                config.load(temp_file)
        finally:
            os.unlink(temp_file)

    def test_nonexistent_config_file(self):
        """Test initialization with non-existent file."""
        config = ConfigManager('/nonexistent/path.json')
        # Should still work with defaults
        assert config.get('temperature') == 298.15

    def test_empty_config_file(self):
        """Test loading empty config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{}')
            temp_file = f.name

        try:
            config = ConfigManager(temp_file)
            # Should have default values
            assert config.get('temperature') == 298.15
        finally:
            os.unlink(temp_file)

    def test_nested_dict_merge(self):
        """Test merging nested dictionaries."""
        config = ConfigManager()
        config.set('nested.level1.level2', 'original')

        # Create update dict
        update = {'nested': {'level1': {'level2': 'updated', 'level3': 'new'}}}

        config._merge_dicts(config._config, update)

        assert config.get('nested.level1.level2') == 'updated'
        assert config.get('nested.level1.level3') == 'new'

    def test_environment_variable_types(self, monkeypatch):
        """Test different environment variable types."""
        test_cases = [
            ('INSECT_TEMPERATURE', '300.5', 300.5),
            ('INSECT_PLOT_DPI', '600', 600),
            ('INSECT_VERBOSE_LOGGING', 'true', True),
            ('INSECT_VERBOSE_LOGGING', 'false', False),
            ('INSECT_ANALYSIS_LIST', '[1,2,3]', [1, 2, 3])
        ]

        for env_var, env_value, expected_value in test_cases:
            monkeypatch.setenv(env_var, env_value)
            config = ConfigManager()
            config_key = env_var.replace('INSECT_', '').lower()
            assert config.get(config_key) == expected_value
            monkeypatch.delenv(env_var, raising=False)

    def test_invalid_environment_variable(self, monkeypatch):
        """Test invalid environment variable value."""
        monkeypatch.setenv('INSECT_TEMPERATURE', 'invalid')

        try:
            config = ConfigManager()
            assert config.get('temperature') == 298.15
        except (ValueError, TypeError):
            pass
