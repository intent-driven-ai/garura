#!/usr/bin/env python3
"""check_prototype.py — Kickoff's pre-flight: a working prototype is given, and it runs (C2).

Kickoff starts from a working prototype (ADR 029 §6). Before the drive opens an issue or a
branch, this script checks it mechanically:

- a link (http or https) must answer — a request that returns a status below 400;
- a file must be there; a project folder must be there and hold files;
- for a file or a folder, the person must have said how it starts (`--start`, their answer to
  Kickoff's question) — a folder cannot be proved to run by looking at it.

    python3 check_prototype.py --prototype <path or link> [--start "<how it starts>"] \
        --out <working>/prototype.json

Exit 0 — the prototype is there and runs (or the person said how it starts). Exit 2 — missing,
a link that does not answer, an empty folder, or no word on how a file or folder starts: the
drive halts before it opens anything (F2). Standard library only.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def check_link(url, timeout):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "garura-kickoff/1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.status
    except urllib.error.HTTPError as exc:
        code = exc.code
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return False, f"the link does not answer: {getattr(exc, 'reason', exc)}"
    return code < 400, f"the link answers with status {code}"


def judge(prototype, start, timeout):
    if not prototype or not prototype.strip():
        return False, "link", "no prototype was given"
    p = prototype.strip()
    if p.startswith(("http://", "https://")):
        ok, why = check_link(p, timeout)
        return ok, "link", why
    if os.path.isdir(p):
        if not any(not n.startswith(".") for n in os.listdir(p)):
            return False, "folder", "the project folder is empty"
        kind = "folder"
    elif os.path.isfile(p):
        kind = "file"
    else:
        return False, "missing", f"nothing is at {p}"
    if not (start and start.strip()):
        return False, kind, f"the {kind} is there, but no one said how it starts"
    return True, kind, f"the {kind} is there; it starts with: {start.strip()}"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check Kickoff's working prototype.")
    ap.add_argument("--prototype", default="")
    ap.add_argument("--start", default="", help="the person's word on how a file or folder starts")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    ok, kind, why = judge(args.prototype, args.start, args.timeout)
    result = {"runs": ok, "kind": kind, "prototype": args.prototype, "start": args.start or None,
              "why": why}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
