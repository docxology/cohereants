"""Shared helpers for thin orchestrator scripts.

Utilities:
- ensure_src_on_path(): add repo root to sys.path for local `src` imports
- setup_paths(): return (fig_dir, data_dir), creating dirs
- set_mpl_backend(): force non-interactive backend
- write_figure_bundle_from_script(): caption + alt sidecars via save_figure_bundle
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple


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


def write_figure_bundle_from_script(
    figure_path: str,
    caption: str,
    *,
    label: str,
    alt_text: str | None = None,
    npz_path: str | None = None,
    npz_payload: dict[str, Any] | None = None,
) -> Path:
    """Write caption and alt-text sidecars using the canonical figure bundle contract."""
    ensure_src_on_path()
    from src.figure_artifacts import save_figure_bundle
    from src.viz.figure_helpers import DEFAULT_CLAIM_BOUNDARY, FIGURE_ALT_TEXT, FIGURE_CLAIM_BOUNDARIES

    resolved_alt = alt_text or FIGURE_ALT_TEXT.get(label, caption.split(".")[0].strip())
    claim_boundary = FIGURE_CLAIM_BOUNDARIES.get(label, DEFAULT_CLAIM_BOUNDARY)
    return save_figure_bundle(
        Path(figure_path),
        caption,
        label=label,
        claim_boundary=claim_boundary,
        alt_text=resolved_alt,
        npz_path=Path(npz_path) if npz_path else None,
        npz_payload=npz_payload,
    )


def analysis_as_dict(analysis: Any) -> dict[str, Any]:
    """Return mapping view of typed case-study analysis objects."""
    if hasattr(analysis, "as_dict"):
        return analysis.as_dict()
    if isinstance(analysis, dict):
        return analysis
    raise TypeError(f"Unsupported analysis type: {type(analysis)!r}")


def write_caption(caption_path: str, text: str) -> None:
    """Deprecated: prefer write_figure_bundle_from_script with a registry label."""
    os.makedirs(os.path.dirname(caption_path), exist_ok=True)
    with open(caption_path, "w") as fh:
        fh.write(text)
