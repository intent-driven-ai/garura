#!/usr/bin/env python3
"""
check_plan_absent.py — the pre-flight check that a business intent has no plan yet (#896, C14).

/shape-plan makes an intent's one plan, once. When the intent already has a plan file, the play
stops before anything else — before start-change, before it reads the model, before any write —
and points to /update-plan, which changes a plan that exists.

    python3 check_plan_absent.py --plans-dir <plans> --plan <intent-issue> [--repo .] [--main main] \
        [--out <record.json>]

The plan file is `<plans>/<id>.yaml`. It counts as there when it is in the checked-out tree, or on
the main branch (a plan's file is kept on main, and the person may be on another branch). The
record: {plan, path, exists, where: [checkout|main], message}. Exit 0 no plan (go on); 3 a plan
exists (stop, nothing written); 2 bad input. With no --out the record is printed only.
"""

import argparse
import json
import os
import re
import subprocess
import sys


def on_ref(path, ref, repo):
    res = subprocess.run(["git", "cat-file", "-e", f"{ref}:{path}"], cwd=repo, capture_output=True, text=True)
    return res.returncode == 0


def check(plans_dir, plan, repo=".", main="main"):
    if not re.fullmatch(r"\d+", str(plan or "")):
        raise ValueError(f"the plan's ID is the business intent's issue number, digits only (got {plan!r})")
    path = os.path.join(plans_dir, f"{plan}.yaml").replace(os.sep, "/")
    where = []
    if os.path.isfile(os.path.join(repo, path)):
        where.append("checkout")
    if on_ref(path, main, repo):
        where.append(main)
    rec = {"plan": str(plan), "path": path, "exists": bool(where), "where": where, "message": None}
    if where:
        rec["message"] = (f"Plan {plan} already exists for #{plan}. /shape-plan makes a plan once. "
                          f"To change it (add an epic, a story, a feature, or a status), run /update-plan {plan}.")
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description="stop /shape-plan when the intent already has a plan")
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--main", default="main")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        rec = check(args.plans_dir, args.plan, args.repo, args.main)
    except ValueError as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    text = json.dumps(rec, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 3 if rec["exists"] else 0


if __name__ == "__main__":
    sys.exit(main())
