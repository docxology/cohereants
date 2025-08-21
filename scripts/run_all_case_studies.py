#!/usr/bin/env python3
"""Run all seven case study generators in sequence.

Thin orchestrator that simply executes each script as a module to ensure
non-redundant generation of data/figures required by the PDF pipeline.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "generate_sensilla_array_directionality.py",
    "generate_environmental_channel_analysis.py",
    "generate_detection_limits.py",
    "generate_neural_encoding_analysis.py",
    "generate_spectral_unmixing.py",
    "generate_plasmonic_geometry_sweep.py",
    "generate_active_inference_demo.py",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    runner = [sys.executable]
    failed: list[str] = []

    for script in SCRIPTS:
        path = repo_root / script
        print(f"Running case study: {script}")
        try:
            subprocess.check_call(runner + [str(path)])
            print(f"✅ Success: {script}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed: {script}")
            failed.append(script)

    if failed:
        print("Some case studies failed:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
