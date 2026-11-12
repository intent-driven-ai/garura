#!/usr/bin/env python3
"""write_work_items.py — write the epic and the Feature issues after the product owner's yes (/shape-plan, C3, C5, C6, C8, C13, C16, C17).

    python3 write_work_items.py --work-items <work-items.json> --drafts <drafts.json> \
        --gather <gather.json> --approval <approval.json> --plan-id <id> \
        [--tracker-file <json>] --out <working>/tracker-record.json

It refuses (exit 2, and writes nothing) unless approval.json reads yes with the person's typed
words, and unless the brief, work-items.json and drafts.json are still the files the person
saw (their sha256 is the one approval.json recorded). It also refuses when work-items.json is
not ok, when an item it must make or change has no draft, or an issue it must use is not in the
tracker. Then:
  - the plan's ONE epic to `make` becomes an issue of type Epic, with no label, in one write.
    Its body holds "Plan: <id>", what it delivers and the "Feature-to-story map";
  - each feature to `make` becomes an issue of type Feature, with no label and with the epic as
    its parent, in one write. Its body has the exact line "Represents: <feature id>", the
    sections "Scope of work" and "Context guidance", and the line "Written from: <the two ICE
    pages>", which this script takes from gather.json (the skill never sees a page path);
  - `reopen`: the same closed Feature issue is opened again, never a second one (C17); then
    it is handled like a found one below, or, when another epic holds it, it stays there;
  - `use` / `add-sections`: a found Feature issue gets only its missing sections, at the end of
    its body (every line of the body stays, checked before the write), the "Represents" line
    when it has none, type Feature when it has another, its labels taken off, and becomes a
    sub-issue of the epic when it is not one;
  - `held`, `completed`, `dropped`, `skip`: nothing is written; a held Feature issue keeps its
    epic and its map line names that epic; a Completed or Dropped feature is left out of the
    plan, and the tracker is not read for it (C16);
  - a used epic gets type Epic when it has another type or none, and its labels taken off; its
    map section is written again only when a line changes (every other line stays);
  - each feature node in `move_out` is taken off the epic's sub-issues and stays open.
No Story is filed. A second run with nothing new writes nothing.

The record is written after every tracker write, not only at the end. When a write fails, the
record keeps every issue made before it, reads `ok: false` and names the `failed` step; the
play still writes the plan file from it, so the next run finds those issues and makes no copy.

Record:
    {ok, plan_id, approval_at, epic, slices: [ids], created: [{issue, kind, represents, title, state}],
     updated: [{issue, kind, represents, changes: [..], lines_kept}],
     reopened: [{issue, feature, closed_as}], moved_out: [{issue, feature, epic}],
     features: {feature: issue}, held: {feature: epic}, map: {feature: issue},
     titles: {issue: title}, left_out: [{feature, issue, reason, kind}],
     skipped: [{feature, reason, issue}], failed, error}

Exit 0 written; 1 the tracker failed part way (the record reads `ok: false`); 2 refused
(nothing written).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

MAKES = ("make",)


class Step(Exception):
    """A tracker write failed; `step` says which."""

    def __init__(self, step, error):
        super().__init__(error)
        self.step = step


def scope_lines(scope):
    out = ["## Scope of work", "", "Goals:"] + [f"- {g}" for g in scope.get("goals") or []]
    out += ["", "Limits:"] + [f"- {x}" for x in scope.get("limits") or []]
    out += ["", "Expectations:"] + [f"- {x}" for x in scope.get("expectations") or []]
    return out


def guidance_lines(guide):
    return ["## Context guidance", "",
            f"- Read: {guide.get('read', '')}", f"- Never read: {guide.get('never_read', '')}",
            f"- Persona: {guide.get('persona', '')}", f"- In and out: {guide.get('in_out', '')}"]


def feature_body(fid, draft, pages):
    lines = [pc.represents_line(fid), ""]
    lines += scope_lines(draft.get("scope_of_work") or {}) + [""]
    lines += guidance_lines(draft.get("context_guidance") or {}) + [""]
    lines.append("Written from: " + "; ".join(pages))
    return "\n".join(lines) + "\n"


def epic_body(epic, plan_id, pairs, held):
    lines = [f"Plan: {plan_id}", "", epic.get("delivers") or epic.get("title") or "", ""]
    return "\n".join(lines + pc.map_lines(pairs, held)) + "\n"


def append_lines(body, extra):
    lines = (body or "").rstrip("\n").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines + ([""] if lines else []) + extra) + "\n"


def precheck(items, drafts, tracker):
    drafted = {d.get("feature"): d for d in drafts.get("features") or [] if isinstance(d, dict)}
    epic = items.get("epic") or {}
    if epic.get("action") == "make" and not (drafts.get("epic") or {}).get("title"):
        raise pc.Refused("the plan's epic has no drafted title")
    if epic.get("action") == "use" and tracker.get(epic.get("issue")) is None:
        raise pc.Refused(f"the tracker has no epic #{epic.get('issue')}")
    for f in items.get("features") or []:
        needs_draft = f["action"] in MAKES + ("add-sections",) or (
            f["action"] == "reopen" and f.get("missing") and f.get("held_by") is None)
        if needs_draft and f["feature"] not in drafted:
            raise pc.Refused(f"the drafts have no Feature issue for {f['feature']}")
        if f["action"] in ("use", "add-sections", "reopen") and tracker.get(f["issue"]) is None:
            raise pc.Refused(f"the tracker has no Feature issue #{f['issue']}")
    for mo in items.get("move_out") or []:
        if tracker.get(mo["issue"]) is None:
            raise pc.Refused(f"the tracker has no issue #{mo['issue']} to take off the epic")
    return drafted


class Writer:
    """Each tracker write goes through do(), which writes the record right after it."""

    def __init__(self, tracker, rec, out):
        self.tracker, self.rec, self.out = tracker, rec, out

    def save(self):
        pc.write_json(self.out, self.rec)

    def do(self, step, fn, *args):
        try:
            result = fn(*args)
        except pc.TrackerError as exc:
            raise Step(step, str(exc))
        self.save()
        return result


def fix_item(w, it, type_, changes, what):
    if it["type"] != type_:
        w.do(f"set the type of {what} #{it['number']}", w.tracker.set_type, it["number"], type_)
        changes.append(f"type set to {type_}")
    if it["labels"]:
        w.do(f"take the labels off {what} #{it['number']}", w.tracker.remove_labels, it["number"], it["labels"])
        changes.append("labels taken off: " + ", ".join(it["labels"]))


def write_plan(w, items, drafted, drafts, pages, plan_id):
    tracker, rec = w.tracker, w.rec
    features = items.get("features") or []
    made = {}

    def keep_map():
        rec["map"] = {f: n for f, n in pc.map_pairs(features, made)}

    epic, epic_changes = items["epic"], []
    if epic["action"] == "make":
        de = drafts.get("epic") or {}
        number = w.do("make the plan's epic", tracker.create, de["title"],
                      epic_body(de, plan_id, [], {}), pc.EPIC_TYPE, None)
        rec["created"].append({"issue": number, "kind": "epic", "represents": None,
                               "title": de["title"], "state": "open"})
        rec["titles"][str(number)] = de["title"]
    else:
        number = int(epic["issue"])
        rec["titles"][str(number)] = tracker.get(number)["title"]
    rec["epic"] = number
    keep_map()
    w.save()
    subs = tracker.get(number)["sub_issues"]
    for f in features:
        fid, act = f["feature"], f["action"]
        if act == "skip":
            rec["skipped"].append({"feature": fid, "reason": f.get("reason"), "issue": f.get("issue")})
            continue
        if act in ("completed", "dropped"):
            rec["left_out"].append({"feature": fid, "issue": None, "reason": f.get("reason"),
                                    "kind": act})
            continue
        if act == "reopen":
            w.do(f"open Feature issue #{f['issue']} of {fid} again", tracker.reopen, int(f["issue"]))
            rec["reopened"].append({"issue": int(f["issue"]), "feature": fid, "closed_as": f.get("closed_as")})
            w.save()
        if act == "held" or (act == "reopen" and f.get("held_by") is not None):
            rec["held"][fid] = int(f["held_by"])
            rec["features"][fid] = int(f["issue"])
            rec["titles"][str(f["issue"])] = f.get("title") or fid
            continue
        if act in MAKES:
            d = drafted[fid]
            n = w.do(f"file the Feature issue of {fid}", tracker.create, d["title"],
                     feature_body(fid, d, pages.get(fid) or []), pc.FEATURE_TYPE, number)
            rec["created"].append({"issue": n, "kind": "feature", "represents": fid, "title": d["title"],
                                   "state": "open"})
            rec["titles"][str(n)] = d["title"]
            made[fid] = n
            rec["features"][fid] = n
            keep_map()
            w.save()
            continue
        it = tracker.get(f["issue"])
        changes, body = [], it["body"]
        if act == "add-sections" or (act == "reopen" and f.get("missing")):
            d = drafted[fid]
            for sec in f.get("missing") or []:
                if not pc.has_heading(body, sec):
                    extra = (scope_lines(d.get("scope_of_work") or {}) if sec == "Scope of work"
                             else guidance_lines(d.get("context_guidance") or {}))
                    body = append_lines(body, extra)
                    changes.append(f"section added: {sec}")
        if not pc.has_line(body, pc.represents_line(fid)):
            body = append_lines(body, [pc.represents_line(fid)])
            changes.append("line added: Represents")
        if body != it["body"]:
            if not pc.lines_kept(it["body"], body):
                raise Step(f"change the Feature issue of {fid}",
                           f"Feature issue #{it['number']} would lose a line a person wrote; nothing is written to it")
            w.do(f"change the body of Feature issue #{it['number']}", tracker.set_body, it["number"], body)
        fix_item(w, it, pc.FEATURE_TYPE, changes, "Feature issue")
        if it["number"] not in subs:
            w.do(f"make Feature issue #{it['number']} a sub-issue of epic #{number}",
                 tracker.add_sub, number, it["number"])
            epic_changes.append(f"sub-issue added: #{it['number']}")
        rec["titles"][str(it["number"])] = it["title"]
        rec["features"][fid] = it["number"]
        if changes:
            rec["updated"].append({"issue": it["number"], "kind": "feature", "represents": fid,
                                   "changes": changes, "lines_kept": True})
        w.save()
    pairs = pc.map_pairs(features, made)
    it = tracker.get(number)
    body = it["body"]
    if pc.read_map(body) != dict(pairs) or (pc.read_map(body, held=True) or {}) != rec["held"]:
        body = pc.with_map(body, pairs, rec["held"])
        if epic["action"] == "use":
            epic_changes.append("feature-to-story map written")
    if body != it["body"]:
        w.do(f"write the map of epic #{number}", tracker.set_body, number, body)
    if epic["action"] == "use":
        fix_item(w, it, pc.EPIC_TYPE, epic_changes, "epic")
    for mo in items.get("move_out") or []:
        if int(mo["issue"]) in tracker.get(number)["sub_issues"]:
            w.do(f"take #{mo['issue']} off epic #{number}", tracker.remove_sub, number, int(mo["issue"]))
            epic_changes.append(f"sub-issue taken off: #{mo['issue']}")
        rec["moved_out"].append({"issue": int(mo["issue"]), "feature": mo["feature"], "epic": number})
        w.save()
    if epic_changes:
        rec["updated"].append({"issue": number, "kind": "epic", "represents": None,
                               "changes": epic_changes, "lines_kept": True})
    keep_map()
    w.save()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the plan's epic and Feature issues after the person's yes.")
    ap.add_argument("--work-items", required=True)
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--gather", required=True)
    ap.add_argument("--approval", required=True)
    ap.add_argument("--plan-id", required=True)
    ap.add_argument("--tracker-file")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        ok, _, reason = pc.approval_is_yes(args.approval)
        if not ok:
            raise pc.Refused(f"no tracker write without the person's yes: {reason}")
        ok, reason = pc.approval_matches(args.approval, args.work_items, args.drafts)
        if not ok:
            raise pc.Refused(f"no tracker write: {reason}")
        items = pc.read_json(args.work_items, "work-items.json")
        drafts = pc.read_json(args.drafts, "drafts.json")
        gather = pc.read_json(args.gather, "gather.json")
        if not items.get("ok", False):
            raise pc.Refused("work-items.json is not ok (a problem or a duplicate); the person must decide first")
        pages = {f["id"]: f.get("ice_pages") or [] for sl in gather.get("slices") or []
                 for f in sl.get("features") or []}
        tracker = pc.open_tracker(args.tracker_file, args.config)
        drafted = precheck(items, drafts, tracker)
    except (pc.Refused, pc.TrackerError) as exc:
        sys.stderr.write(f"write_work_items.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    approval = pc.read_json(args.approval, "approval.json")
    rec = {"ok": True, "plan_id": str(args.plan_id), "approval_at": approval.get("at"), "epic": None,
           "slices": [s.get("id") for s in items.get("slices") or []],
           "created": [], "updated": [], "reopened": [], "moved_out": [], "features": {}, "held": {},
           "map": {}, "titles": {}, "left_out": [], "skipped": [], "failed": None, "error": None}
    w = Writer(tracker, rec, args.out)
    try:
        write_plan(w, items, drafted, drafts, pages, args.plan_id)
        tracker.save()
    except Step as exc:
        rec.update(ok=False, failed=exc.step, error=str(exc))
        w.save()
        sys.stderr.write(f"write_work_items.py: stopped at '{exc.step}': {exc}\n")
        print(json.dumps({"ok": False, "failed": exc.step, "reason": str(exc), "out": args.out}))
        return 1
    w.save()
    print(json.dumps({"ok": True, "out": args.out, "created": len(rec["created"]),
                      "updated": len(rec["updated"]), "reopened": len(rec["reopened"]),
                      "moved_out": len(rec["moved_out"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
