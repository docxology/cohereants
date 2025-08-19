#!/usr/bin/env python3
"""Test runner script for cohereAnts project.

This script provides an easy way to run tests with various options
including coverage reporting, test selection, and output formatting.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_tests_with_coverage(verbose: bool = False, 
                           html_report: bool = False,
                           xml_report: bool = False,
                           fail_under: int = 100) -> int:
    """Run tests with coverage reporting.
    
    Args:
        verbose: Whether to run tests in verbose mode
        html_report: Whether to generate HTML coverage report
        xml_report: Whether to generate XML coverage report
        fail_under: Minimum coverage percentage required
        
    Returns:
        Exit code from pytest
    """
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=src",
        "--cov-report=term-missing",
        f"--cov-fail-under={fail_under}"
    ]
    
    if html_report:
        cmd.append("--cov-report=html:htmlcov")
    
    if xml_report:
        cmd.append("--cov-report=xml")
    
    if verbose:
        cmd.append("--verbose")
    
    print(f"Running tests with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    return result.returncode


def run_specific_test(test_path: str, verbose: bool = False) -> int:
    """Run a specific test file or test function.
    
    Args:
        test_path: Path to test file or specific test function
        verbose: Whether to run tests in verbose mode
        
    Returns:
        Exit code from pytest
    """
    cmd = [sys.executable, "-m", "pytest", test_path]
    
    if verbose:
        cmd.append("--verbose")
    
    print(f"Running specific test: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    return result.returncode


def run_tests_by_marker(marker: str, verbose: bool = False) -> int:
    """Run tests by marker (e.g., 'unit', 'integration', 'slow').
    
    Args:
        marker: Test marker to run
        verbose: Whether to run tests in verbose mode
        
    Returns:
        Exit code from pytest
    """
    cmd = [sys.executable, "-m", "pytest", f"-m {marker}"]
    
    if verbose:
        cmd.append("--verbose")
    
    print(f"Running tests with marker '{marker}': {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    return result.returncode


def list_available_tests() -> None:
    """List all available tests in the project."""
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    
    print("Available tests:")
    print("=" * 50)
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent, 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Parse and format the output
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip() and not line.startswith('='):
                print(f"  {line.strip()}")
    else:
        print("Error collecting tests")
        print(result.stderr)


def show_test_coverage() -> None:
    """Show current test coverage without running tests."""
    cmd = [sys.executable, "-m", "pytest", "--cov=src", "--cov-report=term-missing", "--collect-only"]
    
    print("Current test coverage:")
    print("=" * 50)
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent, 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extract coverage information
        lines = result.stdout.strip().split('\n')
        coverage_lines = [line for line in lines if 'coverage:' in line.lower()]
        
        if coverage_lines:
            for line in coverage_lines:
                print(line.strip())
        else:
            print("No coverage information available")
    else:
        print("Error getting coverage information")
        print(result.stderr)


def main():
    """Main function for the test runner."""
    parser = argparse.ArgumentParser(
        description="Test runner for cohereAnts project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests with coverage
  python run_tests.py --verbose         # Run tests in verbose mode
  python run_tests.py --html           # Generate HTML coverage report
  python run_tests.py --test tests/test_insect_analysis.py  # Run specific test file
  python run_tests.py --marker unit    # Run only unit tests
  python run_tests.py --list           # List all available tests
  python run_tests.py --coverage       # Show current coverage
        """
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run tests in verbose mode"
    )
    
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML coverage report"
    )
    
    parser.add_argument(
        "--xml",
        action="store_true",
        help="Generate XML coverage report"
    )
    
    parser.add_argument(
        "--fail-under",
        type=int,
        default=100,
        help="Minimum coverage percentage required (default: 100)"
    )
    
    parser.add_argument(
        "--test",
        help="Run a specific test file or test function"
    )
    
    parser.add_argument(
        "--marker",
        help="Run tests with specific marker (e.g., 'unit', 'integration', 'slow')"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available tests"
    )
    
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Show current test coverage without running tests"
    )
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    try:
        if args.list:
            list_available_tests()
            return 0
        
        if args.coverage:
            show_test_coverage()
            return 0
        
        if args.test:
            return run_specific_test(args.test, args.verbose)
        
        if args.marker:
            return run_tests_by_marker(args.marker, args.verbose)
        
        # Default: run all tests with coverage
        return run_tests_with_coverage(
            verbose=args.verbose,
            html_report=args.html,
            xml_report=args.xml,
            fail_under=args.fail_under
        )
        
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        return 130
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
