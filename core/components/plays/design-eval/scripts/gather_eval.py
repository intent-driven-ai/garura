#!/usr/bin/env python3
"""gather_eval.py — gather the inputs of the plan's one eval, and copy them (C1, C8, C12).

    python3 gather_eval.py --plan-file <plans>/<id>.yaml --plans <plans> \
        --library <copy of steps-<kind>.yaml> [--library ...] [--tracker-file <json>] \
        --working <working> --out <working>inputs.json

It reads, and only reads:
  - the plan file: its `epic: <n>` mark and its Slices list (`slices`, each slice by its id, with its
    status);
  - the plan's epic, from the tracker, and its feature-to-story map, in its order: one line for
    each feature of the plan, to its Feature issue (`(under Epic #<n>)` marks one that sits under
    another plan's epic, `held_by`; a plan-file item of kind `feature` with `held_by` marks it too);
  - each Feature issue of the map, from the tracker: its type (Feature, when the tracker says), its
    exact line `Represents: <feature id>`, its "Scope of work" (Goals, Limits, Expectations) and its
    "Context guidance";
  - the hidden file of each slice of the Slices list, found by the slice id of its first heading in
    `<plans>/<home>/evals/<slug>/failure-and-recovery.md`, where <home> is the plan of the slice's
    first intent, which need not be this plan: its Surface line, its features in the order of its
    entries (the slice's build order) and each feature's failure conditions.
It never reads an ICE page, the usage guide, the code or the product model (C1). It copies the epic,
each Feature issue and each hidden file into `<working>inputs/`, and the eval files the plan already
has (`<plans>/<id>/evals/eval.*`) into `<working>inputs/existing/` (the state before this run), so
the agent and the skill are given only those copies.

A slice whose status in the Slices list is Dropped is left out (C14): it is listed in `dropped`, it
gets no section, its missing hidden file blocks nothing, and a map feature that only dropped slices
hold (its hidden file names it, or a dropped slice has no hidden file to tell) is listed in
`left_out` with why, and gets no feature file. A live slice's features in the eval are its hidden
file's entries that the map names, in that order. A feature that sits in two live slices is written
once, with the step library and the hidden-file entry of the first slice in the Slices list that
holds it (C12). The plan is ready when its epic, its map, each Feature issue (of type Feature, with
its Represents line and a Scope of work), each live slice's hidden file, a slice for each feature of
the map, and a step library for each live slice's surface kind are all there. A plan that is not
ready gets `ready: false` and each `reasons` line, and no eval (C8, C12).

Writes inputs.json: {plan_id, intent_title, plans, folder (<plans>/<id>/evals), epic, epic_title,
ready, reasons, dropped: [{slice_id, hidden}], left_out: [{feature, issue, why}], slices: [{slice_id, slug, hidden_folder, hidden, surface, surface_kind, library,
features, reason}], features: [{feature, issue, title, type, held_by, goals, limits, expectations,
context, has_scope, has_represents, path, slices, slice, surface_kind, library, failures}],
recovery_lines, existing: [file names], out_of_plan: [file names]}.
Exit 0 written (also when the plan is not ready), 2 refused (no plan file).
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

FEATURE_TYPE = "Feature"


def walk(nodes):
    for node in nodes or []:
        if isinstance(node, dict):
            yield node
            yield from walk(node.get("children"))


DROPPED = "dropped"


def slice_list(plan):
    """The plan's Slices list, in its order: [(slice id, status)]. An item is a slice id, or a mapping with
    `id` (or `slice`) and `status`."""
    out, seen = [], set()
    for item in plan.get("slices") or []:
        sid = (item.get("id") or item.get("slice")) if isinstance(item, dict) else item
        status = str(item.get("status") or "") if isinstance(item, dict) else ""
        if sid and str(sid) not in seen:
            seen.add(str(sid))
            out.append((str(sid), status))
    return out


def intent_title(plan):
    for key in ("title", "business_intent", "intent"):
        v = plan.get(key)
        if isinstance(v, dict):
            v = v.get("title")
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def find_hidden(plans, plan_id, slice_id):
    """The slice's hidden file, in the evals folder of the plan for its first intent (which need not be this
    plan): this plan's folder first, then every other plan's."""
    own = sorted(glob.glob(os.path.join(plans, str(plan_id), "evals", "*", "failure-and-recovery.md")))
    rest = [p for p in sorted(glob.glob(os.path.join(plans, "*", "evals", "*", "failure-and-recovery.md")))
            if p not in own]
    for path in own + rest:
        if ec.parse_hidden(ec.read_text(path, "a hidden file"))["slice_id"] == slice_id:
            return path
    return None


def gather(plan_file, plans, libraries, tracker, working):
    plan = ec.read_yaml(plan_file, "the plan file")
    if not isinstance(plan, dict):
        raise ec.Refused(f"no plan file at {plan_file}: run /shape-plan <intent> first")
    plan_id = plan.get("id")
    inputs_dir = os.path.join(working, "inputs")
    if os.path.isdir(inputs_dir):
        shutil.rmtree(inputs_dir)
    os.makedirs(inputs_dir)
    folder = os.path.join(plans, str(plan_id), "evals")
    out = {"plan_id": plan_id, "intent_title": intent_title(plan), "plans": plans, "folder": folder,
           "epic": plan.get("epic"), "epic_title": None, "ready": False, "reasons": [], "slices": [],
           "features": [], "recovery_lines": [], "existing": [], "out_of_plan": [], "dropped": [], "left_out": []}
    reasons = out["reasons"]
    libs = [ec.load_library(p) | {"path": p} for p in libraries]

    # the hidden file of each slice the plan holds
    listed = slice_list(plan)
    if not listed:
        reasons.append("the plan file has no Slices list: run /shape-plan first")
    dropped_entries, dropped_unknown = set(), False
    for sid, status in listed:
        if status.strip().lower() == DROPPED:  # C14: a dropped slice is left out; its hidden file is read only to
            hidden = find_hidden(plans, plan_id, sid)  # know which features only it holds, and never copied
            if hidden:
                dropped_entries.update(ec.parse_hidden(ec.read_text(hidden, "a hidden file"))["features"])
            else:
                dropped_unknown = True
            out["dropped"].append({"slice_id": sid, "hidden": bool(hidden)})
            continue

        sl = {"slice_id": sid, "slug": None, "hidden_folder": None, "hidden": None, "surface": None,
              "surface_kind": None, "library": None, "features": [], "entries": [], "failures": {},
              "reason": None}
        out["slices"].append(sl)
        hidden = find_hidden(plans, plan_id, sid)
        if not hidden:
            sl["reason"] = f"slice {sid} has no hidden file: run /design-slice first"
            continue
        sl["hidden_folder"] = os.path.dirname(hidden)
        sl["slug"] = os.path.basename(sl["hidden_folder"])
        copy = os.path.join(inputs_dir, f"hidden-{sl['slug']}.md")
        shutil.copyfile(hidden, copy)
        sl["hidden"] = copy
        h = ec.parse_hidden(ec.read_text(hidden, "the hidden file"))
        sl["surface"], sl["entries"], sl["failures"] = h["surface"], h["features"], h["failures"]
        for line in h["recovery_lines"]:
            if line not in out["recovery_lines"]:
                out["recovery_lines"].append(line)
        lib = ec.kind_of(h["surface"], libs)
        if lib:
            sl["surface_kind"], sl["library"] = lib["kind"], lib["path"]
        else:
            sl["reason"] = f"slice {sid}: no step library for the surface '{sl['surface']}' yet"

    # the epic and its map
    fmap = []
    epic = tracker.get(out["epic"]) if out["epic"] else None
    if not out["epic"]:
        reasons.append("the plan file has no `epic:` mark: run /shape-plan first")
    elif epic is None:
        reasons.append(f"the plan's epic #{out['epic']} is not in the tracker")
    else:
        out["epic_title"] = epic["title"]
        ec.atomic_write(os.path.join(inputs_dir, f"epic-{epic['number']}.md"), epic["body"])
        fmap = ec.parse_map(epic["body"])
        if not fmap:
            reasons.append(f"epic #{out['epic']} has no feature-to-story map: run /shape-plan first")
    held_in_plan = {str(n.get("represents")): n.get("held_by") for n in walk(plan.get("tree"))
                    if n.get("kind") == "feature" and n.get("held_by")}

    # each Feature issue of the map, joined to the slices that hold its feature
    for line in fmap:
        fid, number = line["feature"], line["issue"]
        holders = [sl for sl in out["slices"] if fid in sl["entries"]]
        if not holders and (fid in dropped_entries or dropped_unknown):
            why = ("only a dropped slice holds it" if fid in dropped_entries
                   else "no live slice holds it, and a dropped slice has no hidden file to tell")
            out["left_out"].append({"feature": fid, "issue": number, "why": why})
            continue
        feat = {"feature": fid, "issue": number, "title": None, "type": None,
                "held_by": line["held_by"] or held_in_plan.get(fid), "goals": [], "limits": [],
                "expectations": [], "context": [], "has_scope": False, "has_represents": False, "path": None,
                "slices": [sl["slice_id"] for sl in holders], "slice": None, "surface_kind": None,
                "library": None, "failures": []}
        out["features"].append(feat)
        if holders:
            first = holders[0]
            feat["slice"], feat["surface_kind"], feat["library"] = first["slice_id"], first["surface_kind"], first["library"]
            feat["failures"] = first["failures"].get(fid, [])
        for sl in holders:
            sl["features"].append(fid)
        issue = tracker.get(number)
        if issue is None:
            reasons.append(f"the tracker has no Feature issue #{number} for {fid}")
            continue
        path = os.path.join(inputs_dir, f"feature-{number}.md")
        ec.atomic_write(path, issue["body"])
        parsed = ec.parse_feature_issue(issue["body"])
        feat.update({"title": issue["title"], "type": issue.get("type"), "goals": parsed["goals"],
                     "limits": parsed["limits"], "expectations": parsed["expectations"],
                     "context": parsed["context"], "has_scope": parsed["has_scope"],
                     "has_represents": ec.has_line(issue["body"], f"Represents: {fid}"), "path": path})
    # each slice's features in its build order: the order of its hidden file's entries
    for sl in out["slices"]:
        sl["features"] = [f for f in sl["entries"] if f in sl["features"]]

    for f in out["features"]:
        if f["title"] is None:
            continue
        if f["type"] and f["type"] != FEATURE_TYPE:
            reasons.append(f"#{f['issue']} is of type {f['type']}, not a Feature issue")
        if not f["has_represents"]:
            reasons.append(f"Feature issue #{f['issue']} has no exact line 'Represents: {f['feature']}'")
        if not f["has_scope"]:
            reasons.append(f"Feature issue #{f['issue']} has no Scope of work: run /shape-plan first")
    for f in out["features"]:
        if not f["slices"]:
            reasons.append(f"{f['feature']} (Feature issue #{f['issue']}) is in no hidden file of a slice "
                           "the plan holds: run /design-slice again")
    reasons += [sl["reason"] for sl in out["slices"] if sl["reason"]]

    # the eval files the plan already has (the state before this run)
    existing_dir = os.path.join(inputs_dir, "existing")
    for path in sorted(glob.glob(os.path.join(folder, "eval.*"))):
        os.makedirs(existing_dir, exist_ok=True)
        shutil.copyfile(path, os.path.join(existing_dir, os.path.basename(path)))
        out["existing"].append(os.path.basename(path))
    in_map = {ec.feature_file_name(f["feature"]) for f in out["features"]}
    out["out_of_plan"] = [f for f in out["existing"] if f.endswith(".feature.md") and f not in in_map]
    for sl in out["slices"]:
        sl.pop("entries", None)
    out["ready"] = not reasons
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gather and copy the inputs of the plan's eval.")
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
    print(json.dumps({"ok": True, "ready": res["ready"], "reasons": res["reasons"],
                      "slices": [s["slice_id"] for s in res["slices"]],
                      "features": len(res["features"])}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
