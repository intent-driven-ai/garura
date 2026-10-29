#!/usr/bin/env python3
"""
resolve_target.py — where does this branch land? (#673)

The branch name says what the change is (start-change, #731):

  plan/<P>/<issue>-<slug>   an issue in plan P   → lands on plan/<P>/base
  plan/<P>/base             plan P itself        → lands on main, while the plan is still in
                                                   progress (a plan merges when it pauses)
  anything else             a one-off change     → lands on main

    python3 resolve_target.py --branch <branch> [--out <target.json>]

Prints { branch, kind, plan_id, issue, base }. Open work in a plan never holds its branch
off main: only the merge preconditions (approved, mergeable, required checks) guard main.
load_plan, work_issues and tracker_state are also used by merge_pr.py to close a
capability once every issue under it is closed. Exit 0. Read only: no git, no network.
"""
import argparse
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ISSUE_IN_PLAN = re.compile(r"^plan/(\d+)/(\d+)(?:-|$)")
PLAN_BASE = re.compile(r"^plan/(\d+)/base$")


def classify(branch):
    m = ISSUE_IN_PLAN.match(branch)
    if m:
        return {"branch": branch, "kind": "issue-in-plan", "plan_id": m.group(1),
                "issue": m.group(2), "base": f"plan/{m.group(1)}/base"}
    m = PLAN_BASE.match(branch)
    if m:
        return {"branch": branch, "kind": "plan", "plan_id": m.group(1), "issue": m.group(1),
                "base": "main"}
    m = re.search(r"/(\d+)(?:-|$)", branch)
    return {"branch": branch, "kind": "one-off", "plan_id": None,
            "issue": m.group(1) if m else None, "base": "main"}


def load_plan(plans_dir, pid):
    path = os.path.join(plans_dir, f"{pid}.yaml")
    with open(path, encoding="utf-8") as fh:
        plan = yaml.safe_load(fh)
    if not isinstance(plan, dict):
        raise ValueError(f"{path} is not a mapping")
    return plan


def work_issues(nodes):
    """Every issue in the tree that is not a capability (capabilities are closed by
    merge-change when all their children are)."""
    for node in nodes or []:
        if not isinstance(node, dict):
            continue
        if node.get("kind") != "capability" and node.get("issue") is not None:
            yield str(node["issue"])
        yield from work_issues(node.get("children"))


def tracker_state(issue, config, states):
    if states is not None:
        return states.get(str(issue), "OPEN")
    import platform_adapter as pa
    res = pa.dispatch("view-issue", {"issue_number": issue, "_tree": False}, config_path=config)
    if res["exit_code"] != 0:
        return "UNKNOWN"
    try:
        return json.loads(res["stdout"]).get("state", "UNKNOWN")
    except ValueError:
        return "UNKNOWN"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", required=True)
    ap.add_argument("--out")
    ns = ap.parse_args(argv)
    record = classify(ns.branch)
    out = json.dumps(record, indent=2)
    print(out)
    if ns.out:
        with open(ns.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
