#!/usr/bin/env python3
"""Comprehensive script validation utility.

This utility runs all scripts in the scripts/ directory and provides
comprehensive validation and reporting of their functionality.
"""
from __future__ import annotations
import subprocess
import sys
import time
import os
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple


class ScriptResult(NamedTuple):
    """Result of running a script."""
    name: str
    success: bool
    duration: float
    stdout: str
    stderr: str
    exit_code: int


def discover_scripts(scripts_dir: Path) -> List[str]:
    """Discover all Python scripts in the scripts directory."""
    scripts = []
    for script in scripts_dir.glob("*.py"):
        if script.name != "__init__.py" and script.name != "validate_all_scripts.py":
            scripts.append(script.name)
    return sorted(scripts)


def run_script(script_path: Path, timeout: int = 60) -> ScriptResult:
    """Run a single script and capture its results."""
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent.parent,  # Run from repo root
            capture_output=True,
            text=True,
            timeout=timeout
        )
        end_time = time.time()
        duration = end_time - start_time
        
        return ScriptResult(
            name=script_path.name,
            success=result.returncode == 0,
            duration=duration,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode
        )
        
    except subprocess.TimeoutExpired:
        end_time = time.time()
        duration = end_time - start_time
        return ScriptResult(
            name=script_path.name,
            success=False,
            duration=duration,
            stdout="",
            stderr=f"Script timed out after {timeout}s",
            exit_code=-1
        )
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        return ScriptResult(
            name=script_path.name,
            success=False,
            duration=duration,
            stdout="",
            stderr=str(e),
            exit_code=-2
        )


def validate_outputs(repo_root: Path) -> Dict[str, List[str]]:
    """Validate that expected outputs exist after running scripts."""
    output_dir = repo_root / "output"
    figures_dir = output_dir / "figures"
    data_dir = output_dir / "data"
    
    validation_results = {
        "missing_figures": [],
        "missing_data": [],
        "missing_captions": [],
        "empty_files": []
    }
    
    # Expected core research figures
    expected_figures = [
        "atmospheric_transmission.png",
        "sensilla_wavelength_matching.png", 
        "chc_spectra_example.png",
        "response_time_comparison.png",
        "composite_cross_domain_overview.png"
    ]
    
    # Expected case study figures
    expected_case_study_figures = [
        "sensilla_array_beam_patterns.png",
        "environmental_channel_capacity.png",
        "detection_limits_operating_points.png",
        "neural_encoding_information_rate.png",
        "spectral_unmixing_components.png",
        "plasmonic_geometry_sweep.png",
        "active_inference_trajectory.png"
    ]
    
    # Expected integrated analysis figures
    expected_integrated_figures = [
        "integrated_analysis_information_analysis.png",
        "integrated_analysis_metamaterial_properties.png",
        "integrated_analysis_system_performance.png",
        "integrated_analysis_cross_domain_synthesis.png"
    ]
    
    all_expected_figures = expected_figures + expected_case_study_figures + expected_integrated_figures
    
    # Check figures
    for fig in all_expected_figures:
        path = figures_dir / fig
        if not path.exists():
            validation_results["missing_figures"].append(fig)
        elif path.stat().st_size == 0:
            validation_results["empty_files"].append(f"Figure: {fig}")
            
        # Check corresponding caption
        caption_path = figures_dir / f"{fig.rsplit('.', 1)[0]}.caption.txt"
        if not caption_path.exists():
            validation_results["missing_captions"].append(f"{fig.rsplit('.', 1)[0]}.caption.txt")
    
    # Check data files
    expected_data_files = [
        "atmospheric_transmission.npz",
        "sensilla_data.npz",
        "sensilla_array.npz",
        "environmental_channel.npz",
        "detection_limits.npz",
        "neural_encoding.npz",
        "spectral_unmixing.npz",
        "plasmonic_geometry.npz",
        "active_inference_demo.npz",
        "integrated_analysis.npz"
    ]
    
    for data_file in expected_data_files:
        path = data_dir / data_file
        if not path.exists():
            validation_results["missing_data"].append(data_file)
        elif path.stat().st_size == 0:
            validation_results["empty_files"].append(f"Data: {data_file}")
    
    return validation_results


def generate_report(results: List[ScriptResult], validation: Dict[str, List[str]], 
                   total_duration: float) -> str:
    """Generate a comprehensive validation report."""
    report = []
    report.append("=" * 80)
    report.append("COMPREHENSIVE SCRIPT VALIDATION REPORT")
    report.append("=" * 80)
    report.append(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total execution time: {total_duration:.2f}s")
    report.append("")
    
    # Summary statistics
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    
    report.append("EXECUTION SUMMARY:")
    report.append(f"  📊 Total scripts tested: {len(results)}")
    report.append(f"  ✅ Successful: {successful}")
    report.append(f"  ❌ Failed: {failed}")
    report.append(f"  📈 Success rate: {successful/len(results)*100:.1f}%")
    report.append("")
    
    # Individual script results
    report.append("INDIVIDUAL SCRIPT RESULTS:")
    report.append("-" * 40)
    
    # Sort by success first, then by duration
    sorted_results = sorted(results, key=lambda x: (not x.success, x.duration))
    
    for result in sorted_results:
        status = "✅ PASS" if result.success else "❌ FAIL"
        report.append(f"{status:8} {result.duration:6.2f}s  {result.name}")
        if not result.success:
            # Add error details for failed scripts
            if result.stderr:
                report.append(f"         Error: {result.stderr[:100]}...")
    report.append("")
    
    # Timing analysis
    report.append("PERFORMANCE ANALYSIS:")
    report.append("-" * 40)
    fastest = min(results, key=lambda x: x.duration)
    slowest = max(results, key=lambda x: x.duration)
    avg_time = sum(r.duration for r in results) / len(results)
    
    report.append(f"  ⚡ Fastest: {fastest.name} ({fastest.duration:.2f}s)")
    report.append(f"  🐌 Slowest: {slowest.name} ({slowest.duration:.2f}s)")
    report.append(f"  📊 Average: {avg_time:.2f}s")
    report.append("")
    
    # Output validation
    report.append("OUTPUT VALIDATION:")
    report.append("-" * 40)
    
    total_issues = sum(len(issues) for issues in validation.values())
    if total_issues == 0:
        report.append("  ✅ All expected outputs generated successfully!")
    else:
        report.append(f"  ⚠️  Found {total_issues} output issues:")
        for category, issues in validation.items():
            if issues:
                report.append(f"    {category.replace('_', ' ').title()}: {len(issues)}")
                for issue in issues[:5]:  # Show first 5 issues per category
                    report.append(f"      - {issue}")
                if len(issues) > 5:
                    report.append(f"      ... and {len(issues) - 5} more")
    report.append("")
    
    # Recommendations
    if failed > 0 or total_issues > 0:
        report.append("RECOMMENDATIONS:")
        report.append("-" * 40)
        if failed > 0:
            report.append("  🔧 Fix failing scripts before deployment")
        if validation["missing_figures"]:
            report.append("  🖼️  Investigate missing figure generation")
        if validation["missing_data"]:
            report.append("  💾 Check data file generation logic")
        if validation["empty_files"]:
            report.append("  📝 Verify empty file generation issues")
        report.append("")
    
    report.append("=" * 80)
    
    return "\n".join(report)


def main() -> int:
    """Run comprehensive script validation."""
    print("🚀 Starting comprehensive script validation...")
    
    repo_root = Path(__file__).resolve().parent.parent
    scripts_dir = repo_root / "scripts"
    
    # Discover all scripts
    scripts = discover_scripts(scripts_dir)
    print(f"📋 Found {len(scripts)} scripts to validate")
    
    # Run all scripts
    results = []
    total_start_time = time.time()
    
    for i, script_name in enumerate(scripts, 1):
        print(f"[{i:2}/{len(scripts)}] Running {script_name}...", end="", flush=True)
        
        script_path = scripts_dir / script_name
        result = run_script(script_path)
        results.append(result)
        
        status = "✅" if result.success else "❌"
        print(f" {status} ({result.duration:.2f}s)")
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Validate outputs
    print("\n🔍 Validating generated outputs...")
    validation_results = validate_outputs(repo_root)
    
    # Generate and save report
    report = generate_report(results, validation_results, total_duration)
    
    # Save report to file
    report_path = repo_root / "output" / "script_validation_report.txt"
    os.makedirs(report_path.parent, exist_ok=True)
    with open(report_path, "w") as f:
        f.write(report)
    
    # Print report
    print("\n" + report)
    print(f"\n📄 Full report saved to: {report_path}")
    
    # Return appropriate exit code
    failed_scripts = sum(1 for r in results if not r.success)
    total_issues = sum(len(issues) for issues in validation_results.values())
    
    if failed_scripts == 0 and total_issues == 0:
        print("\n🎉 All scripts passed validation!")
        return 0
    else:
        print(f"\n⚠️  Validation completed with issues (scripts: {failed_scripts}, outputs: {total_issues})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
