"""Scoped matplotlib/numpy warning suppression for plot boundaries."""

from __future__ import annotations

import warnings
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def suppress_plot_warnings() -> Iterator[None]:
    """Suppress benign numerical warnings during figure construction."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield
