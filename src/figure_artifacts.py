"""Save figure bundles (PNG, caption, optional NPZ) and registry metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .figure_registry_contract import FIGURE_VALIDATION_NOTE, caption_with_contract, figure_method


def save_figure_bundle(
    figure_path: Path,
    caption: str,
    *,
    label: str,
    claim_boundary: str,
    source_artifact: str = "",
    alt_text: str = "",
    npz_path: Path | None = None,
    npz_payload: dict[str, Any] | None = None,
) -> Path:
    """Write caption sidecar, optional alt-text sidecar, and optional NPZ; return figure path."""
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    method = figure_method(label)
    full_caption = caption_with_contract(caption, method)
    if claim_boundary and claim_boundary not in full_caption:
        full_caption = f"{full_caption} Claim boundary: {claim_boundary} {FIGURE_VALIDATION_NOTE}"
    caption_path = figure_path.with_suffix(".caption.txt")
    caption_path.write_text(full_caption, encoding="utf-8")
    if alt_text:
        alt_path = figure_path.with_suffix(".alt.txt")
        alt_path.write_text(alt_text.strip(), encoding="utf-8")
    if npz_payload is not None:
        target = npz_path or figure_path.with_name(figure_path.stem).with_suffix(".npz")
        if target.parent.name == "figures":
            target = figure_path.parent.parent / "data" / target.name
        target.parent.mkdir(parents=True, exist_ok=True)
        import numpy as np

        np.savez(target, **npz_payload)
    if source_artifact:
        _ = source_artifact  # reserved for registry consumers
    return figure_path


def write_figure_registry(figure_dir: Path, records: dict[str, dict[str, object]]) -> Path:
    """Write ``figure_registry.json`` for infrastructure validation."""
    from .figure_registry_contract import finalize_figure_registry

    registry_path = figure_dir / "figure_registry.json"
    finalized = finalize_figure_registry(records)
    registry_path.write_text(json.dumps(finalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return registry_path
