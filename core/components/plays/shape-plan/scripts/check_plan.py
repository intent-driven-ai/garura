#!/usr/bin/env python3
"""check_plan.py — the plan check (/shape-plan, D1; C1, C3, C5, C6, C9, C15, C16).

    python3 check_plan.py --plan-file <plans>/<id>.yaml --gather <gather.json> \
        --record <tracker-record.json> --out <working>/plan-check.json

`ok: true` only when:
  - the plan file exists, its `id` is the plan's ID, and its first line names the business
    intent (`intent: bi-<id>`), with its `title`;
  - its `epic:` mark is the epic the record names, and the tree's top holds exactly one epic
    node, with that issue;
  - its `slices` list holds each slice of gather.json once, each with a status a person can set
    (Not Started, In Progress, Done or Dropped);
  - each feature the record puts in the plan (its map) has exactly one feature node under the
    epic node, with the same issue, and a `held_by` feature's node names its epic;
  - no feature node stands for a feature that is in no slice of the plan, or that is left out
    (built) or skipped (not ready);
  - the plan file holds no "Fails if" line, the words "Fails if", or a recovery phrase.
Features that are not ready are listed in `skipped`, and features left out of the plan in
`left_out`, with their reasons: built (their Feature issue is closed as completed, or was filed
closed) or not planned (their Feature issue is closed as not planned). They do not fail the
check; a node for one of them does.

Output: {ok, problems: [..], skipped: [{feature, reason}], left_out: [{feature, issue, reason}],
         epic, features: {feature: issue}}
Exit 0 ok; 1 not ok (written); 2 bad input (nothing written). No git, no network.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

SLICE_STATUSES = ("Not Started", "In Progress", "Done", "Dropped")


def check(plan_path, gather, rec):
    problems = []
    plan = pc.load_plan(plan_path)
    if plan is None:
        return {"ok": False, "problems": [f"there is no plan file at {plan_path}"], "skipped": [],
                "left_out": [], "epic": None, "features": {}}
    plan_id = str(gather.get("plan_id"))
    if str(plan.get("id")) != plan_id:
        problems.append(f"the plan file's id is {plan.get('id')!r}, not {plan_id}")
    first = next((ln for ln in pc.read_text(plan_path).splitlines() if ln.strip()), "")
    if first.strip() != f"intent: bi-{plan_id}" or not plan.get("title"):
        problems.append(f"the plan file does not name its business intent at the top "
                        f"(intent: bi-{plan_id}, then its title)")
    want_epic = rec.get("epic")
    if want_epic is None or str(plan.get("epic")) != str(want_epic):
        problems.append(f"the plan file's epic mark is {plan.get('epic')!r}, the record says {want_epic}")
    tree = plan.get("tree") or []
    epics = [n for n in tree if str(n.get("kind") or "") == "epic"]
    if len(epics) != 1:
        problems.append(f"the plan file has {len(epics)} epic nodes at the top of its tree, not one")
    node = next((n for n in epics if str(n.get("issue")) == str(want_epic)), None)
    if epics and node is None:
        problems.append(f"no epic node of the tree has the issue #{want_epic}")
    slice_ids = [sl["id"] for sl in gather.get("slices") or []]
    listed = [s for s in plan.get("slices") or [] if isinstance(s, dict)]
    for sid in slice_ids:
        mine = [s for s in listed if str(s.get("id")) == sid]
        if len(mine) != 1:
            problems.append(f"the slices list holds {sid} {len(mine)} times, not once")
        elif mine[0].get("status") not in SLICE_STATUSES:
            problems.append(f"slice {sid} has the status {mine[0].get('status')!r}, not one of "
                            + ", ".join(SLICE_STATUSES))
    in_slices = {f["id"]: f for sl in gather.get("slices") or [] for f in sl.get("features") or []}
    skipped = [{"feature": fid, "reason": f.get("reason")} for fid, f in in_slices.items()
               if not f.get("ready")]
    left_out = [dict(x) for x in rec.get("left_out") or [] if isinstance(x, dict)]
    out_ids = {x["feature"] for x in skipped} | {x.get("feature") for x in left_out}
    tree_map = {}
    held = {str(k): int(v) for k, v in (rec.get("held") or {}).items()}
    for k in pc.children(node) if node else []:
        fid = str(k.get("represents") or "")
        if not fid:
            continue
        if fid not in in_slices:
            problems.append(f"feature node #{k.get('issue')} stands for {fid}, which is in no slice of the plan")
            continue
        if fid in out_ids:
            problems.append(f"{fid} is left out of the plan (built, not planned or not ready), but has a feature node")
            continue
        if fid in tree_map:
            problems.append(f"{fid} has two feature nodes under the epic")
        tree_map[fid] = int(k.get("issue") or -1)
        if fid in held and str(k.get("held_by")) != str(held[fid]):
            problems.append(f"the node of {fid} does not say held_by: {held[fid]}")
    rec_map = {f: int(n) for f, n in (rec.get("map") or {}).items()}
    for fid in rec_map:
        if fid not in tree_map:
            problems.append(f"the feature {fid} has no feature node under the epic")
    for fid, f in in_slices.items():
        if f.get("ready") and fid not in out_ids and fid not in rec_map:
            problems.append(f"the ready feature {fid} is not in the plan and is not named as left out")
    if rec_map != tree_map:
        problems.append(f"the epic's map and the plan file's tree disagree: map {rec_map}, tree {tree_map}")
    for reason in pc.forbidden_in(pc.read_text(plan_path)):
        problems.append(f"the plan file: {reason}")
    return {"ok": not problems, "problems": problems, "skipped": skipped, "left_out": left_out,
            "epic": node.get("issue") if node else None, "features": tree_map}


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
