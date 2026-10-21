#!/usr/bin/env python3
"""commit_run_files.py — commit a play's run files under the drive's issue (Shared Drive Run, R5).

Inside a drive a play commits only its own product change; the run files it writes under the
issue (context, review, evidence) are the drive's to commit (#662 finding V-4). After each
play the drive runs this, so the next play starts from a clean tree. Canonical copy lives at
drive-creator/references/commit_run_files.py and is stamped into each drive's scripts/.

    python3 commit_run_files.py --issue-dir .garura/project/issues/<n>/ --issue <n> \
        --branch <the contract's branch> --play <play> --out <working>/<play>-commit.json

It commits only paths under the issue folder, on the drive's branch, and never sweeps in
anything someone else staged. After a round (ADR 043) the drive commits the round once: the
gap skills changed the product model too, so `--also <product_base>product-os` adds that folder
to the same commit (`--play round-<n>`). Exit 0 — committed, or nothing to commit, and the tree is clean.
Exit 1 — committed, but files outside the issue folder are still changed: the drive halts.
Exit 2 — wrong branch, something else already staged, or git failed: nothing committed.
Fixed git work, no judgment (#484). Standard library only.
"""
import argparse
import json
import os
import subprocess
import sys
import time


def git(*args, check=True):
    """Run git; retry a moment when another git process holds the index lock."""
    for attempt in range(6):
        run = subprocess.run(["git", *args], capture_output=True, text=True)
        if run.returncode == 0 or "index.lock" not in run.stderr:
            break
        time.sleep(1)
    if check and run.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {run.stderr.strip()}")
    return run.stdout


def changed_paths():
    """Changed paths (tracked or not) from `git status --porcelain`, as repo-relative text."""
    out = git("-c", "core.quotepath=off", "status", "--porcelain", "-uall")
    return [line[3:].split(" -> ")[-1] for line in out.splitlines() if line.strip()]


def under(path, folder):
    folder = folder.rstrip("/") + "/"
    return path == folder.rstrip("/") or path.startswith(folder)


def run(args):
    folder = os.path.relpath(args.issue_dir).replace(os.sep, "/")
    branch = git("branch", "--show-current").strip()
    if branch != args.branch:
        return 2, {"committed": False, "why": f"on `{branch}`, not the drive's branch `{args.branch}`"}
    staged = [p for p in git("diff", "--cached", "--name-only").splitlines() if p.strip()]
    if staged:
        return 2, {"committed": False, "why": "something is already staged: " + ", ".join(staged[:5])}
    sha = None
    folders = [folder] + [os.path.relpath(a).replace(os.sep, "/") for a in (args.also or [])]
    if any(under(p, f) for p in changed_paths() for f in folders):
        git("add", "-A", "--", *[f for f in folders if os.path.exists(f)])
        what = "run files" if not args.also else "round"
        git("commit", "-q", "-m", f"chore(stm): record {args.play} {what} (#{args.issue})")
        sha = git("rev-parse", "HEAD").strip()
    leftover = changed_paths()
    result = {"committed": sha is not None, "sha": sha, "play": args.play, "leftover": leftover}
    if leftover:
        result["why"] = "files outside the folders committed are still changed"
        return 1, result
    return 0, result


def main(argv=None):
    ap = argparse.ArgumentParser(description="Commit a play's run files for the drive.")
    ap.add_argument("--issue-dir", required=True)
    ap.add_argument("--issue", required=True, type=int)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--play", required=True)
    ap.add_argument("--also", action="append",
                    help="another folder to commit with the run files (after a round: the product model)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        code, result = run(args)
    except (OSError, RuntimeError) as exc:
        code, result = 2, {"committed": False, "why": str(exc)}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
