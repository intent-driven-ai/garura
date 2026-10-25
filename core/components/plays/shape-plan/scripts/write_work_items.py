#!/usr/bin/env python3
"""write_work_items.py — write the epics and stories after the product owner's yes (/shape-plan, C3–C6, C8, C12, C13).

    python3 write_work_items.py --work-items <work-items.json> --drafts <drafts.json> \
        --approval <approval.json> --plan-id <id> [--tracker-file <json>] \
        --out <working>/tracker-record.json

It refuses (exit 2, and writes nothing) unless approval.json reads yes with the person's typed
words, and unless every item it must make or change has its draft and every issue it must use
is in the tracker. Then, for each slice:
  - each story to `make` becomes an issue of type Story, with no label. Its body has the line
    "Represents: <feature id>", the line "Plan: <id>", the sections "Scope of work" and
    "Context guidance", and the line "Written from: <the two ICE pages>";
  - each story to `add-sections` gets only its missing sections, at the end of its body;
    every line of the body stays, in its order (checked before the write);
  - a used story gets type Story when it has another type or none, its labels taken off, and
    the line "Represents: <feature id>" at the end when it has none;
  - the epic to `make` becomes an issue of type Feature, with no label, its body holding
    "Represents: <slice id>", "Plan: <id>", what it delivers and the "Feature-to-story map";
  - a used epic gets type Feature when it has another type or none, its labels taken off, the
    "Represents" line when it has none, and its map section written again only when a line
    changes (every other line of its body stays);
  - each story of the map becomes a sub-issue of its epic; each story in `move_out` is taken
    off the epic's sub-issues (and so off the map) and stays open. Nothing is deleted.
A second run with nothing new writes nothing.

Record:
    {ok, plan_id, approval_at, created: [{issue, kind, represents, title}],
     updated: [{issue, kind, represents, changes: [..], lines_kept}],
     moved_out: [{issue, feature, epic}], epics: {slice: issue}, stories: {feature: issue},
     maps: {slice: {feature: issue}}, titles: {issue: title}, skipped: [{feature, reason, issue}]}

Exit 0 written; 1 the tracker failed part way (the record lists what was done, `ok: false`;
a --tracker-file is then left as it was); 2 refused (nothing written).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


def scope_lines(scope):
    out = ["## Scope of work", "", "Goals:"] + [f"- {g}" for g in scope.get("goals") or []]
    out += ["", "Limits:"] + [f"- {x}" for x in scope.get("limits") or []]
    out += ["", "Expectations:"] + [f"- {x}" for x in scope.get("expectations") or []]
    return out


def guidance_lines(guide):
    return ["## Context guidance", "",
            f"- Read: {guide.get('read', '')}", f"- Never read: {guide.get('never_read', '')}",
            f"- Persona: {guide.get('persona', '')}", f"- In and out: {guide.get('in_out', '')}"]


def story_body(fid, story, plan_id):
    lines = [f"Represents: {fid}", f"Plan: {plan_id}", ""]
    lines += scope_lines(story.get("scope_of_work") or {}) + [""]
    lines += guidance_lines(story.get("context_guidance") or {}) + [""]
    lines.append("Written from: " + "; ".join(story.get("written_from") or []))
    return "\n".join(lines) + "\n"


def epic_body(sid, epic, plan_id, pairs):
    lines = [f"Represents: {sid}", f"Plan: {plan_id}", "", epic.get("delivers") or epic.get("title") or "", ""]
    return "\n".join(lines + pc.map_lines(pairs)) + "\n"


def append_lines(body, extra):
    lines = (body or "").rstrip("\n").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines + ([""] if lines else []) + extra) + "\n"


def fix_item(tracker, it, type_, changes):
    if it["type"] != type_:
        tracker.set_type(it["number"], type_)
        changes.append(f"type set to {type_}")
    if it["labels"]:
        tracker.remove_labels(it["number"], it["labels"])
        changes.append("labels taken off: " + ", ".join(it["labels"]))


def precheck(items, drafts, tracker):
    by_slice = {d.get("slice"): d for d in drafts.get("slices") or [] if isinstance(d, dict)}
    for sl in items.get("slices") or []:
        d = by_slice.get(sl.get("slice"))
        if d is None:
            raise pc.Refused(f"the drafts have no entry for slice {sl.get('slice')}")
        stories = {s.get("feature"): s for s in d.get("stories") or [] if isinstance(s, dict)}
        if sl["epic"]["action"] == "make" and not (d.get("epic") or {}).get("title"):
            raise pc.Refused(f"the epic of slice {sl['slice']} has no drafted title")
        if sl["epic"]["action"] == "use" and tracker.get(sl["epic"]["issue"]) is None:
            raise pc.Refused(f"the tracker has no epic #{sl['epic']['issue']}")
        for st in sl.get("stories") or []:
            if st["action"] in ("make", "add-sections") and st["feature"] not in stories:
                raise pc.Refused(f"the drafts have no story for {st['feature']}")
            if st["action"] in ("use", "add-sections") and tracker.get(st["issue"]) is None:
                raise pc.Refused(f"the tracker has no story #{st['issue']}")
        for mo in sl.get("move_out") or []:
            if tracker.get(mo["issue"]) is None:
                raise pc.Refused(f"the tracker has no story #{mo['issue']} to move out")
    return by_slice


def write(items, by_slice, tracker, plan_id, rec):
    for sl in items.get("slices") or []:
        sid, d = sl["slice"], by_slice[sl["slice"]]
        drafted = {s.get("feature"): s for s in d.get("stories") or [] if isinstance(s, dict)}
        made = {}
        for st in sl.get("stories") or []:
            fid, act = st["feature"], st["action"]
            if act == "skip":
                rec["skipped"].append({"feature": fid, "reason": st.get("reason"), "issue": st.get("issue")})
                if st.get("issue") is not None:
                    rec["stories"][fid] = int(st["issue"])
                continue
            if act == "make":
                ds = drafted[fid]
                n = tracker.create(ds["title"], story_body(fid, ds, plan_id), pc.STORY_TYPE)
                made[fid] = n
                rec["created"].append({"issue": n, "kind": "story", "represents": fid, "title": ds["title"]})
                rec["titles"][str(n)] = ds["title"]
                rec["stories"][fid] = n
                continue
            it = tracker.get(st["issue"])
            changes, body = [], it["body"]
            if act == "add-sections":
                ds = drafted[fid]
                for sec in st.get("missing") or []:
                    if not pc.has_heading(body, sec):
                        extra = (scope_lines(ds.get("scope_of_work") or {}) if sec == "Scope of work"
                                 else guidance_lines(ds.get("context_guidance") or {}))
                        body = append_lines(body, extra)
                        changes.append(f"section added: {sec}")
            if not pc.has_line(body, f"Represents: {fid}"):
                body = append_lines(body, [f"Represents: {fid}"])
                changes.append("line added: Represents")
            if body != it["body"]:
                if not pc.lines_kept(it["body"], body):
                    raise pc.TrackerError(f"story #{it['number']} would lose a line a person wrote; nothing is written to it")
                tracker.set_body(it["number"], body)
            fix_item(tracker, it, pc.STORY_TYPE, changes)
            rec["titles"][str(it["number"])] = it["title"]
            rec["stories"][fid] = it["number"]
            if changes:
                rec["updated"].append({"issue": it["number"], "kind": "story", "represents": fid,
                                       "changes": changes, "lines_kept": True})
        pairs = pc.map_pairs(sl, made)
        epic = sl["epic"]
        changes = []
        if epic["action"] == "make":
            de = d.get("epic") or {}
            number = tracker.create(de["title"], epic_body(sid, de, plan_id, pairs), pc.EPIC_TYPE)
            rec["created"].append({"issue": number, "kind": "epic", "represents": sid, "title": de["title"]})
            rec["titles"][str(number)] = de["title"]
        else:
            it = tracker.get(epic["issue"])
            number, body = it["number"], it["body"]
            if not pc.has_line(body, f"Represents: {sid}"):
                body = append_lines(body, [f"Represents: {sid}"])
                changes.append("line added: Represents")
            if pc.read_map(body) != dict(pairs):
                body = pc.with_map(body, pairs)
                changes.append("feature-to-story map written")
            if body != it["body"]:
                tracker.set_body(number, body)
            fix_item(tracker, it, pc.EPIC_TYPE, changes)
            rec["titles"][str(number)] = it["title"]
        subs = tracker.get(number)["sub_issues"]
        for fid, n in pairs:
            if n not in subs:
                tracker.add_sub(number, n)
                if epic["action"] == "use":
                    changes.append(f"sub-issue added: #{n}")
        for mo in sl.get("move_out") or []:
            if int(mo["issue"]) in subs:
                tracker.remove_sub(number, int(mo["issue"]))
                changes.append(f"sub-issue taken off: #{mo['issue']}")
            rec["moved_out"].append({"issue": int(mo["issue"]), "feature": mo["feature"], "epic": number})
        if changes:
            rec["updated"].append({"issue": number, "kind": "epic", "represents": sid,
                                   "changes": changes, "lines_kept": True})
        rec["epics"][sid] = number
        rec["maps"][sid] = {f: n for f, n in pairs}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the epics and stories after the person's yes.")
    ap.add_argument("--work-items", required=True)
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--approval", required=True)
    ap.add_argument("--plan-id", required=True)
    ap.add_argument("--tracker-file")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    ok, _, reason = pc.approval_is_yes(args.approval)
    try:
        if not ok:
            raise pc.Refused(f"no tracker write without the person's yes: {reason}")
        items = pc.read_json(args.work_items, "work-items.json")
        drafts = pc.read_json(args.drafts, "drafts.json")
        if not items.get("ok", False):
            raise pc.Refused("work-items.json is not ok (a problem or a duplicate); the person must decide first")
        tracker = pc.open_tracker(args.tracker_file, args.config)
        by_slice = precheck(items, drafts, tracker)
    except (pc.Refused, pc.TrackerError) as exc:
        sys.stderr.write(f"write_work_items.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    approval = pc.read_json(args.approval, "approval.json")
    rec = {"ok": True, "plan_id": str(args.plan_id), "approval_at": approval.get("at"),
           "created": [], "updated": [], "moved_out": [], "epics": {}, "stories": {}, "maps": {},
           "titles": {}, "skipped": []}
    try:
        write(items, by_slice, tracker, args.plan_id, rec)
        tracker.save()
    except (pc.TrackerError, pc.Refused) as exc:
        rec.update(ok=False, error=str(exc), saved=not args.tracker_file)
        pc.write_json(args.out, rec)
        sys.stderr.write(f"write_work_items.py: stopped part way: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc), "out": args.out}))
        return 1
    pc.write_json(args.out, rec)
    print(json.dumps({"ok": True, "out": args.out, "created": len(rec["created"]),
                      "updated": len(rec["updated"]), "moved_out": len(rec["moved_out"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
