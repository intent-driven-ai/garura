#!/usr/bin/env python3
"""check_eval.py — the eval file check: is each slice's eval complete, exact and runnable with no agent (C3–C6, C12–C14).

    python3 check_eval.py --inputs <working>inputs.json --place <working>place.json \
        --out <working>eval-check.json

It reads the eval files in each ready slice's evals folder (after place_eval.py) and the
inputs.json gather_eval.py wrote. It never runs an eval. For each ready slice:

  - The slice file `eval.<slice-id>.md` names the slice and its epic, the surface kind of the
    slice, a time limit for each scenario (a whole number of seconds, more than 0) and the pass
    rule; it lists every story of the epic's map, in the map's order, each with its story file,
    and every story file out of the slice; its "Names" list holds each name the story files use,
    and no other (C3, C13, C14).
  - Each story file `eval.<feature-id>.feature.md` is Markdown with Gherkin with one `Feature:`,
    which is its story ("Story #<n> — ..."), and the tag `@story-<n>` above it (C3).
  - Each scenario has a tag line, and each tag is something its story or its feature's hidden-file
    entry says: `@goal-<k>` and `@expectation-<k>` (the k-th line of the story's lists),
    `@F<n>` (a failure condition of the feature) (C5).
  - Each step is a sentence of the surface kind's step library; the first step is not And or
    But; each scenario has a Then (C3, C4, C12). A value the build will make is a [name] (C13).
  - Every goal, expectation and failure condition is covered by a scenario or by a line under
    "Untestable" with a reason (C5).
  - No line holds a recovery or handoff text: "the builder can fix this alone", "a person must
    decide", "Way back:", "Who fixes:", or a recovery line of the hidden file (C6). A phrase quoted
    in a "does not contain" step checks that the phrase is absent, so it does not count.
  - The folder holds no other eval file: a story file for a story that is not in the slice is a
    problem (C14).
A slice that is not ready must have got no file from this run (place.json) (C8).

Writes eval-check.json {ok, problems, slices: [{slice, ready, reason, stories: [{issue, feature,
title, scenarios, goals: [covered, total], expectations: [...], failure_conditions: [...],
untestable: [{tags, reason}]}]}]}. Exit 0 ok, 1 problems, 2 refused.
"""

import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval_common as ec  # noqa: E402


def check_story(sl, story, text, lib, problems, names):
    where = ec.story_file_name(story["feature"])
    p = ec.parse_story_file(text)
    for e in p["errors"]:
        problems.append(f"{where}: {e}")
    if not p["feature"] or not p["feature"].startswith(f"Story #{story['issue']}"):
        problems.append(f"{where}: its Feature: is not 'Story #{story['issue']} — ...'")
    if f"story-{story['issue']}" not in p["top_tags"]:
        problems.append(f"{where}: no tag `@story-{story['issue']}` above its Feature:")
    valid = ({f"goal-{k}" for k in range(1, len(story["goals"]) + 1)}
             | {f"expectation-{k}" for k in range(1, len(story["expectations"]) + 1)}
             | {f["id"] for f in sl["failures"].get(story["feature"], [])})
    covered = set()

    def steps_ok(steps, label):
        resolved = ec.resolve_keywords(steps)
        if resolved and resolved[0][2] in ("And", "But"):
            problems.append(f"{where}: {label} starts with {resolved[0][2]}")
        for real, stext, _ in resolved:
            if real is None or ec.match_step(real, stext, lib) is None:
                problems.append(f"{where}: {label}: '{real or ''} {stext}' is not a sentence of the "
                                f"{lib['kind']} step library")
            names.update(ec.names_in(stext))
        return resolved

    steps_ok(p["background"], "the Background")
    for sc in p["scenarios"]:
        label = f"the scenario '{sc['title']}'"
        if not sc["tags"]:
            problems.append(f"{where}: {label} has no tag that says what it covers")
        for t in sc["tags"]:
            if t not in valid:
                problems.append(f"{where}: {label} covers '{t}', which story #{story['issue']} and "
                                "its hidden-file entry do not say")
        covered.update(t for t in sc["tags"] if t in valid)
        if not sc["steps"]:
            problems.append(f"{where}: {label} has no steps")
        resolved = steps_ok(sc["steps"], label)
        if not any(real == "Then" for real, _, _ in resolved):
            problems.append(f"{where}: {label} has no Then")
    untestable = []
    for u in p["untestable"]:
        bad = [t for t in u["tags"] if t not in valid]
        if bad:
            problems.append(f"{where}: the Untestable line for {', '.join(bad)} names nothing the story says")
        if not u["reason"].strip():
            problems.append(f"{where}: an Untestable line has no reason")
        untestable.append(u)
    open_tags = {t for u in untestable for t in u["tags"]} - covered
    for t in sorted(valid - covered - open_tags):
        problems.append(f"{where}: '{t}' has no scenario and no Untestable line")
    # a recovery phrase quoted in a "does not contain" step checks that it is absent; it is not recovery text
    low = "\n".join(re.sub(r'(does not contain\s+)"[^"]*"', r'\1""', ln) for ln in text.splitlines()).lower()
    for w in ec.RECOVERY_WORDS:
        if w in low:
            problems.append(f"{where}: holds recovery or handoff text ('{w}')")
    for line in sl["recovery_lines"]:
        if len(line) > 20 and line.lower() in low:
            problems.append(f"{where}: holds a recovery line of the hidden file")

    def count(prefix, total):
        return [len({t for t in covered if t.startswith(prefix)}), total]

    fails = sl["failures"].get(story["feature"], [])
    return {"issue": story["issue"], "feature": story["feature"], "title": story.get("title"),
            "scenarios": len(p["scenarios"]),
            "goals": count("goal-", len(story["goals"])),
            "expectations": count("expectation-", len(story["expectations"])),
            "failure_conditions": [len({t for t in covered if t.startswith("F")}), len(fails)],
            "untestable": [{"tags": [t for t in u["tags"] if t not in covered], "reason": u["reason"]}
                           for u in untestable if [t for t in u["tags"] if t not in covered]]}


def check_slice(sl, problems):
    lib = ec.load_library(sl["library"])
    folder, out = sl["folder"], {"slice": sl["slice_id"], "ready": True, "reason": None, "stories": []}
    sname = ec.slice_file_name(sl["slice_id"])
    spath = os.path.join(folder, sname)
    names = set()
    in_slice = set()
    for story in sl["stories"]:
        name = ec.story_file_name(story["feature"])
        in_slice.add(name)
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            problems.append(f"{sl['slice_id']}: no story file {name} for story #{story['issue']}")
            continue
        out["stories"].append(check_story(sl, story, ec.read_text(path, "a story file"), lib, problems, names))
    allowed = in_slice | set(sl["out_of_slice"]) | {sname}
    for path in sorted(glob.glob(os.path.join(folder, "eval.*"))):
        if os.path.basename(path) not in allowed:
            problems.append(f"{sl['slice_id']}: {os.path.basename(path)} is not a story of the slice")
    if not os.path.isfile(spath):
        problems.append(f"{sl['slice_id']}: no slice file {sname}")
        return out
    sf = ec.parse_slice_file(ec.read_text(spath, "the slice file"))
    if not sf["title"] or sl["slice_id"] not in sf["title"] or f"#{sl['epic']}" not in sf["title"]:
        problems.append(f"{sname}: its title does not name slice {sl['slice_id']} and epic #{sl['epic']}")
    if sf["surface_kind"] != sl["surface_kind"]:
        problems.append(f"{sname}: its surface kind is '{sf['surface_kind']}', not '{sl['surface_kind']}'")
    if not sf["time_limit"] or sf["time_limit"] <= 0:
        problems.append(f"{sname}: no time limit for each scenario (a whole number of seconds, more than 0)")
    if not sf["has_pass_rule"]:
        problems.append(f"{sname}: no Pass rule section")
    want = [(s["feature"], s["issue"], ec.story_file_name(s["feature"])) for s in sl["stories"]]
    if sf["stories"] != want:
        problems.append(f"{sname}: its stories are not the epic's map in build order")
    if sorted(f for _, _, f in sf["out_of_slice"]) != sorted(sl["out_of_slice"]):
        problems.append(f"{sname}: its 'Out of the slice' list is not the story files whose feature left the slice")
    for n in sorted(names - set(sf["names"])):
        problems.append(f"{sname}: the name [{n}] is used but not listed under Names")
    for n in sorted(set(sf["names"]) - names):
        problems.append(f"{sname}: the name [{n}] is listed but no story file uses it")
    return out


def check(inputs, place):
    problems, slices = [], []
    made = {p for s in place.get("slices") or [] for p in s.get("new_files") or []}
    for sl in inputs["slices"]:
        if not sl["ready"]:
            slices.append({"slice": sl["slice_id"], "ready": False, "reason": sl["reason"], "stories": []})
            folder = sl.get("folder")
            if folder and any(p.startswith(folder + os.sep) for p in made):
                problems.append(f"{sl['slice_id']}: is not ready but got an eval file in this run")
            continue
        slices.append(check_slice(sl, problems))
    return {"ok": not problems, "problems": problems, "slices": slices}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check each slice's eval files.")
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--place", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        res = check(ec.read_json(args.inputs, "inputs.json"), ec.read_json(args.place, "place.json"))
    except ec.Refused as exc:
        sys.stderr.write(f"check_eval.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    ec.write_json(args.out, res)
    print(json.dumps({"ok": res["ok"], "problems": res["problems"][:20]}, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
