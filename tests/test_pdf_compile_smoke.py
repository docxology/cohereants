"""Smoke checks for combined PDF LaTeX compile artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "output" / "pdf" / "_combined_manuscript.log"
TEX_PATH = PROJECT_ROOT / "output" / "pdf" / "_combined_manuscript.tex"
PDF_PATH = PROJECT_ROOT / "output" / "pdf" / "cohereants_combined.pdf"


@pytest.mark.requires_latex
def test_combined_tex_log_has_no_fatal_latex_errors(skip_if_no_latex: None) -> None:
    if not LOG_PATH.is_file():
        pytest.skip(f"Compile log not found: {LOG_PATH}")
    log = LOG_PATH.read_text(encoding="utf-8", errors="replace")
    forbidden = (
        r"\mathrm allowed only in math mode",
        r"\textwidth ' invalid",
        "ended by \\end{document}",
        "Emergency stop",
    )
    hits = [msg for msg in forbidden if msg in log]
    assert not hits, f"LaTeX log contains fatal errors: {hits}"


@pytest.mark.requires_latex
def test_combined_tex_has_no_double_textwidth(skip_if_no_latex: None) -> None:
    if not TEX_PATH.is_file():
        pytest.skip(f"Combined tex not found: {TEX_PATH}")
    tex = TEX_PATH.read_text(encoding="utf-8", errors="replace")
    assert "\\textwidth\\textwidth" not in tex


@pytest.mark.requires_latex
def test_combined_tex_has_no_html_alt_inside_figure(skip_if_no_latex: None) -> None:
    if not TEX_PATH.is_file():
        pytest.skip(f"Combined tex not found: {TEX_PATH}")
    import re

    tex = TEX_PATH.read_text(encoding="utf-8", errors="replace")
    for block in re.findall(r"\\begin\{figure\}[\s\S]*?\\end\{figure\}", tex):
        assert "<!-- alt:" not in block


@pytest.mark.requires_latex
def test_combined_pdf_exists_when_rendered(skip_if_no_latex: None) -> None:
    if not PDF_PATH.is_file():
        pytest.skip(f"Combined PDF not found: {PDF_PATH}")
    assert PDF_PATH.stat().st_size > 500_000, "Combined PDF looks truncated"


@pytest.mark.requires_latex
def test_pdf_validation_cli_when_pdf_present(skip_if_no_latex: None) -> None:
    if not PDF_PATH.is_file():
        pytest.skip(f"Combined PDF not found: {PDF_PATH}")
    import subprocess

    template_root = PROJECT_ROOT.parent.parent.parent / "template"
    copied = template_root / "output" / "cohereants" / "pdf" / "cohereants_combined.pdf"
    target = copied if copied.is_file() else PDF_PATH
    if not template_root.is_dir():
        pytest.skip("template repo not available for infrastructure validation CLI")
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "infrastructure.validation.cli",
            "pdf",
            str(target),
        ],
        cwd=str(template_root),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
