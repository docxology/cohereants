import os
import shutil
import sys

import pytest

# Force headless backend for matplotlib in tests
os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Ensure project root is importable so that `import src.*` works
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

_PLOTLY_MODULE_KEYS = ("plotly", "plotly.graph_objects", "plotly.express")


@pytest.fixture(autouse=True)
def _cleanup_plotly_module_stubs():
    """Remove plotly stubs injected by individual tests."""
    saved = {key: sys.modules.get(key) for key in _PLOTLY_MODULE_KEYS}
    yield
    for key in _PLOTLY_MODULE_KEYS:
        prior = saved.get(key)
        if prior is None:
            sys.modules.pop(key, None)
        else:
            sys.modules[key] = prior


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "requires_latex: tests requiring xelatex installation")


@pytest.fixture
def skip_if_no_latex() -> None:
    if not shutil.which("xelatex"):
        pytest.skip("xelatex not installed")

