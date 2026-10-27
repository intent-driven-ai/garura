#!/usr/bin/env python3
"""
edit_slice.py — the edit path of /shape-slice (C20): change only the parts of an existing slice
that the person named, and nothing else.

    python3 edit_slice.py snapshot --root <product-os dir> --spine <_spine.yaml> \\
        (--slice-id <id> | --intent <bi-n>) --plans-root <plans dir> --working <working> \\
        --out <edit-before.json>
    python3 edit_slice.py check-list --before <edit-before.json> --list <edit-list.json> \\
        --out <edit-list-check.json>
    python3 edit_slice.py apply --before <edit-before.json> --list <edit-list.json> \\
        --request <edit-request.md> --by "<the person's role>" --at <date> --out <edit-apply.json>
    python3 edit_slice.py check --before <edit-before.json> --list <edit-list.json> \\
        --request <edit-request.md> --apply <edit-apply.json> --out <edit-check.json>
    python3 edit_slice.py restore --before <edit-before.json> --out <edit-restore.json>

The three records an edit may change, and the parts of each (the list's `file` and `part`):
  record  — the slice record: `slice.name`, `slice.outcome`, `surface.user_action`
  hidden  — the hidden file: `<feature id>/<F id>/when`, `.../way_back`, `.../who_fixes`
            (who fixes is exactly "the builder can fix this alone" or "a person must decide")
  spine   — a part's spine one-line: `<part id>/one_line`

edit-list.json (written by author-slice, edit mode):
    {changes: [{file, part, old, new, why}], out_of_date: [{record, why}],
     not_editable: [{what, why}]}

snapshot finds the slice (--slice-id, or the one slice the spine links to --intent) and
copies the three records into <working>edit-before/ and names them. It also records whether
the slice is in progress (`in_progress`, and each `epics` entry {id, status} past ready, the rule
find_serving_slice.py holds): an edit may change a slice in progress, and the brief says so. check-list refuses
(exit 1) a change to another file or part, an `old` that is not the part's text now, an empty
`new`, a `new` equal to `old`, a who fixes that is neither answer, or two changes to one part;
with --evals, it also refuses an out-of-date eval file that is not one of the slice's eval files.
apply writes exactly the list through safe_write.atomic_write: the slice record keeps its layout
(spine_text), the hidden file changes only the named field lines, and the spine only the named
one-lines; it adds a history line (who asked, when, their words) to the slice record (`edits:`)
on every edit, and, when the hidden file changes, to the hidden file's opening lines. check builds, from the
snapshot, what each record must read after the list and the history lines, and compares it with
each record on disk: any other change is a problem (exit 1). restore writes the snapshot back.
Exit 0 ok, 1 problems, 2 refused or usage error.
"""

import argparse
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spine_text  # noqa: E402
from safe_write import atomic_write  # noqa: E402
from find_serving_slice import IN_PROGRESS  # noqa: E402

WHO = ("the builder can fix this alone", "a person must decide")
RECORD_PARTS = {"slice.name": ("slice", "name"), "slice.outcome": ("slice", "outcome"),
                "surface.user_action": ("surface", "user_action")}
HIDDEN_KEYS = {"when": "When", "way_back": "Way back", "who_fixes": "Who fixes"}
HEAD = re.compile(r"^## (?P<feature>[^:\s]+): ")
FOR = re.compile(r"^- For (?P<id>F\d+)\s*$")
FIELD = re.compile(r"^(?P<lead>\s+- (?P<key>When|Way back|Who fixes):\s*)(?P<text>.*?)\s*$")
KINDS = ("domains", "capabilities", "features")


class Refused(Exception):
    pass


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def norm(text):
    return " ".join(str(text or "").split())


def load_json(path, what):
    try:
        return json.loads(read(path))
    except (OSError, ValueError) as exc:
        raise Refused(f"cannot read {what} {path}: {exc}")


def emit(out, data, code):
    atomic_write(out, json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))
    return code


# -- the slice's records ----------------------------------------------------------------------
def cmd_snapshot(args):
    spine = yaml.safe_load(read(args.spine)) or {}
    slices = [s for s in spine.get("slices") or [] if isinstance(s, dict)]
    if args.slice_id:
        found = [s for s in slices if s.get("id") == args.slice_id]
        if not found:
            raise Refused(f"the spine has no slice '{args.slice_id}'")
    else:
        found = [s for s in slices if args.intent in (s.get("intents") or [])]
        if len(found) != 1:
            raise Refused(f"the spine has {len(found)} slices for {args.intent}; an edit needs exactly one "
                          "(give --slice-id)")
    sl = found[0]
    args.slice_id = sl["id"]
    record = os.path.join(args.root, sl.get("record") or f"slices/{args.slice_id}.yaml")
    plan_id = str((sl.get("intents") or [""])[0]).replace("bi-", "")
    hidden = os.path.join(args.plans_root, plan_id, "evals", sl["slug"], "failure-and-recovery.md")
    files = {"record": record, "hidden": hidden, "spine": args.spine}
    copies = os.path.join(args.working, "edit-before")
    os.makedirs(copies, exist_ok=True)
    busy = [{"id": e.get("id"), "status": e.get("status")} for e in spine.get("epics") or []
            if isinstance(e, dict) and e.get("slice_ref") == args.slice_id and e.get("status") in IN_PROGRESS]
    out = {"slice": args.slice_id, "in_progress": bool(busy), "epics": busy, "files": {}, "copies": {}}
    for name, path in files.items():
        if not os.path.isfile(path):
            raise Refused(f"the {name} file is not at {path}")  # before any copy, so none is left behind
    for name, path in files.items():
        copy = os.path.join(copies, f"{name}{os.path.splitext(path)[1]}")
        atomic_write(copy, read(path))
        out["files"][name], out["copies"][name] = path, copy
    return emit(args.out, dict(out, ok=True), 0)


def record_value(data, part):
    top, key = RECORD_PARTS[part]
    return (data.get(top) or {}).get(key)


def hidden_field(lines, feature, fid, key):
    """The index and the text of the named field line of the hidden file, or (None, None)."""
    in_block, in_rec = False, False
    for i, ln in enumerate(lines):
        h = HEAD.match(ln)
        if h:
            in_block, in_rec = h.group("feature") == feature, False
            continue
        if not in_block:
            continue
        f = FOR.match(ln)
        if f:
            in_rec = f.group("id") == fid
            continue
        m = FIELD.match(ln)
        if in_rec and m and m.group("key") == HIDDEN_KEYS[key]:
            return i, m.group("text")
    return None, None


def spine_part(data, pid):
    for kind in KINDS:
        for e in data.get(kind) or []:
            if isinstance(e, dict) and e.get("id") == pid:
                return e
    return None


def current(before, change):
    """The part's text now, in the snapshot; raises Refused for a part an edit may not change."""
    f, part = change.get("file"), str(change.get("part") or "")
    text = read(before["copies"][f]) if f in before["copies"] else None
    if f == "record":
        if part not in RECORD_PARTS:
            raise Refused(f"'{part}' is not a part an edit may change in the slice record")
        return record_value(yaml.safe_load(text) or {}, part)
    if f == "hidden":
        bits = part.split("/")
        if len(bits) != 3 or bits[2] not in HIDDEN_KEYS or not re.match(r"^F\d+$", bits[1]):
            raise Refused(f"'{part}' is not '<feature>/<F id>/when|way_back|who_fixes'")
        return hidden_field(text.splitlines(), *bits)[1]
    if f == "spine":
        bits = part.split("/")
        if len(bits) != 2 or bits[1] != "one_line":
            raise Refused(f"'{part}' is not '<part id>/one_line'")
        e = spine_part(yaml.safe_load(text) or {}, bits[0])
        return e.get("one_line") if e else None
    raise Refused(f"'{f}' is not a file an edit may change (record, hidden or spine)")


def list_problems(before, lst):
    problems, seen = [], set()
    changes = lst.get("changes") or []
    if not changes:
        problems.append("the list names no change")
    for c in changes:
        key = (c.get("file"), c.get("part"))
        try:
            now = current(before, c)
        except Refused as exc:
            problems.append(str(exc))
            continue
        if key in seen:
            problems.append(f"{key[1]} is changed twice")
        seen.add(key)
        if now is None:
            problems.append(f"{key[1]} is not in the {key[0]} file")
        elif norm(now) != norm(c.get("old")):
            problems.append(f"{key[1]}: the old text is not what the {key[0]} file says now")
        if not norm(c.get("new")):
            problems.append(f"{key[1]}: the new text is empty")
        elif norm(c.get("new")) == norm(c.get("old")):
            problems.append(f"{key[1]}: the new text is the old text")
        if c.get("file") == "hidden" and str(c.get("part", "")).endswith("/who_fixes") \
                and norm(c.get("new")) not in WHO:
            problems.append(f"{key[1]}: who fixes must be '{WHO[0]}' or '{WHO[1]}'")
    return problems


def eval_problems(lst, evals_path):
    """An out-of-date record that names an eval file must be one of the slice's eval files, by
    name: the skill sees only their names, never their text."""
    with open(evals_path, encoding="utf-8") as fh:
        names = {ln.strip() for ln in fh if ln.strip()}
    problems = []
    for o in lst.get("out_of_date") or []:
        rec = str(o.get("record") or "")
        base = os.path.basename(rec)
        if "eval" in base and base not in names:
            problems.append(f"'{rec}' is named as out of date, but it is not one of the slice's eval files")
    return problems


def cmd_check_list(args):
    before = load_json(args.before, "edit-before.json")
    lst = load_json(args.list, "edit-list.json")
    problems = list_problems(before, lst)
    if args.evals:
        problems += eval_problems(lst, args.evals)
    return emit(args.out, {"ok": not problems, "problems": problems}, 0 if not problems else 1)


# -- what each record must read after the edit ------------------------------------------------
def history_entry(request, by, at, parts):
    return {"at": at, "by": by, "words": norm(request), "changed": parts}


def expected(before, lst, request, by, at):
    """{file: the text it must hold after the list and the history lines} for the files changed."""
    changes = lst.get("changes") or []
    out = {}
    for f in ("record", "hidden", "spine"):
        mine = [c for c in changes if c.get("file") == f]
        if not mine and not (f == "record" and changes):  # every edit leaves its history line on the record
            continue
        text = read(before["copies"][f])
        if f == "record":
            old = yaml.safe_load(text) or {}
            new = json.loads(json.dumps(old))
            for c in mine:
                top, key = RECORD_PARTS[c["part"]]
                new[top][key] = norm(c["new"])
            body = spine_text.dump(text, old, new)[0]
            entry = history_entry(request, by, at, [c["part"] for c in changes])
            if "edits" in old:
                body = body.rstrip("\n") + "\n" + yaml.safe_dump([entry], sort_keys=False, allow_unicode=True)
            else:
                body = body.rstrip("\n") + "\n" + yaml.safe_dump({"edits": [entry]}, sort_keys=False,
                                                                  allow_unicode=True)
            out[f] = body
        elif f == "hidden":
            lines = text.splitlines(keepends=True)
            plain = [ln.rstrip("\n") for ln in lines]
            for c in mine:
                feature, fid, key = c["part"].split("/")
                i, _ = hidden_field(plain, feature, fid, key)
                m = FIELD.match(plain[i])
                end = "\n" if lines[i].endswith("\n") else ""
                lines[i] = f"{m.group('lead')}{norm(c['new'])}{end}"
            first = next(i for i, ln in enumerate(lines) if HEAD.match(ln))
            note = (f"Edited on {at} by {by}, on the person's words: \"{norm(request)}\" "
                    f"({', '.join(c['part'] for c in mine)}).\n\n")
            out[f] = "".join(lines[:first]) + note + "".join(lines[first:])
        else:
            old = yaml.safe_load(text) or {}
            new = json.loads(json.dumps(old))
            for c in mine:
                spine_part(new, c["part"].split("/")[0])["one_line"] = norm(c["new"])
            out[f] = spine_text.dump(text, old, new)[0]
    return out


def cmd_apply(args):
    before = load_json(args.before, "edit-before.json")
    lst = load_json(args.list, "edit-list.json")
    problems = list_problems(before, lst)
    if problems:
        raise Refused("the list does not hold: " + "; ".join(problems))
    request = read(args.request)
    want = expected(before, lst, request, args.by, args.at)
    for f, text in want.items():
        atomic_write(before["files"][f], text)
    return emit(args.out, {"ok": True, "written": sorted(want), "by": args.by, "at": args.at,
                           "changes": len(lst.get("changes") or [])}, 0)


def cmd_check(args):
    before = load_json(args.before, "edit-before.json")
    lst = load_json(args.list, "edit-list.json")
    applied = load_json(args.apply, "edit-apply.json")
    want = expected(before, lst, read(args.request), applied["by"], applied["at"])
    problems = []
    for f, path in before["files"].items():
        now = read(path)
        if f in want:
            if now != want[f]:
                problems.append(f"the {f} file holds a change that is not on the list")
        elif now != read(before["copies"][f]):
            problems.append(f"the {f} file changed, but the list names no change to it")
    return emit(args.out, {"ok": not problems, "problems": problems,
                           "changes": len(lst.get("changes") or [])}, 0 if not problems else 1)


def cmd_restore(args):
    before = load_json(args.before, "edit-before.json")
    for f, path in before["files"].items():
        atomic_write(path, read(before["copies"][f]))
    return emit(args.out, {"ok": True, "restored": sorted(before["files"])}, 0)


def main(argv=None):
    ap = argparse.ArgumentParser(description="The edit path of /shape-slice.")
    sub = ap.add_subparsers(dest="command", required=True)
    s = sub.add_parser("snapshot")
    for a in ("--root", "--spine", "--plans-root", "--working", "--out"):
        s.add_argument(a, required=True)
    which = s.add_mutually_exclusive_group(required=True)
    which.add_argument("--slice-id")
    which.add_argument("--intent", help="the business intent's id (bi-<n>): its one slice")
    for name in ("check-list", "apply", "check", "restore"):
        p = sub.add_parser(name)
        p.add_argument("--before", required=True)
        p.add_argument("--out", required=True)
        if name != "restore":
            p.add_argument("--list", required=True)
        if name == "check-list":
            p.add_argument("--evals", help="edit-evals.txt: the names of the slice's eval files")
        if name in ("apply", "check"):
            p.add_argument("--request", required=True)
        if name == "apply":
            p.add_argument("--by", required=True)
            p.add_argument("--at", required=True)
        if name == "check":
            p.add_argument("--apply", required=True)
    args = ap.parse_args(argv)
    try:
        return {"snapshot": cmd_snapshot, "check-list": cmd_check_list, "apply": cmd_apply,
                "check": cmd_check, "restore": cmd_restore}[args.command](args)
    except Refused as exc:
        sys.stderr.write(f"edit_slice.py: not done — {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
