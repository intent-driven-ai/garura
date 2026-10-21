#!/usr/bin/env python3
"""
setup_branch.py — start-change Step 4 as a script (#484).

Cuts the feature branch off latest main (or switches to it on resume), sets up a
git worktree when config calls for it, pushes, and writes branch.json. Replaces
the repo-orchestrator → setup-branch dispatch. Pure git — a fixed sequence, zero
judgment.

    python3 setup_branch.py --issue N --branch-name feature/N-slug \
        [--base main] [--plan-branch plan/P/base] [--worktree] [--no-push] --out <branch.json>

With --plan-branch (an issue in a plan, from resolve_plan.py — #731): the plan branch is
cut from the latest main when it does not exist yet (the plan's work starts now); when it
exists, the latest main is merged into it first. The issue's branch
(plan/P/<issue>-<slug>) is then cut from the plan branch. A merge conflict stops the run
(exit 1) with the plan branch left as it was.

Idempotent: if the branch already exists (local or remote), it is a resume —
switch to it, do not re-cut. Writes branch.json:
  { branch_name, base_sha, on_default_branch, worktree_path, plan_branch, plan_branch_created }

Exit 0 on success, 1 on a git failure.
"""

import argparse
import json
import os
import subprocess
import sys


def _git(*args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _branch_exists(branch):
    _, out_l, _ = _git("branch", "--list", branch)
    if out_l.strip():
        return True
    _, out_r, _ = _git("ls-remote", "--heads", "origin", branch)
    return bool(out_r.strip())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", required=True)
    ap.add_argument("--branch-name", required=True)
    ap.add_argument("--base", default="main")
    ap.add_argument("--plan-branch")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--out", required=True)
    ns = ap.parse_args(argv)
    branch = ns.branch_name

    # Bring base to its latest origin tip so the cut is off up-to-date main.
    rc, _, err = _git("checkout", ns.base)
    if rc != 0:
        sys.stderr.write(f"setup_branch.py: checkout {ns.base} failed: {err}\n")
        sys.exit(1)
    _git("pull", "--ff-only", "origin", ns.base)
    _, base_sha, _ = _git("rev-parse", f"origin/{ns.base}")

    plan_created = False
    if ns.plan_branch and not _branch_exists(branch):
        # The issue sits in a plan: bring the plan branch up to the latest main, or cut it.
        plan = ns.plan_branch
        if _branch_exists(plan):
            _git("fetch", "origin", plan)
            rc, _, err = _git("checkout", plan)
            if rc != 0:
                rc, _, err = _git("checkout", "-b", plan, f"origin/{plan}")
            if rc != 0:
                sys.stderr.write(f"setup_branch.py: checkout {plan} failed: {err}\n")
                sys.exit(1)
            _git("pull", "--ff-only", "origin", plan)
            rc, _, err = _git("merge", "--no-edit", f"origin/{ns.base}")
            if rc != 0:
                _git("merge", "--abort")
                sys.stderr.write(f"setup_branch.py: merging {ns.base} into {plan} conflicts — "
                                 f"resolve it by hand: {err}\n")
                sys.exit(1)
        else:
            rc, _, err = _git("checkout", "-b", plan, f"origin/{ns.base}")
            if rc != 0:
                sys.stderr.write(f"setup_branch.py: cutting {plan} failed: {err}\n")
                sys.exit(1)
            plan_created = True
        if not ns.no_push:
            _git("push", "-u", "origin", plan)
        _, base_sha, _ = _git("rev-parse", "HEAD")

    worktree_path = None
    if _branch_exists(branch):
        # Resume: switch to the existing branch, do not re-cut or duplicate.
        rc, _, err = _git("checkout", branch)
        if rc != 0:
            sys.stderr.write(f"setup_branch.py: resume checkout failed: {err}\n")
            sys.exit(1)
    elif ns.worktree:
        # Sibling worktree dir: ../{repo}-{branch-slug}
        repo = os.path.basename(os.path.abspath("."))
        slug = branch.replace("/", "-")
        worktree_path = os.path.abspath(os.path.join("..", f"{repo}-{slug}"))
        rc, _, err = _git("worktree", "add", worktree_path, "-b", branch)
        if rc != 0:
            sys.stderr.write(f"setup_branch.py: worktree add failed: {err}\n")
            sys.exit(1)
    else:
        rc, _, err = _git("checkout", "-b", branch)
        if rc != 0:
            sys.stderr.write(f"setup_branch.py: checkout -b failed: {err}\n")
            sys.exit(1)

    if not ns.no_push:
        _git("push", "-u", "origin", branch)

    record = {"branch_name": branch, "base_sha": base_sha,
              "on_default_branch": False, "worktree_path": worktree_path,
              "plan_branch": ns.plan_branch, "plan_branch_created": plan_created}
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps(record, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
