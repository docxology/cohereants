#!/usr/bin/env python3
"""Thin orchestrator: generate integrated analysis figures via src.integrated_figures."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def main() -> int:
    from src.integrated_figures import generate_integrated_analysis_figures

    paths = generate_integrated_analysis_figures(_PROJECT_ROOT)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
