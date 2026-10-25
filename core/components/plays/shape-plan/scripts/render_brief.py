#!/usr/bin/env python3
"""render_brief.py — the one brief the product owner reads before any write (/shape-plan, C8, C9, C11).

    python3 render_brief.py --gather <gather.json> --work-items <work-items.json> \
        --drafts <drafts.json> --out <working>/brief.md

The brief is built from the run's records only, so no write can be left out of it:
  - what the run will write in the tracker: for each slice, the epic (make, use) and each
    story (make, use, add sections, move out), with the text a new item or a new section gets,
    and each type, label or sub-issue change on an item that exists;
  - the plan-file change: made or updated, each node it adds, each node it takes out;
  - each skipped feature, with its reason;
  - what the person types next: yes, change: <what>, or stop.

Exit 0 written; 2 bad input (nothing written). No git, no network.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402


def bullets(items):
    return [f"  - {i}" for i in items or []]


def story_text(story):
    scope = story.get("scope_of_work") or {}
    guide = story.get("context_guidance") or {}
    out = ["  - Goals:"] + ["  " + b for b in bullets(scope.get("goals"))]
    out += ["  - Limits:"] + ["  " + b for b in bullets(scope.get("limits"))]
    out += ["  - Expectations:"] + ["  " + b for b in bullets(scope.get("expectations"))]
    out += [f"  - Read: {guide.get('read', '')}", f"  - Never read: {guide.get('never_read', '')}",
            f"  - Persona: {guide.get('persona', '')}", f"  - In and out: {guide.get('in_out', '')}"]
    return out


def fix_lines(item, type_):
    out = []
    if item.get("type") != type_:
        out.append(f"set its type to {type_} (it is {item.get('type') or 'not set'} now)")
    if item.get("labels"):
        out.append("take off its labels: " + ", ".join(item["labels"]))
    return out


def render(gather, items, drafts):
    plan_id = gather.get("plan_id")
    drafts_by = {d.get("slice"): d for d in drafts.get("slices") or [] if isinstance(d, dict)}
    items_by = {s.get("slice"): s for s in items.get("slices") or []}
    lines = [f"# The plan for business intent #{plan_id}: {gather.get('intent_title', '')}", "",
             "This run makes the plan for this business intent, or brings it up to date: the plan "
             "file, one epic for each slice and one story for each feature. Nothing below is "
             "written yet. Read each write, then type yes to write all of it, change: <what> to "
             "have it drafted again, or stop to write nothing.", ""]
    lines += ["## What the run writes in the tracker", ""]
    adds, removes, skipped = [], [], []
    writes = 0
    for sl in gather.get("slices") or []:
        sid = sl["id"]
        it = items_by.get(sid) or {}
        d = drafts_by.get(sid) or {}
        epic, depic = it.get("epic") or {}, d.get("epic") or {}
        lines += [f"### Slice {sid}: {sl.get('name', '')}", ""]
        if epic.get("action") == "make":
            writes += 1
            lines += [f"- Make a new epic, type Feature, no label: \"{depic.get('title', '')}\"",
                      f"  - Delivers: {depic.get('delivers', '')}",
                      f"  - It says it represents {sid}, and holds the feature-to-story map."]
            adds.append(f"an epic node for {sid}")
        else:
            fixes = fix_lines(epic, pc.EPIC_TYPE)
            if not epic.get("represents_line"):
                fixes.append(f"add the line \"Represents: {sid}\" at the end of its text")
            pairs = pc.map_pairs(it)
            new_story = any(st.get("action") == "make" for st in it.get("stories") or [])
            if new_story or it.get("move_out") or epic.get("map") != dict(pairs):
                fixes.append("write its feature-to-story map: " + (", ".join(
                    f"{f} → #{n}" for f, n in pairs) or "no story yet")
                    + (", and a line for each new story" if new_story else ""))
            writes += bool(fixes)
            lines.append(f"- Use epic #{epic.get('issue')} \"{epic.get('title') or ''}\""
                         + (": " + "; ".join(fixes) + "." if fixes else ", as it is."))
        stories = {s.get("feature"): s for s in d.get("stories") or [] if isinstance(s, dict)}
        for st in it.get("stories") or []:
            fid, act = st.get("feature"), st.get("action")
            ds = stories.get(fid) or {}
            if act == "make":
                writes += 1
                lines += [f"- Make a new story for {fid}, type Story, no label, a sub-issue of the "
                          f"epic: \"{ds.get('title', '')}\""] + story_text(ds)
                adds.append(f"a story node for {fid}")
            elif act == "add-sections":
                writes += 1
                fixes = fix_lines(st, pc.STORY_TYPE)
                lines += [f"- Use story #{st.get('issue')} \"{st.get('title') or ''}\" for {fid}: add "
                          "the section" + ("s " if len(st.get("missing") or []) > 1 else " ")
                          + " and ".join(f"\"{m}\"" for m in st.get("missing") or [])
                          + " at the end; every line a person wrote stays"
                          + ("; " + "; ".join(fixes) if fixes else "") + "."] + story_text(ds)
            elif act == "use":
                fixes = fix_lines(st, pc.STORY_TYPE)
                if not st.get("attached"):
                    fixes.append("make it a sub-issue of the epic")
                if not st.get("represents_line"):
                    fixes.append(f"add the line \"Represents: {fid}\" at the end of its text")
                writes += bool(fixes)
                lines.append(f"- Use story #{st.get('issue')} \"{st.get('title') or ''}\" for {fid}"
                             + (": " + "; ".join(fixes) + "." if fixes else ", as it is."))
            elif act == "skip":
                skipped.append((sl["id"], fid, st.get("reason"), st.get("issue")))
                lines.append(f"- Skip {fid}: no story is made or changed. Why: {st.get('reason')}")
        for mo in it.get("move_out") or []:
            writes += 1
            lines.append(f"- Move story #{mo.get('issue')} out of the plan: {mo.get('feature')} is no "
                         "longer in the slice. It comes off the epic's sub-issues and map, and stays "
                         "open in the tracker. It is not deleted.")
            removes.append(f"the story node #{mo.get('issue')} ({mo.get('feature')})")
        lines.append("")
    lines += ["## The plan file", ""]
    path = gather.get("plan_file")
    if items.get("plan_file_exists"):
        lines.append(f"- Update `{path}`. Every other node and line stays as it is.")
    else:
        lines.append(f"- Make `{path}` (id {plan_id}, status active, and its tree).")
    lines += [f"- Add {a}." for a in adds] + [f"- Take out {r}." for r in removes]
    if not adds and not removes:
        lines.append("- No node changes. The file stays as it is.")
    lines += ["", "## Skipped features", ""]
    if skipped:
        for sid, fid, reason, issue in skipped:
            keep = f" Its story #{issue} stays as it is." if issue else ""
            lines.append(f"- {fid} (slice {sid}): its ICE is not ready, so no story is written.{keep} "
                         f"Why: {reason}")
    else:
        lines.append("- None. Every feature's ICE is ready.")
    lines += ["", "## Your answer", "",
              f"The run makes {writes} tracker write(s) of the kinds above, and then the plan-file change.",
              "Type **yes** to write all of it, **change: <what>** to have the epic or stories drafted "
              "again, or **stop** to write nothing.", ""]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the /shape-plan brief from the run's records.")
    ap.add_argument("--gather", required=True)
    ap.add_argument("--work-items", required=True)
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        gather = pc.read_json(args.gather, "gather.json")
        items = pc.read_json(args.work_items, "work-items.json")
        drafts = pc.read_json(args.drafts, "drafts.json")
    except pc.Refused as exc:
        sys.stderr.write(f"render_brief.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    pc.atomic_write(args.out, render(gather, items, drafts))
    print(json.dumps({"ok": True, "out": args.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
