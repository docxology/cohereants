#!/usr/bin/env python3
"""Run all seven case study generators in sequence.

Thin orchestrator that simply executes each script as a module to ensure
non-redundant generation of data/figures required by the PDF pipeline.
"""
from __future__ import annotations
import subprocess
import sys
import time
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
    """Execute all case study scripts with enhanced progress reporting."""
    repo_root = Path(__file__).resolve().parent
    runner = [sys.executable]
    failed: list[str] = []
    timings: list[tuple[str, float]] = []
    
    print(f"🚀 Starting execution of {len(SCRIPTS)} case studies...")
    total_start_time = time.time()

    for i, script in enumerate(SCRIPTS, 1):
        path = repo_root / script
        print(f"\n📊 [{i}/{len(SCRIPTS)}] Running case study: {script}")
        
        start_time = time.time()
        try:
            result = subprocess.run(runner + [str(path)], 
                                  capture_output=True, text=True, check=True)
            end_time = time.time()
            duration = end_time - start_time
            timings.append((script, duration))
            
            print(f"✅ Success: {script} ({duration:.2f}s)")
            # Print the output path if it's in stdout
            if result.stdout.strip():
                output_lines = result.stdout.strip().split('\n')
                # Look for the output path (typically the last line)
                for line in reversed(output_lines):
                    if line.strip() and ('figures/' in line or 'output/' in line):
                        print(f"   📁 Output: {line.strip()}")
                        break
                        
        except subprocess.CalledProcessError as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"❌ Failed: {script} (after {duration:.2f}s)")
            if e.stderr:
                print(f"   Error: {e.stderr.strip()}")
            failed.append(script)

    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Summary report
    print(f"\n📋 Execution Summary ({total_duration:.2f}s total):")
    print(f"   ✅ Successful: {len(SCRIPTS) - len(failed)}/{len(SCRIPTS)}")
    if failed:
        print(f"   ❌ Failed: {len(failed)} scripts: {', '.join(failed)}")
        
    # Timing report
    if timings:
        print(f"\n⏱️  Timing Report:")
        for script, duration in sorted(timings, key=lambda x: x[1], reverse=True):
            print(f"   {duration:6.2f}s - {script}")

    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
