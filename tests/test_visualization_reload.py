"""
Tests that reload the visualization module under different import conditions to
exercise top-level import branches (seaborn present/absent and config fallback).
"""
import sys
import runpy
import types


def test_reload_with_seaborn_and_config_missing(tmp_path, monkeypatch):
    """Run the visualization module with seaborn present and src.config missing."""
    vis_path = 'src/visualization.py'

    # Ensure seaborn present
    fake_seaborn = types.ModuleType('seaborn')
    sys.modules['seaborn'] = fake_seaborn

    # Ensure src.config cannot be imported
    if 'src.config' in sys.modules:
        monkeypatch.delitem(sys.modules, 'src.config', raising=False)

    # Execute module in fresh namespace
    ns = runpy.run_path(vis_path)

    # HAS_SEABORN should be True in the executed namespace
    assert ns.get('HAS_SEABORN', False) is True


def test_reload_without_seaborn_and_with_config(tmp_path, monkeypatch):
    """Run the visualization module with seaborn absent and real src.config available."""
    vis_path = 'src/visualization.py'

    # Ensure seaborn absent
    monkeypatch.setitem(sys.modules, 'seaborn', None)
    if 'seaborn' in sys.modules:
        del sys.modules['seaborn']

    # Execute module and ensure HAS_SEABORN is False
    ns = runpy.run_path(vis_path)
    assert ns.get('HAS_SEABORN', False) is False


