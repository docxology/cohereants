"""Manuscript LaTeX safety checks for Pandoc/xelatex compatibility."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"


def _manuscript_md_files() -> list[Path]:
    return sorted(
        p for p in MANUSCRIPT_DIR.glob("*.md") if p.name not in {"AGENTS.md", "README.md"}
    )


def _strip_fenced_blocks(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"~~~[\s\S]*?~~~", "", text)
    return text


def test_alt_comments_outside_figure_environments() -> None:
    violations: list[str] = []
    for md in _manuscript_md_files():
        text = md.read_text(encoding="utf-8")
        for match in re.finditer(
            r"\\begin\{figure\}[\s\S]*?\\end\{figure\}",
            text,
        ):
            block = match.group(0)
            if "<!-- alt:" in block:
                violations.append(md.name)
                break
    assert not violations, f"Alt comments inside figure environments: {violations}"


def test_list_items_do_not_use_pandoc_fragile_inline_math() -> None:
    violations: list[str] = []
    fragile = re.compile(r"^[-*]\s.*\\\(")
    for md in _manuscript_md_files():
        body = _strip_fenced_blocks(md.read_text(encoding="utf-8"))
        for line_no, line in enumerate(body.splitlines(), start=1):
            if fragile.search(line):
                violations.append(f"{md.name}:{line_no}: {line.strip()[:80]}")
    assert not violations, "List items with \\( ... \\): " + "; ".join(violations[:5])


def test_figure_blocks_have_alt_comment_before_begin() -> None:
    missing: list[str] = []
    for md in _manuscript_md_files():
        text = md.read_text(encoding="utf-8")
        for match in re.finditer(r"\\begin\{figure\}", text):
            before = text[max(0, match.start() - 400) : match.start()]
            if "<!-- alt:" not in before:
                missing.append(md.name)
                break
    assert not missing, f"Figure blocks missing preceding alt comment: {missing}"
