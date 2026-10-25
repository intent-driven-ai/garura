#!/usr/bin/env python3
"""check_drafts.py — check the epic and story drafts before the brief (/shape-plan, C5, C6, C9, C11).

    python3 check_drafts.py --drafts <drafts.json> --gather <gather.json> \
        --out <working>/drafts-check.json

`ok: true` only when, for each slice of gather.json:
  - the drafts have the slice, with an epic title;
  - each ready feature has exactly one story, and no story is for a feature that is not ready
    or not in the slice;
  - each story has a title, goals, limits and expectations that are not empty, and the four
    Context guidance fields (read, never_read, persona, in_out); `written_from` is not the
    skill's: write_work_items.py fills it from gather.json;
  - no text of the epic or of a story holds any line of a "Fails if" block of its two ICE
    (read from the original ICE pages that gather.json names: the line itself and every line
    under it, nested bullets and wrapped text included), the words "Fails if", or a recovery
    phrase
    ("the builder can fix this alone", "a person must decide"). The epic is checked against
    the lines of every feature of its slice.
Each problem names its slice and feature, so the skill fixes only what is wrong.

Output: {ok, problems: [{slice, feature, problem}], counts: {slices, stories}}
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
    by_slice = {}
    for d in drafts.get("slices") or []:
        if isinstance(d, dict):
            by_slice.setdefault(d.get("slice"), []).append(d)
    n_stories = 0
    for sl in gather.get("slices") or []:
        sid = sl["id"]

        def bad(feature, problem):
            problems.append({"slice": sid, "feature": feature, "problem": problem})

        got = by_slice.pop(sid, [])
        if len(got) != 1:
            bad(None, "the drafts have no entry for this slice" if not got
                else "the drafts have two entries for this slice")
            continue
        d = got[0]
        features = {f["id"]: f for f in sl.get("features") or []}
        lines_of = {fid: page_fails_lines(f.get("ice_pages")) for fid, f in features.items()}
        epic = d.get("epic") or {}
        if not filled(epic.get("title")):
            bad(None, "the epic has no title")
        every_line = [ln for lines in lines_of.values() for ln in lines]
        for reason in pc.forbidden_in(pc.all_text(epic), every_line):
            bad(None, f"the epic text: {reason}")
        seen = {}
        for story in d.get("stories") or []:
            fid = story.get("feature") if isinstance(story, dict) else None
            seen[fid] = seen.get(fid, 0) + 1
            if fid not in features:
                bad(fid, "a story is drafted for a feature that is not in the slice")
                continue
            if not features[fid].get("ready"):
                bad(fid, "a story is drafted for a feature whose ICE is not ready")
                continue
            n_stories += 1
            if not filled(story.get("title")):
                bad(fid, "the story has no title")
            scope = story.get("scope_of_work") or {}
            for key in SCOPE:
                if not filled(scope.get(key)):
                    bad(fid, f"the scope of work has no {key}")
            guide = story.get("context_guidance") or {}
            for key in GUIDANCE:
                if not filled(guide.get(key)):
                    bad(fid, f"the Context guidance has no '{key}' line")
            text = pc.all_text({k: v for k, v in story.items() if k != "written_from"})
            for reason in pc.forbidden_in(text, lines_of.get(fid)):
                bad(fid, f"the story text: {reason}")
        for fid, f in features.items():
            if f.get("ready") and seen.get(fid, 0) == 0:
                bad(fid, "a ready feature has no story")
            if seen.get(fid, 0) > 1:
                bad(fid, "a feature has two stories")
    for sid in by_slice:
        problems.append({"slice": sid, "feature": None,
                         "problem": "the drafts have a slice that gather.json does not hold"})
    return {"ok": not problems, "problems": problems,
            "counts": {"slices": len(gather.get("slices") or []), "stories": n_stories}}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the epic and story drafts.")
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--gather", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        drafts = pc.read_json(args.drafts, "drafts.json")
        gather = pc.read_json(args.gather, "gather.json")
        if not isinstance(drafts, dict):
            raise pc.Refused("drafts.json must be a JSON object with a slices list")
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
