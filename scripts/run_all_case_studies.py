#!/usr/bin/env python3
"""Run all seven case study generators (parallel when safe)."""
from __future__ import annotations

import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
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


def _run_script(path: Path) -> tuple[str, float, str, int]:
    start = time.time()
    result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    return path.name, time.time() - start, result.stdout, result.returncode


def main() -> int:
    """Execute all case study scripts with deterministic summary ordering."""
    repo_root = Path(__file__).resolve().parent
    script_paths = [repo_root / name for name in SCRIPTS]
    print(f"Starting execution of {len(SCRIPTS)} case studies...")
    total_start = time.time()
    results: dict[str, tuple[float, str, int]] = {}

    with ProcessPoolExecutor(max_workers=min(4, len(script_paths))) as pool:
        futures = {pool.submit(_run_script, path): path.name for path in script_paths}
        for future in as_completed(futures):
            name, duration, stdout, code = future.result()
            results[name] = (duration, stdout, code)
            status = "Success" if code == 0 else "Failed"
            print(f"{status}: {name} ({duration:.2f}s)")

    failed = [name for name in SCRIPTS if results.get(name, (0, "", 1))[2] != 0]
    total_duration = time.time() - total_start
    print(f"\nExecution summary ({total_duration:.2f}s total): {len(SCRIPTS) - len(failed)}/{len(SCRIPTS)} succeeded")
    if failed:
        print(f"Failed scripts: {', '.join(failed)}")
        return 1

    print("\nTiming report (declared script order):")
    for name in SCRIPTS:
        duration, stdout, _ = results[name]
        print(f"  {duration:6.2f}s - {name}")
        for line in reversed(stdout.strip().splitlines()):
            if "figures/" in line or "output/" in line:
                print(f"           Output: {line.strip()}")
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
