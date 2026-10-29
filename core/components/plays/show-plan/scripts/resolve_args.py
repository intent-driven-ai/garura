#!/usr/bin/env python3
"""
resolve_args.py — /show-plan's plan number: one argument, the plan's ID (its business
intent's issue number).

    python3 resolve_args.py --args "<the play's arguments>" --out <working>/plan.json

Writes {plan: "<id>" | null, error: null | "<message>"}. Exit 0 = resolved, 2 = no argument,
more than one, or one that is not a number: the play halts and prints the error; a plan is
never guessed.
"""
import argparse
import json
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--args", default="")
ap.add_argument("--out", required=True)
a = ap.parse_args()
words = a.args.replace("#", "").split()
if len(words) == 1 and words[0].isdigit():
    rec = {"plan": words[0], "error": None}
else:
    rec = {"plan": None, "error": f"give one plan number, for example /show-plan 717 (got {a.args!r})"}
with open(a.out, "w", encoding="utf-8") as fh:
    json.dump(rec, fh)
print(json.dumps(rec))
sys.exit(0 if rec["plan"] else 2)
