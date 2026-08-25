#!/usr/bin/env python3
"""Run the public tests and print a readable summary.

    python run_tests.py               # everything
    python run_tests.py -k astar      # only tests whose name contains "astar"
    python run_tests.py -x            # stop at the first failure

This runs the same test_search.py the autograder runs, so green here means
the public tests pass. The autograder also runs a hidden set on other pairs.
"""
import subprocess
import sys


def main():
    try:
        import pytest  # noqa: F401
    except ImportError:
        print("pytest is not installed. Activate the course environment:")
        print("    conda activate ai-search")
        return 1
    cmd = [sys.executable, "-B", "-m", "pytest", "test_search.py", "-v", "--tb=short"]
    return subprocess.call(cmd + sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
