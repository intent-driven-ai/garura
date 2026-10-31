#!/usr/bin/env python3
"""
setup_branch.py — start-change Step 4 as a script (#484).

Cuts the feature branch off latest main (or switches to it on resume), sets up a
git worktree when config calls for it, pushes, and writes branch.json. Replaces
the repo-orchestrator → cut-branch dispatch. Pure git — a fixed sequence, zero
judgment.

    python3 setup_branch.py --issue N --branch-name feature/N-slug \
        [--base main] [--plan-branch plan/P/base --plan-tool <plan_branch.py> --plans-dir <plans>
         --ignore <folder>] [--worktree] [--no-push] --out <branch.json>

With --plan-branch (an issue in a plan, from resolve_plan.py — #731): the plan branch is
cut main first when it is not on origin yet (the plan's work starts now); when it
exists, the latest main is merged into it first. The issue's branch
(plan/P/<issue>-<slug>) is then cut from the plan branch. A merge conflict stops the run
(exit 1) with the plan branch left as it was.

A plan branch that is not on origin is cut by the plan tool's plan_branch.py (--plan-tool),
the one way every play cuts a plan's branch (ADR 061, #989): main's plan file is set to In
Progress with the branch named, committed and pushed on main, and the branch is cut from that
commit. A copy that is gone on origin but still here is deleted and cut fresh only when every
commit on it is on main; otherwise the plan tool stops, keeps the copy and names the commits
(#953), and so does this script. A failed lookup on origin (offline, a login error, a stalled
server) stops the run and says origin could not be reached. A push that fails stops the run.
Network calls never prompt and give up after a time limit.

Idempotent: if the branch already exists (local or remote), it is a resume —
switch to it, do not re-cut. Writes branch.json:
  { branch_name, base_sha, on_default_branch, worktree_path, plan_branch, plan_branch_created,
    stale_plan_branch: null | { deleted: true, tip: <sha>, on_main: true } }

Exit 0 on success, 1 on a git failure.
"""

import argparse
import json
import os
import subprocess
import sys


TIME_LIMIT = 120  # seconds for a call to origin; a stalled server is a failure, never a hang
NO_PROMPT = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def _git(*args):
    try:
        proc = subprocess.run(["git", *args], capture_output=True, text=True,
                              timeout=TIME_LIMIT, env=NO_PROMPT)
    except subprocess.TimeoutExpired:
        return 124, "", f"git {args[0]} gave up after {TIME_LIMIT} seconds"
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _branch_exists(branch):
    _, out_l, _ = _git("branch", "--list", branch)
    if out_l.strip():
        return True
    _, out_r, _ = _git("ls-remote", "--heads", "origin", branch)
    return bool(out_r.strip())


def _on_origin(branch):
    """True or False; None when origin cannot be asked (offline, a login error)."""
    rc, out_r, _ = _git("ls-remote", "--heads", "origin", branch)
    if rc != 0:
        return None
    return bool(out_r.strip())


def _is_ancestor(a, b):
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b], capture_output=True).returncode == 0


def _cut_plan(ns, plan):
    """Cut the plan's branch through the plan tool, main first; return (created, stale)."""
    out = os.path.join(os.path.dirname(os.path.abspath(ns.out)), "plan-branch.json")
    cmd = [sys.executable, ns.plan_tool, "go", "--plan", plan.split("/")[1],
           "--plans-dir", ns.plans_dir, "--out", out]
    for folder in ns.ignore:
        cmd += ["--ignore", folder]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=NO_PROMPT)
    try:
        with open(out, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = {"action": "stop", "error": (proc.stderr or proc.stdout).strip()}
    if proc.returncode != 0 or rec.get("action") not in ("cut", "switch", "stay") or rec.get("error"):
        files = "".join(f"\n  {f}" for f in rec.get("files") or [])
        sys.stderr.write(f"setup_branch.py: the plan tool did not get onto {plan}: {rec.get('error')}{files}\n")
        sys.exit(1)
    return rec["action"] == "cut", rec.get("stale")


def _push(branch):
    rc, _, err = _git("push", "-u", "origin", branch)
    if rc != 0:
        sys.stderr.write(f"setup_branch.py: pushing {branch} to origin failed: {err}\n")
        sys.exit(1)


def _tip(branch):
    rc, sha, _ = _git("rev-parse", f"origin/{branch}")
    if rc != 0 or not sha.strip():
        rc, sha, _ = _git("rev-parse", branch)
    return sha.strip() if rc == 0 else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", required=True)
    ap.add_argument("--branch-name", required=True)
    ap.add_argument("--base", default="main")
    ap.add_argument("--plan-branch")
    ap.add_argument("--plan-tool", default=os.path.join(".garura", "core", "tools", "plan", "plan_branch.py"))
    ap.add_argument("--plans-dir", default=os.path.join(".garura", "project", "plans"))
    ap.add_argument("--ignore", action="append", default=[])
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
    stale = None
    if ns.plan_branch and not _branch_exists(branch):
        # The issue sits in a plan: bring the plan branch up to the latest main, or cut it.
        plan = ns.plan_branch
        on_origin = _on_origin(plan)
        if on_origin is None:
            sys.stderr.write(f"setup_branch.py: origin could not be reached to look for {plan}; "
                             f"nothing was changed — run again when it can be reached\n")
            sys.exit(1)
        if not on_origin:
            # The plan's work starts now: main's plan file first, then the cut (ADR 061). A stale
            # local copy is the plan tool's to judge (#953).
            plan_created, stale = _cut_plan(ns, plan)
        else:
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
        if not ns.no_push:
            _push(plan)
        _, base_sha, _ = _git("rev-parse", "HEAD")
    elif ns.plan_branch:
        # Resume of an issue in a plan: its branch was cut from the plan branch, so the
        # base it records is the plan branch's tip, not main's.
        base_sha = _tip(ns.plan_branch) or base_sha

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
        _push(branch)

    record = {"branch_name": branch, "base_sha": base_sha,
              "on_default_branch": False, "worktree_path": worktree_path,
              "plan_branch": ns.plan_branch, "plan_branch_created": plan_created,
              "stale_plan_branch": stale}
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps(record, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
