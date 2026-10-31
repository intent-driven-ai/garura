#!/usr/bin/env python3
"""
check_plan_start.py — prove a plan's start (#989): `/start-change plan <id>`.

Reads the plan tool's record (`plan_branch.py go`) and git, and writes what holds:

  on_plan_branch   the session is on plan/<id>/base, and the branch is on origin
  main_agrees      when the branch was cut: it equals the main commit it was cut from, that
                   commit is on origin/main, and main's plan file there reads `status: In
                   Progress` and `branch: plan/<id>/base`; when it stayed or switched: true
  no_story_branch  no branch plan/<id>/<anything but base> was made by this run
  ok               all three

    python3 check_plan_start.py --save-branches <branches-before.txt> [--repo .]
    python3 check_plan_start.py --record <plan-branch.json> --plans-dir <plans> \
        --branches-before <branches-before.txt> [--repo .] --out <plan-start-check.json>

`--save-branches` writes the branches here and on origin before the run; the check compares
against that list. Exit 0 ok, 1 not ok (the problems are named), 2 bad input.
"""
import argparse
import json
import os
import subprocess
import sys

import yaml


def _git(repo, *args):
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                       env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    return p.returncode, p.stdout.strip()


def branches(repo):
    _, out = _git(repo, "branch", "-a", "--format=%(refname:short)")
    return set(out.split())


def check(rec, plans_dir, before, repo):
    plan = str(rec.get("plan"))
    base = f"plan/{plan}/base"
    problems = []
    _, here = _git(repo, "branch", "--show-current")
    _, remote = _git(repo, "ls-remote", "--heads", "origin", base)
    on_plan_branch = here == base and bool(remote)
    if not on_plan_branch:
        problems.append(f"the session is on {here or 'no branch'}, or {base} is not on origin")

    main_agrees = True
    if rec.get("action") == "cut":
        cut = rec.get("main_commit")
        tip = remote.split()[0] if remote else None
        if not cut or tip != cut:
            main_agrees = False
            problems.append(f"{base} on origin is {tip}, not the main commit it was cut from ({cut})")
        elif _git(repo, "merge-base", "--is-ancestor", cut, "origin/main")[0] != 0:
            main_agrees = False
            problems.append(f"the main commit {cut[:7]} is not on origin/main")
        else:
            rel = os.path.relpath(os.path.join(plans_dir, f"{plan}.yaml"), repo).replace(os.sep, "/")
            _, text = _git(repo, "show", f"{cut}:{rel}")
            data = yaml.safe_load(text) or {}
            if data.get("status") != "In Progress" or data.get("branch") != base:
                main_agrees = False
                problems.append(f"main's plan file reads status {data.get('status')!r} and branch "
                                f"{data.get('branch')!r}, not In Progress on {base}")
    elif rec.get("action") not in ("stay", "switch"):
        main_agrees = False
        problems.append(f"the plan tool's record reads action {rec.get('action')!r}: {rec.get('error')}")

    def name(b):
        return b[len("origin/"):] if b.startswith("origin/") else b
    made = sorted(b for b in branches(repo) - before
                  if name(b).startswith(f"plan/{plan}/") and name(b) != base)
    no_story_branch = not made
    if made:
        problems.append(f"a story branch was made: {', '.join(made)}")
    return {"plan": plan, "action": rec.get("action"), "on_plan_branch": on_plan_branch,
            "main_agrees": main_agrees, "no_story_branch": no_story_branch,
            "ok": on_plan_branch and main_agrees and no_story_branch, "problems": problems}


def main(argv=None):
    ap = argparse.ArgumentParser(description="prove a plan's start")
    ap.add_argument("--save-branches")
    ap.add_argument("--record")
    ap.add_argument("--plans-dir")
    ap.add_argument("--branches-before")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out")
    ns = ap.parse_args(argv)
    if ns.save_branches:
        with open(ns.save_branches, "w", encoding="utf-8") as fh:
            fh.write("\n".join(sorted(branches(ns.repo))) + "\n")
        return 0
    if not (ns.record and ns.plans_dir and ns.branches_before and ns.out):
        ap.error("--record, --plans-dir, --branches-before and --out are needed for the check")
    try:
        with open(ns.record, encoding="utf-8") as fh:
            rec = json.load(fh)
        with open(ns.branches_before, encoding="utf-8") as fh:
            before = set(fh.read().split())
    except (OSError, ValueError) as e:
        print(f"check_plan_start.py: {e}", file=sys.stderr)
        return 2
    out = check(rec, ns.plans_dir, before, ns.repo)
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(json.dumps(out, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
