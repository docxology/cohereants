"""Manuscript discovery contract for combined PDF inclusion."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_SECTIONS = [
    "00_abstract.md",
    "01_introduction.md",
    "02_methodology.md",
    "03_experimental_results.md",
    "04_discussion.md",
    "05_conclusion.md",
    "06_mathematical_appendix.md",
    "07_empirical_studies.md",
    "08_ant_stack.md",
    "09_symbols_glossary.md",
    "10_appendix_active_inference.md",
    "11_appendix_detection_limits.md",
    "12_appendix_environmental_channel.md",
    "13_appendix_neural_encoding.md",
    "14_appendix_plasmonic_geometry.md",
    "15_appendix_sensilla_array_directionality.md",
    "16_appendix_spectral_unmixing.md",
    "99_references.md",
]

FILES_WITHOUT_H1 = frozenset({"01_introduction.md", "99_references.md"})


def _template_root() -> Path:
    candidates = [
        PROJECT_ROOT.parent.parent,
        PROJECT_ROOT.parent.parent.parent / "template",
    ]
    env_root = os.environ.get("TEMPLATE_ROOT")
    if env_root:
        candidates.append(Path(env_root))
    for candidate in candidates:
        if (candidate / "infrastructure" / "rendering" / "manuscript_discovery.py").is_file():
            return candidate.resolve()
    pytest.skip("template infrastructure not found for manuscript discovery import")


@pytest.fixture(scope="module")
def discover_manuscript_files():
    template_root = _template_root()
    if str(template_root) not in sys.path:
        sys.path.insert(0, str(template_root))
    from infrastructure.rendering.manuscript_discovery import discover_manuscript_files as discover

    return discover


def test_discover_manuscript_includes_all_sections(discover_manuscript_files) -> None:
    manuscript_dir = PROJECT_ROOT / "manuscript"
    discovered = [path.name for path in discover_manuscript_files(manuscript_dir)]
    assert discovered == EXPECTED_SECTIONS


def test_manuscript_section_headings_are_unique(discover_manuscript_files) -> None:
    manuscript_dir = PROJECT_ROOT / "manuscript"
    headings: list[str] = []
    for path in discover_manuscript_files(manuscript_dir):
        if path.name in FILES_WITHOUT_H1:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                headings.append(line[2:].strip())
                break
        else:
            pytest.fail(f"No H1 heading in {path.name}")
    assert len(headings) == len(set(headings)), "Duplicate H1 headings would collide in combined PDF TOC"
