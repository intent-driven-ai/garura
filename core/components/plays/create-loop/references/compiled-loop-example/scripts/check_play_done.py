#!/usr/bin/env python3
"""check_play_done.py — did a play the loop ran prove its done check? (Shared Loop Run, R5)

Each play writes its stop-condition verdict at close
(`{stm_base}<issue>/status/stop-condition-<play>.yaml`). The loop goes on only when that
verdict reads `held` and was written by this run — a verdict older than the play's start is
left from an earlier run and proves nothing. Canonical copy lives at
create-loop/references/check_play_done.py and is stamped into each loop's scripts/.

    python3 check_play_done.py --verdict <stop-condition-<play>.yaml> --not-before <epoch> \
        --out <working>/<play>-done.json

Exit 0 held; 1 not done (missing, older than the start, or unmet); 2 the verdict cannot be
read. Reads files only. Standard library only (the verdict's `stop_condition:` line is read
as text).
"""
import argparse
import json
import os
import re
import sys


def verdict_of(text):
    m = re.search(r"^stop_condition:\s*['\"]?(\w+)", text, re.M)
    return m.group(1) if m else None


def judge(path, not_before):
    if not os.path.isfile(path):
        return 1, {"done": False, "why": "the play wrote no stop-condition verdict"}
    if os.path.getmtime(path) < not_before:
        return 1, {"done": False, "why": "the verdict is older than this run's start — "
                                          "the play did not reach its close"}
    with open(path, encoding="utf-8") as fh:
        verdict = verdict_of(fh.read())
    if verdict is None:
        return 2, {"done": False, "why": "the verdict file has no stop_condition line"}
    if verdict != "held":
        return 1, {"done": False, "why": f"the play's done check reads `{verdict}`"}
    return 0, {"done": True, "why": "held"}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a play's done check for the loop.")
    ap.add_argument("--verdict", required=True)
    ap.add_argument("--not-before", required=True, type=float, help="the play's start, epoch seconds")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        code, result = judge(args.verdict, args.not_before)
    except OSError as exc:
        code, result = 2, {"done": False, "why": f"cannot read the verdict: {exc.__class__.__name__}"}
    result["verdict"] = args.verdict
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
