#!/usr/bin/env python3
"""write_plan_file.py — make or update the intent's one plan file after the tracker writes (/shape-plan, C1, C3, C6, C7).

    python3 write_plan_file.py --plan-file <plans>/<id>.yaml --gather <gather.json> \
        --record <tracker-record.json> --out <working>/plan-write.json

When the plan file is missing it is made. Its first lines name the business intent
(`intent: bi-<id>` and `title`, the intent's title); then `id`, `status: Not Started`,
`direction` (empty; a person sets it), the mark `epic: <issue>`, the `slices` list (each slice
of the plan with `status: Not Started`) and the `tree`: the plan's one epic node, with one
`feature` node under it for each line of the epic's map (`issue`, `kind: feature`, `title`,
`status`, `represents`, and `held_by: <epic>` for a Feature issue another plan's epic holds).
A feature left out of the plan (Completed or Dropped in the model, or not ready) gets no node.
A feature whose Feature issue is closed as completed by hand (`closed_by_hand` in the record)
gets its node with `status: Done`: its item follows its own issue (ADR 064).

When the plan file is there, it is updated: the `epic:` mark and each missing slice of the
`slices` list are added, the epic node is added when the tree has none with that issue, a
feature node is added under it for each line of the map that has none, and each moved-out
node is taken out. The file is changed line by line: every other node, line and comment stays
as it is. With nothing to change, the file is not written and stays byte for byte the same. A
new node's status, and a new slice's status, is `Not Started`.

A record that reads `ok: false` (the tracker failed part way) is still written: each issue it
lists gets its node and its mark, so the next run finds it and makes no copy. The run then
closes HALTED; `record_ok` in the output says so.

Output: {ok, path, made, changed, added: [{issue, kind, represents}], removed: [..],
        added_top: [{epic} | {slice}], record_ok}
Exit 0 written (or nothing to change); 2 refused or bad input (the file is not written).
No git, no network.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_common as pc  # noqa: E402

KEY = re.compile(r"^(?P<key>[A-Za-z_][\w-]*):(?:\s+(?P<val>.*?))?\s*$")
TREE = re.compile(r"^tree:(?:\s+(?P<val>.*?))?\s*$")
YAML_ERROR = pc.yaml.YAMLError if pc.yaml else ValueError


def indent_of(ln):
    return len(ln) - len(ln.lstrip(" "))


def neutral(ln):
    s = ln.strip()
    return not s or s.startswith("#")


def value(raw):
    if raw is None or raw == "":
        return None
    try:
        return pc.yaml.safe_load(raw)
    except pc.yaml.YAMLError:
        return raw


def scalar(v):
    text = pc.yaml.safe_dump({"k": v}, width=10 ** 9, allow_unicode=True,
                             default_flow_style=False).rstrip("\n")
    return text[3:]


def parse_list(lines, start, end, d):
    """The items of a block list whose dash sits at indent d, from line `start`."""
    items, i = [], start
    while i < end:
        ln = lines[i]
        if neutral(ln):
            i += 1
            continue
        if indent_of(ln) == d and ln[d:].startswith("- "):
            j = i + 1
            while j < end and (neutral(lines[j]) or indent_of(lines[j]) > d):
                j += 1
            k = j
            while k > i + 1 and neutral(lines[k - 1]):
                k -= 1
            items.append(parse_item(lines, i, k, d))
            i = j
            continue
        break
    return items


def parse_item(lines, s, e, d):
    ci = d + 2
    node = {"start": s, "end": e, "indent": d, "keys": {}, "children": [],
            "children_line": None, "children_inline": None}
    for i in range(s, e):
        ln = lines[i]
        if i == s:
            text = ln[ci:]
        elif not neutral(ln) and indent_of(ln) == ci and not ln[ci:].startswith("- "):
            text = ln[ci:]
        else:
            continue
        m = KEY.match(text)
        if m:
            node["keys"][m.group("key")] = (i, value(m.group("val")))
    if "children" in node["keys"]:
        c, val = node["keys"]["children"]
        node["children_line"] = c
        node["children_inline"] = val
        nxt = next((i for i in range(c + 1, e) if not neutral(lines[i])), None)
        if nxt is not None and lines[nxt].lstrip().startswith("- "):
            node["children"] = parse_list(lines, c + 1, e, indent_of(lines[nxt]))
    return node


def rep(node):
    return str(node["keys"].get("represents", (None, ""))[1] or "")


def parse_tree(lines):
    """(tree line index or None, top item indent, [nodes])."""
    t = next((i for i, ln in enumerate(lines) if TREE.match(ln)), None)
    if t is None:
        return None, 0, []
    nxt = next((i for i in range(t + 1, len(lines)) if not neutral(lines[i])), None)
    if nxt is None or not lines[nxt].lstrip().startswith("- "):
        return t, 0, []
    d = indent_of(lines[nxt])
    return t, d, parse_list(lines, t + 1, len(lines), d)


def find(nodes, represents):
    for n in nodes:
        if rep(n) == represents:
            return n
        hit = find(n["children"], represents)
        if hit:
            return hit
    return None


def find_issue(nodes, issue):
    return next((n for n in nodes if str(n["keys"].get("issue", (None, ""))[1]) == str(issue)), None)


def render(d, issue, kind, title, represents=None, held_by=None, kids=(), status="Not Started"):
    p = " " * d
    out = [f"{p}- issue: {scalar(issue)}", f"{p}  kind: {kind}", f"{p}  title: {scalar(title)}",
           f"{p}  status: {status}"]
    if represents:
        out.append(f"{p}  represents: {scalar(represents)}")
    if held_by is not None:
        out.append(f"{p}  held_by: {scalar(int(held_by))}")
    if kids:
        out.append(f"{p}  children:")
        for k in kids:
            out += render(d + 2, *k)
    return out


def top_key(lines, key):
    return next((i for i, ln in enumerate(lines) if re.match(rf"^{key}:(\s|$)", ln)), None)


def ensure_top(lines, rec):
    """Add the `epic:` mark and each slice missing from the `slices` list, before `tree:`.
    Returns what it added: {"epic": n} and {"slice": id}."""
    added = []
    t = top_key(lines, "tree")
    if t is None:
        lines.append("tree: []")
        t = len(lines) - 1
    if top_key(lines, "epic") is None and rec.get("epic") is not None:
        lines[t:t] = [f"epic: {scalar(int(rec['epic']))}"]
        added.append({"epic": int(rec["epic"])})
        t += 1
    s = top_key(lines, "slices")
    want = [sid for sid in rec.get("slices") or []]
    if s is None:
        block = (["slices:"] + [ln for sid in want for ln in (f"- id: {scalar(sid)}", "  status: Not Started")]
                 if want else ["slices: []"])
        lines[t:t] = block
        return added + [{"slice": sid} for sid in want]
    nxt = next((i for i in range(s + 1, len(lines)) if not neutral(lines[i])), None)
    items = parse_list(lines, s + 1, len(lines), indent_of(lines[nxt])) \
        if nxt is not None and lines[nxt].lstrip().startswith("- ") else []
    have = {str(it["keys"].get("id", (None, ""))[1]) for it in items}
    missing = [sid for sid in want if sid not in have]
    if not missing:
        return added
    d = items[-1]["indent"] if items else 0
    block = [ln for sid in missing for ln in (f"{' ' * d}- id: {scalar(sid)}", f"{' ' * d}  status: Not Started")]
    if items:
        at = items[-1]["end"]
    else:
        lines[s] = "slices:"
        at = s + 1
    lines[at:at] = block
    return added + [{"slice": sid} for sid in missing]


def edit(lines, gather, rec):
    added, removed = [], []
    titles = rec.get("titles") or {}
    held = rec.get("held") or {}
    done = rec.get("closed_by_hand") or {}
    added_slices = ensure_top(lines, rec)
    if rec.get("epic") is None:
        return added, removed, added_slices
    epic_no = int(rec["epic"])
    pairs = [(f, int(n)) for f, n in (rec.get("map") or {}).items()]
    t, d, tree = parse_tree(lines)
    node = find_issue(tree, epic_no)
    if node is None:
        kids = [(n, "feature", titles.get(str(n), f), f, held.get(f), (),
                 "Done" if f in done else "Not Started") for f, n in pairs]
        block = render(d, epic_no, "epic", titles.get(str(epic_no), f"Plan {gather.get('plan_id')}"),
                       None, None, kids)
        if tree:
            at = tree[-1]["end"]
        else:
            lines[t] = "tree:"
            at = t + 1
        lines[at:at] = block
        added.append({"issue": epic_no, "kind": "epic", "represents": None})
        added += [{"issue": n, "kind": "feature", "represents": f} for f, n in pairs]
        return added, removed, added_slices
    for mo in rec.get("moved_out") or []:
        if int(mo.get("epic", -1)) != epic_no:
            continue
        node = find_issue(parse_tree(lines)[2], epic_no)
        child = next((c for c in node["children"] if rep(c) == mo["feature"]), None)
        if child is None:
            continue
        del lines[child["start"]:child["end"]]
        removed.append({"issue": int(mo["issue"]), "kind": "feature", "represents": mo["feature"]})
        node = find_issue(parse_tree(lines)[2], epic_no)
        if node["children_line"] is not None and not node["children"]:
            lines[node["children_line"]] = " " * (node["indent"] + 2) + "children: []"
    for f, n in pairs:
        node = find_issue(parse_tree(lines)[2], epic_no)
        if any(rep(c) == f for c in node["children"]):
            continue
        ci = node["indent"] + 2
        new = (n, "feature", titles.get(str(n), f), f, held.get(f), (),
               "Done" if f in done else "Not Started")
        if node["children"]:
            cd = node["children"][-1]["indent"]
            at = node["children"][-1]["end"]
            lines[at:at] = render(cd, *new)
        elif node["children_line"] is not None:
            lines[node["children_line"]] = " " * ci + "children:"
            at = node["children_line"] + 1
            lines[at:at] = render(ci, *new)
        else:
            at = node["end"]
            lines[at:at] = [" " * ci + "children:"] + render(ci, *new)
        added.append({"issue": n, "kind": "feature", "represents": f})
    return added, removed, added_slices


def main(argv=None):
    ap = argparse.ArgumentParser(description="Make or update the plan file from the tracker record.")
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--gather", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        if pc.yaml is None:
            raise pc.Refused("PyYAML is needed (pip install pyyaml)")
        gather = pc.read_json(args.gather, "gather.json")
        rec = pc.read_json(args.record, "tracker-record.json")
        if not isinstance(rec.get("map"), dict) or not rec.get("slices"):
            raise pc.Refused("the tracker record has no map or no slices; the plan file is not written")
        made = not os.path.isfile(args.plan_file)
        if made:
            lines = [f"intent: {scalar('bi-' + str(gather['plan_id']))}",
                     f"title: {scalar(gather.get('intent_title') or 'Plan ' + str(gather['plan_id']))}",
                     f"id: {scalar(int(gather['plan_id']))}",
                     "status: Not Started", "direction:", "tree: []"]
        else:
            original = pc.read_text(args.plan_file)
            if not isinstance(pc.yaml.safe_load(original), dict):
                raise pc.Refused("the plan file must be a YAML mapping")
            lines = original.splitlines()
        added, removed, added_slices = edit(lines, gather, rec)
        text = "\n".join(lines) + "\n"
        try:
            pc.yaml.safe_load(text)
        except YAML_ERROR as exc:
            raise pc.Refused(f"the changed plan file would not read as YAML: {exc}")
    except (pc.Refused, KeyError, ValueError, YAML_ERROR) as exc:
        sys.stderr.write(f"write_plan_file.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    changed = made or bool(added or removed or added_slices)
    if changed:
        pc.atomic_write(args.plan_file, text)
    result = {"ok": True, "path": args.plan_file, "made": made, "changed": changed,
              "added": added, "removed": removed, "added_top": added_slices, "record_ok": bool(rec.get("ok"))}
    pc.write_json(args.out, result)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
