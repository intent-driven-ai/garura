#!/usr/bin/env python3
"""close_session.py — how the session ended, for the Done means (C5, C7, C12).

    python3 close_session.py --work <working folder> [--repo R] --out <session.json>

It reads the session's records in the working folder — branch.json, answer.json,
github-record.json, plan-write.json, agreement.json, commit.json, model-record.json — and the
branch checked out now, and writes:
  - outcome: `stopped` (the branch step stopped), `landed` (approved, and the landing ran),
    `aborted` (the person said "abort": the list is dropped), or `open` (no final answer yet;
    a "rejected" answer is not an end — the session goes on);
  - written: whether anything reached the tracker, the model or the plan file (beyond the
    branch step);
  - ok: landed with the agreement check ok and the commit pushed; or stopped / aborted with
    nothing written;
  - back: the branch checked out is the one the session started on (or the plan's branch, when it
    started there).
Exit 0 written; 2 bad input. Reads only.
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def rec(work, name):
    path = os.path.join(work, name)
    return ps.read_json(path, name) if os.path.isfile(path) else None


def main(argv=None):
    ap = argparse.ArgumentParser(description="how the session ended")
    ap.add_argument("--work", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        branch = rec(args.work, "branch.json") or {}
        answer = rec(args.work, "answer.json") or {}
        gh = rec(args.work, "github-record.json")
        pw = rec(args.work, "plan-write.json")
        agree = rec(args.work, "agreement.json")
        commit = rec(args.work, "commit.json")
        model = rec(args.work, "model-record.json")
    except ps.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    written = bool((gh and gh.get("done")) or (pw and pw.get("ok")) or (commit and commit.get("commit"))
                   or (model and model.get("files")))
    if branch.get("action") == "stop":
        outcome = "stopped"
    elif answer.get("decision") == "approved" and (gh is not None or pw is not None):
        outcome = "landed"
    elif answer.get("decision") == "abort":
        outcome = "aborted"
    else:
        outcome = "open"
    if outcome == "landed":
        ok = bool(agree and agree.get("ok") and commit and commit.get("ok") and
                  (commit.get("pushed") or not commit.get("commit")))
    else:
        ok = outcome in ("stopped", "aborted") and not written
    now = subprocess.run(["git", "branch", "--show-current"], cwd=args.repo,
                         capture_output=True, text=True).stdout.strip()
    target = branch.get("back_to") or branch.get("start_branch")
    back = bool(target) and now == target
    ps.write_json(args.out, {"outcome": outcome, "written": written, "ok": ok, "back": back,
                             "on": now, "start": target})
    return 0


if __name__ == "__main__":
    sys.exit(main())
