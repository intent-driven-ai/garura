#!/usr/bin/env python3
"""check_adr_scope.py — nothing but the ADR, its pointers and the index changed (/adr, C9).

The shared scoped-write guard watches only the product model; `/adr` also writes in `docs/adr/`.
This compares two `git status --porcelain` captures — before the run and after it — and fails
on any path that changed in between and is not allowed. The run's own records under the issue
folder (`.garura/project/issues/`) are always allowed. No git call of its own (the play passes
the captures), no network.

Capture both with `git -c core.quotepath=off status --porcelain -uall` — `-uall` lists files
inside new folders, and quotepath off keeps non-English names as they are (otherwise git quotes
them and the check fails closed). Allow exact paths where you can: a `*` glob also matches
nested folders. Inside a drive, a file already changed before the run and changed again is not
seen — the drive's own final review covers it.

    python3 check_adr_scope.py --before <working>/porcelain-before.txt \
        --after <working>/porcelain-after.txt --allow <path or glob> [--allow ...] \
        --out <working>/guard-report.json

Exit 0 ok · 1 out-of-scope changes (listed in the report) · 2 unreadable input.
"""
import argparse
import fnmatch
import json
import sys

ALWAYS = [".garura/project/issues/*"]


def paths(porcelain):
    out = set()
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:                      # a rename: both sides changed
            old, new = path.split(" -> ", 1)
            out.update({old.strip('"'), new.strip('"')})
        else:
            out.add(path.strip('"'))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--allow", action="append", default=[])
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        before = paths(open(args.before, encoding="utf-8").read())
        after_text = open(args.after, encoding="utf-8").read()
    except OSError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    # A path already changed before the run (inside a drive) and changed again is not seen here;
    # within one run by hand the tree starts clean, so every change is seen.
    changed = sorted(paths(after_text) - before)
    allowed = args.allow + ALWAYS
    violations = [p for p in changed if not any(fnmatch.fnmatch(p, g) for g in allowed)]
    report = {"ok": not violations, "changed": changed, "violations": violations, "allowed": allowed}
    out = json.dumps(report, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
