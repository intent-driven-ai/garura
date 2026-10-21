#!/usr/bin/env python3
"""test_resolve_plan.py — fixture tests for resolve_plan.py and the branch-name issue reader (#731).

    python3 test_resolve_plan.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import preflight  # noqa: E402
import resolve_plan as rp  # noqa: E402

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


def write(d, name, plan):
    with open(os.path.join(d, name), "w") as fh:
        yaml.safe_dump(plan, fh)


def main():
    with tempfile.TemporaryDirectory() as d:
        write(d, "717.yaml", {"id": 717, "tree": [
            {"issue": 721, "children": [{"issue": 731}, {"issue": 673}]},
            {"issue": 718, "children": [{"issue": 727}]}]})
        write(d, "722.yaml", {"id": 722, "tree": [{"issue": 723, "children": [{"issue": 724}]}]})
        r = rp.resolve(d, 731, "plan-branches")
        check("an issue in a plan gets a sub-branch of its plan",
              r["plan_branch"] == "plan/717/base" and r["issue_branch"] == "plan/717/731-plan-branches")
        check("a capability in a plan is found too", rp.resolve(d, 721, "x")["plan_id"] == "717")
        check("the business intent itself belongs to its own plan", rp.resolve(d, 722, "x")["plan_id"] == "722")
        r = rp.resolve(d, 999, "one-off")
        check("an issue in no plan gets feature/<issue>-<slug> from main",
              r["plan_id"] is None and r["issue_branch"] == "feature/999-one-off")
        write(d, "800.yaml", {"id": 800, "tree": [{"issue": 731}]})
        check("an issue in two plans is an error, not a guess", rp.main(["--plans-dir", d, "--issue", "731", "--slug", "x"]) == 2)
        os.remove(os.path.join(d, "800.yaml"))
        check("the command exits 0 for a found issue", rp.main(["--plans-dir", d, "--issue", "724", "--slug", "x"]) == 0)
    with tempfile.TemporaryDirectory() as d:
        check("an empty plans folder means no plan", rp.resolve(d, 5, "x")["plan_id"] is None)
    cfg = {}
    for branch, want in (("feature/731-plan-branches", "731"), ("plan/717/731-plan-branches", "731"),
                         ("plan/717/base", None), ("fix/42-typo", "42"), ("main", None)):
        got = preflight.resolve(cfg, "start-change", branch, "")["issue"]
        check(f"pre-flight reads issue {want} from {branch}", got == want)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
