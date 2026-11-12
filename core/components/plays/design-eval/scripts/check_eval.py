#!/usr/bin/env python3
"""check_eval.py — the eval file check: is the plan's eval complete, exact and runnable with no agent (C3–C6, C12–C14).

    python3 check_eval.py --inputs <working>inputs.json --place <working>place.json \
        --out <working>eval-check.json

It reads the eval files in the plan's evals folder (after place_eval.py) and the inputs.json
gather_eval.py wrote. It never runs an eval. When the plan is ready:

  - The plan file `eval.<plan-id>.md` names the plan and its epic and has a Pass rule section; it
    has one `## Slice <slice id>` section for each slice of the plan's Slices list, in that order,
    each with the slice's surface kind, a time limit for each scenario (a whole number of seconds,
    more than 0) and the slice's features in its build order, each with its feature file (a
    Feature issue held by another plan's epic says so); it lists every feature file out of the
    plan; its "Names" list holds each name the feature files use, and no other (C3, C13, C14).
  - Each feature file `eval.<feature-id>.feature.md` is Markdown with Gherkin with one `Feature:`,
    which is its Feature issue ("Feature issue #<n> — ..."), and the tag `@feature-<n>` above it (C3).
  - Each scenario has a tag line, and each tag is something its Feature issue or its feature's
    hidden-file entry says: `@goal-<k>` and `@expectation-<k>` (the k-th line of the Feature
    issue's lists), `@F<n>` (a failure condition of the feature) (C5).
  - Each step is a sentence of the step library of the feature's surface kind (the first slice
    that holds it); the first step is not And or But; each scenario has a Then (C3, C4, C12). A
    value the build will make is a [name] (C13).
  - Every goal, expectation and failure condition is covered by a scenario or by a line under
    "Untestable" with a reason (C5).
  - Each goal and expectation a scenario covers is recorded under "Lines covered" with the Feature
    issue line's exact text. On a feature file the plan had before the run, a recorded line that
    no longer matches the Feature issue (it moved, changed or is gone) is listed under `moved`, for
    a person: the scenario stays as it is, and it is not a problem (C16).
  - No line holds a recovery or handoff text: "the builder can fix this alone", "a person must
    decide", "Way back:", "Who fixes:", or a recovery line of a hidden file (C6). A phrase quoted
    in a "does not contain" step checks that the phrase is absent, so it does not count.
  - The folder holds no other eval file: a feature file for a feature that is not in the plan's
    map is a problem (C14).
A plan that is not ready must have got no file from this run (place.json) (C8).

Writes eval-check.json {ok, ready, reasons, problems, moved: [{file, tag, scenarios, was, now}],
features: [{issue, feature, title, slices, held_by, scenarios, goals: [covered, total],
expectations: [...], failure_conditions: [...], untestable: [{tags, reason, partly}]}]}: every
Untestable line, `partly` true when each of its tags also has a scenario (the line names the part
the scenario cannot check). Exit 0 ok, 1 problems, 2 refused.
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


def check_feature(inputs, feat, text, lib, problems, names, before=None, moved=None):
    """`before` is the feature file as the plan had it before the run (None for a new file). A tag the
    file had before keeps its scenario: when its Feature issue line moved or changed, it goes to `moved`
    for a person (C16), never to the problems."""
    where = ec.feature_file_name(feat["feature"])
    p = ec.parse_feature_file(text)
    old = ec.parse_feature_file(before) if before is not None else None
    old_tags = ({t for sc in old["scenarios"] for t in sc["tags"]} | set(old["lines_covered"])) if old else set()
    moved = moved if moved is not None else []
    for e in p["errors"]:
        problems.append(f"{where}: {e}")
    if not p["feature"] or not p["feature"].startswith(f"Feature issue #{feat['issue']}"):
        problems.append(f"{where}: its Feature: is not 'Feature issue #{feat['issue']} — ...'")
    if f"feature-{feat['issue']}" not in p["top_tags"]:
        problems.append(f"{where}: no tag `@feature-{feat['issue']}` above its Feature:")
    valid = ({f"goal-{k}" for k in range(1, len(feat["goals"]) + 1)}
             | {f"expectation-{k}" for k in range(1, len(feat["expectations"]) + 1)}
             | {f["id"] for f in feat["failures"]})
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
            if t not in valid and t in old_tags and ec.issue_line(feat, t) is None and re.match(r"^(goal|expectation)-\d+$", t):
                continue  # its Feature issue line is gone: named under moved below, never a problem
            if t not in valid:
                problems.append(f"{where}: {label} covers '{t}', which Feature issue #{feat['issue']} and "
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
            problems.append(f"{where}: the Untestable line for {', '.join(bad)} names nothing the Feature issue says")
        if not u["reason"].strip():
            problems.append(f"{where}: an Untestable line has no reason")
        untestable.append(u)
    open_tags = {t for u in untestable for t in u["tags"]} - covered
    for t in sorted(valid - covered - open_tags):
        problems.append(f"{where}: '{t}' has no scenario and no Untestable line")
    # C16: each covered line is recorded with its text; a line that moved or changed is named, not fixed
    for t in sorted({t for sc in p["scenarios"] for t in sc["tags"]} | set(p["lines_covered"])):
        if not re.match(r"^(goal|expectation)-\d+$", t):
            continue
        now, recorded = ec.issue_line(feat, t), p["lines_covered"].get(t)
        titles = [sc["title"] for sc in p["scenarios"] if t in sc["tags"]]
        if t in old_tags:
            if recorded is None or now is None or not ec.same_line(recorded, now):
                moved.append({"file": where, "tag": t, "scenarios": titles,
                              "was": recorded, "now": now if now is not None else "(the line is gone)"})
        elif titles and recorded is None:
            problems.append(f"{where}: '{t}' has no line under 'Lines covered' with its Feature issue line's text")
        elif recorded is not None and not ec.same_line(recorded, now):
            problems.append(f"{where}: the Lines covered text of '{t}' is not Feature issue #{feat['issue']}'s line now")
    # a recovery phrase quoted in a "does not contain" step checks that it is absent; it is not recovery text
    low = "\n".join(re.sub(r'(does not contain\s+)"[^"]*"', r'\1""', ln) for ln in text.splitlines()).lower()
    for w in ec.RECOVERY_WORDS:
        if w in low:
            problems.append(f"{where}: holds recovery or handoff text ('{w}')")
    for line in inputs["recovery_lines"]:
        if len(line) > 20 and line.lower() in low:
            problems.append(f"{where}: holds a recovery line of a hidden file")

    def count(prefix, total):
        return [len({t for t in covered if t.startswith(prefix)}), total]

    return {"issue": feat["issue"], "feature": feat["feature"], "title": feat.get("title"),
            "slices": feat["slices"], "held_by": feat.get("held_by"),
            "scenarios": len(p["scenarios"]),
            "goals": count("goal-", len(feat["goals"])),
            "expectations": count("expectation-", len(feat["expectations"])),
            "failure_conditions": [len({t for t in covered if t.startswith("F")}), len(feat["failures"])],
            "untestable": [{"tags": u["tags"], "reason": u["reason"],
                            "partly": all(t in covered for t in u["tags"])} for u in untestable]}


def check_plan(inputs, problems, working=None, moved=None):
    folder, out = inputs["folder"], []
    pname = ec.plan_file_name(inputs["plan_id"])
    libs = {}
    names, in_plan = set(), set()
    for feat in inputs["features"]:
        name = ec.feature_file_name(feat["feature"])
        in_plan.add(name)
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            problems.append(f"no feature file {name} for Feature issue #{feat['issue']}")
            continue
        if feat["library"] not in libs:
            libs[feat["library"]] = ec.load_library(feat["library"])
        prior = os.path.join(working or "", "inputs", "existing", name)
        before = ec.read_text(prior, "the feature file from before the run") if working and name in inputs["existing"] \
            and os.path.isfile(prior) else None
        out.append(check_feature(inputs, feat, ec.read_text(path, "a feature file"), libs[feat["library"]],
                                 problems, names, before, moved))
    allowed = in_plan | set(inputs["out_of_plan"]) | {pname}
    for path in sorted(glob.glob(os.path.join(folder, "eval.*"))):
        if os.path.basename(path) not in allowed:
            problems.append(f"{os.path.basename(path)} is not a feature of the plan's map")
    ppath = os.path.join(folder, pname)
    if not os.path.isfile(ppath):
        problems.append(f"no plan file {pname}")
        return out
    pf = ec.parse_plan_file(ec.read_text(ppath, "the plan file"))
    if not pf["title"] or f"plan {inputs['plan_id']}" not in pf["title"] or f"#{inputs['epic']}" not in pf["title"]:
        problems.append(f"{pname}: its title does not name plan {inputs['plan_id']} and epic #{inputs['epic']}")
    if not pf["has_pass_rule"]:
        problems.append(f"{pname}: no Pass rule section")
    want_ids = [sl["slice_id"] for sl in inputs["slices"]]
    if [s["slice"] for s in pf["slices"]] != want_ids:
        problems.append(f"{pname}: its slice sections are not the plan's slices, one each, in the Slices list's "
                        f"order ({', '.join(want_ids)})")
    by_id = {f["feature"]: f for f in inputs["features"]}
    for sec in pf["slices"]:
        sl = next((x for x in inputs["slices"] if x["slice_id"] == sec["slice"]), None)
        if sl is None:
            continue
        where = f"{pname}, slice {sl['slice_id']}"
        if sec["surface_kind"] != sl["surface_kind"]:
            problems.append(f"{where}: its surface kind is '{sec['surface_kind']}', not '{sl['surface_kind']}'")
        if not sec["time_limit"] or sec["time_limit"] <= 0:
            problems.append(f"{where}: no time limit for each scenario (a whole number of seconds, more than 0)")
        want = [(f, by_id[f]["issue"], ec.feature_file_name(f)) for f in sl["features"]]
        if sec["features"] != want:
            problems.append(f"{where}: its features are not the slice's features in build order")
        for f in sl["features"]:
            held = by_id[f].get("held_by")
            if held and sec["held"].get(f) != held:
                problems.append(f"{where}: {f} sits under epic #{held}; its line does not say 'held by epic #{held}'")
    if sorted(f for _, _, f in pf["out_of_plan"]) != sorted(inputs["out_of_plan"]):
        problems.append(f"{pname}: its 'Out of the plan' list is not the feature files whose feature left the plan")
    for n in sorted(names - set(pf["names"])):
        problems.append(f"{pname}: the name [{n}] is used but not listed under Names")
    for n in sorted(set(pf["names"]) - names):
        problems.append(f"{pname}: the name [{n}] is listed but no feature file uses it")
    return out


def check(inputs, place, working=None):
    problems, moved = [], []
    res = {"ok": True, "ready": inputs["ready"], "reasons": inputs["reasons"], "problems": problems,
           "moved": moved, "features": []}
    if not inputs["ready"]:
        if place.get("new_files") or place.get("files"):
            problems.append(f"plan {inputs['plan_id']} is not ready but got an eval file in this run")
    else:
        res["features"] = check_plan(inputs, problems, working, moved)
    res["ok"] = not problems
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the plan's eval files.")
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--place", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        res = check(ec.read_json(args.inputs, "inputs.json"), ec.read_json(args.place, "place.json"),
                    os.path.dirname(os.path.abspath(args.inputs)))
    except ec.Refused as exc:
        sys.stderr.write(f"check_eval.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    ec.write_json(args.out, res)
    print(json.dumps({"ok": res["ok"], "problems": res["problems"][:20]}, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
