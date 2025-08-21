"""Shared helpers for thin orchestrator scripts.

Utilities:
- ensure_src_on_path(): add repo root to sys.path for local `src` imports
- setup_paths(): return (fig_dir, data_dir), creating dirs
- set_mpl_backend(): force non-interactive backend
- write_caption(path, text): write a single-line caption
"""
from __future__ import annotations

import os
import sys
from typing import Tuple


def ensure_src_on_path() -> None:
    """Ensure repository root is on sys.path for `import src.*` to work."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


def setup_paths() -> Tuple[str, str]:
    """Create and return figure and data directories under output/."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fig_dir = os.path.join(repo_root, "output", "figures")
    data_dir = os.path.join(repo_root, "output", "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    return fig_dir, data_dir


def set_mpl_backend() -> None:
    """Set a non-interactive matplotlib backend for headless rendering."""
    os.environ.setdefault("MPLBACKEND", "Agg")


def write_caption(caption_path: str, text: str) -> None:
    """Write caption text to a file, ensuring parent directory exists."""
    os.makedirs(os.path.dirname(caption_path), exist_ok=True)
    with open(caption_path, "w") as fh:
        fh.write(text)


