#!/usr/bin/env python3
"""render_brief.py — the one brief the product owner reads before any write (/shape-plan, C8, C9, C11, C16, C17, C18).

    python3 render_brief.py --gather <gather.json> --work-items <work-items.json> \
        --drafts <drafts.json> --out <working>/brief.md

The brief is built from the run's records only, so no write can be left out of it:
  - what the run writes in the tracker: the plan's one epic (make, use), and each feature's
    Feature issue (make, use, add sections, open again), with the text a new item or a new
    section gets, and each type, label or sub-issue change on an item that exists;
  - the Feature issues another plan's epic holds (`held_by`): shown, never moved;
  - under "Opened again", each closed Feature issue of a feature the plan takes in, with its
    issue number and how it was closed: on the yes the same issue opens again (C17);
  - under "Built, left out" and "Dropped, left out", each feature whose state in the model is
    Completed or Dropped: no tracker search, no write (C16);
  - under "Had no state", each feature whose spine entry has no `status`, or a value outside
    the five: it is treated as Unplanned (C16);
  - under "State changes in the product model", each feature the plan takes in that moves from
    Unplanned to Planned, and each that keeps its state (C18);
  - the plan-file change: the business intent at the top, the `epic:` mark, the Slices list
    (each slice at Not Started), and each node it adds or takes out;
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


def feature_text(draft):
    scope = draft.get("scope_of_work") or {}
    guide = draft.get("context_guidance") or {}
    out = ["  - Goals:"] + ["  " + b for b in bullets(scope.get("goals"))]
    out += ["  - Limits:"] + ["  " + b for b in bullets(scope.get("limits"))]
    out += ["  - Expectations:"] + ["  " + b for b in bullets(scope.get("expectations"))]
    out += [f"  - Read: {guide.get('read', '')}", f"  - Never read: {guide.get('never_read', '')}",
            f"  - Persona: {guide.get('persona', '')}", f"  - In and out: {guide.get('in_out', '')}"]
    return out


def parent_words(parent):
    if not parent:
        return "it has no parent now"
    where = f" in {parent['repo']}" if parent.get("repo") else ""
    return f"it leaves its parent #{parent['number']} \"{parent.get('title') or ''}\"{where}"


def fix_lines(item, type_):
    out = []
    if item.get("type") != type_:
        out.append(f"set its type to {type_} (it is {item.get('type') or 'not set'} now)")
    if item.get("labels"):
        out.append("take off its labels: " + ", ".join(item["labels"]))
    return out


def render(gather, items, drafts):
    plan_id = gather.get("plan_id")
    drafted = {d.get("feature"): d for d in drafts.get("features") or [] if isinstance(d, dict)}
    epic, depic = items.get("epic") or {}, drafts.get("epic") or {}
    features = items.get("features") or []
    lines = [f"# The plan for business intent #{plan_id}: {gather.get('intent_title', '')}", "",
             "This run makes the plan for this business intent: the plan file, one epic for the "
             "plan, and one Feature issue for each feature that is not Completed and not Dropped, "
             "across all the plan's slices. In the product model it changes one field: each "
             "Unplanned feature the plan takes in becomes Planned. It files no Stories. Nothing "
             "below is written yet. Read each write, then type yes to write all of it, change: "
             "<what> to have it drafted again, or stop to write nothing.", ""]
    lines += ["## What the run writes in the tracker", "", "### The plan's epic", ""]
    writes, adds, removes = 0, [], []
    held, reopened, built, dropped, skipped = [], [], [], [], []
    if epic.get("action") == "make":
        writes += 1
        lines += [f"- Make a new epic, type {pc.EPIC_TYPE}, no label: \"{depic.get('title', '')}\"",
                  f"  - Delivers: {depic.get('delivers', '')}",
                  "  - It stands for the plan, and holds the feature-to-story map: one line for "
                  "each feature in the plan."]
        adds.append("the epic node")
    else:
        fixes = fix_lines(epic, pc.EPIC_TYPE)
        pairs = pc.map_pairs(features)
        new = any(f.get("action") in ("make", "reopen") for f in features)
        if new or items.get("move_out") or epic.get("map") != dict(pairs):
            fixes.append("write its feature-to-story map" + (", with a line for each new Feature issue" if new else ""))
        writes += bool(fixes)
        lines.append(f"- Use epic #{epic.get('issue')} \"{epic.get('title') or ''}\""
                     + (": " + "; ".join(fixes) + "." if fixes else ", as it is."))
    lines += ["", "### The Feature issues", ""]
    for f in features:
        fid, act = f.get("feature"), f.get("action")
        d = drafted.get(fid) or {}
        where = " (slices " + ", ".join(f.get("slices") or []) + ")" if len(f.get("slices") or []) > 1 else ""
        if act == "make":
            writes += 1
            lines += [f"- File a new Feature issue for {fid}{where}, type {pc.FEATURE_TYPE}, no label, a "
                      f"sub-issue of the epic, with the line \"{pc.represents_line(fid)}\": "
                      f"\"{d.get('title', '')}\""] + feature_text(d)
            adds.append(f"a feature node for {fid}")
        elif act == "reopen":
            writes += 1
            fixes = []
            if f.get("held_by") is None:
                if f.get("missing"):
                    fixes.append("add the section" + ("s " if len(f["missing"]) > 1 else " ")
                                 + " and ".join(f"\"{m}\"" for m in f["missing"])
                                 + " at the end; every line a person wrote stays")
                fixes += fix_lines(f, pc.FEATURE_TYPE)
                if not f.get("attached"):
                    fixes.append("make it a sub-issue of the epic (" + parent_words(f.get("parent")) + ")")
            if not f.get("represents_line"):
                fixes.append(f"add the line \"{pc.represents_line(fid)}\" at the end of its text")
            writes += len(fixes)
            lines.append(f"- Open Feature issue #{f.get('issue')} \"{f.get('title') or ''}\" again for {fid}{where}: "
                         f"it is closed as {f.get('closed_as')}. No second Feature issue is filed"
                         + ("; " + "; ".join(fixes) if fixes else "") + ".")
            if f.get("missing") and f.get("held_by") is None:
                lines += feature_text(d)
            reopened.append(f"{fid}: Feature issue #{f.get('issue')} \"{f.get('title') or ''}\", closed as "
                            f"{f.get('closed_as')}, opens again"
                            + (f"; it stays under epic #{f.get('held_by')}" if f.get("held_by") else "") + ".")
            adds.append(f"a feature node for {fid}" + (f", held_by {f.get('held_by')}" if f.get("held_by") else ""))
        elif act == "add-sections":
            writes += 1
            fixes = fix_lines(f, pc.FEATURE_TYPE)
            if not f.get("attached"):
                fixes.append("make it a sub-issue of the epic (" + parent_words(f.get("parent")) + ")")
            lines += [f"- Use Feature issue #{f.get('issue')} \"{f.get('title') or ''}\" for {fid}{where}: add the "
                      "section" + ("s " if len(f.get("missing") or []) > 1 else " ")
                      + " and ".join(f"\"{m}\"" for m in f.get("missing") or [])
                      + " at the end; every line a person wrote stays"
                      + ("; " + "; ".join(fixes) if fixes else "") + "."] + feature_text(d)
            adds.append(f"a feature node for {fid}")
        elif act == "use":
            fixes = fix_lines(f, pc.FEATURE_TYPE)
            if not f.get("attached"):
                fixes.append("make it a sub-issue of the epic (" + parent_words(f.get("parent")) + ")")
            if not f.get("represents_line"):
                fixes.append(f"add the line \"{pc.represents_line(fid)}\" at the end of its text")
            writes += bool(fixes)
            lines.append(f"- Use Feature issue #{f.get('issue')} \"{f.get('title') or ''}\" for {fid}{where}"
                         + (": " + "; ".join(fixes) + "." if fixes else ", as it is."))
            adds.append(f"a feature node for {fid}")
        elif act == "held":
            held.append(f"{fid}: Feature issue #{f.get('issue')} \"{f.get('title') or ''}\" sits under epic "
                        f"#{f.get('held_by')}. It stays there; the plan shows it as held_by: {f.get('held_by')}, "
                        "and the epic's map names that epic. It moves only on your answer.")
            adds.append(f"a feature node for {fid}, held_by {f.get('held_by')}")
        elif act == "completed":
            built.append(f"{fid}: it is Completed in the model. It is not in the plan, and the tracker "
                         "is not searched or written for it.")
        elif act == "dropped":
            dropped.append(f"{fid}: it is Dropped in the model. It is not in the plan, and the tracker "
                           "is not searched or written for it.")
        elif act == "skip":
            keep = f" Its Feature issue #{f.get('issue')} stays as it is." if f.get("issue") else ""
            skipped.append(f"{fid}: its ICE is not ready, so no Feature issue is filed or changed.{keep} "
                           f"Why: {f.get('reason')}")
    for mo in items.get("move_out") or []:
        writes += 1
        lines.append(f"- Take #{mo.get('issue')} off the epic: {mo.get('feature')} is in no slice of the plan. "
                     "It stays open in the tracker. It is not deleted.")
        removes.append(f"the node #{mo.get('issue')} ({mo.get('feature')})")
    lines += ["", "## Held by another plan's epic", ""]
    lines += [f"- {h}" for h in held] or ["- None."]
    lines += ["", "## Opened again", ""]
    lines += [f"- {x}" for x in reopened] or ["- None."]
    lines += ["", "## Built, left out", ""]
    lines += [f"- {x}" for x in built] or ["- None. No feature of the plan is Completed."]
    lines += ["", "## Dropped, left out", ""]
    lines += [f"- {x}" for x in dropped] or ["- None."]
    lines += ["", "## Had no state", ""]
    lines += [f"- {n['feature']}: its spine entry has "
              + (f"the status {n['status']!r}, which is not one of the five" if n.get("status") is not None
                 else "no status")
              + ". It is treated as Unplanned." for n in items.get("no_state") or []] or ["- None."]
    lines += ["", "## State changes in the product model", ""]
    changes = items.get("state_changes") or []
    lines += [f"- {c['feature']}: Unplanned → Planned"
              + (" (it had no state)" if c.get("had_no_state") else "") + "." for c in changes]
    lines += [f"- {k['feature']}: stays {k['state']}." for k in items.get("kept_states") or []]
    if not changes and not items.get("kept_states"):
        lines.append("- None.")
    if changes:
        lines.append("- These are written after the tracker writes and the plan file, through "
                     "link-model-part. Nothing else in the product model changes.")
    lines += ["", "## The plan file", ""]
    path = gather.get("plan_file")
    slice_names = ", ".join(f"{sl['id']} ({sl.get('name', '')})" for sl in gather.get("slices") or [])
    if items.get("plan_file_exists"):
        lines.append(f"- Update `{path}`. Every other node and line stays as it is.")
    else:
        lines.append(f"- Make `{path}`. At the top: the business intent (bi-{plan_id}, "
                     f"\"{gather.get('intent_title', '')}\"), then id {plan_id}, status Not Started, "
                     "the epic mark (epic: <the epic's issue>), and the Slices list.")
    lines.append(f"- Slices list, each at Not Started: {slice_names}.")
    lines += [f"- Add {a}." for a in adds] + [f"- Take out {r}." for r in removes]
    lines += ["", "## Skipped features", ""]
    lines += [f"- {x}" for x in skipped] or ["- None. Every feature's ICE is ready."]
    lines += ["", "## Your answer", "",
              f"The run makes {writes} tracker write(s) of the kinds above, then the plan-file change, "
              f"then {len(changes)} state change(s) in the product model.",
              "Type **yes** to write all of it, **change: <what>** to have the epic or the Feature "
              "issues drafted again, or **stop** to write nothing.", ""]
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
