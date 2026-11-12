#!/usr/bin/env python3
"""render_summary.py — the short summary the product owner sees at the checkpoint, never the eval (C9).

    python3 render_summary.py --check <working>eval-check.json --place <working>place.json \
        --inputs <working>inputs.json --out <working>summary.md

It opens with one plain sentence (what the plan's eval checks, how many slices, Feature issues,
scenarios and failure conditions, how many items it cannot test yet, and how to read the tables),
then, for each slice of the plan, one line per Feature issue with its counts: Scenarios, Goals,
Expectations and Failure conditions (covered / in the Feature issue or its hidden-file entry) and
Untestable (a Feature issue that sits in two slices is counted under the first, and named in the
other); then each untestable item in one line with its reason; then each slice left out because the
Slices list marks it Dropped, and each feature left out because only dropped slices hold it, with why
(C14); then where the eval files are. A
plan that is not ready is named with each reason, and gets no table. An Untestable line for a part
of a line that also has a scenario is shown too, marked "partly tested". Each scenario whose Feature
issue line moved or changed since the eval was written is named, for a person to judge (C16). On a
later run (the plan had eval files), it says how many scenarios and untestable lines the run adds,
and that every scenario that was there is kept. The summary is built from the run's records only;
it is never edited by hand. Exit 0 written, 2 refused.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval_common as ec  # noqa: E402


def frac(pair):
    return f"{pair[0]}/{pair[1]}"


def render(check, place, inputs):
    pid = inputs["plan_id"]
    name = inputs.get("epic_title") or inputs.get("intent_title") or f"plan {pid}"
    if not check.get("ready", inputs["ready"]):
        lines = [f"## Plan {pid}: no eval", "", "The plan is not ready, so no eval was written:", ""]
        lines += [f"- {r}" for r in check.get("reasons") or inputs["reasons"]] or ["- (no reason given)"]
        return "\n".join(lines) + "\n"
    feats = check["features"]
    by_id = {f["feature"]: f for f in feats}
    total = sum(f["scenarios"] for f in feats)
    items_n = sum(len(f["untestable"]) for f in feats)
    fails = sum(f["failure_conditions"][1] for f in feats)
    lines = [f"## Eval for \"{name}\" (plan {pid}, epic #{inputs['epic']})", "",
             f"This eval checks, from the outside, that the {len(feats)} Feature issues of the plan's "
             f"{len(inputs['slices'])} slice(s) do what they promise and that none of their {fails} failure "
             f"conditions happens: {total} scenarios, each pass or fail, and {items_n} item(s) it cannot test "
             "yet. In the tables, 2/3 means two of the Feature issue's three lines have a scenario.", ""]
    if inputs["existing"]:
        lines += [f"A later run: it adds {place.get('added_scenarios', 0)} scenarios and "
                  f"{place.get('added_untestable', 0)} untestable lines; every scenario that was there "
                  "is kept, word for word.", ""]
    for sl in inputs["slices"]:
        lines += [f"### Slice {sl['slice_id']} ({sl['surface_kind']})", "",
                  "| Feature issue | Scenarios | Goals | Expectations | Failure conditions | Untestable |",
                  "|---|---|---|---|---|---|"]
        for fid in sl["features"]:
            f = by_id.get(fid)
            if f is None:
                continue
            label = f"#{f['issue']} {f.get('title') or fid}" + (f" (held by epic #{f['held_by']})" if f.get("held_by") else "")
            if f["slices"] and f["slices"][0] != sl["slice_id"]:
                lines.append(f"| {label} | counted under slice {f['slices'][0]} | | | | |")
                continue
            lines.append(f"| {label} | {f['scenarios']} | {frac(f['goals'])} | {frac(f['expectations'])} | "
                         f"{frac(f['failure_conditions'])} | {len(f['untestable'])} |")
        lines.append("")
    items = [(f["issue"], u) for f in feats for u in f["untestable"]]
    lines += [f"Untestable ({len(items)}):"]
    lines += [f"- #{n} {', '.join(u['tags'])}" + (" (partly tested)" if u.get("partly") else "")
              + f": {u['reason']}" for n, u in items] or ["- none"]
    moved = check.get("moved") or []
    if moved:
        lines += ["", f"Feature issue lines that moved or changed since the eval was written ({len(moved)}) — the "
                  "scenarios stay as they are; a person judges whether they still fit:"]
        lines += [f"- {m['file']} {m['tag']} ({', '.join(m['scenarios']) or 'no scenario'}): was \"{m['was']}\", "
                  f"now \"{m['now']}\"" for m in moved]
    if inputs.get("dropped"):
        lines += ["", "Dropped slices, left out of the eval: " + ", ".join(d["slice_id"] for d in inputs["dropped"])]
    if inputs.get("left_out"):
        lines += ["Features left out:"] + [f"- #{f['issue']} {f['feature']}: {f['why']}" for f in inputs["left_out"]]
    if inputs["out_of_plan"]:
        lines += ["", "Out of the plan (kept, not run): " + ", ".join(inputs["out_of_plan"])]
    lines += ["", f"The files: {inputs['folder']}/ (open them for the detail).", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render the short summary for the checkpoint.")
    ap.add_argument("--check", required=True)
    ap.add_argument("--place", required=True)
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        text = render(ec.read_json(args.check, "eval-check.json"), ec.read_json(args.place, "place.json"),
                      ec.read_json(args.inputs, "inputs.json"))
    except ec.Refused as exc:
        sys.stderr.write(f"render_summary.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    ec.atomic_write(args.out, text)
    print(json.dumps({"ok": True, "out": args.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
