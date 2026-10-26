#!/usr/bin/env python3
"""render_summary.py — the short summary the product owner sees at the checkpoint, never the eval (C9).

    python3 render_summary.py --check <working>eval-check.json --place <working>place.json \
        --inputs <working>inputs.json --out <working>summary.md

For each slice it opens with one plain sentence (what the eval checks, how many scenarios and
failure conditions, how many items it cannot test yet, and how to read the table), then one line
per story with its counts: Scenarios, Goals, Expectations and
Failure conditions (covered / in the story or its hidden-file entry) and Untestable; then each
untestable item in one line with its reason; then where the eval files are. A slice that is not
ready is named with its reason. An Untestable line for a part of a line that also has a scenario is
shown too, marked "partly tested". Each scenario whose story line moved or changed since the eval was
written is named, for a person to judge (C16). On a later run (the slice had eval files), it says how many
scenarios and untestable lines the run adds, and that every scenario that was there is kept.
The summary is built from the run's records only; it is never edited by hand. Exit 0 written,
2 refused.
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
    by_slice = {s["slice"]: s for s in place.get("slices") or []}
    info = {s["slice_id"]: s for s in inputs["slices"]}
    lines = []
    for sl in check["slices"]:
        src = info[sl["slice"]]
        if not sl["ready"]:
            lines += [f"## Slice {sl['slice']}: no eval", "", f"- Not ready: {sl['reason']}", ""]
            continue
        total = sum(st["scenarios"] for st in sl["stories"])
        items_n = sum(len(st["untestable"]) for st in sl["stories"])
        fails = sum(st["failure_conditions"][1] for st in sl["stories"])
        name = src.get("epic_title") or sl["slice"]
        lines += [f"## Eval for \"{name}\" (slice {sl['slice']}, epic #{src['epic']})", "",
                  f"This eval checks, from the outside, that the {len(sl['stories'])} stories of this slice do what "
                  f"they promise and that none of their {fails} failure conditions happens: {total} scenarios, each "
                  f"pass or fail, and {items_n} item(s) it cannot test yet. In the table, 2/3 means two of the "
                  "story's three lines have a scenario.", ""]
        p = by_slice.get(sl["slice"], {})
        if src["existing"]:
            lines += [f"A later run: it adds {p.get('added_scenarios', 0)} scenarios and "
                      f"{p.get('added_untestable', 0)} untestable lines; every scenario that was there "
                      "is kept, word for word.", ""]
        lines += ["| Story | Scenarios | Goals | Expectations | Failure conditions | Untestable |",
                  "|---|---|---|---|---|---|"]
        for st in sl["stories"]:
            lines.append(f"| #{st['issue']} {st.get('title') or st['feature']} | {st['scenarios']} | "
                         f"{frac(st['goals'])} | {frac(st['expectations'])} | "
                         f"{frac(st['failure_conditions'])} | {len(st['untestable'])} |")
        items = [(st["issue"], u) for st in sl["stories"] for u in st["untestable"]]
        lines += ["", f"Untestable ({len(items)}):"]
        lines += [f"- #{n} {', '.join(u['tags'])}" + (" (partly tested)" if u.get("partly") else "")
              + f": {u['reason']}" for n, u in items] or ["- none"]
        moved = [m for m in check.get("moved") or [] if m["file"] in {f"eval.{st['feature']}.feature.md" for st in sl["stories"]}]
        if moved:
            lines += ["", f"Story lines that moved or changed since the eval was written ({len(moved)}) — the scenarios "
                      "stay as they are; a person judges whether they still fit:"]
            lines += [f"- {m['file']} {m['tag']} ({', '.join(m['scenarios']) or 'no scenario'}): was \"{m['was']}\", "
                      f"now \"{m['now']}\"" for m in moved]
        if src["out_of_slice"]:
            lines += ["", "Out of the slice (kept, not run): " + ", ".join(src["out_of_slice"])]
        lines += ["", f"The files: {src['folder']}/ (open them for the detail).", ""]
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
