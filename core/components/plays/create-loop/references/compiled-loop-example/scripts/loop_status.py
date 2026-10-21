#!/usr/bin/env python3
"""loop_status.py — keep the run's status file current (standards/rules/run-status.md).

A loop presents what it is doing now in one small file; a display — for Claude Code, a
plugin — reads it. The loop never displays anything itself. This script writes the file whole
(a temporary file renamed over it), so a reader never sees half a file. Canonical copy lives at
create-loop/references/loop_status.py and is stamped into each loop's scripts/.

    python3 loop_status.py --file <stm_base><issue>/status/run-<loop>.json \
        [--name discovery --issue 7 --run-id discovery-<ts>]   # the first call
        [--state running|asking|checking|landing|done|halted] [--round N] \
        [--play <play>] [--step "<plain words>"] [--note "<plain words>"]

Fields not given keep their last value; `updated_at` is always set to now; `started_at` is set
on the first call. Exit 0 written; 2 bad input. Standard library only.
"""
import argparse
import datetime
import json
import os
import sys
import tempfile

STATES = ("running", "asking", "checking", "landing", "done", "halted")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Keep the run's status file current.")
    ap.add_argument("--file", required=True)
    ap.add_argument("--name")
    ap.add_argument("--issue", type=int)
    ap.add_argument("--run-id")
    ap.add_argument("--state", choices=STATES)
    ap.add_argument("--round", type=int)
    ap.add_argument("--play")
    ap.add_argument("--step")
    ap.add_argument("--note")
    args = ap.parse_args(argv)
    status = {}
    if os.path.isfile(args.file):
        try:
            with open(args.file, encoding="utf-8") as fh:
                status = json.load(fh)
        except (OSError, ValueError):
            status = {}  # a broken file is replaced, never trusted
    if not status and not (args.name and args.run_id):
        sys.stderr.write("loop_status.py: the first call names the run (--name and --run-id)\n")
        return 2
    status.setdefault("kind", "loop")
    status.setdefault("started_at", now())
    status.setdefault("state", "running")
    for key in ("name", "issue", "run_id", "state", "round", "play", "step", "note"):
        value = getattr(args, key.replace("-", "_"))
        if value is not None:
            status[key] = value
    status["updated_at"] = now()
    folder = os.path.dirname(os.path.abspath(args.file))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".run-status-")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(status, fh, indent=2)
    os.replace(tmp, args.file)
    print(json.dumps({k: status.get(k) for k in ("state", "round", "play", "step")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
