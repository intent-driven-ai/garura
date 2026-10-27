#!/usr/bin/env python3
"""
record_approval.py — record the product owner's typed answer at the /shape-eval checkpoint (C9).

    python3 record_approval.py --decision yes|change|stop --reply "<their exact words>" \
        --at <timestamp> --out <approval.json>

Writes {"decision", "reply", "at", "history": [...]}: the latest answer on top, and every
earlier answer of the run kept in `history` (a change goes back and is shown again). Only a
person's own typed reply is recorded: an empty reply is refused. Exit 0 written, 2 refused.

    python3 record_approval.py verify --file <approval.json>

The gate right before the eval commit: exit 0 only when the file reads
`decision: yes` with a typed reply; exit 1 when the decision is anything else (change, stop)
or the reply is empty; exit 2 when the file is missing or cannot be read. Nothing is
committed unless it exits 0 (C9).
"""

import argparse
import json
import os
import sys

DECISIONS = ("yes", "change", "stop")


def verify(argv):
    ap = argparse.ArgumentParser(description="Gate the commit on a recorded yes.")
    ap.add_argument("--file", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.file, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"record_approval.py: no approval to check at {args.file}: {exc}\n")
        print(json.dumps({"ok": False, "reason": "no approval recorded"}))
        return 2
    decision = rec.get("decision") if isinstance(rec, dict) else None
    reply = rec.get("reply") if isinstance(rec, dict) else None
    ok = decision == "yes" and isinstance(reply, str) and reply.strip() != ""
    reason = "the person typed yes" if ok else (
        f"the decision is {decision!r}, not yes" if decision != "yes" else "the reply is empty")
    print(json.dumps({"ok": ok, "decision": decision, "reason": reason}))
    if not ok:
        sys.stderr.write(f"record_approval.py: do not commit — {reason}\n")
    return 0 if ok else 1


def main(argv=None):
    if argv and argv[0] == "verify":
        return verify(argv[1:])
    ap = argparse.ArgumentParser(description="Record the checkpoint answer.")
    ap.add_argument("--decision", required=True, choices=DECISIONS)
    ap.add_argument("--reply", required=True)
    ap.add_argument("--at", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if not args.reply.strip():
        sys.stderr.write("record_approval.py: no reply — only the person's typed words are recorded\n")
        return 2
    history = []
    if os.path.isfile(args.out):
        try:
            with open(args.out, encoding="utf-8") as fh:
                old = json.load(fh)
            history = list(old.get("history") or []) + [
                {k: old.get(k) for k in ("decision", "reply", "at")}]
        except (OSError, json.JSONDecodeError):
            history = []
    rec = {"decision": args.decision, "reply": args.reply, "at": args.at, "history": history}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
