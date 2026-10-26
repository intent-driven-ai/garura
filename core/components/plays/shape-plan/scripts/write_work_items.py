#!/usr/bin/env python3
"""write_work_items.py — write the epics and stories after the product owner's yes (/shape-plan, C3–C6, C8, C12, C13).

    python3 write_work_items.py --work-items <work-items.json> --drafts <drafts.json> \
        --gather <gather.json> --approval <approval.json> --plan-id <id> \
        [--tracker-file <json>] --out <working>/tracker-record.json

It refuses (exit 2, and writes nothing) unless approval.json reads yes with the person's typed
words, and unless the brief, work-items.json and drafts.json are still the files the person
saw (their sha256 is the one approval.json recorded). It also refuses when an item it must
make or change has no draft, or an issue it must use is not in the tracker. Then, for each
slice:
  - the epic to `make` becomes an issue of type Epic, with no label, in one write. Its body
    holds "Represents: <slice id>", "Plan: <id>", what it delivers and the "Feature-to-story
    map";
  - each story to `make` becomes an issue of type Story, with no label and with the epic as
    its parent, in one write. Its body has the line "Represents: <feature id>", the line
    "Plan: <id>", the sections "Scope of work" and "Context guidance", and the line "Written
    from: <the two ICE pages>", which this script takes from gather.json (the skill never sees
    a page path);
  - each story to `add-sections` gets only its missing sections, at the end of its body;
    every line of the body stays, in its order (checked before the write);
  - a used story gets type Story when it has another type or none, its labels taken off, the
    line "Represents: <feature id>" at the end when it has none, and becomes a sub-issue of
    its epic when it is not one;
  - a used epic gets type Epic when it has another type or none, its labels taken off, and
    the "Represents" line when it has none; an epic's map section is written again only when
    a line changes (every other line of its body stays);
  - each story in `move_out` is taken off the epic's sub-issues (and so off the map) and stays
    open. Nothing is deleted.
A second run with nothing new writes nothing.

The record is written after every tracker write, not only at the end. When a write fails, the
record keeps every issue made before it, reads `ok: false` and names the `failed` step; the
play still writes the plan file from it, so the next run finds those issues and makes no copy.

Record:
    {ok, plan_id, approval_at, created: [{issue, kind, represents, title}],
     updated: [{issue, kind, represents, changes: [..], lines_kept}],
     moved_out: [{issue, feature, epic}], epics: {slice: issue}, stories: {feature: issue},
     maps: {slice: {feature: issue}}, titles: {issue: title}, skipped: [{feature, reason, issue}],
     failed, error}

Exit 0 written; 1 the tracker failed part way (the record reads `ok: false`); 2 refused
(nothing written).
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


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


def story_body(fid, story, plan_id, pages):
    lines = [f"Represents: {fid}", f"Plan: {plan_id}", ""]
    lines += scope_lines(story.get("scope_of_work") or {}) + [""]
    lines += guidance_lines(story.get("context_guidance") or {}) + [""]
    lines.append("Written from: " + "; ".join(pages))
    return "\n".join(lines) + "\n"


def epic_body(sid, epic, plan_id, pairs):
    lines = [f"Represents: {sid}", f"Plan: {plan_id}", "", epic.get("delivers") or epic.get("title") or "", ""]
    return "\n".join(lines + pc.map_lines(pairs)) + "\n"


def append_lines(body, extra):
    lines = (body or "").rstrip("\n").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines + ([""] if lines else []) + extra) + "\n"


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


def write_slice(w, sl, d, pages, plan_id):
    tracker, rec = w.tracker, w.rec
    sid = sl["slice"]
    drafted = {s.get("feature"): s for s in d.get("stories") or [] if isinstance(s, dict)}
    made = {}

    def keep_map():
        rec["maps"][sid] = {f: n for f, n in pc.map_pairs(sl, made)}

    epic = sl["epic"]
    epic_changes = []
    if epic["action"] == "make":
        de = d.get("epic") or {}
        number = w.do(f"make the epic of {sid}", tracker.create, de["title"],
                      epic_body(sid, de, plan_id, []), pc.EPIC_TYPE, None)
        rec["created"].append({"issue": number, "kind": "epic", "represents": sid, "title": de["title"]})
        rec["titles"][str(number)] = de["title"]
    else:
        number = int(epic["issue"])
        rec["titles"][str(number)] = tracker.get(number)["title"]
    rec["epics"][sid] = number
    rec["others"][sid] = [int(o["issue"]) for o in epic.get("others") or []]
    keep_map()
    w.save()
    subs = tracker.get(number)["sub_issues"]
    for st in sl.get("stories") or []:
        fid, act = st["feature"], st["action"]
        if act == "skip":
            rec["skipped"].append({"feature": fid, "reason": st.get("reason"), "issue": st.get("issue")})
            if st.get("issue") is not None:
                rec["stories"][fid] = int(st["issue"])
            continue
        if act == "make":
            ds = drafted[fid]
            n = w.do(f"make the story of {fid}", tracker.create, ds["title"],
                     story_body(fid, ds, plan_id, pages.get(fid) or []), pc.STORY_TYPE, number)
            made[fid] = n
            rec["created"].append({"issue": n, "kind": "story", "represents": fid, "title": ds["title"]})
            rec["titles"][str(n)] = ds["title"]
            rec["stories"][fid] = n
            keep_map()
            w.save()
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
                raise Step(f"change the story of {fid}",
                           f"story #{it['number']} would lose a line a person wrote; nothing is written to it")
            w.do(f"change the body of story #{it['number']}", tracker.set_body, it["number"], body)
        fix_item(w, it, pc.STORY_TYPE, changes, "story")
        if it["number"] not in subs:
            w.do(f"make story #{it['number']} a sub-issue of epic #{number}", tracker.add_sub, number, it["number"])
            epic_changes.append(f"sub-issue added: #{it['number']}")
        rec["titles"][str(it["number"])] = it["title"]
        rec["stories"][fid] = it["number"]
        if changes:
            rec["updated"].append({"issue": it["number"], "kind": "story", "represents": fid,
                                   "changes": changes, "lines_kept": True})
            w.save()
    for st in sl.get("stories") or []:
        if st["action"] == "skip" and st.get("issue") is not None and int(st["issue"]) not in subs:
            w.do(f"make story #{st['issue']} a sub-issue of epic #{number}", tracker.add_sub, number, int(st["issue"]))
            epic_changes.append(f"sub-issue added: #{st['issue']}")
    pairs = pc.map_pairs(sl, made)
    it = tracker.get(number)
    body = it["body"]
    if not pc.has_line(body, f"Represents: {sid}"):
        body = append_lines(body, [f"Represents: {sid}"])
        epic_changes.append("line added: Represents")
    if pc.read_map(body) != dict(pairs):
        body = pc.with_map(body, pairs)
        if epic["action"] == "use":
            epic_changes.append("feature-to-story map written")
    if body != it["body"]:
        w.do(f"write the map of epic #{number}", tracker.set_body, number, body)
    if epic["action"] == "use":
        fix_item(w, it, pc.EPIC_TYPE, epic_changes, "epic")
    for mo in sl.get("move_out") or []:
        if int(mo["issue"]) in tracker.get(number)["sub_issues"]:
            w.do(f"take story #{mo['issue']} off epic #{number}", tracker.remove_sub, number, int(mo["issue"]))
            epic_changes.append(f"sub-issue taken off: #{mo['issue']}")
        rec["moved_out"].append({"issue": int(mo["issue"]), "feature": mo["feature"], "epic": number})
        w.save()
    if epic_changes:
        rec["updated"].append({"issue": number, "kind": "epic", "represents": sid,
                               "changes": epic_changes, "lines_kept": True})
    keep_map()
    w.save()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write the epics and stories after the person's yes.")
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
        by_slice = precheck(items, drafts, tracker)
    except (pc.Refused, pc.TrackerError) as exc:
        sys.stderr.write(f"write_work_items.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    approval = pc.read_json(args.approval, "approval.json")
    rec = {"ok": True, "plan_id": str(args.plan_id), "approval_at": approval.get("at"),
           "created": [], "updated": [], "moved_out": [], "epics": {}, "stories": {}, "maps": {},
           "others": {},
           "titles": {}, "skipped": [], "failed": None, "error": None}
    w = Writer(tracker, rec, args.out)
    try:
        for sl in items.get("slices") or []:
            write_slice(w, sl, by_slice[sl["slice"]], pages, args.plan_id)
        tracker.save()
    except Step as exc:
        rec.update(ok=False, failed=exc.step, error=str(exc))
        w.save()
        sys.stderr.write(f"write_work_items.py: stopped at '{exc.step}': {exc}\n")
        print(json.dumps({"ok": False, "failed": exc.step, "reason": str(exc), "out": args.out}))
        return 1
    w.save()
    print(json.dumps({"ok": True, "out": args.out, "created": len(rec["created"]),
                      "updated": len(rec["updated"]), "moved_out": len(rec["moved_out"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
