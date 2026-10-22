#!/usr/bin/env python3
"""
resolve_plan.py — which plan does this issue belong to, and what are its branches? (#731)

A plan's file is `<plans-dir>/<plan-id>.yaml` (ontology v5, Plan): its ID is its business
intent's issue number, and its `tree` lists every capability and functionality under it,
each with its `issue`. This script finds the plan whose tree holds the issue (or whose ID is
the issue) and names the branches:

  plan branch   plan/<plan-id>/base
  issue branch  plan/<plan-id>/<issue>-<slug>      (an issue in a plan)
                feature/<issue>-<slug>             (an issue in no plan — a one-off fix)

    python3 resolve_plan.py --plans-dir .garura/project/plans/ --issue N --slug <slug> \
        [--out <path.json>]

Prints { issue, plan_id, plan_branch, issue_branch }; plan_id and plan_branch are null for
an issue in no plan. Exit 0 found or not found, 2 when a plan file cannot be read, or when
the issue sits in more than one plan. Read only: no git, no network, no LLM.
"""
import argparse
import glob
import json
import os
import sys

import yaml


def issues_in(nodes):
    for node in nodes or []:
        if isinstance(node, dict):
            if node.get("issue") is not None:
                yield str(node["issue"])
            yield from issues_in(node.get("children"))


def resolve(plans_dir, issue, slug):
    issue = str(issue)
    found = []
    for path in sorted(glob.glob(os.path.join(plans_dir, "*.yaml"))):
        if os.path.basename(path) == "index.yaml":
            continue
        with open(path, encoding="utf-8") as fh:
            plan = yaml.safe_load(fh) or {}
        if not isinstance(plan, dict):
            raise ValueError(f"{path} is not a mapping")
        pid = str(plan.get("id", os.path.splitext(os.path.basename(path))[0]))
        if issue == pid or issue in set(issues_in(plan.get("tree"))):
            found.append(pid)
    if len(found) > 1:
        raise ValueError(f"issue {issue} sits in more than one plan: {', '.join(found)}")
    pid = found[0] if found else None
    if pid:
        return {"issue": issue, "plan_id": pid, "plan_branch": f"plan/{pid}/base",
                "issue_branch": f"plan/{pid}/{issue}-{slug}"}
    return {"issue": issue, "plan_id": None, "plan_branch": None,
            "issue_branch": f"feature/{issue}-{slug}"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out")
    ns = ap.parse_args(argv)
    try:
        record = resolve(ns.plans_dir, ns.issue, ns.slug)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    out = json.dumps(record, indent=2)
    print(out)
    if ns.out:
        with open(ns.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
