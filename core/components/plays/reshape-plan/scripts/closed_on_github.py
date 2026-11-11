#!/usr/bin/env python3
"""
closed_on_github.py — the items whose own issue is closed on GitHub but open in the plan file (#1007).

An item's status follows its own issue: closed as completed means Done, closed as not planned
(or as a duplicate) means Dropped. Nothing is worked out from the items under it (no roll-ups). When a session
starts, this script reads the plan file and the session's snapshot of the issues, and writes one
status entry for each such item, as a draft in the shape of draft-entries.json. The play checks
the draft and takes it into the list like any other; nothing lands before the person's
"approved".

    python3 closed_on_github.py --plan-file <plans>/<id>.yaml --snapshot <working>/snapshot.json \
        --out <working>/draft-closed.json

The draft: {instruction: "closed on GitHub", entries: [{op: status, issue, to}], questions: []}.
Exit 0 (the entries may be none); 2 when the plan file or the snapshot cannot be read.
"""

import argparse
import sys

import plan_session as ps

INSTRUCTION = "closed on GitHub"


def entries(plan, snap):
    issues = (snap or {}).get("issues") or {}
    out = []
    for node, _ in ps.walk(plan.get("tree")):
        if node.get("status") in ps.CLOSED:
            continue
        now = issues.get(str(node.get("issue")))
        if not now or now.get("state") != "CLOSED":
            continue
        # Closed as not planned or as a duplicate is Dropped; any other close is Done.
        to = "Dropped" if ps.closed_as(now, "not planned") else "Done"
        out.append({"op": "status", "issue": node["issue"], "to": to})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="list the items closed on GitHub but open in the plan file")
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        plan = ps.load_plan(args.plan_file)
        snap = ps.read_json(args.snapshot, "snapshot.json")
    except ps.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    found = entries(plan, snap)
    ps.write_json(args.out, {"instruction": INSTRUCTION, "entries": found, "questions": []})
    print(f"{len(found)} item(s) closed on GitHub but open in the plan file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
