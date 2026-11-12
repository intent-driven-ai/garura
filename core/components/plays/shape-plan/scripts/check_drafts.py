#!/usr/bin/env python3
"""check_drafts.py — check the epic and Feature issue drafts before the brief (/shape-plan, C5, C6, C9, C11).

    python3 check_drafts.py --drafts <drafts.json> --gather <gather.json> \
        --out <working>/drafts-check.json

drafts.json is {"epic": {title, delivers}, "features": [{feature, title, scope_of_work,
context_guidance}]}: one epic for the plan, and one draft for each ready feature of the plan's
slices, once (a feature in two slices has one draft). `ok: true` only when:
  - the epic has a title;
  - each ready feature has exactly one draft, and no draft is for a feature that is not ready
    or in no slice of the plan;
  - each draft has a title, goals, limits and expectations that are not empty, and the four
    Context guidance fields (read, never_read, persona, in_out); `written_from` is not the
    skill's: write_work_items.py fills it from gather.json;
  - no text of the epic or of a draft holds any line of a "Fails if" block of its two ICE
    (read from the original ICE pages that gather.json names: the line itself and every line
    under it, nested bullets and wrapped text included), the words "Fails if", or a recovery
    phrase ("the builder can fix this alone", "a person must decide"). The epic is checked
    against the lines of every feature of the plan.
Each problem names its feature, so the skill fixes only what is wrong.

Output: {ok, problems: [{feature, problem}], counts: {features}}
Exit 0 ok; 1 not ok (written); 2 bad input (nothing written). No git, no network.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

GUIDANCE = ("read", "never_read", "persona", "in_out")
SCOPE = ("goals", "limits", "expectations")


def page_fails_lines(paths):
    lines = []
    for path in paths or []:
        if not os.path.isfile(path):
            continue
        text = pc.read_text(path).splitlines()
        lines += pc.fails_if_texts(text)
    return lines


def filled(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(v, str) and v.strip() for v in value)
    return False


def check(drafts, gather):
    problems = []

    def bad(feature, problem):
        problems.append({"feature": feature, "problem": problem})

    features = {}
    for sl in gather.get("slices") or []:
        for f in sl.get("features") or []:
            features.setdefault(f["id"], f)
    lines_of = {fid: page_fails_lines(f.get("ice_pages")) for fid, f in features.items()}
    epic = drafts.get("epic") or {}
    if not filled(epic.get("title")):
        bad(None, "the epic has no title")
    every_line = [ln for lines in lines_of.values() for ln in lines]
    for reason in pc.forbidden_in(pc.all_text(epic), every_line):
        bad(None, f"the epic text: {reason}")
    seen, n_drafts = {}, 0
    for draft in drafts.get("features") or []:
        fid = draft.get("feature") if isinstance(draft, dict) else None
        seen[fid] = seen.get(fid, 0) + 1
        if fid not in features:
            bad(fid, "a Feature issue is drafted for a feature that is in no slice of the plan")
            continue
        if not features[fid].get("ready"):
            bad(fid, "a Feature issue is drafted for a feature whose ICE is not ready")
            continue
        n_drafts += 1
        if not filled(draft.get("title")):
            bad(fid, "the Feature issue has no title")
        scope = draft.get("scope_of_work") or {}
        for key in SCOPE:
            if not filled(scope.get(key)):
                bad(fid, f"the scope of work has no {key}")
        guide = draft.get("context_guidance") or {}
        for key in GUIDANCE:
            if not filled(guide.get(key)):
                bad(fid, f"the Context guidance has no '{key}' line")
        text = pc.all_text({k: v for k, v in draft.items() if k != "written_from"})
        for reason in pc.forbidden_in(text, lines_of.get(fid)):
            bad(fid, f"the Feature issue text: {reason}")
    for fid, f in features.items():
        if f.get("ready") and seen.get(fid, 0) == 0:
            bad(fid, "a ready feature has no Feature issue draft")
        if seen.get(fid, 0) > 1:
            bad(fid, "a feature has two Feature issue drafts")
    return {"ok": not problems, "problems": problems, "counts": {"features": n_drafts}}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the epic and Feature issue drafts.")
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--gather", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        drafts = pc.read_json(args.drafts, "drafts.json")
        gather = pc.read_json(args.gather, "gather.json")
        if not isinstance(drafts, dict):
            raise pc.Refused("drafts.json must be a JSON object with an epic and a features list")
    except pc.Refused as exc:
        sys.stderr.write(f"check_drafts.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    result = check(drafts, gather)
    pc.write_json(args.out, result)
    print(json.dumps({"ok": result["ok"], "problems": len(result["problems"])}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
