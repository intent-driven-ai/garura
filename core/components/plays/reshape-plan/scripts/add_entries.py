#!/usr/bin/env python3
"""add_entries.py — keep the session's running list (changes.yaml) (C3, C4, C5).

    python3 add_entries.py start  --changes <changes.yaml> --plan <id> --title "<plan title>" \
        --plan-branch <branch> --at <UTC time>
    python3 add_entries.py add    --changes <changes.yaml> --checked <checked.json> \
        [--pick 1,2] [--confirmed 2] [--override 3] --out <taken.json>
    python3 add_entries.py remove --changes <changes.yaml> --n 4

`start` makes an empty list (it refuses to overwrite a list that has entries: the play asks the
person first, carry on or start fresh, and moves the old one aside).

`add` takes entries of checked.json by their place in it (1, 2, …; without --pick, every entry):
  - an entry that `already` reads so is never added;
  - a big entry is added only when it is in --confirmed (the person said yes to it);
  - an entry with a problem is added only when it is in --override (the person said "do it
    anyway"); its `override` keeps the rule it breaks, for the history entry;
  - the instruction is kept once in `asked`, in the person's words.
Each added entry gets the next number `n`. taken.json names what was added and what was not,
and why. A refused entry is never added half way.

`remove` takes entry n out of the list (the person asked); the other numbers stay.

The list: {plan, title, plan_branch, started, asked: [..], entries: [..]}. Nothing is written but
the list. Exit 0 done; 2 refused or bad input.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def nums(text):
    return {int(x) for x in (text or "").split(",") if x.strip()}


def main(argv=None):
    ap = argparse.ArgumentParser(description="keep the session's running list")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("--plan", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--plan-branch", required=True)
    s.add_argument("--at", required=True)
    a = sub.add_parser("add")
    a.add_argument("--checked", required=True)
    a.add_argument("--pick")
    a.add_argument("--confirmed")
    a.add_argument("--override")
    a.add_argument("--out", required=True)
    r = sub.add_parser("remove")
    r.add_argument("--n", type=int, required=True)
    for p in (s, a, r):
        p.add_argument("--changes", required=True)
    args = ap.parse_args(argv)
    try:
        cur = ps.load_list(args.changes)
        if args.cmd == "start":
            if cur and cur.get("entries"):
                raise ps.Refused("a list with entries is waiting; carry on with it or set it aside first")
            ps.save_list(args.changes, {"plan": str(args.plan), "title": args.title,
                                        "plan_branch": args.plan_branch, "started": args.at,
                                        "asked": [], "entries": []})
            return 0
        if cur is None:
            raise ps.Refused("there is no list; start one first")
        if args.cmd == "remove":
            before = len(cur.get("entries") or [])
            cur["entries"] = [e for e in cur.get("entries") or [] if e.get("n") != args.n]
            if len(cur["entries"]) == before:
                raise ps.Refused(f"the list has no entry {args.n}")
            ps.save_list(args.changes, cur)
            return 0
        checked = ps.read_json(args.checked, "checked.json")
        entries = checked.get("entries") or []
        pick = nums(args.pick) or set(range(1, len(entries) + 1))
        confirmed, override = nums(args.confirmed), nums(args.override)
        taken, left = [], []
        nxt = max([e.get("n", 0) for e in cur.get("entries") or []] + [0]) + 1
        for i, e in enumerate(entries, 1):
            if i not in pick:
                continue
            if e.get("already"):
                left.append({"at": i, "why": "already so"})
                continue
            if e.get("problem") and i not in override:
                left.append({"at": i, "why": f"breaks a rule: {e['problem']}"})
                continue
            if e.get("big") and i not in confirmed:
                left.append({"at": i, "why": f"needs a yes: {e['big_why']}"})
                continue
            entry = {k: v for k, v in e.items() if k not in ("problem", "fix", "already")}
            entry["override"] = e["problem"] if e.get("problem") else None
            entry["n"] = nxt
            nxt += 1
            cur.setdefault("entries", []).append(entry)
            taken.append(entry["n"])
        instruction = (checked.get("instruction") or "").strip()
        if taken and instruction and instruction not in (cur.get("asked") or []):
            cur.setdefault("asked", []).append(instruction)
        ps.save_list(args.changes, cur)
        ps.write_json(args.out, {"taken": taken, "left": left})
        return 0
    except ps.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
