#!/usr/bin/env python3
"""
check_tree.py — /show-plan's check: the tree is what the plan file and the template say, the
same way twice, and no plan file changed (C1–C8, F1–F7).

    python3 check_tree.py hash  --plans-dir D --out <working>/before.json
    python3 check_tree.py check --plans-dir D --template T --plan ID --tool-exit <working>/tool-exit.json \
        --view <working>/view.txt --view2 <working>/view2.txt --before <working>/before.json \
        --out <working>/check.json

`check` re-derives the tree from the plan files and the template, independently of the plan
tool, and writes check.json: {plan_found, lines_ok, hidden_ok, needs_ok, no_plan_plain,
same_twice, unchanged, tree_ok, problems}. Exit 0 = tree_ok, 1 = a check failed, 2 = bad input.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys

import yaml

BLOCK = re.compile(r"^```yaml plan-view\s*\n(.*?)^```", re.S | re.M)
PREFIX = re.compile(r"^[│ ]*[├└]─ ")
NODE = re.compile(r"^\S+ #(\d+)  \S")


def plan_paths(plans_dir):
    return sorted(p for p in glob.glob(os.path.join(plans_dir, "*.yaml")) if os.path.basename(p) != "index.yaml")


def hashes(plans_dir):
    out = {}
    for p in plan_paths(plans_dir):
        with open(p, "rb") as fh:
            out[os.path.basename(p)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def walk(nodes):
    for n in nodes or []:
        yield n
        yield from walk(n.get("children"))


def expected(plan, t):
    """Every node line the tree must print, every node it must not, and its hidden-count line."""
    shown = {s["name"]: s["shown"] for s in t["statuses"]}
    marks = {s["name"]: s["mark"] for s in t["statuses"]}

    def visible(n):
        return shown[n["status"]] or any(visible(c) for c in n.get("children") or [])

    def printed(nodes, keep_all=False):
        # A shown node whose children are all hidden prints them too, one level (#1005).
        for n in nodes or []:
            if keep_all or visible(n):
                yield n
                kids = n.get("children") or []
                if not keep_all:
                    yield from printed(kids, shown[n["status"]] and kids and not any(visible(c) for c in kids))

    on_tree = {id(n) for n in printed(plan.get("tree"))}
    lines, absent, counts = [], [], {}
    for n in walk(plan.get("tree")):
        line = t["tree"]["line"].format(mark=marks[n["status"]], issue=n["issue"], title=n["title"])
        if id(n) in on_tree:
            lines.append(line)
        else:
            absent.append(str(n["issue"]))
            counts[n["status"]] = counts.get(n["status"], 0) + 1
    hidden = None
    if counts:
        order = [s["name"] for s in t["statuses"] if s["name"] in counts]
        hidden = t["tree"]["hidden"].format(counts=t["tree"]["hidden_join"].join(f"{counts[s]} {s}" for s in order))
    return lines, absent, hidden


def check(a):
    with open(a.template, encoding="utf-8") as fh:
        m = BLOCK.search(fh.read())
    if not m:
        print("check_tree.py: the template has no plan-view block", file=sys.stderr)
        return 2
    t = yaml.safe_load(m.group(1))
    plans = {}
    for p in plan_paths(a.plans_dir):
        with open(p, encoding="utf-8") as fh:
            plan = yaml.safe_load(fh) or {}
        plans[str(plan.get("id", os.path.splitext(os.path.basename(p))[0]))] = plan
    view = open(a.view, encoding="utf-8").read().splitlines()
    view2 = open(a.view2, encoding="utf-8").read().splitlines()
    with open(a.tool_exit, encoding="utf-8") as fh:
        tool_exit = json.load(fh)["exit"]
    with open(a.before, encoding="utf-8") as fh:
        before = json.load(fh)
    rec = {"plan_found": str(a.plan) in plans, "same_twice": view == view2,
           "unchanged": before == hashes(a.plans_dir), "lines_ok": None, "hidden_ok": None,
           "needs_ok": None, "no_plan_plain": None}
    problems = []
    if not rec["plan_found"]:
        rec["no_plan_plain"] = tool_exit == 1 and view == [t["tree"]["no_plan"].format(plan=a.plan, dir=a.plans_dir)]
        rec["tree_ok"] = rec["no_plan_plain"] and rec["same_twice"] and rec["unchanged"]
    else:
        body = [PREFIX.sub("", ln) for ln in view]
        target = plans[str(a.plan)]
        lines_ok, hidden_ok = tool_exit == 0, True
        for plan in [target] + [plans[str(n)] for n in target.get("needs_plans") or [] if str(n) in plans]:
            want, absent, hidden = expected(plan, t)
            for line in want:
                if line not in body:
                    lines_ok = False
                    problems.append(f"plan {plan['id']}: missing line {line!r}")
            printed = {mm.group(1) for mm in (NODE.match(ln) for ln in body) if mm}
            for issue in absent:
                if issue in printed:
                    lines_ok = False
                    problems.append(f"plan {plan['id']}: #{issue} is hidden but printed")
            if hidden and hidden not in body:
                hidden_ok = False
                problems.append(f"plan {plan['id']}: no hidden-count line {hidden!r}")
        for ln in body:
            if re.match(r"^\S+ #\d+\s*$", ln):
                lines_ok = False
                problems.append(f"a line has no title: {ln!r}")
        needs = [str(n) for n in target.get("needs_plans") or []]
        rec["needs_ok"] = all(t["tree"]["needs"].format(plan=target["id"], needed=n) in view or
                              t["tree"]["no_plan"].format(plan=n, dir=a.plans_dir) in view for n in needs)
        legend = t["tree"]["legend_join"].join(f"{s['mark']} {s['name']}" for s in t["statuses"])
        if not view or view[0] != legend:
            lines_ok = False
            problems.append("the first line is not the template's legend")
        root = t["tree"]["root"].format(issue=target["id"], title=target.get("title", ""))
        if len(view) < 3 or view[2] != root:
            lines_ok = False
            problems.append(f"the plan's first line is not {root!r}")
        rec.update(lines_ok=lines_ok, hidden_ok=hidden_ok)
        rec["tree_ok"] = all([lines_ok, hidden_ok, rec["needs_ok"], rec["same_twice"], rec["unchanged"]])
    for key in ("same_twice", "unchanged", "needs_ok", "no_plan_plain"):
        if rec[key] is False:
            problems.append(f"{key} is false")
    rec["problems"] = problems
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
    print(json.dumps(rec))
    return 0 if rec["tree_ok"] else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["hash", "check"])
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--template")
    ap.add_argument("--plan")
    ap.add_argument("--tool-exit")
    ap.add_argument("--view")
    ap.add_argument("--view2")
    ap.add_argument("--before")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.command == "hash":
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(hashes(a.plans_dir), fh, indent=2)
        return 0
    if not all([a.template, a.plan, a.tool_exit, a.view, a.view2, a.before]):
        print("check_tree.py: check needs --template, --plan, --tool-exit, --view, --view2 and --before",
              file=sys.stderr)
        return 2
    return check(a)


if __name__ == "__main__":
    sys.exit(main())
