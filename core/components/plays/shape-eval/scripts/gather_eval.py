#!/usr/bin/env python3
"""gather_eval.py — gather the three inputs of each slice's eval, and copy them (C1, C8, C12).

    python3 gather_eval.py --plan-file <plans>/<id>.yaml --plans <plans> \
        --library <copy of steps-<kind>.yaml> [--library ...] [--tracker-file <json>] \
        --working <working> --out <working>inputs.json

For each epic node of the plan file that stands for a slice (`kind: epic`, `represents: <slice
id>`), it reads, and only reads:
  - the epic, from the tracker, and its feature-to-story map, in its order (the build order);
  - each story of the map, from the tracker: its "Scope of work" (Goals, Limits, Expectations)
    and its "Context guidance";
  - the slice's hidden file, found in `<plans>/<id>/evals/<slug>/failure-and-recovery.md` by
    the slice id of its first heading: its Surface line and each feature's failure conditions.
It never reads an ICE page, the usage guide, the code or the product model (C1). It copies the
epic, each story and the hidden file into `<working>inputs/`, and any eval files the slice
already has into `<working>inputs/existing/<slug>/` (the state before this run), so the agent
and the skill are given only those copies.

A slice is ready when its epic, its map, a "Scope of work" on each story, its hidden file, an
entry in it for each feature of the map, and a step library for its surface kind are all there.
A slice that is not ready gets `ready: false` and a `reason`, and no eval (C8, C12).

Writes inputs.json: {plan_id, intent_title, plans, slices: [{slice_id, slug, folder, epic,
epic_title, ready, reason, surface, surface_kind, library, stories: [{feature, issue, title,
goals, limits, expectations, context, path}], failures: {feature: [{id, text}]},
recovery_lines, hidden, existing: [file names], out_of_slice: [file names]}]}.
Exit 0 written (also when no slice is ready), 2 refused (no plan file, or no epic node).
"""

import argparse
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval_common as ec  # noqa: E402


def walk(nodes):
    for node in nodes or []:
        if isinstance(node, dict):
            yield node
            yield from walk(node.get("children"))


def find_hidden(plans, plan_id, slice_id):
    for path in sorted(glob.glob(os.path.join(plans, str(plan_id), "evals", "*", "failure-and-recovery.md"))):
        if ec.parse_hidden(ec.read_text(path, "a hidden file"))["slice_id"] == slice_id:
            return path
    return None


def gather(plan_file, plans, libraries, tracker, working):
    plan = ec.read_yaml(plan_file, "the plan file")
    if not isinstance(plan, dict):
        raise ec.Refused(f"no plan file at {plan_file}: run /shape-plan <intent> first")
    plan_id = plan.get("id")
    epics = [n for n in walk(plan.get("tree")) if n.get("kind") == "epic" and n.get("represents")]
    if not epics:
        raise ec.Refused("the plan file has no epic that stands for a slice: run /shape-plan first")
    inputs_dir = os.path.join(working, "inputs")
    if os.path.isdir(inputs_dir):
        shutil.rmtree(inputs_dir)
    os.makedirs(inputs_dir)
    out = {"plan_id": plan_id, "intent_title": plan.get("title"), "plans": plans, "slices": []}
    for node in epics:
        sl = {"slice_id": node["represents"], "slug": None, "folder": None, "epic": node.get("issue"),
              "epic_title": None, "ready": False, "reason": None, "surface": None, "surface_kind": None,
              "library": None, "stories": [], "failures": {}, "recovery_lines": [], "hidden": None,
              "existing": [], "out_of_slice": []}
        out["slices"].append(sl)
        epic = tracker.get(node["issue"]) if node.get("issue") else None
        if epic is None:
            sl["reason"] = f"the epic of slice {sl['slice_id']} is not in the tracker"
            continue
        sl["epic_title"] = epic["title"]
        ec.atomic_write(os.path.join(inputs_dir, f"epic-{epic['number']}.md"), epic["body"])
        fmap = ec.parse_map(epic["body"])
        hidden = find_hidden(plans, plan_id, sl["slice_id"])
        if hidden:
            sl["folder"] = os.path.dirname(hidden)
            sl["slug"] = os.path.basename(sl["folder"])
            copy = os.path.join(inputs_dir, f"hidden-{sl['slug']}.md")
            shutil.copyfile(hidden, copy)
            sl["hidden"] = copy
            h = ec.parse_hidden(ec.read_text(hidden, "the hidden file"))
            sl["surface"], sl["failures"], sl["recovery_lines"] = h["surface"], h["failures"], h["recovery_lines"]
            lib = ec.kind_of(h["surface"], [ec.load_library(p) | {"path": p} for p in libraries])
            if lib:
                sl["surface_kind"], sl["library"] = lib["kind"], lib["path"]
            existing_dir = os.path.join(inputs_dir, "existing", sl["slug"])
            for path in sorted(glob.glob(os.path.join(sl["folder"], "eval.*"))):
                os.makedirs(existing_dir, exist_ok=True)
                shutil.copyfile(path, os.path.join(existing_dir, os.path.basename(path)))
                sl["existing"].append(os.path.basename(path))
        for feature, number in fmap:
            story = tracker.get(number)
            if story is None:
                sl["stories"].append({"feature": feature, "issue": number, "missing": True})
                continue
            path = os.path.join(inputs_dir, f"story-{number}.md")
            ec.atomic_write(path, story["body"])
            parsed = ec.parse_story(story["body"])
            sl["stories"].append({"feature": feature, "issue": number, "title": story["title"],
                                  "goals": parsed["goals"], "limits": parsed["limits"],
                                  "expectations": parsed["expectations"], "context": parsed["context"],
                                  "has_scope": parsed["has_scope"], "path": path})
        in_map = {ec.story_file_name(f) for f, _ in fmap}
        sl["out_of_slice"] = [f for f in sl["existing"] if f.endswith(".feature.md") and f not in in_map]
        sl["reason"] = why_not_ready(sl, fmap)
        sl["ready"] = sl["reason"] is None
    return out


def why_not_ready(sl, fmap):
    if not fmap:
        return f"epic #{sl['epic']} has no feature-to-story map: run /shape-plan first"
    missing = [str(s["issue"]) for s in sl["stories"] if s.get("missing")]
    if missing:
        return "the tracker has no story #" + ", #".join(missing)
    no_scope = [str(s["issue"]) for s in sl["stories"] if not s.get("has_scope")]
    if no_scope:
        return "story #" + ", #".join(no_scope) + " has no Scope of work: run /shape-plan first"
    if not sl["hidden"]:
        return f"slice {sl['slice_id']} has no hidden file in the plan's evals folder: run /shape-slice first"
    no_entry = [f for f, _ in fmap if f not in sl["failures"]]
    if no_entry:
        return "the hidden file has no entry for " + ", ".join(no_entry) + ": run /shape-slice again"
    if not sl["surface_kind"]:
        return f"no step library for the surface '{sl['surface']}' yet"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gather and copy the inputs of each slice's eval.")
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--plans", required=True)
    ap.add_argument("--library", action="append", default=[], required=True)
    ap.add_argument("--tracker-file")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--working", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        if not os.path.isfile(args.plan_file):
            raise ec.Refused(f"no plan file at {args.plan_file}: run /shape-plan <intent> first")
        res = gather(args.plan_file, args.plans, args.library,
                     ec.open_tracker(args.tracker_file, args.config), args.working)
    except ec.Refused as exc:
        sys.stderr.write(f"gather_eval.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    ec.write_json(args.out, res)
    print(json.dumps({"ok": True, "ready": [s["slice_id"] for s in res["slices"] if s["ready"]],
                      "skipped": [{"slice": s["slice_id"], "reason": s["reason"]}
                                  for s in res["slices"] if not s["ready"]]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
