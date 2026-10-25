#!/usr/bin/env python3
"""write_plan_file.py — make or update the intent's one plan file after the tracker writes (/shape-plan, C1, C4, C6, C7).

    python3 write_plan_file.py --plan-file <plans>/<id>.yaml --gather <gather.json> \
        --record <tracker-record.json> --out <working>/plan-write.json

When the plan file is missing it is made: `id`, `title` (the business intent's title),
`status: active` and `tree`. Then, for each slice of gather.json, from the record:
  - when no node of the tree has `represents: <slice id>`, an epic node is added at the end
    of the tree (`issue`, `kind: epic`, `title`, `status`, `represents`), with one story node
    for each line of the epic's map (`issue`, `kind: story`, `title`, `status`, `represents`)
    as its children;
  - when the epic node is there, a story node is added under it for each feature of the map
    that has none;
  - each moved-out story's node is taken out of the tree.
The file is changed line by line: every other node, line and comment stays as it is. With
nothing to change, the file is not written and stays byte for byte the same. A new node's
status is `next`.

A record that reads `ok: false` (the tracker failed part way) is still written: each issue it
lists gets its node and its mark, so the next run finds it and makes no copy. The run then
closes HALTED; `record_ok` in the output says so.

Output: {ok, path, made, changed, added: [{issue, kind, represents}], removed: [..], record_ok}
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


def render(d, issue, kind, title, represents, kids=()):
    p = " " * d
    out = [f"{p}- issue: {scalar(issue)}", f"{p}  kind: {kind}", f"{p}  title: {scalar(title)}",
           f"{p}  status: next", f"{p}  represents: {scalar(represents)}"]
    if kids:
        out.append(f"{p}  children:")
        for k in kids:
            out += render(d + 2, *k)
    return out


def edit(lines, gather, rec):
    added, removed = [], []
    titles = rec.get("titles") or {}
    for sl in gather.get("slices") or []:
        sid = sl["id"]
        if sid not in (rec.get("epics") or {}):
            continue
        epic_no = int(rec["epics"][sid])
        pairs = [(f, int(n)) for f, n in (rec.get("maps") or {}).get(sid, {}).items()]
        t, d, tree = parse_tree(lines)
        if t is None:
            lines.append("tree: []")
            t, d, tree = parse_tree(lines)
        node = find(tree, sid)
        if node is None:
            kids = [(n, "story", titles.get(str(n), f), f) for f, n in pairs]
            block = render(d, epic_no, "epic", titles.get(str(epic_no), sid), sid, kids)
            if tree:
                at = tree[-1]["end"]
            else:
                lines[t] = "tree:"
                at = t + 1
            lines[at:at] = block
            added.append({"issue": epic_no, "kind": "epic", "represents": sid})
            added += [{"issue": n, "kind": "story", "represents": f} for f, n in pairs]
            continue
        for mo in rec.get("moved_out") or []:
            if int(mo.get("epic", -1)) != epic_no:
                continue
            node = find(parse_tree(lines)[2], sid)
            child = next((c for c in node["children"] if rep(c) == mo["feature"]), None)
            if child is None:
                continue
            del lines[child["start"]:child["end"]]
            removed.append({"issue": int(mo["issue"]), "kind": "story", "represents": mo["feature"]})
            node = find(parse_tree(lines)[2], sid)
            if node["children_line"] is not None and not node["children"]:
                lines[node["children_line"]] = " " * (node["indent"] + 2) + "children: []"
        for f, n in pairs:
            node = find(parse_tree(lines)[2], sid)
            if any(rep(c) == f for c in node["children"]):
                continue
            ci = node["indent"] + 2
            if node["children"]:
                cd = node["children"][-1]["indent"]
                at = node["children"][-1]["end"]
                lines[at:at] = render(cd, n, "story", titles.get(str(n), f), f)
            elif node["children_line"] is not None:
                lines[node["children_line"]] = " " * ci + "children:"
                at = node["children_line"] + 1
                lines[at:at] = render(ci, n, "story", titles.get(str(n), f), f)
            else:
                at = node["end"]
                lines[at:at] = [" " * ci + "children:"] + render(ci, n, "story", titles.get(str(n), f), f)
            added.append({"issue": n, "kind": "story", "represents": f})
    return added, removed


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
        if not isinstance(rec.get("epics"), dict):
            raise pc.Refused("the tracker record has no epics; the plan file is not written")
        made = not os.path.isfile(args.plan_file)
        if made:
            lines = [f"# Plan {gather['plan_id']}. Its ID is the business intent's issue number.",
                     "# Made by /shape-plan. Status: done | now | next | blocked | later.",
                     f"id: {scalar(int(gather['plan_id']))}",
                     f"title: {scalar(gather.get('intent_title') or 'Plan ' + str(gather['plan_id']))}",
                     "status: active", "tree: []"]
        else:
            original = pc.read_text(args.plan_file)
            if not isinstance(pc.yaml.safe_load(original), dict):
                raise pc.Refused("the plan file must be a YAML mapping")
            lines = original.splitlines()
        added, removed = edit(lines, gather, rec)
        text = "\n".join(lines) + "\n"
        try:
            pc.yaml.safe_load(text)
        except YAML_ERROR as exc:
            raise pc.Refused(f"the changed plan file would not read as YAML: {exc}")
    except (pc.Refused, KeyError, ValueError, YAML_ERROR) as exc:
        sys.stderr.write(f"write_plan_file.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    changed = made or bool(added or removed)
    if changed:
        pc.atomic_write(args.plan_file, text)
    result = {"ok": True, "path": args.plan_file, "made": made, "changed": changed,
              "added": added, "removed": removed, "record_ok": bool(rec.get("ok"))}
    pc.write_json(args.out, result)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
