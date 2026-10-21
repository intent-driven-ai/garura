#!/usr/bin/env python3
"""
resolve_target.py — where does this branch land, and may it land yet? (#673)

The branch name says what the change is (start-change, #731):

  plan/<P>/<issue>-<slug>   an issue in plan P   → lands on plan/<P>/base
  plan/<P>/base             plan P itself        → lands on main, only when P is done
  anything else             a one-off change     → lands on main

    python3 resolve_target.py --branch <branch> [--plans-dir .garura/project/plans/] \
        [--check-done] [--config .garura/core/config.yaml] [--states <states.json>] \
        [--out <target.json>]

Prints { branch, kind, plan_id, issue, base }. With --check-done, for kind "plan", it
also reads the plan file and the tracker and adds { plan_done, open_issues, needs_unmet }:

- every issue in the plan that is not a capability is closed (an issue in a plan is
  closed when it lands on its plan branch — merge-change does that, because the code
  host closes issues only on main);
- every plan this one needs (`needs_plans`) is done the same way, and its branch has
  landed on main or been merged into this plan's branch.

Issue states come from the tracker through platform_adapter.py, or from --states (a
JSON map of issue number to OPEN/CLOSED, for tests). Exit 0 always on a read; 2 when a
plan file is missing or cannot be read. The play applies the halt policy.
"""
import argparse
import json
import os
import re
import subprocess
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


def is_ancestor(a, b):
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b],
                          capture_output=True).returncode == 0


def plan_open_issues(plans_dir, pid, config, states):
    plan = load_plan(plans_dir, pid)
    return plan, [i for i in work_issues(plan.get("tree"))
                  if tracker_state(i, config, states) != "CLOSED"]


def check_done(plans_dir, pid, config, states):
    plan, open_issues = plan_open_issues(plans_dir, pid, config, states)
    needs_unmet = []
    for q in plan.get("needs_plans") or []:
        q = str(q)
        _, q_open = plan_open_issues(plans_dir, q, config, states)
        landed = (is_ancestor(f"origin/plan/{q}/base", "origin/main") or
                  is_ancestor(f"origin/plan/{q}/base", f"origin/plan/{pid}/base"))
        if q_open:
            needs_unmet.append(f"plan {q} is not done (open: {', '.join('#' + i for i in q_open)})")
        elif not landed:
            needs_unmet.append(f"plan {q} has not landed on main or been merged into plan/{pid}/base")
    return {"plan_done": not open_issues and not needs_unmet,
            "open_issues": open_issues, "needs_unmet": needs_unmet}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", required=True)
    ap.add_argument("--plans-dir", default=".garura/project/plans/")
    ap.add_argument("--check-done", action="store_true")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--states")
    ap.add_argument("--out")
    ns = ap.parse_args(argv)
    record = classify(ns.branch)
    if ns.check_done and record["kind"] == "plan":
        try:
            states = json.load(open(ns.states)) if ns.states else None
            record.update(check_done(ns.plans_dir, record["plan_id"], ns.config, states))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            record["error"] = str(exc)
            print(json.dumps(record, indent=2))
            return 2
    out = json.dumps(record, indent=2)
    print(out)
    if ns.out:
        with open(ns.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
