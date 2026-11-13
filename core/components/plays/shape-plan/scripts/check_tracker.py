#!/usr/bin/env python3
"""check_tracker.py — the tracker check (/shape-plan, D4; C3, C5, C13, C16, C17).

    python3 check_tracker.py --record <tracker-record.json> [--tracker-file <json>] \
        --out <working>/tracker-check.json

It reads each work item of the record back from the tracker (through platform_adapter.py, or
the --tracker-file fixture). `ok: true` only when:
  - each issue the record names exists;
  - the plan's epic has type Epic and no label, and its map is the map of the record (a
    `held_by` line names the epic that holds it);
  - each Feature issue of the map has type Feature, no label, the exact line
    "Represents: <feature id>", and the sections "Scope of work" and "Context guidance"; it is
    a sub-issue of the plan's epic, or, when `held_by`, of the epic that holds it;
  - the epic's sub-issues are the Feature issues of its map that it holds (and the items the
    plan already placed under it), no more;
  - each Feature issue the run opened again is open, and no Feature issue was filed for its
    feature (C17);
  - each Feature issue closed as completed by hand is still closed as completed, was not
    opened again, and no Feature issue was filed for its feature; it need not be under the
    epic, because the run writes nothing to it (C17);
  - no Feature issue was filed for a feature left out as Completed or Dropped (C16);
  - no body this run made holds the words "Fails if" or a recovery phrase (a found item's own
    lines are a person's, and are kept as they are);
  - no Story was filed by the run;
  - each moved-out item is open and is not a sub-issue of the epic.

Output: {ok, problems: [..], checked: [issue numbers]}
Exit 0 ok; 1 not ok (written); 2 bad input (nothing written). Reads only; writes nothing in the tracker.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


def check(rec, tracker, kept_subs=()):
    problems, checked = [], []
    made = {int(c["issue"]) for c in rec.get("created") or []}

    def fetch(number, what):
        it = tracker.get(number)
        checked.append(int(number))
        if it is None:
            problems.append(f"{what} #{number} is not in the tracker")
        return it

    def feature_shape(it, n, fid):
        if it["type"] != pc.FEATURE_TYPE:
            problems.append(f"Feature issue #{n} has type {it['type'] or 'none'}, not {pc.FEATURE_TYPE}")
        if it["labels"]:
            problems.append(f"Feature issue #{n} carries a label: {', '.join(it['labels'])}")
        if not pc.has_line(it["body"], pc.represents_line(fid)):
            problems.append(f"Feature issue #{n} has no line \"{pc.represents_line(fid)}\"")
        if n in made:
            for reason in pc.forbidden_in(it["body"]):
                problems.append(f"Feature issue #{n}: {reason}")

    epic_no = rec.get("epic")
    epic = fetch(epic_no, "the plan's epic") if epic_no is not None else None
    if epic_no is None:
        problems.append("the record names no epic for the plan")
    the_map = {f: int(n) for f, n in (rec.get("map") or {}).items()}
    held = {f: int(e) for f, e in (rec.get("held") or {}).items()}
    by_hand = {f: int(n) for f, n in (rec.get("closed_by_hand") or {}).items()}
    for fid, n in the_map.items():
        it = fetch(n, f"the Feature issue of {fid}")
        if it is None:
            continue
        if fid in by_hand:
            if not pc.finished(it):
                problems.append(f"Feature issue #{n} of {fid} was closed as completed by hand and must stay "
                                f"so, but it is {it['state']}")
            if not pc.has_line(it["body"], pc.represents_line(fid)):
                problems.append(f"Feature issue #{n} has no line \"{pc.represents_line(fid)}\"")
            continue
        feature_shape(it, n, fid)
        if fid in held:
            holder = tracker.get(held[fid])
            if holder is None or n not in holder["sub_issues"]:
                problems.append(f"Feature issue #{n} of {fid} is not under epic #{held[fid]}, which the "
                                "record says holds it")
            continue
        for sec in ("Scope of work", "Context guidance"):
            if not pc.has_heading(it["body"], sec):
                problems.append(f"Feature issue #{n} has no \"{sec}\" section")
        if epic is not None and n not in epic["sub_issues"]:
            problems.append(f"Feature issue #{n} of {fid} is not a sub-issue of epic #{epic_no}")
    if epic is not None:
        if epic["type"] != pc.EPIC_TYPE:
            problems.append(f"epic #{epic_no} has type {epic['type'] or 'none'}, not {pc.EPIC_TYPE}")
        if epic["labels"]:
            problems.append(f"epic #{epic_no} carries a label: {', '.join(epic['labels'])}")
        if pc.read_map(epic["body"]) != the_map or (pc.read_map(epic["body"], held=True) or {}) != held:
            problems.append(f"epic #{epic_no}'s map in the tracker is not the map of the record")
        if int(epic_no) in made:
            for reason in pc.forbidden_in(epic["body"]):
                problems.append(f"epic #{epic_no}: {reason}")
        own = {n for f, n in the_map.items() if f not in held} | {int(k) for k in kept_subs}
        for n in sorted(set(int(x) for x in epic["sub_issues"]) - own):
            it = tracker.get(n)
            title = f" \"{it['title']}\"" if it else ""
            problems.append(f"epic #{epic_no} holds #{n}{title}, which the plan does not place: file "
                            "it in its own place and take it off the epic (C13)")
    created_for = {c.get("represents") for c in rec.get("created") or []}
    for fid, n in by_hand.items():
        if fid in created_for:
            problems.append(f"the run filed a Feature issue for {fid}, whose Feature issue #{n} is closed "
                            "as completed by hand")
        if any(int(ro["issue"]) == n for ro in rec.get("reopened") or []):
            problems.append(f"the run opened Feature issue #{n} of {fid} again; it was closed as completed "
                            "by hand and stays closed")
    for ro in rec.get("reopened") or []:
        it = fetch(ro["issue"], f"the Feature issue of {ro.get('feature')} opened again")
        if it is not None and it["state"] != "open":
            problems.append(f"Feature issue #{ro['issue']} of {ro.get('feature')} was to open again, but it is "
                            f"{it['state']}")
        if ro.get("feature") in created_for:
            problems.append(f"the run filed a second Feature issue for {ro.get('feature')}, whose Feature "
                            f"issue #{ro['issue']} it opened again")
    for out in rec.get("left_out") or []:
        if out.get("feature") in created_for:
            problems.append(f"the run filed a Feature issue for {out.get('feature')}, which is left out "
                            f"({out.get('kind')})")
    for c in rec.get("created") or []:
        it = tracker.get(c["issue"])
        if it is not None and it["type"] == pc.STORY_TYPE:
            problems.append(f"the run filed a Story, #{c['issue']}; /shape-plan files no Stories")
    for mo in rec.get("moved_out") or []:
        it = fetch(mo["issue"], "the moved-out item")
        if it is not None and it["state"] != "open":
            problems.append(f"the moved-out item #{mo['issue']} is {it['state']}, not open")
        if epic is not None and int(mo["issue"]) in tracker.get(epic_no)["sub_issues"]:
            problems.append(f"the moved-out item #{mo['issue']} is still a sub-issue of epic #{epic_no}")
    for item in (rec.get("created") or []) + (rec.get("updated") or []):
        if int(item["issue"]) not in checked:
            fetch(item["issue"], f"the {item.get('kind', 'work item')}")
    return {"ok": not problems, "problems": problems, "checked": sorted(set(checked))}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the tracker against the run's record.")
    ap.add_argument("--record", required=True)
    ap.add_argument("--work-items", help="work-items.json, for the items the plan already placed under the epic")
    ap.add_argument("--tracker-file")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        rec = pc.read_json(args.record, "tracker-record.json")
        kept = []
        if args.work_items:
            items = pc.read_json(args.work_items, "work-items.json")
            kept = (items.get("epic") or {}).get("kept_subs") or []
        tracker = pc.open_tracker(args.tracker_file, args.config)
        result = check(rec, tracker, kept)
    except (pc.Refused, pc.TrackerError, ValueError, TypeError) as exc:
        sys.stderr.write(f"check_tracker.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, result)
    print(json.dumps({"ok": result["ok"], "problems": result["problems"]}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
