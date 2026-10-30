#!/usr/bin/env python3
"""
plan_branch.py — get onto a plan's branch, the one way every play does it (#720, #730).

A plan's work is on its own branch, `plan/<id>/base`. Only two copies of a plan file count: the
one on the plan's branch (the latest) and the one on main (which names the branch). This script
moves a session onto the plan's branch, and back again at the end:

    python3 plan_branch.py go   --plan ID [--plans-dir D] [--repo R] [--remote origin]
                                [--main main] [--ignore PREFIX ...] --out <record.json>
    python3 plan_branch.py back  --record <record.json> [--repo R] [--ignore PREFIX ...]
    python3 plan_branch.py abort --record <record.json> [--repo R] [--remote origin] [--main main]
                                 [--ignore PREFIX ...]

`go`:
  - on the plan's branch already: it stays (and takes the remote's new commits, fast-forward only);
  - else, when anything is uncommitted (a changed, staged or new file outside the --ignore
    folders): it stops, names the files and changes nothing (exit 3). The person cleans up;
  - else, when the plan's branch exists (here or on the remote): it switches to it;
  - else (the plan has no branch): it switches to main, takes the remote's new commits, sets main's
    plan file to `status: In Progress` and `branch: plan/<id>/base` (every other line stays as it
    is), commits that on main, pushes main, cuts the branch from that commit and pushes it. This is
    the one write a plan session makes before the person approves anything (#720 design).
A plan that main's file marks Done or Dropped gets no branch: it stops with the status named
(exit 2), and nothing is written.

`back` switches to the branch the record says the session started on, when that is another
branch. Uncommitted work outside the --ignore folders stops it (exit 3).

`abort` undoes what `go` did, then goes back. When `go` cut the plan's branch, it checks that
the branch holds nothing but main's commit (here and on the remote) — else it stops and names
the commits (exit 3) — then reverts that commit on main (main's plan file is back as it was),
pushes main, and deletes the branch here and on the remote. When `go` stayed or switched, the
plan's branch is left as it is. Uncommitted work outside the --ignore folders stops it (exit 3).

The record: {action: stay|switch|cut|stop|back|abort, plan, plan_branch, start_branch, back_to,
main_commit, files, error}. Exit 0 done; 2 bad input or a git step failed (the error is named);
3 stopped on uncommitted work. Users: /update-plan (#730), and start-change once #989 is built.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

import yaml

DEFAULT_PLANS = os.path.join(".garura", "project", "plans")
CLOSED = {"Done", "Dropped"}


class Stop(Exception):
    def __init__(self, message, code=2, files=None):
        super().__init__(message)
        self.code = code
        self.files = files or []


def git(args, repo, check=True):
    """Run git; retry while another git process holds the index lock."""
    for attempt in range(8):
        done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
        if done.returncode == 0 or "index.lock" not in done.stderr:
            break
        time.sleep(2)
    if check and done.returncode != 0:
        line = (done.stderr or done.stdout).strip().splitlines()
        raise Stop(f"git {' '.join(args)} failed: {line[-1] if line else 'no message'}")
    return done


def current_branch(repo):
    name = git(["branch", "--show-current"], repo).stdout.strip()
    if not name:
        raise Stop("not on a branch (a detached HEAD); switch to a branch first")
    return name


def uncommitted(repo, ignore):
    """Every uncommitted path outside the --ignore folders, and every staged path anywhere:
    a staged file would ride into the next commit, so no folder excuses it."""
    out = git(["status", "--porcelain", "-z", "--untracked-files=all"], repo).stdout
    entries = out.split("\0")
    files, i = [], 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        if code[0] in "RC":
            i += 1  # the rename's old path follows; the new one is what counts
        staged = code[0] not in " ?"
        ignored = any(path == p.rstrip("/") or path.startswith(p.rstrip("/") + "/") for p in ignore)
        if staged or not ignored:
            files.append(path)
    return files


def has_ref(ref, repo):
    return git(["rev-parse", "--verify", "--quiet", ref], repo, check=False).returncode == 0


def has_remote(remote, repo):
    return remote in git(["remote"], repo).stdout.split()


def pull(branch, remote, repo):
    """Take the remote's new commits, fast-forward only; nothing when the branch is not there."""
    if has_remote(remote, repo) and has_ref(f"{remote}/{branch}", repo):
        git(["merge", "--ff-only", f"{remote}/{branch}"], repo)


def set_fields(text, branch):
    """Set the top-level `status:` and `branch:` lines; every other line stays byte for byte."""
    lines = text.splitlines(keepends=True)
    status_at = branch_at = None
    for i, line in enumerate(lines):
        if re.match(r"status:", line):
            status_at = i
        elif re.match(r"branch:", line):
            branch_at = i
    if status_at is None:
        raise Stop("the plan file has no top-level status line")
    end = "\r\n" if lines[status_at].endswith("\r\n") else "\n"
    lines[status_at] = f"status: In Progress{end}"
    if branch_at is not None:
        lines[branch_at] = f"branch: {branch}{end}"
    else:
        lines.insert(status_at + 1, f"branch: {branch}{end}")
    return "".join(lines)


def go(args):
    repo, plan = args.repo, str(args.plan)
    plan_branch = f"plan/{plan}/base"
    rec = {"action": None, "plan": plan, "plan_branch": plan_branch, "start_branch": None,
           "back_to": None, "main_commit": None, "files": [], "error": None}
    start = current_branch(repo)
    rec["start_branch"] = start
    remote = has_remote(args.remote, repo)
    if remote:
        git(["fetch", "--quiet", args.remote], repo)
    if start == plan_branch:
        pull(plan_branch, args.remote, repo)
        rec["action"] = "stay"
        return rec
    files = uncommitted(repo, args.ignore)
    if files:
        raise Stop(f"{start} has uncommitted work; commit or clean it, then run again", 3, files)
    rec["back_to"] = start
    if has_ref(plan_branch, repo) or (remote and has_ref(f"{args.remote}/{plan_branch}", repo)):
        if has_ref(plan_branch, repo):
            git(["checkout", "--quiet", plan_branch], repo)
            pull(plan_branch, args.remote, repo)
        else:
            git(["checkout", "--quiet", "-b", plan_branch, "--track", f"{args.remote}/{plan_branch}"], repo)
        rec["action"] = "switch"
        return rec
    # The plan has no branch: main's plan file first, then the cut. Until main is pushed,
    # any stop puts main back as it was and returns to the starting branch.
    path = os.path.join(args.plans_dir, f"{plan}.yaml")
    committed = False
    try:
        if start != args.main:
            git(["checkout", "--quiet", args.main], repo)
        pull(args.main, args.remote, repo)
        full = os.path.join(repo, path)
        try:
            with open(full, encoding="utf-8", newline="") as fh:
                text = fh.read()
        except OSError:
            raise Stop(f"no plan {plan} on {args.main}: {path} is missing")
        try:
            status = (yaml.safe_load(text) or {}).get("status")
        except yaml.YAMLError as e:
            raise Stop(f"the plan file {path} on {args.main} cannot be read: {str(e).splitlines()[0]}")
        if status in CLOSED:
            raise Stop(f"plan {plan} is {status} on {args.main}; a person sets its status before work starts again")
        with open(full, "w", encoding="utf-8", newline="") as fh:
            fh.write(set_fields(text, plan_branch))
        git(["add", "--", path], repo)
        # Only the plan file goes into this commit, whatever else is staged.
        git(["commit", "--quiet", "-m",
             f"chore(plan): plan {plan} — In Progress on {plan_branch} (#{plan})", "--", path], repo)
        committed = True
        rec["main_commit"] = git(["rev-parse", "HEAD"], repo).stdout.strip()
        if remote:
            git(["push", "--quiet", args.remote, args.main], repo)
    except Stop:
        if committed:
            # The push of main failed: take the local commit back, keep the file as it was.
            git(["reset", "--quiet", "--soft", "HEAD~1"], repo, check=False)
            git(["restore", "--quiet", "--staged", "--worktree", "--", path], repo, check=False)
        else:
            git(["checkout", "--quiet", "--", path], repo, check=False)
        back(repo, start)
        raise
    git(["checkout", "--quiet", "-b", plan_branch], repo)
    rec["action"] = "cut"
    if remote:
        pushed = git(["push", "--quiet", "-u", args.remote, plan_branch], repo, check=False)
        if pushed.returncode != 0:
            # Main says In Progress and the branch is cut here, but not on the remote. The
            # record keeps the cut, so `abort` can undo it, and names what is missing.
            rec["error"] = f"{plan_branch} is cut here but not pushed: {(pushed.stderr or '').strip()}"
    return rec


def back(repo, branch):
    if branch and current_branch(repo) != branch:
        git(["checkout", "--quiet", branch], repo)


def abort(args, rec):
    repo, branch = args.repo, rec.get("plan_branch")
    start = rec.get("back_to") or rec.get("start_branch")
    files = uncommitted(repo, args.ignore)
    if files:
        raise Stop(f"{current_branch(repo)} has uncommitted work; commit or clean it first", 3, files)
    out = {"action": "abort", "plan": rec.get("plan"), "plan_branch": branch, "back_to": start,
           "reverted": None, "deleted": False}
    if branch != f"plan/{rec.get('plan')}/base":
        raise Stop(f"the record names {branch!r}, not plan/{rec.get('plan')}/base; nothing is undone")
    if rec.get("action") == "cut":
        cut = rec.get("main_commit")
        remote = has_remote(args.remote, repo)
        if remote:
            git(["fetch", "--quiet", args.remote], repo)
        for ref in [branch] + ([f"{args.remote}/{branch}"] if remote and has_ref(f"{args.remote}/{branch}", repo) else []):
            if has_ref(ref, repo):
                extra = git(["log", "--oneline", f"{cut}..{ref}"], repo).stdout.strip()
                if extra:
                    raise Stop(f"{ref} holds more than the cut; nothing is undone: {extra.splitlines()[0]}", 3)
        if current_branch(repo) != args.main:
            git(["checkout", "--quiet", args.main], repo)
        pull(args.main, args.remote, repo)
        if git(["merge-base", "--is-ancestor", cut, "HEAD"], repo, check=False).returncode != 0:
            raise Stop(f"{args.main} does not hold the cut {cut[:7]}; nothing is undone")
        if git(["revert", "--no-edit", cut], repo, check=False).returncode != 0:
            git(["revert", "--abort"], repo, check=False)
            back(repo, start)
            raise Stop(f"reverting {cut[:7]} on {args.main} clashes with later work; nothing is undone")
        out["reverted"] = git(["rev-parse", "HEAD"], repo).stdout.strip()
        if remote and git(["push", "--quiet", args.remote, args.main], repo, check=False).returncode != 0:
            git(["reset", "--quiet", "--keep", "HEAD~1"], repo, check=False)
            back(repo, start)
            raise Stop(f"the push of {args.main} failed; the revert is taken back and nothing is undone")
        if has_ref(branch, repo):
            git(["branch", "--quiet", "-D", branch], repo)
        if remote and has_ref(f"{args.remote}/{branch}", repo):
            git(["push", "--quiet", args.remote, "--delete", branch], repo)
        out["deleted"] = True
    back(repo, start)
    return out


def write(path, rec):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
        fh.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="get onto a plan's branch, and back")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("go")
    g.add_argument("--plan", required=True)
    g.add_argument("--plans-dir", default=DEFAULT_PLANS)
    g.add_argument("--repo", default=".")
    g.add_argument("--remote", default="origin")
    g.add_argument("--main", default="main")
    g.add_argument("--ignore", action="append", default=[])
    g.add_argument("--out", required=True)
    b = sub.add_parser("back")
    b.add_argument("--record", required=True)
    b.add_argument("--repo", default=".")
    b.add_argument("--ignore", action="append", default=[])
    x = sub.add_parser("abort")
    x.add_argument("--record", required=True)
    x.add_argument("--repo", default=".")
    x.add_argument("--remote", default="origin")
    x.add_argument("--main", default="main")
    x.add_argument("--ignore", action="append", default=[])
    args = ap.parse_args(argv)

    if args.cmd == "go":
        try:
            rec = go(args)
        except Stop as e:
            on = git(["branch", "--show-current"], args.repo, check=False).stdout.strip() or None
            rec = {"action": "stop", "plan": str(args.plan), "plan_branch": f"plan/{args.plan}/base",
                   "start_branch": on, "back_to": None, "files": e.files, "error": str(e)}
            write(args.out, rec)
            print(json.dumps(rec, indent=2))
            return e.code
        write(args.out, rec)
        print(json.dumps(rec, indent=2))
        return 0

    try:
        with open(args.record, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as e:
        print(f"cannot read the record {args.record}: {e}", file=sys.stderr)
        return 2
    if args.cmd == "abort":
        try:
            out = abort(args, rec)
        except Stop as e:
            print(json.dumps({"action": "stop", "files": e.files, "error": str(e)}, indent=2))
            return e.code
        print(json.dumps(out, indent=2))
        return 0
    target = rec.get("back_to")
    try:
        if target and current_branch(args.repo) != target:
            files = uncommitted(args.repo, args.ignore)
            if files:
                raise Stop(f"{current_branch(args.repo)} has uncommitted work; commit or clean it first", 3, files)
            back(args.repo, target)
    except Stop as e:
        print(json.dumps({"action": "stop", "back_to": target, "files": e.files, "error": str(e)}, indent=2))
        return e.code
    print(json.dumps({"action": "back", "back_to": target}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
