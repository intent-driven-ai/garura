#!/usr/bin/env python3
"""
record_approval.py — record the person's typed answer at the /shape-slice checkpoint (C12).

    python3 record_approval.py --decision yes|change|stop --reply "<their exact words>" \
        --at <timestamp> --out <approval.json>

Writes {"decision", "reply", "at", "history": [...]}: the latest answer on top, and every
earlier answer of the run kept in `history` (a change goes back and is shown again). Only a
person's own typed reply is recorded: an empty reply is refused. Exit 0 written, 2 refused.
"""

import argparse
import json
import os
import sys

DECISIONS = ("yes", "change", "stop")


def main(argv=None):
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
