#!/usr/bin/env python3
"""
pull.py — the memory tool's pull and pulled commands, on folders (contract version 1).

    python3 pull.py pull <path-or-glob>... [--phoenix DIR] [--garura DIR]
    python3 pull.py pulled [--behind] [--phoenix DIR] [--garura DIR]

Phoenix memory is a git repository on disk. Garura memory is a folder in the project.
Their places come from the flags, else from MEMORY_PHOENIX_ROOT and MEMORY_GARURA_ROOT —
never from a fixed path.

pull copies pieces from Phoenix memory into Garura memory, at the same path. Nothing
leaves Phoenix memory. Each piece is recorded in Garura memory's pulled list, pulled.json:
its path, the Phoenix version it came from (the repository's commit) and the fingerprint
of its text. Pulling a piece again refreshes its entry.

pulled lists those pieces with the current Phoenix version, and says which are behind:
the text in Phoenix memory no longer matches the fingerprint that was pulled.

Answers are JSON in the contract's shapes (contract/v1.json). pull prints one answer per
piece, one per line. Exit 0 when every answer is ok, 1 when any is an error.
Standard library only, Python 3.10 or newer.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

CONTRACT_VERSION = "1"
LIST = "pulled.json"
SAFE_PATH = re.compile(r"^(?!/)(?!.*\.\.)[^\\\n\r]+\Z")


class Refusal(Exception):
    """An answer the contract gives as an error."""

    def __init__(self, code, message, tier=None):
        super().__init__(message)
        self.code, self.message, self.tier = code, message, tier


def error(command, refusal):
    return {"ok": False, "contract_version": CONTRACT_VERSION, "command": command,
            "error": {"code": refusal.code, "message": refusal.message, "tier": refusal.tier}}


def fingerprint_file(path):
    with open(path, "rb") as fh:
        return "sha256:" + hashlib.sha256(fh.read()).hexdigest()


def roots(phoenix, garura):
    """The two tiers' folders, from the flags or the environment."""
    phoenix = phoenix or os.environ.get("MEMORY_PHOENIX_ROOT")
    garura = garura or os.environ.get("MEMORY_GARURA_ROOT")
    if not phoenix and not garura:
        raise Refusal("settings_missing", "No setting for Phoenix memory or Garura memory "
                      "(--phoenix/--garura or MEMORY_PHOENIX_ROOT/MEMORY_GARURA_ROOT).")
    for tier, path in (("phoenix", phoenix), ("garura", garura)):
        if not path:
            raise Refusal("tier_missing", f"{tier} memory has no setting.", tier)
        if not os.path.isdir(os.path.expanduser(path)):
            raise Refusal("tier_missing", f"{tier} memory cannot be reached at its setting.", tier)
    return os.path.expanduser(phoenix), os.path.expanduser(garura)


def version(phoenix):
    """Phoenix memory's version: the commit it is at."""
    run = subprocess.run(["git", "-C", phoenix, "rev-parse", "--short=12", "HEAD"],
                         capture_output=True, text=True)
    if run.returncode != 0 or not run.stdout.strip():
        raise Refusal("tier_missing", "Phoenix memory is not a git repository with a commit.", "phoenix")
    return run.stdout.strip()


def expand(phoenix, pattern):
    """The pieces of Phoenix memory a path or glob names, as paths relative to its root."""
    if not SAFE_PATH.match(pattern):
        raise Refusal("bad_request", f"{pattern!r} is not a path inside a tier.")
    if any(c in pattern for c in "*?["):
        found = glob.glob(os.path.join(phoenix, pattern), recursive=True)
        rels = sorted(os.path.relpath(p, phoenix) for p in found if os.path.isfile(p))
        rels = [r for r in rels if not r.startswith(".git" + os.sep) and os.sep + ".git" + os.sep not in r]
    else:
        rels = [pattern] if os.path.isfile(os.path.join(phoenix, pattern)) else []
    if not rels:
        raise Refusal("not_found", f"Phoenix memory holds nothing at {pattern!r}.", "phoenix")
    return [r.replace(os.sep, "/") for r in rels]


def read_list(garura):
    path = os.path.join(garura, LIST)
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {p["path"]: p for p in json.load(fh)["pieces"]}


def write_list(garura, entries):
    data = {"pieces": [entries[k] for k in sorted(entries)]}
    with open(os.path.join(garura, LIST), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


def pull(phoenix, garura, patterns):
    """Copy each named piece into Garura memory and record it. Returns the answers."""
    at = version(phoenix)
    entries, answers = read_list(garura), []
    for pattern in patterns:
        try:
            rels = expand(phoenix, pattern)
        except Refusal as r:
            answers.append(error("pull", r))
            continue
        for rel in rels:
            src, dest = os.path.join(phoenix, rel), os.path.join(garura, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(src, dest)
            fp = fingerprint_file(dest)
            entries[rel] = {"path": rel, "version": at, "fingerprint": fp}
            answers.append({"ok": True, "contract_version": CONTRACT_VERSION, "command": "pull",
                            "tier": "garura", "path": rel, "version": at, "fingerprint": fp})
    write_list(garura, entries)
    return answers


def pulled(phoenix, garura, behind_only=False):
    """What Garura memory pulled, and which pieces are behind Phoenix memory."""
    now, pieces = version(phoenix), []
    for rel, entry in sorted(read_list(garura).items()):
        src = os.path.join(phoenix, rel)
        behind = not os.path.isfile(src) or fingerprint_file(src) != entry["fingerprint"]
        if behind or not behind_only:
            pieces.append({"path": rel, "version": entry["version"], "current_version": now,
                           "behind": behind})
    return {"ok": True, "contract_version": CONTRACT_VERSION, "command": "pulled", "pieces": pieces}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    sub = ap.add_subparsers(dest="command", required=True)
    p_pull = sub.add_parser("pull")
    p_pull.add_argument("patterns", nargs="+")
    p_pulled = sub.add_parser("pulled")
    p_pulled.add_argument("--behind", action="store_true")
    for p in (p_pull, p_pulled):
        p.add_argument("--phoenix")
        p.add_argument("--garura")
    ns = ap.parse_args(argv)
    try:
        phoenix, garura = roots(ns.phoenix, ns.garura)
        answers = pull(phoenix, garura, ns.patterns) if ns.command == "pull" else [
            pulled(phoenix, garura, ns.behind)]
    except Refusal as r:
        answers = [error(ns.command, r)]
    for a in answers:
        print(json.dumps(a))
    return 0 if all(a["ok"] for a in answers) else 1


if __name__ == "__main__":
    sys.exit(main())
