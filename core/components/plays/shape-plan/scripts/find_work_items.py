#!/usr/bin/env python3
"""find_work_items.py — find each epic and story before any is made (/shape-plan, C3, C4, C9, C12).

    python3 find_work_items.py --gather <gather.json> --plan-file <plans>/<id>.yaml \
        [--tracker-file <json>] --out <working>/work-items.json

A work item stands for a slice or a feature only when the plan file marks it so:
`represents: <slice id>` on the epic's node, `represents: <feature id>` on a story's node under
that epic. A title is never compared.

For each slice of gather.json:
  - the epic is `use` (with its issue) when a node of the tree has `represents: <slice id>`,
    else `make`;
  - each feature is `use` (its marked story has both "Scope of work" and "Context guidance"),
    `add-sections` (marked, but one of the two sections is missing; `missing` names it),
    `make` (no marked story), or `skip` (the feature is not ready; `reason` says why, and a
    marked story is left as it is);
  - `move_out` lists each marked story under the epic whose feature is no longer in the slice;
  - `misplaced` lists each sub-issue of a used epic that is neither a story of its slice nor a
    moved-out story, with its title: an epic stands for its slice, so such work is not its
    slice's (C13, #879).
The tracker is only read here (through platform_adapter.py, or the --tracker-file fixture).
For each used item it records its type, labels, title and whether a story is a sub-issue of
its epic, and for a used epic its feature-to-story map as its text holds it now, so the brief
can show each change the write will make.

Output:
    {ok, plan_file_exists, problems: [..], duplicates: [..],
     misplaced: [{slice, epic, issue, title}],
     slices: [{slice, epic: {action, issue, title, type, labels, represents_line, map},
               stories: [{feature, action, issue, missing, reason, title, type, labels,
                          represents_line, attached}],
               move_out: [{issue, feature, title}]}]}

Exit 0 written; 1 written, with a problem (a marked issue the tracker does not have), a
duplicate (two nodes stand for one slice, or for one feature in one epic) or misplaced work (a
sub-issue of an epic that is not its slice's): the run shows them to the person and stops
before any tracker write; 2 bad input (nothing written).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

SECTIONS = ("Scope of work", "Context guidance")


def tracker_facts(tracker, number, represents, problems, what):
    it = tracker.get(number) if number is not None else None
    if it is None:
        problems.append(f"the plan file names #{number} as the {what} for {represents}, "
                        "but the tracker has no such issue")
        return None
    return it


def find(gather, plan, tracker):
    tree = (plan or {}).get("tree") or []
    problems, duplicates, misplaced, out = [], [], [], []
    for sl in gather.get("slices") or []:
        sid = sl["id"]
        feature_ids = [f["id"] for f in sl.get("features") or []]
        epics = pc.marked(tree, sid)
        if len(epics) > 1:
            duplicates.append({"kind": "epic", "represents": sid, "kept": epics[0].get("issue"),
                               "copies": [e.get("issue") for e in epics[1:]]})
        node = epics[0] if epics else None
        epic = {"action": "make", "issue": None, "title": None, "type": None, "labels": [],
                "represents_line": False, "map": None}
        kids = pc.children(node) if node else []
        sub_issues = []
        if node is not None:
            epic.update(action="use", issue=node.get("issue"))
            it = tracker_facts(tracker, node.get("issue"), sid, problems, "epic")
            if it:
                epic.update(title=it["title"], type=it["type"], labels=it["labels"],
                            represents_line=pc.has_line(it["body"], f"Represents: {sid}"),
                            map=pc.read_map(it["body"]))
                sub_issues = it["sub_issues"]
        stories = []
        for f in sl.get("features") or []:
            fid = f["id"]
            mine = [k for k in kids if str(k.get("represents") or "") == fid]
            if len(mine) > 1:
                duplicates.append({"kind": "story", "represents": fid, "epic": epic["issue"],
                                   "kept": mine[0].get("issue"),
                                   "copies": [k.get("issue") for k in mine[1:]]})
            story = {"feature": fid, "action": "make", "issue": None, "missing": [], "reason": "",
                     "title": None, "type": None, "labels": [], "represents_line": False,
                     "attached": False}
            if mine:
                story["issue"] = mine[0].get("issue")
            if not f.get("ready"):
                story.update(action="skip", reason=f.get("reason") or "its ICE is not ready")
                stories.append(story)
                continue
            if mine:
                it = tracker_facts(tracker, story["issue"], fid, problems, "story")
                if it:
                    missing = [s for s in SECTIONS if not pc.has_heading(it["body"], s)]
                    story.update(action="add-sections" if missing else "use", missing=missing,
                                 title=it["title"], type=it["type"], labels=it["labels"],
                                 represents_line=pc.has_line(it["body"], f"Represents: {fid}"),
                                 attached=int(story["issue"]) in sub_issues)
                else:
                    story["action"] = "use"
            stories.append(story)
        move_out = []
        for k in kids:
            rep = str(k.get("represents") or "")
            if rep and rep not in feature_ids:
                move_out.append({"issue": k.get("issue"), "feature": rep, "title": k.get("title")})
        own = {int(s["issue"]) for s in stories if s.get("issue") is not None}
        own |= {int(m["issue"]) for m in move_out if m.get("issue") is not None}
        for n in sorted(int(x) for x in sub_issues):
            if n not in own:
                it = tracker.get(n)
                misplaced.append({"slice": sid, "epic": epic["issue"], "issue": n,
                                  "title": it["title"] if it else None})
        out.append({"slice": sid, "epic": epic, "stories": stories, "move_out": move_out})
    return {"ok": not problems and not duplicates and not misplaced,
            "plan_file_exists": plan is not None, "problems": problems, "duplicates": duplicates,
            "misplaced": misplaced, "slices": out}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find the epics and stories that already stand for a slice or a feature.")
    ap.add_argument("--gather", required=True)
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--tracker-file")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        gather = pc.read_json(args.gather, "gather.json")
        plan = pc.load_plan(args.plan_file)
        tracker = pc.open_tracker(args.tracker_file, args.config)
        result = find(gather, plan, tracker)
    except (pc.Refused, pc.TrackerError) as exc:
        sys.stderr.write(f"find_work_items.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, result)
    print(json.dumps({"ok": result["ok"], "out": args.out, "problems": result["problems"],
                      "duplicates": result["duplicates"], "misplaced": result["misplaced"]}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
