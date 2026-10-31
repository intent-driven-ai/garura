#!/usr/bin/env python3
"""
resolve_args.py — /show-plan's plan number: one argument, the plan's ID (its business
intent's issue number), or, with no argument, the plan of the branch the person is on (#1000).

    python3 resolve_args.py --args "<the play's arguments>" [--branch "<current branch>"] \
        --out <working>/plan.json

A typed number always wins. With no argument, the number is read from the branch name: a plan's
own branch is `plan/<id>/base` and an issue's branch in it is `plan/<id>/<issue>-<slug>`. A
branch that belongs to no plan (main, feature/...) gets a plain message.

Writes {plan: "<id>" | null, from: "args" | "branch" | null, error: null | "<message>"}. Exit 0 =
resolved, 2 = no plan: more than one argument, one that is not a number, or no argument on a
branch that belongs to no plan. The play halts and prints the error; a plan is never guessed.
"""
import argparse
import json
import re
import sys

PLAN_BRANCH = re.compile(r"^plan/(\d+)/.+")


def resolve(args, branch):
    words = (args or "").replace("#", "").split()
    if len(words) == 1 and words[0].isdigit():
        return {"plan": words[0], "from": "args", "error": None}
    if words:
        return {"plan": None, "from": None,
                "error": f"give one plan number, for example /show-plan 717 (got {args!r})"}
    m = PLAN_BRANCH.match(branch or "")
    if m:
        return {"plan": m.group(1), "from": "branch", "error": None}
    return {"plan": None, "from": None,
            "error": f"this branch ({branch or 'none'}) belongs to no plan; give a plan number, "
                     f"for example /show-plan 717"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--args", default="")
    ap.add_argument("--branch", default="")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rec = resolve(a.args, a.branch)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    print(json.dumps(rec))
    return 0 if rec["plan"] else 2


if __name__ == "__main__":
    sys.exit(main())
