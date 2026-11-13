#!/usr/bin/env python3
"""place_eval.py — put the skill's drafts into the plan's evals folder; an eval is a fixed yardstick (C2, C7).

    python3 place_eval.py --inputs <working>inputs.json --drafts <working>drafts \
        --out <working>place.json --yardstick-out <working>yardstick-check.json
    python3 place_eval.py --undo <working>place.json --inputs <working>inputs.json
    python3 place_eval.py --clear <working>clear.json --inputs <working>inputs.json

The drafts are in `<drafts>/`: one feature file `eval.<feature-id>.feature.md` for each Feature
issue of the epic's map, and the plan file `eval.<plan-id>.md`. When the plan is ready:

  - A feature file the plan does not have yet is written as drafted.
  - A feature file the plan has keeps every line it has. Only the drafted scenarios that cover
    something the file does not cover yet (a tag no scenario and no Untestable line of the file
    has) are added, before its "Untestable" section, and only the drafted Untestable lines for
    what is still not covered are added to that section. A file with nothing to add is not
    touched.
  - A feature file whose feature left the plan (in inputs.json `out_of_plan`) stays; its first
    tag line gains `@out-of-plan`.
  - The plan file is written from the draft, unless what it says (each slice section with its
    surface kind, its time limit and its features in order, the features out of the plan, the
    names) is the same as the file the plan has; then the file is not touched.
A plan that is not ready gets nothing. Each placing starts from the state before the run: an
earlier place.json of the run is undone first, and the files the plan had are read from the copies
in `<working>inputs/existing/`, so placing again after a fix gives the same files.

The yardstick check reads each feature file the plan had before and the file now: every scenario
it had must be in it, word for word (C7). It writes yardstick-check.json {ok, problems, kept,
added}. place.json lists each file written, with whether it was there before, for the guard and
for --undo, which puts back each file as it was before the run (a stop or a change, C9). A feature
file's "Lines covered" list only grows: a placed scenario's covered lines are added, and a line the
file had stays as it was (C16). --clear deletes the drafts, the hidden-file copies and the copies of
the plan's eval files from before the run, and writes clear.json {ok, removed, left}: run it after
the eval commit and after a stop's undo (C15).
Exit 0 written and the yardstick holds, 1 the yardstick does not hold, 2 refused.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval_common as ec  # noqa: E402

OUT = "out-of-plan"


def covered(parsed):
    tags = set()
    for sc in parsed["scenarios"]:
        tags.update(sc["tags"])
    for u in parsed["untestable"]:
        tags.update(u["tags"])
    return tags


def merge_feature(old, draft):
    """(new text, scenarios added, untestable lines added) for a feature file the plan has."""
    po, pd = ec.parse_feature_file(old), ec.parse_feature_file(draft)
    have = covered(po)
    new_sc = [sc for sc in pd["scenarios"] if set(sc["tags"]) - have]
    after = have | {t for sc in new_sc for t in sc["tags"]}
    new_un = [u for u in pd["untestable"] if set(u["tags"]) - after]
    new_cov = {t: x for t, x in pd["lines_covered"].items()
               if t not in po["lines_covered"] and t in {t for sc in new_sc for t in sc["tags"]}}
    if not new_sc and not new_un:
        return old, 0, 0
    lines = old.rstrip("\n").split("\n")

    def section(name):
        return next((i for i, ln in enumerate(lines) if ln.lstrip().startswith("#")
                     and ln.strip().lstrip("#").strip() == name), None)

    first = min([i for i in (section("Untestable"), section("Lines covered")) if i is not None], default=None)
    head, tail = (lines, []) if first is None else (lines[:first], lines[first:])
    while head and not head[-1].strip():
        head.pop()
    for sc in new_sc:
        head += ["", sc["raw"]]
    tail = add_lines(tail, "Untestable",
                     ["- " + " ".join(f"`@{t}`" for t in u["tags"]) + f": {u['reason']}" for u in new_un])
    tail = add_lines(tail, "Lines covered", [f"- `@{t}`: {x}" for t, x in new_cov.items()])
    text = "\n".join(head + ([""] + tail if tail else [])) + "\n"
    return text, len(new_sc), len(new_un)


def add_lines(tail, name, new):
    """Append lines at the end of the `## <name>` section of `tail` (made at the end when missing)."""
    if not new:
        return tail
    at = next((i for i, ln in enumerate(tail) if ln.lstrip().startswith("#")
               and ln.strip().lstrip("#").strip() == name), None)
    if at is None:
        while tail and not tail[-1].strip():
            tail.pop()
        return tail + ([""] if tail else []) + [f"## {name}", ""] + new
    end = next((i for i in range(at + 1, len(tail)) if tail[i].lstrip().startswith("#")), len(tail))
    body = tail[at + 1:end]
    while body and not body[-1].strip():
        body.pop()
    return tail[:at + 1] + body + new + ([""] + tail[end:] if end < len(tail) else [])


def mark_out(text):
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ec.TAG_LINE.match(ln):
            if f"`@{OUT}`" not in ln:
                lines[i] = ln.rstrip() + f" `@{OUT}`"
            return "\n".join(lines)
        if ec.KEYWORD.match(ln):
            break
    return f"`@{OUT}`\n" + text


def same_plan(a, b):
    pa, pb = ec.parse_plan_file(a), ec.parse_plan_file(b)
    return (pa["slices"] == pb["slices"] and pa["out_of_plan"] == pb["out_of_plan"]
            and sorted(pa["names"]) == sorted(pb["names"]))


def plan_writes(inputs, working, drafts):
    existing_dir = os.path.join(working, "inputs", "existing")
    writes, added_sc, added_un, kept, problems = {}, 0, 0, 0, []

    def before(name):
        p = os.path.join(existing_dir, name)
        return ec.read_text(p, "an eval file") if os.path.isfile(p) else None

    for feat in inputs["features"]:
        name = ec.feature_file_name(feat["feature"])
        dpath = os.path.join(drafts, name)
        if not os.path.isfile(dpath):
            problems.append(f"no draft {name} for Feature issue #{feat['issue']}")
            continue
        draft, old = ec.read_text(dpath, "a draft"), before(name)
        if old is None:
            writes[name] = draft
        else:
            text, n_sc, n_un = merge_feature(old, draft)
            added_sc, added_un = added_sc + n_sc, added_un + n_un
            if text != old:
                writes[name] = text
    for name in inputs["out_of_plan"]:
        old = before(name)
        text = mark_out(old)
        if text != old:
            writes[name] = text
    pname = ec.plan_file_name(inputs["plan_id"])
    ppath = os.path.join(drafts, pname)
    if not os.path.isfile(ppath):
        problems.append(f"no draft {pname}")
    else:
        draft, old = ec.read_text(ppath, "a draft"), before(pname)
        if old is None or not same_plan(old, draft):
            writes[pname] = draft
    # the yardstick: every scenario of every feature file the plan had stays, word for word
    for name in inputs["existing"]:
        if not name.endswith(".feature.md"):
            continue
        old = before(name)
        now = writes.get(name, old)
        for sc in ec.parse_feature_file(old)["scenarios"]:
            kept += 1
            if sc["raw"] not in now:
                problems.append(f"{name}: the scenario '{sc['title']}' changed or went away")
    return writes, added_sc, added_un, kept, problems


def place(inputs, working, drafts):
    record = {"ok": True, "plan": inputs["plan_id"], "files": [], "new_files": [],
              "added_scenarios": 0, "added_untestable": 0, "skipped": None}
    yard = {"ok": True, "problems": [], "kept": 0, "added": 0}
    if not inputs["ready"]:
        record["skipped"] = inputs["reasons"]
        return record, yard
    writes, n_sc, n_un, kept, problems = plan_writes(inputs, working, drafts)
    yard["kept"], yard["added"] = kept, n_sc
    missing = [p for p in problems if p.startswith("no draft")]
    if missing:
        raise ec.Refused("; ".join(missing))
    if problems:
        yard["ok"] = record["ok"] = False
        yard["problems"] = problems
        return record, yard
    folder = inputs["folder"]
    for name, text in writes.items():
        path = os.path.join(folder, name)
        record["files"].append({"path": path, "existed": name in inputs["existing"]})
        ec.atomic_write(path, text)
        if name not in inputs["existing"]:
            record["new_files"].append(path)
    record["added_scenarios"], record["added_untestable"] = n_sc, n_un
    return record, yard


def clear(working, inputs):
    """C15: delete every copy of an eval or the hidden file from the run's short-term memory."""
    import shutil
    removed = []
    hidden = [s["hidden"] for s in inputs["slices"] if s.get("hidden")]
    for path in [os.path.join(working, "drafts"), os.path.join(working, "inputs", "existing")] + hidden:
        if os.path.isdir(path):
            shutil.rmtree(path)
            removed.append(path)
        elif os.path.isfile(path):
            os.unlink(path)
            removed.append(path)
    left = [p for p in (os.path.join(working, "drafts"), os.path.join(working, "inputs", "existing"))
            if os.path.exists(p)] + [h for h in hidden if os.path.exists(h)]
    return {"ok": not left, "removed": removed, "left": left}


def undo(place_path, inputs):
    rec = ec.read_json(place_path, "the place record")
    undone = []
    for f in rec.get("files") or []:
        path = f["path"]
        if f["existed"]:
            src = os.path.join(inputs["_working"], "inputs", "existing", os.path.basename(path))
            ec.atomic_write(path, ec.read_text(src, "the copy from before the run"))
        elif os.path.isfile(path):
            os.unlink(path)
        undone.append(path)
    return {"ok": True, "undone": undone}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Place the eval drafts; keep every scenario that was there.")
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--drafts")
    ap.add_argument("--out")
    ap.add_argument("--yardstick-out")
    ap.add_argument("--undo", help="a place.json: put back each file as it was before the run")
    ap.add_argument("--clear", help="write clear.json here: delete the drafts and every copy of an eval or a hidden file (C15)")
    args = ap.parse_args(argv)
    try:
        inputs = ec.read_json(args.inputs, "inputs.json")
        working = os.path.dirname(os.path.abspath(args.inputs))
        if args.undo:
            inputs["_working"] = working
            print(json.dumps(undo(args.undo, inputs), indent=2))
            if not args.clear:
                return 0
        if args.clear:
            res = clear(working, inputs)
            ec.write_json(args.clear, res)
            print(json.dumps(res, indent=2))
            return 0 if res["ok"] else 1
        if not (args.drafts and args.out and args.yardstick_out):
            raise ec.Refused("give --drafts, --out and --yardstick-out (or --undo)")
        if os.path.isfile(args.out):  # placing again after a fix starts from the state before the run
            inputs["_working"] = working
            undo(args.out, inputs)
        record, yard = place(inputs, working, args.drafts)
    except ec.Refused as exc:
        sys.stderr.write(f"place_eval.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    ec.write_json(args.yardstick_out, yard)
    ec.write_json(args.out, record)
    print(json.dumps({"ok": record["ok"], "files": len(record["files"]), "yardstick": yard["ok"]}, indent=2))
    return 0 if yard["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
