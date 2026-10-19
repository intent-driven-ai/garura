#!/usr/bin/env python3
"""
pull.py — the memory tool's pull and pulled commands, on folders (contract version 4).

    python3 pull.py pull <path-or-glob>... [--phoenix DIR] [--garura DIR] [--ref REF]
    python3 pull.py pulled [--behind] [--phoenix DIR] [--garura DIR] [--ref REF]

The memory tool's one entry is memory.py, which calls these functions with its settings;
this command line stays for direct use.

Phoenix memory is a git repository on disk, read only at its approved version: the commit
REF names (default origin/main — a change reaches it when a person merges it, outside this
tool). Working-tree edits and unmerged commits are never read. Garura memory is a folder in
the project. Their places come from the flags, else from MEMORY_PHOENIX_ROOT,
MEMORY_GARURA_ROOT and MEMORY_PHOENIX_REF — never from a fixed path. When Phoenix memory's
place is empty, memory.py downloads it there from its source (download) the first time a
command needs it.

pull copies pieces from Phoenix memory into Garura memory, at the same path. Nothing
leaves Phoenix memory. A piece is never written over a different file: if Garura memory
already holds a file at that path that pull did not write, or that changed since, the
answer is would_overwrite and nothing is written. Each piece is recorded in Garura memory's pulled list, pulled.json:
its path, the Phoenix version it came from (the repository's commit) and the fingerprint
of its text. Pulling a piece again refreshes its entry.

pulled lists those pieces with the current Phoenix version, and says which are behind:
the text in Phoenix memory no longer matches the fingerprint that was pulled.

Answers are JSON in the contract's shapes (contract/v4.json). pull prints one answer per
piece, one per line. Exit 0 when every answer is ok, 1 when any is an error.
Standard library only, Python 3.10 or newer.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CONTRACT_VERSION = "4"
LIST = "pulled.json"
SAFE_PATH = re.compile(r"^(?!/)(?!.*\.\.)[^\\\n\r]+\Z")
DOWNLOAD_SECONDS = 600  # the longest a first-use download may take


class Refusal(Exception):
    """An answer the contract gives as an error."""

    def __init__(self, code, message, tier=None):
        super().__init__(message)
        self.code, self.message, self.tier = code, message, tier


def error(command, refusal):
    return {"ok": False, "contract_version": CONTRACT_VERSION, "command": command,
            "error": {"code": refusal.code, "message": refusal.message, "tier": refusal.tier}}


def fingerprint_bytes(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def glob_regex(pattern):
    """A shell-style glob as a regex over '/'-separated paths: * within one folder,
    ** any depth, ? one character."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def git(phoenix, *args):
    return subprocess.run(["git", "-C", phoenix, *args], capture_output=True)


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


def download(source, phoenix):
    """Download Phoenix memory to its place on this machine, the first time it is needed.
    It is cloned beside the place and moved in whole, so a cut-off download never looks like
    Phoenix memory, and two first runs at once keep one copy."""
    parent = os.path.dirname(os.path.abspath(phoenix))
    try:
        os.makedirs(parent, exist_ok=True)
        part = tempfile.mkdtemp(prefix=".phoenix-memory-download-", dir=parent)
    except OSError as exc:
        raise Refusal("tier_missing", f"Phoenix memory is not on this machine, and there is no room "
                      f"to download it: {exc}.", "phoenix") from exc
    # never wait for a password nobody is there to type, nor on a stalled network: fail and say so
    try:
        run = subprocess.run(["git", "clone", "--quiet", "--", source, part], capture_output=True,
                             env=dict(os.environ, GIT_TERMINAL_PROMPT="0"), timeout=DOWNLOAD_SECONDS)
        why = run.stderr.decode(errors="replace").strip().splitlines() if run.returncode else None
    except subprocess.TimeoutExpired:
        why = [f"no answer from {source} within {DOWNLOAD_SECONDS} seconds"]
    if why is not None:
        shutil.rmtree(part, ignore_errors=True)
        raise Refusal("tier_missing", "Phoenix memory is not on this machine, and downloading it "
                      f"failed: {why[-1] if why else 'git clone failed'}.", "phoenix")
    try:
        os.rename(part, phoenix)
    except OSError as exc:
        shutil.rmtree(part, ignore_errors=True)
        if not os.path.isdir(phoenix):  # not another first run that got there first: say why
            raise Refusal("tier_missing", "Phoenix memory was downloaded but could not be put in "
                          f"its place, {phoenix}: {exc}.", "phoenix") from exc


def version(phoenix, ref="HEAD"):
    """Phoenix memory's version: the commit its approved ref is at."""
    run = git(phoenix, "rev-parse", "--short=12", "--verify", "--quiet", ref + "^{commit}")
    if run.returncode != 0 or not run.stdout.strip():
        raise Refusal("tier_missing", f"Phoenix memory has no approved version at {ref!r} "
                      "(not a git repository, or no such commit).", "phoenix")
    return run.stdout.decode().strip()


def files(phoenix, ref="HEAD"):
    """Every file in Phoenix memory at the approved ref, as paths relative to its root."""
    run = git(phoenix, "ls-tree", "-r", "--name-only", "-z", ref)
    if run.returncode != 0:
        raise Refusal("tier_missing", f"Phoenix memory cannot be listed at {ref!r}.", "phoenix")
    return sorted(p for p in run.stdout.decode().split("\0") if p)


def show(phoenix, rel, ref="HEAD"):
    """The bytes of one file in Phoenix memory at the approved ref, or None."""
    run = git(phoenix, "cat-file", "blob", f"{ref}:{rel}")
    return run.stdout if run.returncode == 0 else None


def expand(phoenix, pattern, ref="HEAD"):
    """The pieces of Phoenix memory a path or glob names, as paths relative to its root."""
    if not SAFE_PATH.match(pattern):
        raise Refusal("bad_request", f"{pattern!r} is not a path inside a tier.")
    if any(c in pattern for c in "*?"):
        rx = glob_regex(pattern)
        rels = [r for r in files(phoenix, ref) if rx.match(r)]
    else:
        rels = [pattern] if pattern in set(files(phoenix, ref)) else []
    if not rels:
        raise Refusal("not_found", f"Phoenix memory holds nothing at {pattern!r}.", "phoenix")
    return rels


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


def pull(phoenix, garura, patterns, ref="HEAD"):
    """Copy each named piece into Garura memory and record it. Returns the answers."""
    at = version(phoenix, ref)
    entries, answers = read_list(garura), []
    for pattern in patterns:
        try:
            rels = expand(phoenix, pattern, ref)
        except Refusal as r:
            answers.append(error("pull", r))
            continue
        for rel in rels:
            data, dest = show(phoenix, rel, ref), os.path.join(garura, rel)
            if os.path.exists(dest):
                with open(dest, "rb") as fh:
                    here = fingerprint_bytes(fh.read())
                ours = rel in entries and entries[rel]["fingerprint"] == here
                if not ours and here != fingerprint_bytes(data):
                    answers.append(error("pull", Refusal(
                        "would_overwrite", f"Garura memory already holds a different file at {rel}, one pull did "
                        "not write or one changed since; nothing was overwritten.", "garura")))
                    continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(data)
            fp = fingerprint_bytes(data)
            entries[rel] = {"path": rel, "version": at, "fingerprint": fp}
            answers.append({"ok": True, "contract_version": CONTRACT_VERSION, "command": "pull",
                            "tier": "garura", "path": rel, "version": at, "fingerprint": fp})
    if entries:
        write_list(garura, entries)
    return answers


def pulled(phoenix, garura, behind_only=False, ref="HEAD"):
    """What Garura memory pulled, and which pieces are behind Phoenix memory."""
    now, pieces = version(phoenix, ref), []
    for rel, entry in sorted(read_list(garura).items()):
        data = show(phoenix, rel, ref)
        behind = data is None or fingerprint_bytes(data) != entry["fingerprint"]
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
        p.add_argument("--ref")
    ns = ap.parse_args(argv)
    ref = ns.ref or os.environ.get("MEMORY_PHOENIX_REF") or "origin/main"
    try:
        phoenix, garura = roots(ns.phoenix, ns.garura)
        answers = pull(phoenix, garura, ns.patterns, ref) if ns.command == "pull" else [
            pulled(phoenix, garura, ns.behind, ref)]
    except Refusal as r:
        answers = [error(ns.command, r)]
    for a in answers:
        print(json.dumps(a))
    return 0 if all(a["ok"] for a in answers) else 1


if __name__ == "__main__":
    sys.exit(main())
