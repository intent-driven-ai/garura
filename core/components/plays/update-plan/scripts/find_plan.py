#!/usr/bin/env python3
"""find_plan.py — which plan the session is about, from a number or a description (C1).

    python3 find_plan.py find    --args "<the play's arguments>" [--plans-dir D] --out <plan.json>
    python3 find_plan.py confirm --out <plan.json>

`find`:
  - a number (`717` or `#717`) is used as given when its plan file exists: plan.json reads
    `by: number, confirmed: true`;
  - a description is matched against each plan's title (each shared word counts 2) and its
    items' titles (each shared word counts 1; words of three letters or more, without the most
    common ones). The one best plan is written with `by: description, confirmed: false`, the
    words it matched on and where; the person confirms it, then `confirm` sets `confirmed: true`.
  - no plan, a number with no plan file, or two plans with the same best score: exit 1, and
    plan.json reads `plan: null` with up to three candidates. Nothing is guessed, and no plan
    is made.
Exit 0 one plan; 1 none or a tie; 2 bad input. Reads only the plan files.
"""

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402

COMMON = {"the", "and", "for", "with", "that", "this", "plan", "one", "its", "from", "into", "are",
          "can", "who", "what", "when", "they", "their", "them", "out", "has", "have", "not", "all",
          "our", "you", "your", "helping", "helps", "about"}


def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) >= 3 and w not in COMMON}


def plans(plans_dir):
    out = []
    for path in sorted(glob.glob(os.path.join(plans_dir, "*.yaml"))):
        if os.path.basename(path) == "index.yaml":
            continue
        plan = ps.load_plan(path)
        out.append((str(plan.get("id", os.path.splitext(os.path.basename(path))[0])), plan))
    return out


def find(args):
    raw = (args.args or "").strip()
    num = re.fullmatch(r"#?(\d+)", raw)
    every = plans(args.plans_dir)
    by_id = dict(every)
    if num:
        pid = num.group(1)
        if pid in by_id:
            return 0, {"plan": pid, "title": by_id[pid].get("title"), "by": "number", "confirmed": True}
        return 1, {"plan": None, "by": "number", "asked": raw, "candidates": []}
    want = words(raw)
    if not want:
        return 1, {"plan": None, "by": "description", "asked": raw, "candidates": []}
    scored = []
    for pid, plan in every:
        title_hit = want & words(plan.get("title"))
        best_item, item_hit = None, set()
        items = 0
        for node, _ in ps.walk(plan.get("tree")):
            hit = want & words(node.get("title"))
            items += len(hit)
            if len(hit) > len(item_hit):
                best_item, item_hit = node, hit
        score = 2 * len(title_hit) + items
        if score:
            where = "the plan's title" if len(title_hit) >= len(item_hit) or not best_item \
                else f"#{best_item.get('issue')}"
            scored.append((score, pid, plan, sorted(title_hit if where == "the plan's title" else item_hit), where))
    scored.sort(key=lambda s: (-s[0], int(s[1]) if s[1].isdigit() else 0))
    cands = [{"plan": s[1], "title": s[2].get("title"), "score": s[0]} for s in scored[:3]]
    if not scored or (len(scored) > 1 and scored[0][0] == scored[1][0]):
        return 1, {"plan": None, "by": "description", "asked": raw, "candidates": cands}
    s = scored[0]
    return 0, {"plan": s[1], "title": s[2].get("title"), "by": "description", "asked": raw,
               "matched": " ".join(s[3]), "where": s[4], "confirmed": False, "candidates": cands}


def main(argv=None):
    ap = argparse.ArgumentParser(description="find the plan of an /update-plan session")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("--args", required=True)
    f.add_argument("--plans-dir", default=os.path.join(".garura", "project", "plans"))
    f.add_argument("--out", required=True)
    c = sub.add_parser("confirm")
    c.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "confirm":
            rec = ps.read_json(args.out, "plan.json")
            if not rec.get("plan"):
                raise ps.Refused("plan.json names no plan to confirm")
            rec["confirmed"] = True
            ps.write_json(args.out, rec)
            return 0
        code, rec = find(args)
    except ps.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    ps.write_json(args.out, rec)
    return code


if __name__ == "__main__":
    sys.exit(main())
