#!/usr/bin/env python3
"""Thin orchestrator: generate core manuscript figures via src.figures."""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def main() -> int:
    from src.figures import generate_core_manuscript_figures

    paths = generate_core_manuscript_figures(_PROJECT_ROOT)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
