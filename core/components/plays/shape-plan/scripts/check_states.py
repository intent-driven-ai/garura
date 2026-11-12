#!/usr/bin/env python3
"""check_states.py — the state check after the model write (/shape-plan, D6; C7, C16, C18).

    python3 check_states.py --before <working>/spine-before.yaml --spine <model>/_spine.yaml \
        --work-items <work-items.json> [--request <planned-request.json>] \
        --out <working>/state-check.json

It reads the spine as it was at the start of the run (gather_plan.py copied it) and the spine
now. `ok: true` only when:
  - the request (when given) asks for exactly the features of `state_changes`, each with kind
    feature, mode update and status Planned, and nothing else;
  - each feature the plan takes in that was Unplanned (or had no state) now reads
    `status: Planned`, and each that was Planned or In progress reads the same state as before;
  - no other feature's `status` changed;
  - nothing else in the spine changed. The only other change allowed is the stamp the skill
    writes on an entry it updates, `metadata.updated_by`, set to the request's `by`, on a
    feature of the request.
The scoped write guard keeps every other file of the model as it was; this check keeps every
other line of the spine as it was, read as data (the skill may lay out a changed entry again).

Output: {ok, problems: [..], planned: [ids], kept: [{feature, state}], changed: [ids]}
Exit 0 ok; 1 not ok (written); 2 bad input (nothing written). No git, no network.
"""

import argparse
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


def features(spine):
    return {f.get("id"): f for f in (spine or {}).get("features") or [] if isinstance(f, dict)}


def stamped(after, ids, by):
    """The features of the request whose entry now carries the request's stamp."""
    return {fid for fid, f in features(after).items()
            if fid in ids and by and isinstance(f.get("metadata"), dict)
            and f["metadata"].get("updated_by") == by}


def without_states(spine, ids):
    """The spine with each feature's `status` taken out, and the stamp
    (`metadata.updated_by`) taken out of the features in `ids`, so what is left must be equal."""
    out = copy.deepcopy(spine or {})
    for f in out.get("features") or []:
        if not isinstance(f, dict):
            continue
        f.pop("status", None)
        if f.get("id") in ids and isinstance(f.get("metadata"), dict):
            f["metadata"].pop("updated_by", None)
            if not f["metadata"]:
                f.pop("metadata")
    return out


def check(before, after, items, request):
    problems = []
    changes = {c["feature"]: c for c in items.get("state_changes") or []}
    kept = {k["feature"]: k["state"] for k in items.get("kept_states") or []}
    by = (request or {}).get("by")
    if request is not None:
        asked = [p.get("id") for p in request.get("parts") or []]
        if sorted(asked) != sorted(changes):
            problems.append(f"the request asks for {sorted(asked)}, the brief showed {sorted(changes)}")
        for p in request.get("parts") or []:
            if (p.get("kind"), p.get("mode"), p.get("status")) != ("feature", "update", "Planned") \
                    or set(p) - {"id", "kind", "mode", "status"}:
                problems.append(f"the request part {p!r} is not a feature set to Planned and nothing else")
    elif changes:
        problems.append("there are state changes to make, but no request was given")
    b, a = features(before), features(after)
    planned, changed = [], []
    for fid in sorted(set(b) | set(a)):
        was, now = (b.get(fid) or {}).get("status"), (a.get(fid) or {}).get("status")
        if was != now:
            changed.append(fid)
        if fid in changes:
            if now != "Planned":
                problems.append(f"{fid} was Unplanned and is taken into the plan, but reads {now!r}, not Planned")
            else:
                planned.append(fid)
        elif fid in kept:
            if now != kept[fid] or was != now:
                problems.append(f"{fid} was {kept[fid]} and must keep its state, but reads {now!r}")
        elif was != now:
            problems.append(f"{fid} is not one the plan sets to Planned, but its status moved from "
                            f"{was!r} to {now!r}")
    ids = stamped(after, set(changes), by)
    left, right = without_states(before, ids), without_states(after, ids)
    if left != right:
        keys = sorted(k for k in set(left) | set(right) if left.get(k) != right.get(k))
        problems.append("the spine changed in more than the features' status: " + ", ".join(keys))
    return {"ok": not problems, "problems": problems, "planned": planned,
            "kept": [{"feature": f, "state": s} for f, s in kept.items()], "changed": changed}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the spine after the plan set Planned.")
    ap.add_argument("--before", required=True)
    ap.add_argument("--spine", required=True)
    ap.add_argument("--work-items", required=True)
    ap.add_argument("--request")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        before = pc.read_yaml(args.before, "the spine at the start of the run")
        after = pc.read_yaml(args.spine, "the spine")
        items = pc.read_json(args.work_items, "work-items.json")
        request = (pc.read_json(args.request, "planned-request.json")
                   if args.request and os.path.isfile(args.request) else None)
        result = check(before, after, items, request)
    except (pc.Refused, ValueError, TypeError) as exc:
        sys.stderr.write(f"check_states.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, result)
    print(json.dumps({"ok": result["ok"], "problems": result["problems"]}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
