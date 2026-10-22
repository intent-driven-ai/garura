#!/usr/bin/env python3
"""test_merge_plan.py — merge_pr.py lands an issue on its plan branch, and refuses a wrong target (#673).

The code host is replaced by a stand-in for platform_adapter.dispatch; git runs for real
in a scratch repo with a scratch remote.

    python3 test_merge_plan.py
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import merge_pr as mp  # noqa: E402

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


class Host:
    """Stands in for the code host: one PR, some issues."""
    def __init__(self, pr_base, states):
        self.pr_base, self.states, self.calls = pr_base, dict(states), []

    def dispatch(self, verb, args, config_path=None, platform=None):
        self.calls.append((verb, dict(args)))
        if verb == "view-pr":
            return {"exit_code": 0, "stdout": json.dumps({"number": 9, "baseRefName": self.pr_base}), "stderr": ""}
        if verb == "merge-pr":
            return {"exit_code": 0, "stdout": "", "stderr": ""}
        if verb == "close-issue":
            self.states[str(args["issue_number"])] = "CLOSED"
            return {"exit_code": 0, "stdout": "", "stderr": ""}
        if verb == "view-issue":
            return {"exit_code": 0, "stdout": json.dumps({"state": self.states.get(str(args["issue_number"]), "OPEN")}), "stderr": ""}
        return {"exit_code": 1, "stdout": "", "stderr": f"unexpected {verb}"}


def run(host, argv):
    mp.pa.dispatch = host.dispatch
    import resolve_target as rt
    rt_dispatch = getattr(rt, "pa", None)
    sys.modules.setdefault("platform_adapter", mp.pa)
    sys.modules["platform_adapter"].dispatch = host.dispatch
    try:
        mp.main(argv)
    except SystemExit as exc:
        return exc.code
    finally:
        if rt_dispatch is not None:
            rt.pa = rt_dispatch
    return 0


def main():
    with tempfile.TemporaryDirectory() as tmp:
        origin, work = os.path.join(tmp, "o.git"), os.path.join(tmp, "w")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin])
        subprocess.run(["git", "clone", "-q", origin, work], capture_output=True)
        git(work, "config", "user.email", "t@t"); git(work, "config", "user.name", "t")
        git(work, "checkout", "-q", "-b", "main")
        open(os.path.join(work, "a"), "w").write("a"); git(work, "add", "a"); git(work, "commit", "-q", "-m", "a")
        git(work, "push", "-q", "-u", "origin", "main")
        git(work, "push", "-q", "origin", "main:plan/717/base")
        git(work, "checkout", "-q", "-b", "plan/717/673-x")
        git(work, "push", "-q", "-u", "origin", "plan/717/673-x")
        plans = os.path.join(tmp, "plans"); os.makedirs(plans)
        yaml.safe_dump({"id": 717, "tree": [{"issue": 721, "kind": "capability", "children": [
            {"issue": 731, "kind": "functionality"}, {"issue": 673, "kind": "functionality"}]}]},
                       open(os.path.join(plans, "717.yaml"), "w"))
        gate = os.path.join(tmp, "gate.json")
        cwd = os.getcwd(); os.chdir(work)
        try:
            json.dump({"approved": True, "mergeable": True, "pr_number": 9}, open(gate, "w"))
            host = Host("main", {"731": "CLOSED"})
            code = run(host, ["--branch", "plan/717/673-x", "--base", "plan/717/base", "--gate", gate,
                              "--close-issue", "673", "--plans-dir", plans, "--plan-id", "717"])
            g = json.load(open(gate))
            check("a PR aimed at the wrong base is refused", code == 1 and g["status"] == "wrong_target")
            check("nothing is merged on a wrong target", not any(v == "merge-pr" for v, _ in host.calls))

            json.dump({"approved": True, "mergeable": True, "pr_number": 9}, open(gate, "w"))
            host = Host("plan/717/base", {"731": "CLOSED"})
            code = run(host, ["--branch", "plan/717/673-x", "--base", "plan/717/base", "--gate", gate,
                              "--close-issue", "673", "--plans-dir", plans, "--plan-id", "717"])
            g = json.load(open(gate))
            check("an issue in a plan merges into its plan branch", code == 0 and g["status"] == "merged" and g["on_target"])
            check("the checkout ends on the plan branch", git(work, "branch", "--show-current").stdout.strip() == "plan/717/base")
            check("the issue is closed, because the host will not close it off main", "673" in g["issues_closed"])
            check("its capability closes once every issue under it is closed", "721" in g["issues_closed"])
            check("the issue branch is gone both sides", g["branch_deleted"])
        finally:
            os.chdir(cwd)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
