#!/usr/bin/env python3
"""test_resolve_target.py — where a branch lands, and whether a plan may land on main (#673).

    python3 test_resolve_target.py
"""
import json
import os
import subprocess
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


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def main():
    c = rt.classify("plan/717/673-plan-aware-merge")
    check("an issue in a plan lands on its plan branch", c["kind"] == "issue-in-plan" and c["base"] == "plan/717/base" and c["issue"] == "673")
    c = rt.classify("plan/717/base")
    check("a plan branch lands on main", c["kind"] == "plan" and c["base"] == "main" and c["plan_id"] == "717")
    c = rt.classify("feature/42-typo")
    check("a one-off lands on main", c["kind"] == "one-off" and c["base"] == "main" and c["issue"] == "42")

    with tempfile.TemporaryDirectory() as tmp:
        origin, work = os.path.join(tmp, "o.git"), os.path.join(tmp, "w")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin])
        subprocess.run(["git", "clone", "-q", origin, work], capture_output=True)
        git(work, "config", "user.email", "t@t"); git(work, "config", "user.name", "t")
        git(work, "checkout", "-q", "-b", "main")
        open(os.path.join(work, "a"), "w").write("a"); git(work, "add", "a"); git(work, "commit", "-q", "-m", "a")
        git(work, "push", "-q", "-u", "origin", "main")
        for b in ("plan/722/base", "plan/717/base"):
            git(work, "push", "-q", "origin", f"main:{b}")
        open(os.path.join(work, "b"), "w").write("b"); git(work, "add", "b"); git(work, "commit", "-q", "-m", "b")
        git(work, "push", "-q", "origin", "HEAD:plan/722/base")
        git(work, "fetch", "-q")
        plans = os.path.join(tmp, "plans"); os.makedirs(plans)
        yaml.safe_dump({"id": 717, "needs_plans": [722], "tree": [
            {"issue": 721, "kind": "capability", "children": [{"issue": 731, "kind": "functionality"},
                                                              {"issue": 673, "kind": "functionality"}]}]},
                       open(os.path.join(plans, "717.yaml"), "w"))
        yaml.safe_dump({"id": 722, "tree": [{"issue": 723, "kind": "capability",
                                              "children": [{"issue": 724, "kind": "functionality"}]}]},
                       open(os.path.join(plans, "722.yaml"), "w"))
        cwd = os.getcwd(); os.chdir(work)
        try:
            r = rt.check_done(plans, "717", None, {"731": "CLOSED", "673": "OPEN", "724": "CLOSED"})
            check("an open issue keeps the plan off main", not r["plan_done"] and r["open_issues"] == ["673"])
            check("a capability's own issue does not hold the plan", "721" not in r["open_issues"])
            r = rt.check_done(plans, "717", None, {"731": "CLOSED", "673": "CLOSED", "724": "OPEN"})
            check("a needed plan that is not done holds the plan", not r["plan_done"] and "plan 722 is not done" in r["needs_unmet"][0])
            r = rt.check_done(plans, "717", None, {"731": "CLOSED", "673": "CLOSED", "724": "CLOSED"})
            check("a needed plan that is done but not landed holds the plan", not r["plan_done"] and "has not landed" in r["needs_unmet"][0])
            git(work, "push", "-q", "origin", "origin/plan/722/base:refs/heads/plan/717/base", "--force")
            git(work, "fetch", "-q")
            r = rt.check_done(plans, "717", None, {"731": "CLOSED", "673": "CLOSED", "724": "CLOSED"})
            check("needed plan merged into this plan's branch: the plan may land", r["plan_done"])
            states = os.path.join(tmp, "s.json"); json.dump({"731": "CLOSED", "673": "OPEN"}, open(states, "w"))
            check("the command runs for a plan branch", rt.main(["--branch", "plan/717/base", "--plans-dir", plans, "--check-done", "--states", states]) == 0)
            check("a missing plan file exits 2", rt.main(["--branch", "plan/999/base", "--plans-dir", plans, "--check-done", "--states", states]) == 2)
        finally:
            os.chdir(cwd)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
