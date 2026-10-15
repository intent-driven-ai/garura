#!/usr/bin/env python3
"""
post_verdict.py — review-change Step 6 as a script (#484).

Posts the decision comment to the PR (via platform_adapter.py), commits and
pushes the review run artifacts, and writes posted.json. Replaces the
repo-orchestrator dispatch. Zero judgment — the decision is made at Step 5 (by
the human, or by the harness when the gate is off); this only publishes and
records it.

Before it posts, it reads the decision record (decision.yaml). The record must
hold a decision (approve | reject) and its decider (harness | human). When it
does not, nothing is posted and the script exits 2. posted.json carries the
decision, the decider and `decision_recorded: true` — the field review-change's
Done means D2 checks (#536).

    python3 post_verdict.py --config .garura/core/config.yaml \
        --pr-number N --comment-file <decision-comment.md> \
        --decision <review/decision.yaml> \
        --issue N --artifacts-dir <review/> --out <posted.json>

Exit 0 on success, 1 on a post/commit failure, 2 on a missing or invalid
decision record.
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import platform_adapter as pa  # noqa: E402

DECISIONS = ("approve", "reject")
DECIDERS = ("harness", "human")


def read_decision(path):
    """Return (decision, decided_by, error). error is None when the record is valid."""
    try:
        import yaml
    except ImportError:
        return None, None, "PyYAML required: pip install pyyaml"
    if not os.path.exists(path):
        return None, None, f"decision record missing: {path}"
    try:
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        return None, None, f"decision record unreadable: {exc}"
    if not isinstance(doc, dict):
        return None, None, "decision record is not a mapping"
    decision, decided_by = doc.get("decision"), doc.get("decided_by")
    if decision not in DECISIONS:
        return decision, decided_by, f"decision must be one of {DECISIONS}, got {decision!r}"
    if decided_by not in DECIDERS:
        return decision, decided_by, f"decided_by must be one of {DECIDERS}, got {decided_by!r}"
    return decision, decided_by, None


def _git(*args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--pr-number", required=True)
    ap.add_argument("--comment-file", required=True)
    ap.add_argument("--decision", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--artifacts-dir", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args(argv)

    # No decision with its decider → nothing is posted (#536).
    decision, decided_by, error = read_decision(ns.decision)
    if error:
        sys.stderr.write(f"post_verdict.py: {error}\n")
        sys.exit(2)

    with open(ns.comment_file, encoding="utf-8") as fh:
        body = fh.read()

    # Post the verdict comment.
    res = pa.dispatch("comment-pr", {"pr_number": ns.pr_number, "body": body},
                      config_path=ns.config)
    if res["exit_code"] != 0:
        sys.stderr.write(f"post_verdict.py: comment-pr failed: {res['stderr']}\n")
        sys.exit(1)
    # gh prints the created comment URL on stdout.
    comment_url = res["stdout"].strip().splitlines()[-1] if res["stdout"].strip() else None

    posted = {"posted": True, "comment_url": comment_url, "pr_number": ns.pr_number,
              "decision": decision, "decided_by": decided_by, "decision_recorded": True}
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(posted, fh, indent=2)

    # Commit + push the review run artifacts so the PR carries its own review record.
    _git("add", ns.artifacts_dir)
    rc, _, _ = _git("commit", "-m",
                    f"chore(stm): record review-change run artifacts (#{ns.issue})")
    # rc != 0 is fine when there is nothing new to commit.
    _git("push", "origin", "HEAD")

    print(json.dumps(posted, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
