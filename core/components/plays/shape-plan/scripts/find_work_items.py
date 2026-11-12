#!/usr/bin/env python3
"""find_work_items.py — find the plan's epic and each feature's work before any is made (/shape-plan, C3, C9, C13, C15, C16).

    python3 find_work_items.py --gather <gather.json> --plan-file <plans>/<id>.yaml \
        [--tracker-file <json>] --out <working>/work-items.json

The plan has ONE epic. It is `use` (with its issue) when the plan file has the mark
`epic: <issue>`, else `make`. A title is never compared, and no issue number is read from the
product model (ADR 068, ADR 069).

Each feature of the plan's slices is listed once, in the order the slices give, with the
slices that hold it. Its Feature issue is the issue a node of the plan file's tree marks with
`represents: <feature id>`; when no node marks it, it is the issue of type Feature, open or
closed, whose text has the exact line `Represents: <feature id>`, found through the tracker's
search (C3). Then:
  - two Feature issues name the feature → a duplicate: the run names both and stops (S15);
  - its Feature issue is closed as completed → `built`; closed as not planned →
    `not-planned`. Either way the feature is left out of the plan and nothing is written to its
    issue: no reopen, no move, no new issue (C16). The run goes on;
  - its ICE is not ready → `skip`, with its reason; nothing about it is searched or moved (C9);
  - its Feature issue is open → `use` (it has "Scope of work" and "Context guidance") or
    `add-sections` (`missing` names what it lacks); `attached` says whether it is a sub-issue
    of the plan's epic, and `parent` names a parent it would leave. When it sits under another
    epic, it is `held`, with `held_by: <epic>`: it is shown, never moved (C3);
  - it has no Feature issue → the old-work search (C15): an open Story that names the feature
    → `make-and-move`, with `move_stories` (each with the parent it leaves); only finished old
    work (closed as completed) → `make-closed`, left out of the plan; nothing → `make`. An old
    issue of type Feature with no exact `Represents:` line is listed in `old.old_groups` and
    left as it is. One old story that two features claim is a problem.
  - `move_out` lists each feature node under the epic's node in the plan file whose feature is
    in no slice of the plan;
  - `misplaced` lists each sub-issue of a used epic that is neither a Feature issue of the plan
    nor an item the plan file's tree places, with its title (C13, #879); `kept_subs` lists the
    items the tree places there (a chore, for example), which the tracker check allows.
The tracker is only read here (through platform_adapter.py, or the --tracker-file fixture).

Output:
    {ok, plan_file_exists, problems: [..], duplicates: [{kind, represents, issues}],
     misplaced: [{epic, issue, title}],
     epic: {action, issue, title, type, labels, map, sub_issues, kept_subs},
     slices: [{id, name, features: [feature ids]}],
     features: [{feature, name, slices, action, issue, source, parent, held_by, missing, reason,
                 title, type, labels, represents_line, attached, old, move_stories}],
     move_out: [{issue, feature, title}]}

Exit 0 written; 1 written, with a problem, a duplicate or misplaced work: the run shows them to
the person and stops before any tracker write; 2 bad input (nothing written).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

SECTIONS = ("Scope of work", "Context guidance")
NO_OLD = {"open_stories": [], "done_stories": [], "old_groups": []}


def plan_features(gather):
    """Each feature of the plan's slices once, in slice order, with the slices that hold it."""
    out, by_id = [], {}
    for sl in gather.get("slices") or []:
        for f in sl.get("features") or []:
            if f["id"] not in by_id:
                by_id[f["id"]] = dict(f, slices=[])
                out.append(by_id[f["id"]])
            by_id[f["id"]]["slices"].append(sl["id"])
    return out


def feature_nodes(tree, fid):
    return [n for n in pc.marked(tree, fid) if str(n.get("kind") or "") != "epic"]


def holder(tracker, parent, epic_no):
    """The epic that holds the issue when its parent is another epic, else None."""
    if not parent or (epic_no is not None and int(parent["number"]) == int(epic_no)):
        return None
    it = tracker.get(parent["number"])
    if it is None or (parent.get("title") and it["title"] != parent["title"]):
        return int(parent["number"])  # cannot tell what holds it: never move it unasked
    return int(parent["number"]) if it.get("type") == pc.EPIC_TYPE else None


def blank(f):
    return {"feature": f["id"], "name": f.get("name") or f["id"], "slices": f["slices"],
            "action": "make", "issue": None, "source": None, "parent": None, "held_by": None,
            "missing": [], "reason": "", "title": None, "type": None, "labels": [],
            "represents_line": False, "attached": False, "old": NO_OLD, "move_stories": []}


def find(gather, plan, tracker):
    tree = (plan or {}).get("tree") or []
    problems, duplicates, misplaced = [], [], []
    epic = {"action": "make", "issue": None, "title": None, "type": None, "labels": [],
            "map": None, "sub_issues": [], "kept_subs": []}
    epic_node = None
    if plan and plan.get("epic") is not None:
        epic.update(action="use", issue=int(plan["epic"]))
        it = tracker.get(epic["issue"])
        if it is None:
            problems.append(f"the plan file names #{epic['issue']} as its epic, but the tracker has "
                            "no such issue")
        else:
            epic.update(title=it["title"], type=it["type"], labels=it["labels"],
                        map=pc.read_map(it["body"]), sub_issues=it["sub_issues"])
        epic_node = next((n for n in tree if str(n.get("issue")) == str(epic["issue"])), None)
    features = plan_features(gather)
    items = []
    for f in features:
        fid, item = f["id"], blank(f)
        nodes = feature_nodes(tree, fid)
        it = None
        if len(nodes) > 1:
            duplicates.append({"kind": "feature node", "represents": fid,
                               "issues": [n.get("issue") for n in nodes]})
        if nodes:
            it = tracker.get(nodes[0].get("issue"))
            item.update(issue=nodes[0].get("issue"), source="plan file")
            if it is None:
                problems.append(f"the plan file names #{nodes[0].get('issue')} as the Feature issue "
                                f"of {fid}, but the tracker has no such issue")
                item["action"] = "use"
                items.append(item)
                continue
        else:
            found = pc.feature_issues(tracker, fid)
            if len(found) > 1:
                nums = [i["number"] for i in found]
                duplicates.append({"kind": "Feature issue", "represents": fid, "issues": nums})
                problems.append(f"two Feature issues name {fid}: "
                                + " and ".join(f"#{n}" for n in nums)
                                + ". A person keeps one and gives the other another type or line")
                item.update(action="duplicate", reason="two Feature issues name it")
                items.append(item)
                continue
            if found:
                it = found[0]
                item.update(issue=it["number"], source="tracker")
        if it is not None:
            item.update(title=it["title"], type=it["type"], labels=it["labels"],
                        represents_line=pc.has_line(it["body"], pc.represents_line(fid)))
            if it["state"] != "open":
                if pc.finished(it):
                    item.update(action="built",
                                reason=f"built: its Feature issue #{it['number']} is closed as completed")
                else:
                    item.update(action="not-planned",
                                reason=f"not planned: its Feature issue #{it['number']} is closed as not planned")
                items.append(item)
                continue
        if not f.get("ready"):
            item.update(action="skip", reason=f.get("reason") or "its ICE is not ready")
            items.append(item)
            continue
        if it is not None:
            held = holder(tracker, it.get("parent"), epic["issue"])
            if held is not None:
                item.update(action="held", held_by=held, parent=it.get("parent"))
                items.append(item)
                continue
            missing = [s for s in SECTIONS if not pc.has_heading(it["body"], s)]
            attached = epic["issue"] is not None and int(it["number"]) in epic["sub_issues"]
            item.update(action="add-sections" if missing else "use", missing=missing,
                        attached=attached, parent=None if attached else it.get("parent"))
            items.append(item)
            continue
        old = pc.old_work(tracker, fid, f.get("name"))
        item["old"] = old
        done_groups = [g for g in old["old_groups"] if g["state"] != "open"]
        if old["open_stories"]:
            item.update(action="make-and-move", move_stories=old["open_stories"])
        elif old["done_stories"] or done_groups:
            item.update(action="make-closed",
                        reason="built: its old work is finished, so its Feature issue is filed "
                               "closed as completed")
        items.append(item)
    claimed = {}
    for item in items:
        for st in item["move_stories"]:
            claimed.setdefault(int(st["issue"]), []).append(item["feature"])
    for number, fids in sorted(claimed.items()):
        if len(fids) > 1:
            problems.append(f"the old story #{number} names more than one feature ({', '.join(fids)}): "
                            "a person says which feature it is for")
    plan_ids = {f["id"] for f in features}
    move_out = []
    if epic_node is not None:
        for k in pc.children(epic_node):
            rep = str(k.get("represents") or "")
            if rep and rep not in plan_ids:
                move_out.append({"issue": k.get("issue"), "feature": rep, "title": k.get("title")})
    if epic["action"] == "use":
        mine = {int(i["issue"]) for i in items if i.get("issue") is not None}
        placed = {int(n["issue"]) for n in pc.walk(tree) if str(n.get("issue") or "").isdigit()}
        placed -= {int(m["issue"]) for m in move_out if m.get("issue") is not None}
        epic["kept_subs"] = sorted(int(x) for x in epic["sub_issues"] if int(x) in placed - mine)
        own = mine | placed | {int(m["issue"]) for m in move_out if m.get("issue") is not None}
        for n in sorted(int(x) for x in epic["sub_issues"]):
            if n not in own:
                it = tracker.get(n)
                misplaced.append({"epic": epic["issue"], "issue": n, "title": it["title"] if it else None})
    slices = [{"id": sl["id"], "name": sl.get("name"),
               "features": [f["id"] for f in sl.get("features") or []]}
              for sl in gather.get("slices") or []]
    return {"ok": not problems and not duplicates and not misplaced,
            "plan_file_exists": plan is not None, "problems": problems, "duplicates": duplicates,
            "misplaced": misplaced, "epic": epic, "slices": slices, "features": items,
            "move_out": move_out}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find the plan's epic and each feature's work before any is made.")
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
