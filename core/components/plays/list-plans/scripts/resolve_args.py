#!/usr/bin/env python3
"""
resolve_args.py — /list-plans's mode (C8): the list (no argument) or the graph (--graph).

    python3 resolve_args.py --args "<the play's arguments>" --out <working>/mode.json

Writes {mode: "list" | "graph", error: null | "<message>"}. Exit 0 = resolved, 2 = any other
argument: the play halts and prints the error; a mode is never guessed.
"""
import argparse
import json
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--args", default="")
ap.add_argument("--out", required=True)
a = ap.parse_args()
words = a.args.split()
if not words:
    rec = {"mode": "list", "error": None}
elif words == ["--graph"]:
    rec = {"mode": "graph", "error": None}
else:
    rec = {"mode": None, "error": f"unknown argument {a.args!r}: run /list-plans, or /list-plans --graph"}
with open(a.out, "w", encoding="utf-8") as fh:
    json.dump(rec, fh)
print(json.dumps(rec))
sys.exit(0 if rec["mode"] else 2)
