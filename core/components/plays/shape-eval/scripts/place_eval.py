#!/usr/bin/env python3
"""place_eval.py — put the skill's drafts into each slice's evals folder; an eval is a fixed yardstick (C2, C7).

    python3 place_eval.py --inputs <working>inputs.json --drafts <working>drafts \
        --out <working>place.json --yardstick-out <working>yardstick-check.json
    python3 place_eval.py --undo <working>place.json --inputs <working>inputs.json
    python3 place_eval.py --clear <working>clear.json --inputs <working>inputs.json

The drafts are in `<drafts>/<slug>/`: one story file `eval.<feature-id>.feature.md` for each
story of the slice's map, and the slice file `eval.<slice-id>.md`. For each ready slice:

  - A story file the slice does not have yet is written as drafted.
  - A story file the slice has keeps every line it has. Only the drafted scenarios that cover
    something the file does not cover yet (a tag no scenario and no Untestable line of the file
    has) are added, before its "Untestable" section, and only the drafted Untestable lines for
    what is still not covered are added to that section. A file with nothing to add is not
    touched.
  - A story file whose feature left the slice (in inputs.json `out_of_slice`) stays; its first
    tag line gains `@out-of-slice`.
  - The slice file is written from the draft, unless what it says (the stories in order, the
    stories out of the slice, the surface kind, the time limit, the names) is the same as the file
    the slice has; then the file is not touched.
A slice that is not ready gets nothing. Each placing starts from the state before the run: an
earlier place.json of the run is undone first, and the files the slice had are read from the copies
in `<working>inputs/existing/<slug>/`, so placing again after a fix gives the same files.

The yardstick check reads each story file the slice had before and the file now: every scenario
it had must be in it, word for word (C7). It writes yardstick-check.json {ok, problems, kept,
added}. place.json lists each file written, with whether it was there before, for the guard and
for --undo, which puts back each file as it was before the run (a stop or a change, C9). A story
file's "Lines covered" list only grows: a placed scenario's covered lines are added, and a line the
file had stays as it was (C16). --clear deletes the drafts, the hidden-file copy and the copies of
the slice's eval files from before the run, and writes clear.json {ok, removed, left}: run it after
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

OUT = "out-of-slice"


def covered(parsed):
    tags = set()
    for sc in parsed["scenarios"]:
        tags.update(sc["tags"])
    for u in parsed["untestable"]:
        tags.update(u["tags"])
    return tags


def merge_story(old, draft):
    """(new text, scenarios added, untestable lines added) for a story file the slice has."""
    po, pd = ec.parse_story_file(old), ec.parse_story_file(draft)
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


def same_slice(a, b):
    pa, pb = ec.parse_slice_file(a), ec.parse_slice_file(b)
    keys = ("stories", "out_of_slice", "surface_kind", "time_limit", "names")
    return all(pa[k] == pb[k] for k in keys) and sorted(pa["names"]) == sorted(pb["names"])


def plan_slice(sl, working, drafts):
    existing_dir = os.path.join(working, "inputs", "existing", sl["slug"])
    draft_dir = os.path.join(drafts, sl["slug"])
    writes, added_sc, added_un, kept, problems = {}, 0, 0, 0, []

    def before(name):
        p = os.path.join(existing_dir, name)
        return ec.read_text(p, "an eval file") if os.path.isfile(p) else None

    for story in sl["stories"]:
        name = ec.story_file_name(story["feature"])
        dpath = os.path.join(draft_dir, name)
        if not os.path.isfile(dpath):
            problems.append(f"no draft {name} for story #{story['issue']}")
            continue
        draft, old = ec.read_text(dpath, "a draft"), before(name)
        if old is None:
            writes[name] = draft
        else:
            text, n_sc, n_un = merge_story(old, draft)
            added_sc, added_un = added_sc + n_sc, added_un + n_un
            if text != old:
                writes[name] = text
    for name in sl["out_of_slice"]:
        old = before(name)
        text = mark_out(old)
        if text != old:
            writes[name] = text
    sname = ec.slice_file_name(sl["slice_id"])
    spath = os.path.join(draft_dir, sname)
    if not os.path.isfile(spath):
        problems.append(f"no draft {sname}")
    else:
        draft, old = ec.read_text(spath, "a draft"), before(sname)
        if old is None or not same_slice(old, draft):
            writes[sname] = draft
    # the yardstick: every scenario of every story file the slice had stays, word for word
    for name in sl["existing"]:
        if not name.endswith(".feature.md"):
            continue
        old = before(name)
        now = writes.get(name, old)
        for sc in ec.parse_story_file(old)["scenarios"]:
            kept += 1
            if sc["raw"] not in now:
                problems.append(f"{name}: the scenario '{sc['title']}' changed or went away")
    return writes, added_sc, added_un, kept, problems


def place(inputs, working, drafts):
    record = {"ok": True, "slices": [], "files": []}
    yard = {"ok": True, "problems": [], "kept": 0, "added": 0}
    for sl in inputs["slices"]:
        if not sl["ready"]:
            record["slices"].append({"slice": sl["slice_id"], "skipped": sl["reason"]})
            continue
        writes, n_sc, n_un, kept, problems = plan_slice(sl, working, drafts)
        yard["kept"] += kept
        yard["added"] += n_sc
        missing = [p for p in problems if p.startswith("no draft")]
        if missing:
            raise ec.Refused("; ".join(missing))
        if problems:
            yard["ok"] = False
            yard["problems"] += problems
            continue
        written = []
        for name, text in writes.items():
            path = os.path.join(sl["folder"], name)
            record["files"].append({"path": path, "existed": name in sl["existing"]})
            ec.atomic_write(path, text)
            written.append(path)
        record["slices"].append({"slice": sl["slice_id"], "written": written,
                                 "added_scenarios": n_sc, "added_untestable": n_un,
                                 "new_files": [os.path.join(sl["folder"], n) for n in writes
                                               if n not in sl["existing"]]})
    record["ok"] = yard["ok"]
    return record, yard


def clear(working, inputs):
    """C15: delete every copy of an eval or the hidden file from the run's short-term memory."""
    import shutil
    removed = []
    for path in [os.path.join(working, "drafts"), os.path.join(working, "inputs", "existing")] + \
            [s["hidden"] for s in inputs["slices"] if s.get("hidden")]:
        if os.path.isdir(path):
            shutil.rmtree(path)
            removed.append(path)
        elif os.path.isfile(path):
            os.unlink(path)
            removed.append(path)
    left = [p for p in (os.path.join(working, "drafts"), os.path.join(working, "inputs", "existing"))
            if os.path.exists(p)] + [s["hidden"] for s in inputs["slices"] if s.get("hidden") and os.path.exists(s["hidden"])]
    return {"ok": not left, "removed": removed, "left": left}


def undo(place_path, inputs):
    rec = ec.read_json(place_path, "the place record")
    slug_of = {s["folder"]: s["slug"] for s in inputs["slices"] if s.get("folder")}
    undone = []
    for f in rec.get("files") or []:
        path = f["path"]
        if f["existed"]:
            slug = slug_of[os.path.dirname(path)]
            src = os.path.join(inputs["_working"], "inputs", "existing", slug, os.path.basename(path))
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
    ap.add_argument("--clear", help="write clear.json here: delete the drafts and every copy of an eval or hidden file (C15)")
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
