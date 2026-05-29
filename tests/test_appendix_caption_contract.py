"""Contract tests comparing appendix manuscript captions to registry claim boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APPENDIX_LABELS = [
    "fig:app_active_inference",
    "fig:app_detection_limits",
    "fig:app_env_channel",
    "fig:app_neural_encoding_full",
    "fig:app_plasmonic_sweep",
    "fig:app_sensilla_beam",
    "fig:app_spectral_unmixing",
]

LABEL_TO_MANUSCRIPT = {
    "fig:app_active_inference": "10_appendix_active_inference.md",
    "fig:app_detection_limits": "11_appendix_detection_limits.md",
    "fig:app_env_channel": "12_appendix_environmental_channel.md",
    "fig:app_neural_encoding_full": "13_appendix_neural_encoding.md",
    "fig:app_plasmonic_sweep": "14_appendix_plasmonic_geometry.md",
    "fig:app_sensilla_beam": "15_appendix_sensilla_array_directionality.md",
    "fig:app_spectral_unmixing": "16_appendix_spectral_unmixing.md",
}


def _load_registry() -> dict[str, dict]:
    registry_path = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    if not registry_path.exists():
        pytest.skip("figure_registry.json not generated yet")
    return json.loads(registry_path.read_text(encoding="utf-8"))


def _extract_caption(manuscript_path: Path, label: str) -> str:
    text = manuscript_path.read_text(encoding="utf-8")
    pattern = rf"\\caption\{{([^}}]+)\}}\s*\\label\{{{re.escape(label)}\}}"
    match = re.search(pattern, text, flags=re.DOTALL)
    assert match, f"Missing caption block for {label} in {manuscript_path.name}"
    return match.group(1)


@pytest.mark.parametrize("label", APPENDIX_LABELS)
def test_appendix_caption_includes_registry_claim_boundary(label: str) -> None:
    registry = _load_registry()
    record = registry[label]
    claim = str(record["metadata"]["claim_boundary"]).strip().rstrip(".")
    manuscript = PROJECT_ROOT / "manuscript" / LABEL_TO_MANUSCRIPT[label]
    caption = _extract_caption(manuscript, label)
    assert "Claim boundary:" in caption
    caption_claim = caption.split("Claim boundary:", 1)[1].strip().rstrip(".")
    registry_head = claim.split(";")[0].strip().lower()
    caption_head = caption_claim.split(";")[0].strip().lower()
    assert registry_head in caption_claim.lower() or caption_head in claim.lower()
