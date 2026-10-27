#!/usr/bin/env python3
"""check_tracker.py — the tracker check (/shape-plan, D4; C4, C5, C12, C13).

    python3 check_tracker.py --record <tracker-record.json> [--tracker-file <json>] \
        --out <working>/tracker-check.json

It reads each work item of the record back from the tracker (through platform_adapter.py, or
the --tracker-file fixture). `ok: true` only when:
  - each issue the record names exists;
  - each epic has type Epic and each story type Story, and none has a label;
  - each epic's sub-issues are its stories: the stories of its map, no more and no fewer;
  - each story's body has the sections "Scope of work" and "Context guidance" and the line
    "Represents: <feature id>"; each epic's body has "Represents: <slice id>" and its map;
    and no body this run made holds the words "Fails if" or a recovery phrase (a found item's
    own lines are a person's, and are kept as they are);
  - each moved-out story is open and is not a sub-issue of its epic.

Output: {ok, problems: [..], checked: [issue numbers]}
Exit 0 ok; 1 not ok (written); 2 bad input (nothing written). Reads only; writes nothing in the tracker.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


def check(rec, tracker):
    problems, checked = [], []
    made = {int(c["issue"]) for c in rec.get("created") or []}

    def fetch(number, what):
        it = tracker.get(number)
        checked.append(int(number))
        if it is None:
            problems.append(f"{what} #{number} is not in the tracker")
        return it

    for sid, epic_no in (rec.get("epics") or {}).items():
        epic = fetch(epic_no, "the epic")
        stories = {f: int(n) for f, n in ((rec.get("maps") or {}).get(sid) or {}).items()}
        for fid, n in stories.items():
            st = fetch(n, f"the story of {fid}")
            if st is None:
                continue
            if st["type"] != pc.STORY_TYPE:
                problems.append(f"story #{n} has type {st['type'] or 'none'}, not {pc.STORY_TYPE}")
            if st["labels"]:
                problems.append(f"story #{n} carries a label: {', '.join(st['labels'])}")
            for sec in ("Scope of work", "Context guidance"):
                if not pc.has_heading(st["body"], sec):
                    problems.append(f"story #{n} has no \"{sec}\" section")
            if not pc.has_line(st["body"], f"Represents: {fid}"):
                problems.append(f"story #{n} has no line \"Represents: {fid}\"")
            if n in made:
                for reason in pc.forbidden_in(st["body"]):
                    problems.append(f"story #{n}: {reason}")
        if epic is None:
            continue
        if epic["type"] != pc.EPIC_TYPE:
            problems.append(f"epic #{epic_no} has type {epic['type'] or 'none'}, not {pc.EPIC_TYPE}")
        if epic["labels"]:
            problems.append(f"epic #{epic_no} carries a label: {', '.join(epic['labels'])}")
        if not pc.has_line(epic["body"], f"Represents: {sid}"):
            problems.append(f"epic #{epic_no} has no line \"Represents: {sid}\"")
        if pc.read_map(epic["body"]) != stories:
            problems.append(f"epic #{epic_no}'s map in the tracker is not the map of the record")
        if int(epic_no) in made:
            for reason in pc.forbidden_in(epic["body"]):
                problems.append(f"epic #{epic_no}: {reason}")
        subs = {int(n) for n in epic["sub_issues"]}
        for fid, n in stories.items():
            if n not in subs:
                problems.append(f"story #{n} of {fid} is not a sub-issue of epic #{epic_no}")
        for n in sorted(subs - set(stories.values())):
            it = tracker.get(n)
            title = f" \"{it['title']}\"" if it else ""
            problems.append(f"epic #{epic_no} holds #{n}{title}, which is not a story of its slice: "
                            "file it in its own place and take it off the epic (C13)")
    for mo in rec.get("moved_out") or []:
        st = fetch(mo["issue"], "the moved-out story")
        if st is not None and st["state"] != "open":
            problems.append(f"the moved-out story #{mo['issue']} is {st['state']}, not open")
        epic = tracker.get(mo.get("epic")) if mo.get("epic") is not None else None
        if epic is not None and int(mo["issue"]) in epic["sub_issues"]:
            problems.append(f"the moved-out story #{mo['issue']} is still a sub-issue of epic #{mo['epic']}")
    for item in (rec.get("created") or []) + (rec.get("updated") or []):
        if int(item["issue"]) not in checked:
            fetch(item["issue"], f"the {item.get('kind', 'work item')}")
    return {"ok": not problems, "problems": problems, "checked": sorted(set(checked))}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the tracker against the run's record.")
    ap.add_argument("--record", required=True)
    ap.add_argument("--tracker-file")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        rec = pc.read_json(args.record, "tracker-record.json")
        tracker = pc.open_tracker(args.tracker_file, args.config)
        result = check(rec, tracker)
    except (pc.Refused, pc.TrackerError, ValueError, TypeError) as exc:
        sys.stderr.write(f"check_tracker.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, result)
    print(json.dumps({"ok": result["ok"], "problems": result["problems"]}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
