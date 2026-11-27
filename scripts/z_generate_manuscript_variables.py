#!/usr/bin/env python3
"""Thin orchestrator: generate and inject manuscript variables."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_TEMPLATE_ROOT = Path(
    os.environ.get("TEMPLATE_ROOT", str(_PROJECT_ROOT.parent.parent.parent / "template"))
).resolve()
if str(_PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "src"))
if _TEMPLATE_ROOT.exists() and str(_TEMPLATE_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEMPLATE_ROOT))
elif str(Path.cwd()) not in sys.path:
    sys.path.insert(0, str(Path.cwd()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate manuscript variables for cohereants")
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Allow N/A fallbacks when analysis outputs are missing",
    )
    args = parser.parse_args()

    import importlib.util

    mv_path = _PROJECT_ROOT / "src" / "manuscript_variables.py"
    spec = importlib.util.spec_from_file_location("cohereants_manuscript_variables", mv_path)
    assert spec and spec.loader
    mv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mv)
    from infrastructure.rendering.manuscript_injection import write_resolved_manuscript_tree

    variables = mv.generate_variables(
        _PROJECT_ROOT,
        require_analysis_outputs=not args.allow_draft,
    )
    out_path = _PROJECT_ROOT / "output" / "data" / "manuscript_variables.json"
    mv.save_variables(variables, out_path)
    resolved = write_resolved_manuscript_tree(_PROJECT_ROOT, variables)
    config = resolved / "config.yaml"
    if config.is_file():
        marker = "# Generated manuscript ordering"
        content = config.read_text(encoding="utf-8")
        if marker not in content:
            config.write_text(f"{marker}\n{content}", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
