#!/usr/bin/env python3
"""test_resolve_target.py — where a branch lands, and whether a plan may land on main (#673).

    python3 test_resolve_target.py
"""
import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import resolve_target as rt  # noqa: E402

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
    c = rt.classify("plan/717/673-plan-aware-merge")
    check("an issue in a plan lands on its plan branch", c["kind"] == "issue-in-plan" and c["base"] == "plan/717/base" and c["issue"] == "673")
    c = rt.classify("plan/717/base")
    check("a plan branch lands on main", c["kind"] == "plan" and c["base"] == "main" and c["plan_id"] == "717")
    c = rt.classify("feature/42-typo")
    check("a one-off lands on main", c["kind"] == "one-off" and c["base"] == "main" and c["issue"] == "42")

    with tempfile.TemporaryDirectory() as tmp:
        plans = os.path.join(tmp, "plans"); os.makedirs(plans)
        yaml.safe_dump({"id": 717, "tree": [
            {"issue": 721, "kind": "capability", "children": [{"issue": 731, "kind": "functionality"},
                                                              {"issue": 673, "kind": "functionality"}]}]},
                       open(os.path.join(plans, "717.yaml"), "w"))
        plan = rt.load_plan(plans, "717")
        check("work issues skip the capability", list(rt.work_issues(plan["tree"])) == ["731", "673"])
        check("issue states come from the given map", rt.tracker_state("673", None, {"673": "OPEN"}) == "OPEN")
        out = os.path.join(tmp, "target.json")
        check("the command runs for a plan branch", rt.main(["--branch", "plan/717/base", "--out", out]) == 0)
        rec = json.load(open(out))
        check("a plan in progress lands on main: no done check holds it",
              rec["base"] == "main" and rec["kind"] == "plan" and "plan_done" not in rec)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
