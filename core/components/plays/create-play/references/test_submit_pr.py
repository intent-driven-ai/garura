#!/usr/bin/env python3
"""test_submit_pr.py — the PR's "points where its branch lands" check (#673, #951).

    python3 test_submit_pr.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import submit_pr  # noqa: E402

PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def main():
    check("a PR the host shows on the asked base is on target",
          submit_pr.on_target({"number": 9, "base": "plan/717/base"}, "plan/717/base") is True)
    check("a PR the host shows on another base is not on target",
          submit_pr.on_target({"number": 9, "base": "main"}, "plan/717/base") is False)
    check("a PR whose number could not be looked up is unknown, not on target by default",
          submit_pr.on_target({"number": None, "base": "plan/717/base"}, "plan/717/base") is None)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
