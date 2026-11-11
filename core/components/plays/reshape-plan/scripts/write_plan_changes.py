#!/usr/bin/env python3
"""write_plan_changes.py — write the approved list into the plan file, line by line (C7, C8).

    python3 write_plan_changes.py --plan-file <plans>/<id>.yaml --changes <changes.yaml> \
        --github-record <github-record.json> --at <UTC time> --out <plan-write.json>

Each entry changes only its own lines; every other line, comment and blank line stays byte for
byte:
  status        the item's `status:` line (a note after the old value goes with it: it described
                the old value)
  add           a new node at the end of its parent's children (`issue`, `kind`, `title`,
                `status: Not Started`)
  move          the node and everything under it, cut and put at the end of the new parent's
                children, indented to fit
  retitle       the item's `title:` line
  kind          the item's `kind:` value
  new-feature   a new node (or the story's own node) with `represents: <feature id>`
  plan-status   the top `status:` line;  plan-direction  the top `direction:` line
  text          nothing in the plan file (the item's text lives in the tracker)
A new item's number comes from the tracker record (the op that made it). Then `updated:` takes
the date. The plan file keeps no history: the landing's one commit names what was asked, the
overrides and what is owed, and git keeps it.

Before it writes, it reads the new text back as YAML and compares it with the old plan with the
list applied to it: they must be the same, or nothing is written (exit 2). With nothing to
change, the file is not written.

Output: {ok, path, changed: [numbers]}. Exit 0 written; 2 refused (not written).
No git, no network.
"""

import argparse
import copy
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402

yaml = ps.yaml
KEY = re.compile(r"^(?P<key>[A-Za-z_][\w-]*):(?:\s+(?P<val>.*?))?\s*$")


def indent_of(ln):
    return len(ln) - len(ln.lstrip(" "))


def neutral(ln):
    s = ln.strip()
    return not s or s.startswith("#")


def scalar(v):
    text = yaml.safe_dump({"k": v}, width=10 ** 9, allow_unicode=True, default_flow_style=False).rstrip("\n")
    return text[3:]


def parse_list(lines, start, end, d):
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
    node = {"start": s, "end": e, "indent": d, "keys": {}, "children": [], "children_line": None}
    for i in range(s, e):
        ln = lines[i]
        if i == s:
            text = ln[ci:]
        elif not neutral(ln) and indent_of(ln) == ci and not ln[ci:].startswith("- "):
            text = ln[ci:]
        else:
            continue
        m = KEY.match(text)
        if m and m.group("key") not in node["keys"]:
            node["keys"][m.group("key")] = i
    if "children" in node["keys"]:
        c = node["keys"]["children"]
        node["children_line"] = c
        nxt = next((i for i in range(c + 1, e) if not neutral(lines[i])), None)
        if nxt is not None and lines[nxt].lstrip().startswith("- "):
            node["children"] = parse_list(lines, c + 1, e, indent_of(lines[nxt]))
    return node


def parse_tree(lines):
    t = next((i for i, ln in enumerate(lines) if re.match(r"tree:", ln)), None)
    if t is None:
        raise ps.Refused("the plan file has no tree")
    nxt = next((i for i in range(t + 1, len(lines)) if not neutral(lines[i])), None)
    if nxt is None or not lines[nxt].lstrip().startswith("- "):
        return t, 0, []
    d = indent_of(lines[nxt])
    return t, d, parse_list(lines, t + 1, len(lines), d)


def node_of(lines, issue):
    def seek(nodes):
        for n in nodes:
            if "issue" in n["keys"] and str(issue_on(lines, n)) == str(issue):
                return n
            hit = seek(n["children"])
            if hit:
                return hit
        return None
    return seek(parse_tree(lines)[2])


def set_value(lines, at, key, value, keep_comment=True):
    ln = lines[at]
    m = re.match(rf"^(\s*(?:- )?{key}:)\s*(.*?)(\s+#.*)?$", ln.rstrip("\n"))
    comment = (m.group(3) or "") if (m and keep_comment) else ""
    lines[at] = f"{m.group(1)} {scalar(value)}{comment}"


def render(d, issue, kind, title, status="Not Started", represents=None):
    p = " " * d
    out = [f"{p}- issue: {scalar(issue)}", f"{p}  kind: {kind}", f"{p}  title: {scalar(title)}",
           f"{p}  status: {status}"]
    if represents:
        out.append(f"{p}  represents: {scalar(represents)}")
    return out


def insert_under(lines, parent_issue, block_at_indent):
    """Put a block (a function of its indent) at the end of the parent's children (or the tree)."""
    if parent_issue is None:
        t, d, tree = parse_tree(lines)
        if tree:
            at, d = tree[-1]["end"], tree[-1]["indent"]
        else:
            lines[t] = "tree:"
            at, d = t + 1, 0
        lines[at:at] = block_at_indent(d)
        return
    node = node_of(lines, parent_issue)
    if node is None:
        raise ps.Refused(f"#{parent_issue} is not in the plan file")
    ci = node["indent"] + 2
    if node["children"]:
        last = node["children"][-1]
        lines[last["end"]:last["end"]] = block_at_indent(last["indent"])
    elif node["children_line"] is not None:
        lines[node["children_line"]] = " " * ci + "children:"
        at = node["children_line"] + 1
        lines[at:at] = block_at_indent(ci)
    else:
        lines[node["end"]:node["end"]] = [" " * ci + "children:"] + block_at_indent(ci)


def top_key(lines, key):
    return next((i for i, ln in enumerate(lines) if re.match(rf"{key}:", ln)), None)


def set_top(lines, key, value, after="status"):
    at = top_key(lines, key)
    if at is None:
        ref = top_key(lines, after)
        lines.insert(ref + 1 if ref is not None else 0, f"{key}: {scalar(value)}")
    else:
        set_value(lines, at, key, value, keep_comment=False)


# --- the same changes, on the parsed plan, to check the text against ---

def data_apply(plan, changes, numbers):
    plan = copy.deepcopy(plan)

    def find(issue):
        return ps.find(plan, issue)

    def children_of(issue):
        if issue is None:
            return plan.setdefault("tree", [])
        node, _ = find(issue)
        if node.get("children") is None:
            node["children"] = []
        return node["children"]

    for e in changes.get("entries") or []:
        op = e["op"]
        if op == "status":
            find(e["issue"])[0]["status"] = e["to"]
        elif op == "retitle":
            find(e["issue"])[0]["title"] = e["to"]
        elif op == "kind":
            find(e["issue"])[0]["kind"] = e["to"]
        elif op in ("add", "new-feature"):
            issue = numbers.get(e["n"], e.get("issue"))
            parent = numbers.get(e.get("parent"), e.get("parent"))
            if op == "new-feature" and e.get("issue") is not None and find(issue)[0] is not None:
                node, at = find(issue)
                node["represents"] = e["feature"]
                if str((at or {}).get("issue")) != str(parent):
                    (at["children"] if at else plan["tree"]).remove(node)
                    children_of(parent).append(node)
                continue
            node = {"issue": issue, "kind": e.get("kind") or "story", "title": e.get("title"),
                    "status": "Not Started"}
            if op == "new-feature" or e.get("feature"):
                node["represents"] = e["feature"]
            children_of(parent).append(node)
        elif op == "move":
            node, at = find(e["issue"])
            (at["children"] if at else plan["tree"]).remove(node)
            children_of(numbers.get(e["to"], e["to"])).append(node)
        elif op == "plan-status":
            plan["status"] = e["to"]
        elif op == "plan-direction":
            plan["direction"] = e["to"]
    return plan


def strip(plan):
    """The parts the check compares: the tree and the plan's own fields, not `updated`."""
    p = {k: v for k, v in plan.items() if k != "updated"}
    return yaml.safe_load(yaml.safe_dump(p))


def apply_lines(lines, changes, numbers):
    for e in changes.get("entries") or []:
        op = e["op"]
        if op in ("status", "retitle", "kind"):
            node = node_of(lines, e["issue"])
            key = {"status": "status", "retitle": "title", "kind": "kind"}[op]
            set_value(lines, node["keys"][key], key, e["to"], keep_comment=False)
        elif op in ("add", "new-feature"):
            issue = numbers.get(e["n"], e.get("issue"))
            parent = numbers.get(e.get("parent"), e.get("parent"))
            if op == "new-feature" and e.get("issue") is not None and node_of(lines, issue) is not None:
                # The story is in the plan already: mark what it stands for, and move it when
                # its plan parent is not the one named.
                node = node_of(lines, issue)
                at_line = node["keys"]["status"]
                lines[at_line + 1:at_line + 1] = [" " * (node["indent"] + 2) + f"represents: {scalar(e['feature'])}"]
                if str(parent_issue_of(lines, issue)) != str(parent):
                    move_block(lines, issue, parent)
                continue
            rep = e["feature"] if op == "new-feature" or e.get("feature") else None
            insert_under(lines, parent, lambda d, i=issue, k=(e.get("kind") or "story"), t=e.get("title"), r=rep:
                         render(d, i, k, t, represents=r))
        elif op == "move":
            move_block(lines, e["issue"], numbers.get(e["to"], e["to"]))
        elif op == "plan-status":
            set_top(lines, "status", e["to"])
        elif op == "plan-direction":
            set_top(lines, "direction", e["to"])


def issue_on(lines, node):
    m = re.search(r"issue:\s*(\S+)", lines[node["keys"]["issue"]])
    return yaml.safe_load(m.group(1)) if m else None


def parent_issue_of(lines, issue):
    """The issue of the node's plan parent: None at the top, False when the node is not there."""
    def seek(nodes, parent):
        for n in nodes:
            if str(issue_on(lines, n)) == str(issue):
                return parent
            hit = seek(n["children"], issue_on(lines, n))
            if hit is not False:
                return hit
        return False
    return seek(parse_tree(lines)[2], None)


def move_block(lines, issue, to):
    node = node_of(lines, issue)
    block = lines[node["start"]:node["end"]]
    old_parent = parent_issue_of(lines, issue)
    del lines[node["start"]:node["end"]]
    if old_parent not in (None, False):
        p = node_of(lines, old_parent)
        if p["children_line"] is not None and not p["children"]:
            lines[p["children_line"]] = " " * (p["indent"] + 2) + "children: []"
    d0 = node["indent"]

    def shifted(d):
        return [(" " * (d - d0) + ln) if d >= d0 else (ln[d0 - d:] if ln.startswith(" " * (d0 - d)) else ln)
                for ln in block]
    insert_under(lines, to, shifted)


def main(argv=None):
    ap = argparse.ArgumentParser(description="write the approved list into the plan file")
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--changes", required=True)
    ap.add_argument("--github-record", required=True)
    ap.add_argument("--at", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        changes = ps.load_list(args.changes)
        if not changes:
            raise ps.Refused("there is no list")
        rec = ps.read_json(args.github_record, "the tracker record") if os.path.isfile(args.github_record) else {"done": {}}
        if rec.get("failed"):
            raise ps.Refused("the tracker writes did not all land; the plan file is not written")
        numbers = {}
        for e in changes.get("entries") or []:
            made = (rec.get("done") or {}).get(f"{e['n']}-create")
            if made:
                numbers[e["n"]] = made["result"]
                numbers[f"@{e['n']}"] = made["result"]
            elif e["op"] in ("add", "new-feature") and e.get("issue") is None:
                raise ps.Refused(f"entry {e['n']} has no issue in the tracker record")
        text = ps.read_text(args.plan_file)
        crlf = "\r\n" in text
        plan = yaml.safe_load(text)
        lines = text.replace("\r\n", "\n").split("\n")
        trail = lines and lines[-1] == ""
        if trail:
            lines = lines[:-1]
        apply_lines(lines, changes, numbers)
        changed = []
        for e in changes.get("entries") or []:
            n = numbers.get(e["n"], e.get("issue"))
            if n is not None and n not in changed:
                changed.append(n)
        if changes.get("entries"):
            set_top(lines, "updated", args.at[:10], after="started")
        new = "\n".join(lines) + ("\n" if trail else "")
        if crlf:
            new = new.replace("\n", "\r\n")
        want = strip(data_apply(plan, changes, numbers))
        got_full = yaml.safe_load(new)
        if strip(got_full) != want:
            raise ps.Refused("the written lines do not read back as the approved list; nothing is written")
        if new != text:
            ps.write_text(args.plan_file, new)
        ps.write_json(args.out, {"ok": True, "path": args.plan_file, "changed": changed})
        return 0
    except (ps.Refused, KeyError, TypeError) as e:
        print(f"refused: {e}", file=sys.stderr)
        ps.write_json(args.out, {"ok": False, "path": args.plan_file, "error": str(e)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
