#!/usr/bin/env python3
"""
resolve_plan.py — which plan does this issue belong to, and what are its branches? (#731, #779)

A plan's file is `<plans-dir>/<plan-id>.yaml` (ontology v5, Plan): its ID is its business
intent's issue number, and its `tree` lists every capability and functionality under it,
each with its `issue`. This script finds the plan whose tree holds the issue (or whose ID is
the issue) and names the branches:

  plan branch   plan/<plan-id>/base
  issue branch  plan/<plan-id>/<issue>-<slug>      (an issue in a plan)
                feature/<issue>-<slug>             (an issue in no plan — a one-off fix)

    python3 resolve_plan.py --plans-dir .garura/project/plans/ --issue N --slug <slug> \
        [--repo .] [--ref origin/main] [--local] [--out <path.json>]

The plan files are read from git, never from the checked-out branch (#779): the script fetches
origin, then reads each plan file at `--ref` (the latest main). When the plan's own branch
(`plan/<plan-id>/base`) is on origin, its copy of the plan file is read too, because a plan
session writes there first; an issue in either copy belongs to the plan. When the fetch fails,
the last fetched copies are read and the record says so (`fetched: false`); the fetch never
prompts and gives up after a time limit. `--plans-dir` may be absolute or relative to the folder
the script runs in; a folder outside the repository is an error. `--local` reads the
folder on disk instead (a plans folder outside git, and the tests).

Prints { issue, plan_id, plan_branch, issue_branch, source }; plan_id and plan_branch are null
for an issue in no plan. An issue in a plan that main marks Done or Dropped (a bug found after
the plan closed) is an issue in no plan: it gets `feature/<issue>-<slug>` off main, and the record
names the plan in `closed_plan` (#989) — a closed plan's branch is never cut. `source` names the
ref read, whether the fetch worked, and each plan branch read. Exit 0 found or not found, 2 when a plan file cannot be read, when `--ref` does
not exist, or when the issue sits in more than one plan. No network beyond the fetch, no LLM.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

import yaml


def issues_in(nodes):
    for node in nodes or []:
        if isinstance(node, dict):
            if node.get("issue") is not None:
                yield str(node["issue"])
            yield from issues_in(node.get("children"))


TIME_LIMIT = 120  # seconds for the fetch; a stalled server reads as a failed fetch, never a hang


def _git(repo, *args):
    try:
        p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=TIME_LIMIT,
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except subprocess.TimeoutExpired:
        return 124, ""
    return p.returncode, p.stdout


def repo_folder(repo, plans_dir):
    """(the repository's root, the plans folder as a path from it), however the folder was given
    (absolute, or relative to the folder the script runs in). A folder outside it is refused."""
    rc, top = _git(repo, "rev-parse", "--show-toplevel")
    if rc != 0:
        raise ValueError(f"{repo} is not inside a git repository")
    top = os.path.realpath(top.strip())
    path = plans_dir if os.path.isabs(plans_dir) else os.path.join(os.path.abspath(repo), plans_dir)
    rel = os.path.relpath(os.path.realpath(path), top).replace(os.sep, "/")
    if rel == ".." or rel.startswith("../"):
        raise ValueError(f"{plans_dir} is outside the repository")
    return top, ("" if rel == "." else rel)


def _read_plan(text, where):
    plan = yaml.safe_load(text) or {}
    if not isinstance(plan, dict):
        raise ValueError(f"{where} is not a mapping")
    return plan


def plans_on_disk(plans_dir):
    """{file name: plan} for the plan files in a folder on disk."""
    out = {}
    for path in sorted(glob.glob(os.path.join(plans_dir, "*.yaml"))):
        name = os.path.basename(path)
        if name != "index.yaml":
            with open(path, encoding="utf-8") as fh:
                out[name] = _read_plan(fh.read(), path)
    return out


def plans_at(repo, ref, plans_dir):
    """{file name: plan} for the plan files at a git ref; None when the ref does not exist."""
    if _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")[0] != 0:
        return None
    folder = plans_dir
    rc, listing = _git(repo, "ls-tree", "--name-only", f"{ref}:{folder}")
    out = {}
    for name in sorted(listing.split()) if rc == 0 else []:
        if name.endswith(".yaml") and name != "index.yaml":
            rc, text = _git(repo, "show", f"{ref}:{folder}/{name}")
            if rc != 0:
                raise ValueError(f"cannot read {folder}/{name} at {ref}")
            out[name] = _read_plan(text, f"{ref}:{folder}/{name}")
    return out


def holds(plan, name, issue):
    pid = str(plan.get("id", os.path.splitext(name)[0]))
    return pid, issue == pid or issue in set(issues_in(plan.get("tree")))


CLOSED = ("Done", "Dropped")


def resolve(plans, issue, slug, branch_plans=None):
    """plans: {file name: plan} as main has them; branch_plans: {file name: plan} from each
    plan's own branch, read where it exists. An issue in either copy belongs to the plan."""
    issue = str(issue)
    found = []
    for name, plan in plans.items():
        pid, here = holds(plan, name, issue)
        if not here and name in (branch_plans or {}):
            here = holds(branch_plans[name], name, issue)[1]
        if here:
            found.append(pid)
    if len(found) > 1:
        raise ValueError(f"issue {issue} sits in more than one plan: {', '.join(found)}")
    pid = found[0] if found else None
    status = next((p.get("status") for n, p in plans.items() if holds(p, n, issue)[0] == pid), None)
    if pid and status not in CLOSED:
        return {"issue": issue, "plan_id": pid, "plan_branch": f"plan/{pid}/base",
                "issue_branch": f"plan/{pid}/{issue}-{slug}", "closed_plan": None}
    return {"issue": issue, "plan_id": None, "plan_branch": None,
            "issue_branch": f"feature/{issue}-{slug}", "closed_plan": pid}


def resolve_from_git(repo, plans_dir, issue, slug, ref="origin/main"):
    remote = ref.split("/", 1)[0] if "/" in ref else "origin"
    repo, plans_dir = repo_folder(repo, plans_dir)   # git reads from the root: ls-tree in a sub-folder lists only it
    fetched = _git(repo, "fetch", "--quiet", remote)[0] == 0
    plans = plans_at(repo, ref, plans_dir)
    if plans is None:
        raise ValueError(f"{ref} does not exist here; fetch it, then run again")
    branch_plans, read = {}, []
    for name, plan in plans.items():
        pid = str(plan.get("id", os.path.splitext(name)[0]))
        copy = plans_at(repo, f"{remote}/plan/{pid}/base", plans_dir)
        if copy is not None and name in copy:
            branch_plans[name] = copy[name]
            read.append(f"plan/{pid}/base")
    record = resolve(plans, issue, slug, branch_plans)
    record["source"] = {"ref": ref, "fetched": fetched, "plan_branches_read": read}
    return record


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--local", action="store_true", help="read the folder on disk, not git")
    ap.add_argument("--out")
    ns = ap.parse_args(argv)
    try:
        if ns.local:
            record = resolve(plans_on_disk(ns.plans_dir), ns.issue, ns.slug)
            record["source"] = {"ref": None, "fetched": None, "plan_branches_read": []}
        else:
            record = resolve_from_git(ns.repo, ns.plans_dir, ns.issue, ns.slug, ns.ref)
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
