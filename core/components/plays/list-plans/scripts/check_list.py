#!/usr/bin/env python3
"""
check_list.py — /list-plans's check: the view holds every plan once, in order, from the
template, the same way twice, and no plan file changed (C1–C8, F1–F6).

    python3 check_list.py hash  --plans-dir D --out <working>/before.json
    python3 check_list.py check --plans-dir D --template T --mode list|graph \
        --view <working>/view.txt --view2 <working>/view2.txt --before <working>/before.json \
        [--repo R] --out <working>/check.json

`hash` records the plan files' hashes before the tool runs. `check` re-derives what the view
must hold from the plan files, the template and git, and writes check.json:
{plans_in_folder, all_listed, in_order, template_used, same_twice, unchanged,
graph_numbers_match, problems, ok}. Exit 0 = ok, 1 = a check failed, 2 = bad input.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

import yaml

BLOCK = re.compile(r"^```yaml plan-view\s*\n(.*?)^```", re.S | re.M)


def plan_paths(plans_dir):
    paths = [p for p in glob.glob(os.path.join(plans_dir, "*.yaml")) if os.path.basename(p) != "index.yaml"]
    key = lambda p: os.path.splitext(os.path.basename(p))[0]
    return sorted(paths, key=lambda p: (int(key(p)) if key(p).isdigit() else float("inf"), key(p)))


def hashes(plans_dir):
    out = {}
    for p in plan_paths(plans_dir):
        with open(p, "rb") as fh:
            out[os.path.basename(p)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def git_ref(branch, repo):
    for ref in (branch, f"origin/{branch}"):
        if subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=repo,
                          capture_output=True).returncode == 0:
            return ref
    return None


def check(a):
    with open(a.template, encoding="utf-8") as fh:
        m = BLOCK.search(fh.read())
    if not m:
        raise SystemExit(2)
    t = yaml.safe_load(m.group(1))
    plans = []
    for p in plan_paths(a.plans_dir):
        with open(p, encoding="utf-8") as fh:
            plan = yaml.safe_load(fh) or {}
        plans.append((str(plan.get("id", os.path.splitext(os.path.basename(p))[0])), plan.get("title", "")))
    view = open(a.view, encoding="utf-8").read().splitlines()
    view2 = open(a.view2, encoding="utf-8").read().splitlines()
    with open(a.before, encoding="utf-8") as fh:
        before = json.load(fh)
    ids = [pid for pid, _ in plans]
    problems = []
    rec = {"plans_in_folder": len(ids), "same_twice": view == view2,
           "unchanged": before == hashes(a.plans_dir), "graph_numbers_match": None}
    if not ids:
        none = (t["list"]["none"].format(dir=a.plans_dir) if a.mode == "list" else t["graph"]["main"])
        rec.update(all_listed=none in view, in_order=True, template_used=none in view)
    elif a.mode == "list":
        heads = [t["list"]["head"].format(plan=pid, title=title) for pid, title in plans]
        seen = [ln for ln in view if ln in heads]
        rec["all_listed"] = sorted(seen) == sorted(heads) and len(seen) == len(heads)
        rec["in_order"] = seen == heads
        listed = [ln for ln in view if re.match(r"^#\d+ ", ln)]
        rec["template_used"] = listed == seen
    else:
        g = t["graph"]
        pat = re.compile(r"^[├└]─ (\S+)  (\S+) ahead · (\S+) behind.*  #(\d+) ")
        found, match = [], True
        main = git_ref("main", a.repo)
        for ln in view:
            mm = pat.match(ln)
            if mm:
                branch, ahead, behind, pid = mm.groups()
                found.append(pid)
                ref = git_ref(branch, a.repo)
                if ref and main:
                    r = subprocess.run(["git", "rev-list", "--left-right", "--count", f"{main}...{ref}"],
                                       cwd=a.repo, capture_output=True, text=True)
                    want_behind, want_ahead = r.stdout.split()
                    if (ahead, behind) != (want_ahead, want_behind):
                        match = False
                        problems.append(f"#{pid}: {ahead} ahead · {behind} behind, git says "
                                        f"{want_ahead} ahead · {want_behind} behind")
                elif (ahead, behind) != ("?", "?"):
                    match = False
        branched = list(found)
        on_main = []
        prefix = g["on_main"].split("{plans}")[0]
        for ln in view:
            if ln.startswith(prefix):
                on_main += [x.strip().lstrip("#") for x in ln[len(prefix):].split(",") if x.strip()]
        found = branched + on_main
        in_plan_order = lambda xs: xs == [p for p in ids if p in xs]
        rec["all_listed"] = sorted(found) == sorted(ids) and len(found) == len(ids)
        rec["in_order"] = in_plan_order(branched) and in_plan_order(on_main)
        rec["template_used"] = bool(view) and view[0] == g["main"]
        rec["graph_numbers_match"] = match
    for key in ("all_listed", "in_order", "template_used", "same_twice", "unchanged"):
        if not rec[key]:
            problems.append(f"{key} is false")
    if rec["graph_numbers_match"] is False and not any("git says" in p for p in problems):
        problems.append("graph_numbers_match is false")
    rec["problems"] = problems
    rec["ok"] = not problems
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
    print(json.dumps(rec))
    return 0 if rec["ok"] else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["hash", "check"])
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--template")
    ap.add_argument("--mode", choices=["list", "graph"], default="list")
    ap.add_argument("--view")
    ap.add_argument("--view2")
    ap.add_argument("--before")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.command == "hash":
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(hashes(a.plans_dir), fh, indent=2)
        return 0
    if not all([a.template, a.view, a.view2, a.before]):
        print("check_list.py: check needs --template, --view, --view2 and --before", file=sys.stderr)
        return 2
    return check(a)


if __name__ == "__main__":
    sys.exit(main())
