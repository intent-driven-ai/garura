#!/usr/bin/env python3
"""
plan_status.py — set one item's status in a plan file, from its own issue (#1007).

An item's status follows its own issue: closed as completed means Done, closed as not planned
means Dropped. Nothing is worked out from the items under it (no roll-ups). This script changes
one item's `status:` line and the file's `updated:` line, and leaves every other line, comment
and order as it is.

    python3 plan_status.py --plans-dir <plans> --plan <id> --issue <n> --status Done|Dropped \
        [--date YYYY-MM-DD] [--out <record.json>]

The record: {plan, issue, from, to, changed}. An item already at that status is left as it is
(changed: false). Exit 0 done; 2 bad input (no plan file, no such item, a status other than
Done or Dropped).
"""

import argparse
import datetime
import json
import os
import re
import sys

CLOSED = ("Done", "Dropped")


class BadInput(Exception):
    pass


def indent(line):
    return len(line) - len(line.lstrip(" "))


def find_status(lines, issue):
    """The index of the `status:` line of the tree item for `issue`."""
    head = re.compile(rf"^(\s*)- issue: {issue}\s*(#.*)?$")
    for i, line in enumerate(lines):
        m = head.match(line)
        if not m:
            continue
        keys = len(m.group(1)) + 2
        for j in range(i + 1, len(lines)):
            ln = lines[j]
            if not ln.strip():
                continue
            if indent(ln) < keys or (indent(ln) == keys and ln.lstrip().startswith("- ")):
                break
            if indent(ln) == keys and ln.lstrip().startswith("status:"):
                return j
        raise BadInput(f"item #{issue} has no status line")
    raise BadInput(f"no item #{issue} in the plan's tree")


def set_status(path, issue, status, date):
    if status not in CLOSED:
        raise BadInput(f"status must be Done or Dropped, not {status!r}")
    if not os.path.isfile(path):
        raise BadInput(f"no plan file {path}")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.split("\n")
    at = find_status(lines, issue)
    old = lines[at].split(":", 1)[1].split("#", 1)[0].strip()
    rec = {"plan": os.path.splitext(os.path.basename(path))[0], "issue": int(issue),
           "from": old, "to": status, "changed": old != status}
    if not rec["changed"]:
        return rec
    lines[at] = " " * indent(lines[at]) + f"status: {status}"
    for i, ln in enumerate(lines):
        if ln.startswith("updated:"):
            lines[i] = f"updated: '{date}'"
            break
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description="set one item's status in a plan file from its own issue")
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--status", required=True)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        if not re.fullmatch(r"\d+", args.plan) or not re.fullmatch(r"\d+", args.issue):
            raise BadInput("the plan and the issue are numbers")
        rec = set_status(os.path.join(args.plans_dir, f"{args.plan}.yaml"), args.issue, args.status, args.date)
    except BadInput as e:
        print(f"plan_status.py: {e}", file=sys.stderr)
        return 2
    text = json.dumps(rec, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
