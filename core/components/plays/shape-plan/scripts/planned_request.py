#!/usr/bin/env python3
"""planned_request.py — the link-model-part request that sets Planned (/shape-plan, C8, C18).

    python3 planned_request.py --work-items <work-items.json> --record <tracker-record.json> \
        --plan-write <plan-write.json> --approval <approval.json> --plan-id <id> \
        --out <working>/planned-request.json

It runs after the yes, after the tracker writes and after the plan file. It refuses (exit 2,
nothing written) unless approval.json reads yes, the tracker record reads `ok: true` and the
plan file was written (`plan-write.json` reads `ok: true`). Then it writes the request the
`product-os-keeper` agent hands to the `link-model-part` skill:

    {"by": "shape-plan",
     "parts": [{"id": "<feature id>", "kind": "feature", "mode": "update", "status": "Planned"}]}

one part for each feature of `state_changes` in work-items.json (each feature the plan takes in
that is Unplanned, or had no state). `by` names the play only: the model holds no plan id and
no issue number (ADR 069), so the plan id stays in the brief and the commit message. A feature that is Planned or In progress keeps its state
and is not in the request. Each feature of the request must be in the plan: in the record's
map. With no state change the request has no parts, and the play skips the model write.

Output (stdout): {ok, out, parts}
Exit 0 written; 2 refused or bad input (nothing written). No git, no network, no model write.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

BY = "shape-plan"


def build(items, rec, plan_id):
    in_plan = set((rec.get("map") or {}).keys())
    parts = []
    for c in items.get("state_changes") or []:
        fid = c.get("feature")
        if fid not in in_plan:
            raise pc.Refused(f"{fid} is to be set to Planned, but the record does not put it in the plan")
        if c.get("to") != "Planned":
            raise pc.Refused(f"{fid}: the plan sets only Planned, not {c.get('to')!r}")
        parts.append({"id": fid, "kind": "feature", "mode": "update", "status": "Planned"})
    return {"by": BY, "parts": parts}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the link-model-part request that sets Planned.")
    ap.add_argument("--work-items", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--plan-write", required=True)
    ap.add_argument("--approval", required=True)
    ap.add_argument("--plan-id", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        ok, _, reason = pc.approval_is_yes(args.approval)
        if not ok:
            raise pc.Refused(f"no model write without the person's yes: {reason}")
        rec = pc.read_json(args.record, "tracker-record.json")
        if not rec.get("ok"):
            raise pc.Refused("the tracker writes did not all land (the record reads ok: false); "
                             "the model is not written")
        if not pc.read_json(args.plan_write, "plan-write.json").get("ok"):
            raise pc.Refused("the plan file was not written; the model is not written")
        items = pc.read_json(args.work_items, "work-items.json")
        request = build(items, rec, args.plan_id)
    except pc.Refused as exc:
        sys.stderr.write(f"planned_request.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, request)
    print(json.dumps({"ok": True, "out": args.out, "parts": len(request["parts"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
