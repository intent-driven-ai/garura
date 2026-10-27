#!/usr/bin/env python3
"""
trace_check.py — the trace check of the decisions the slice rests on (/shape-slice, D5, C10).

A run records many decisions with `memory.py cite`. Some are replaced later in the run (the
person changed an answer), and some cite a file the run itself rewrites. The memory tool cannot
yet mark a record as replaced (#852). So the run names the LIVE decisions — the ones the slice
rests on, each recorded again after the run's last write — and this script keeps only their
problems.

    python3 trace_check.py --issue <n> --live <citations-live.json> \
        [--check <citations-check.json>] --out <trace-check.json>

citations-live.json is {"live": [citation ids]}. --check is the memory tool's
`citations --check` answer; without it the script runs
`python3 .garura/core/tools/memory/memory.py citations --issue <n> --check` from the
current folder (the project root).

Writes {ok, live, problems, not_live}: `problems` holds the problems of live records only,
plus {"citation_id", "problem": "not_recorded"} for a live id with no record; `not_live`
lists the other record ids (shown apart, never counted). Exit 0 when `problems` is empty, 1
when not, 2 on a usage or read error. Reads files, and runs the memory tool only when no
--check is given; no git, no network.
"""

import argparse
import json
import os
import subprocess
import sys

TOOL = os.path.join(".garura", "core", "tools", "memory", "memory.py")


def run_tool(issue):
    p = subprocess.run([sys.executable, TOOL, "citations", "--issue", str(issue), "--check"],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        raise ValueError(f"the memory tool gave no answer: {p.stderr.strip() or p.stdout.strip()}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the trace of the decisions the slice rests on.")
    ap.add_argument("--issue", required=True)
    ap.add_argument("--live", required=True)
    ap.add_argument("--check")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.live, encoding="utf-8") as fh:
            live = json.load(fh).get("live")
        if not isinstance(live, list) or not all(isinstance(x, str) and x for x in live):
            raise ValueError(f"{args.live} must hold {{\"live\": [citation ids]}}")
        if args.check:
            with open(args.check, encoding="utf-8") as fh:
                answer = json.load(fh)
        else:
            answer = run_tool(args.issue)
        if not isinstance(answer, dict) or answer.get("ok") is False:
            raise ValueError(f"the citations check did not answer: {answer}")
    except (OSError, ValueError, AttributeError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"trace_check.py: {exc}\n")
        return 2
    live_set = list(dict.fromkeys(live))
    recorded = [r.get("citation_id") for r in answer.get("records") or [] if isinstance(r, dict)]
    problems = [p for p in answer.get("problems") or []
                if isinstance(p, dict) and p.get("citation_id") in live_set]
    problems += [{"citation_id": c, "problem": "not_recorded"} for c in live_set if c not in recorded]
    result = {"ok": not problems, "live": live_set, "problems": problems,
              "not_live": [c for c in recorded if c not in live_set]}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({"ok": result["ok"], "live": len(live_set), "problems": len(problems),
                      "not_live": len(result["not_live"])}, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
