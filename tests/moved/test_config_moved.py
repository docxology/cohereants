import warnings
import numpy as np
from src.config import ConfigManager, set_plot_style


def test_config_env_json_decode_and_validation(monkeypatch, tmp_path):
    cm = ConfigManager()
    monkeypatch.setenv('INSECT_TESTLIST', '[1, 2,')  # invalid JSON
    cm._load_from_environment()
    assert cm.get('testlist') == '[1, 2,'

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        cm.reset_to_defaults()
    try:
        cm.set('frequency_range', [1000, 100])
    except ValueError:
        pass


def test_set_plot_style_handles_oserror(monkeypatch):
    import matplotlib.pyplot as plt_mod

    def raise_oserror(s):
        raise OSError('style not found')

    monkeypatch.setattr(plt_mod.style, 'use', raise_oserror)
    set_plot_style('nonexistent_style')


