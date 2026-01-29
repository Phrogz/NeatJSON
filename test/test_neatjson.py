#!/usr/bin/env python3
"""
Test runner for NeatJSON Python port.

Matches the structure and output of test_neatjson.rb.

Usage:
    python test/test_neatjson.py         # Run all tests
    python test/test_neatjson.py -p      # Run with performance testing
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Any

# Add the python src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "src"))

from neatjson import neat_json

from tests import TESTS, PYTHON_TESTS, CUSTOM_JSON_TESTS


def run_tests() -> None:
    """Run all test cases and report results."""
    passed = 0
    count = 0
    perf_testing = len(sys.argv) > 1 and sys.argv[1] in ("-p", "--perftest")

    # Load large.json for performance testing
    large_data: Any = None
    if perf_testing:
        large_path = Path(__file__).parent / "large.json"
        if large_path.exists():
            with open(large_path) as f:
                large_data = json.load(f)

    start = time.perf_counter()

    # Run all test suites
    all_tests = TESTS + PYTHON_TESTS + CUSTOM_JSON_TESTS

    for value_tests in all_tests:
        val = value_tests["value"]
        tests = value_tests["tests"]

        for test in tests:
            opts = test.get("opts", {})
            expected = test["json"]

            # Build command description for error reporting
            opts_str = ", ".join(f"{k}={v!r}" for k, v in opts.items())
            cmd = f"neat_json({val!r}, {opts_str})" if opts else f"neat_json({val!r})"

            try:
                result = neat_json(val, **opts)

                # Check result against expected (string or regex)
                if isinstance(expected, re.Pattern):
                    if not expected.search(result):
                        raise AssertionError(
                            f"EXPECTED (regex):\n{expected.pattern}\nACTUAL:\n{result}"
                        )
                else:
                    if result != expected:
                        raise AssertionError(
                            f"EXPECTED:\n{expected}\nACTUAL:\n{result}"
                        )

                passed += 1

            except Exception as e:
                print(f"Failure running {cmd}")
                print(e)
                print()

            count += 1

            # Performance testing with large data
            if perf_testing and large_data is not None:
                try:
                    neat_json(large_data, **opts)
                except Exception:
                    print(f"Error serializing large data with {opts!r}")

    elapsed = time.perf_counter() - start
    elapsed = max(elapsed, 0.0001)  # Avoid division by zero

    tests_word = "test" if count == 1 else "tests"
    print(
        f"{passed}/{count} {tests_word} passed in {elapsed * 1000:.2f}ms "
        f"({int(count / elapsed)} tests per second)"
    )

    # Exit with error code if any tests failed
    sys.exit(0 if passed == count else 1)


if __name__ == "__main__":
    run_tests()
