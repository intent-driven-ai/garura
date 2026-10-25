#!/usr/bin/env python3
"""record_approval.py — record the product owner's typed answer at the /shape-plan checkpoint (C8).

    python3 record_approval.py --decision yes|change|stop --reply "<the person's words>" \
        --at <UTC timestamp> --brief <brief.md> --work-items <work-items.json> \
        --drafts <drafts.json> --out <working>/approval.json

Writes {"decision", "reply", "at", "files", "history": [...]}: the latest answer on top, and
every earlier answer of the run kept in `history` (a change sends the run back and the brief is
shown again). `files` ties the answer to what the person saw: for the brief, work-items.json
and drafts.json, its path and its sha256. write_work_items.py writes nothing when one of the
three no longer matches. Only the person's own typed reply is recorded: an empty reply, or a
file that cannot be read, is refused. Exit 0 written, 2 refused (nothing written).

    python3 record_approval.py verify --file <approval.json>

The gate right before the first tracker write and the plan-file commit: exit 0 only when the
file reads `decision: yes` with a typed reply; exit 1 when the decision is change or stop, or
the reply is empty; exit 2 when the file is missing or cannot be read. Nothing reaches the
tracker, and nothing is committed, unless it exits 0.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

DECISIONS = ("yes", "change", "stop")


def verify(argv):
    ap = argparse.ArgumentParser(description="Gate the writes on a recorded yes.")
    ap.add_argument("--file", required=True)
    args = ap.parse_args(argv)
    if not os.path.isfile(args.file):
        print(json.dumps({"ok": False, "reason": "no approval is recorded"}))
        sys.stderr.write(f"record_approval.py: no approval to check at {args.file}\n")
        return 2
    try:
        json.loads(pc.read_text(args.file))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "reason": f"the approval cannot be read: {exc}"}))
        return 2
    ok, decision, reason = pc.approval_is_yes(args.file)
    print(json.dumps({"ok": ok, "decision": decision, "reason": reason}))
    if not ok:
        sys.stderr.write(f"record_approval.py: write nothing — {reason}\n")
    return 0 if ok else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "verify":
        return verify(argv[1:])
    ap = argparse.ArgumentParser(description="Record the checkpoint answer.")
    ap.add_argument("--decision", required=True, choices=DECISIONS)
    ap.add_argument("--reply", required=True)
    ap.add_argument("--at", required=True)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--work-items", required=True)
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    files = {}
    for key, path in (("brief", args.brief), ("work_items", args.work_items), ("drafts", args.drafts)):
        digest = pc.sha256_of(path)
        if digest is None:
            sys.stderr.write(f"record_approval.py: cannot read {path}; the answer must be tied to what the person saw\n")
            print(json.dumps({"ok": False, "reason": f"cannot read {path}"}))
            return 2
        files[key] = {"path": path, "sha256": digest}
    if not args.reply.strip():
        sys.stderr.write("record_approval.py: no reply — only the person's typed words are recorded\n")
        print(json.dumps({"ok": False, "reason": "the reply is empty"}))
        return 2
    history = []
    if os.path.isfile(args.out):
        try:
            old = json.loads(pc.read_text(args.out))
            history = list(old.get("history") or []) + [
                {k: old.get(k) for k in ("decision", "reply", "at", "files")}]
        except (OSError, json.JSONDecodeError, AttributeError):
            history = []
    rec = {"decision": args.decision, "reply": args.reply, "at": args.at, "files": files,
           "history": history}
    pc.write_json(args.out, rec)
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
