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
nested folders.

A file already changed before the run (normal inside a drive) is caught when it changes again:
take a snapshot of those files' contents at the start, and pass it to the check.

    python3 check_adr_scope.py --snapshot --before <working>/porcelain-before.txt \
        --out <working>/hashes-before.json                       # at the start of the run
    python3 check_adr_scope.py --before <working>/porcelain-before.txt \
        --before-hashes <working>/hashes-before.json \
        --after <working>/porcelain-after.txt --allow <path or glob> [--allow ...] \
        --out <working>/guard-report.json

Exit 0 ok · 1 out-of-scope changes (listed in the report) · 2 unreadable input.
"""
import argparse
import fnmatch
import hashlib
import json
import os
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


def digest(path):
    if os.path.isdir(path):
        return "dir"
    if not os.path.exists(path):
        return "absent"
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after")
    ap.add_argument("--allow", action="append", default=[])
    ap.add_argument("--snapshot", action="store_true",
                    help="record the contents of the paths already changed before the run, then exit")
    ap.add_argument("--before-hashes", help="the snapshot taken at the start of the run")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        before = paths(open(args.before, encoding="utf-8").read())
        if args.snapshot:
            snap = {p: digest(p) for p in sorted(before)}
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, indent=2)
            print(json.dumps({"snapshot": len(snap), "out": args.out}))
            return 0
        after_text = open(args.after, encoding="utf-8").read()
        snap = json.load(open(args.before_hashes, encoding="utf-8")) if args.before_hashes else {}
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    after = paths(after_text)
    again = {p for p in before & after if p in snap and digest(p) != snap[p]}
    changed = sorted((after - before) | again)
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
