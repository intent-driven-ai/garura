#!/usr/bin/env python3
"""check_plan.py — the plan check (/shape-plan, D1; C1, C3, C4, C5, C6, C9).

    python3 check_plan.py --plan-file <plans>/<id>.yaml --gather <gather.json> \
        --record <tracker-record.json> --out <working>/plan-check.json

`ok: true` only when:
  - the plan file exists, and its `id` is the plan's ID;
  - each slice of gather.json has exactly one epic node (`represents: <slice id>`), with the
    issue the record names for that slice;
  - each ready feature of the slice has exactly one story node under that epic node;
  - no story node under the epic stands for a feature outside its slice;
  - each epic's map in the record names the same story for each feature as the tree, and the
    tree has no story node the map leaves out;
  - the plan file holds no "Fails if" line, the words "Fails if", or a recovery phrase.
Features that are not ready are listed in `skipped`, with their reasons; they do not fail
the check.

Output: {ok, problems: [..], skipped: [{slice, feature, reason}], slices: [{slice, epic, stories}]}
Exit 0 ok; 1 not ok (written); 2 bad input (nothing written). No git, no network.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


def check(plan_path, gather, rec):
    problems, skipped, slices = [], [], []
    plan = pc.load_plan(plan_path)
    if plan is None:
        return {"ok": False, "problems": [f"there is no plan file at {plan_path}"], "skipped": [], "slices": []}
    if str(plan.get("id")) != str(gather.get("plan_id")):
        problems.append(f"the plan file's id is {plan.get('id')!r}, not {gather.get('plan_id')}")
    tree = plan.get("tree") or []
    for sl in gather.get("slices") or []:
        sid = sl["id"]
        features = {f["id"]: f for f in sl.get("features") or []}
        epics = pc.marked(tree, sid)
        if len(epics) != 1:
            problems.append(f"slice {sid} has {len(epics)} epic nodes in the plan file, not one")
            continue
        node = epics[0]
        want = (rec.get("epics") or {}).get(sid)
        if want is None or int(node.get("issue") or -1) != int(want):
            problems.append(f"the epic node of {sid} is #{node.get('issue')}, the record says #{want}")
        kids = [k for k in pc.children(node) if k.get("represents")]
        tree_map = {}
        for k in kids:
            fid = str(k["represents"])
            if fid not in features:
                problems.append(f"story node #{k.get('issue')} under the epic of {sid} stands for "
                                f"{fid}, which is not a feature of the slice")
                continue
            if fid in tree_map:
                problems.append(f"{fid} has two story nodes under the epic of {sid}")
            tree_map[fid] = int(k.get("issue") or -1)
        for fid, f in features.items():
            if not f.get("ready"):
                skipped.append({"slice": sid, "feature": fid, "reason": f.get("reason")})
                continue
            if fid not in tree_map:
                problems.append(f"the ready feature {fid} has no story node under the epic of {sid}")
        rec_map = {f: int(n) for f, n in ((rec.get("maps") or {}).get(sid) or {}).items()}
        if rec_map != tree_map:
            problems.append(f"the epic's map of {sid} and the plan file's tree disagree: "
                            f"map {rec_map}, tree {tree_map}")
        slices.append({"slice": sid, "epic": node.get("issue"), "stories": tree_map})
    for reason in pc.forbidden_in(pc.read_text(plan_path)):
        problems.append(f"the plan file: {reason}")
    return {"ok": not problems, "problems": problems, "skipped": skipped, "slices": slices}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the plan file against the slices and the tracker record.")
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--gather", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        gather = pc.read_json(args.gather, "gather.json")
        rec = pc.read_json(args.record, "tracker-record.json")
        result = check(args.plan_file, gather, rec)
    except (pc.Refused, ValueError, TypeError) as exc:
        sys.stderr.write(f"check_plan.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.write_json(args.out, result)
    print(json.dumps({"ok": result["ok"], "problems": result["problems"]}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
