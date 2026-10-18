#!/usr/bin/env python3
"""
memory.py — the memory tool: the one way agents find memory (contract version 4).

    python3 memory.py health
    python3 memory.py find   --issue N --glob GLOB [--tier T | --every-tier]
    python3 memory.py search --issue N --pattern P [--fixed] [--ignore-case] [--glob GLOB]
                             [--tier T | --every-tier] [--max M]
    python3 memory.py read   --issue N --tier T --path PATH [--start S] [--end E]
    python3 memory.py pull   PATH-OR-GLOB... | --path PATH
    python3 memory.py pulled [--behind]
    python3 memory.py propose --request '{"issue": 658, "missing": ..., "target_path": "658/...", ...}'
    python3 memory.py updates [--status waiting]
    python3 memory.py decide  --request '{"id": "mu-...", "verdict": "approve", "by": ..., "reply": ..., "decided_in": "review-tool"}'
    python3 memory.py apply   --id mu-...
    python3 memory.py cite    --request '{"issue": 659, "question": ..., "answer": ..., "sources": [...], ...}'
    python3 memory.py citations --issue 659 [--play /vision] [--check]
    python3 memory.py <command> --request '{"issue": 657, ...}'

Each request field is a flag, or the whole request is one JSON object (--request). Every
answer is one JSON object per line, in the contract's shapes (contract/v4.json). A request
that does not match the contract is refused with bad_request.

Lookups go short-term -> garura -> phoenix and stop at the first tier that answers.
Short-term memory is read only in the request's issue folder; a request with no issue has
no short-term memory and starts at Garura memory. Phoenix memory is read only
at its approved version (phoenix_ref). A file read from Phoenix memory is used, so it is
pulled into Garura memory: the next lookup answers from the project. It is never saved over
a different Garura file; the read answer says saved_to, or not_saved and why.

Settings — where each tier lives — come from one source: the JSON file MEMORY_SETTINGS
names, else the environment. Relative places in the file are relative to the file.

    key              environment               what
    engine           MEMORY_ENGINE             "folder" (the only engine built; a server
                                               engine is one setting away)
    short-term       MEMORY_SHORT_TERM_ROOT    folder holding one folder per issue
    garura           MEMORY_GARURA_ROOT        Garura memory's folder
    phoenix          MEMORY_PHOENIX_ROOT       Phoenix memory's git repository
    phoenix_ref      MEMORY_PHOENIX_REF        Phoenix memory's approved version
                                               (default origin/main)
    garura_pull_dir  MEMORY_GARURA_PULL_DIR    where pulled pieces land, inside Garura
                                               memory (default: Garura memory's root)
    updates_dir      MEMORY_UPDATES_DIR        where an issue's memory updates are kept,
                                               inside its short-term folder
                                               (default: review/memory-updates)
    citations_file   MEMORY_CITATIONS_FILE     where an issue's decision records are kept,
                                               inside its short-term folder
                                               (default: context/citations.jsonl)

Exit 0 when every answer is ok, 1 when any is an error. Standard library only, Python 3.10
or newer.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "contract"))

import check_contract  # noqa: E402
import pull as phoenix_git  # noqa: E402
from pull import CONTRACT_VERSION, SAFE_PATH, Refusal, error, glob_regex  # noqa: E402
from citations import CitationStore  # noqa: E402
from updates import UpdateStore  # noqa: E402

CONTRACT = check_contract.load(os.path.join(HERE, "contract", "v4.json"))
ORDER = CONTRACT["lookup_order"]
KEYS = {"engine": "MEMORY_ENGINE", "short-term": "MEMORY_SHORT_TERM_ROOT",
        "garura": "MEMORY_GARURA_ROOT", "phoenix": "MEMORY_PHOENIX_ROOT",
        "phoenix_ref": "MEMORY_PHOENIX_REF", "garura_pull_dir": "MEMORY_GARURA_PULL_DIR",
        "updates_dir": "MEMORY_UPDATES_DIR", "citations_file": "MEMORY_CITATIONS_FILE"}


def fingerprint(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def ok(command, **fields):
    return {"ok": True, "contract_version": CONTRACT_VERSION, "command": command, **fields}


# --- settings ------------------------------------------------------------------------

def load_settings(env=None):
    """The tool's settings from one source: the MEMORY_SETTINGS file, else the environment."""
    env = os.environ if env is None else env
    path = env.get("MEMORY_SETTINGS")
    if path:
        try:
            with open(os.path.expanduser(path), encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, ValueError) as exc:
            raise Refusal("settings_missing", f"The settings file cannot be read: {exc}.")
        base = os.path.dirname(os.path.abspath(os.path.expanduser(path)))
        settings = {k: raw.get(k) for k in KEYS}
        for tier in ORDER:
            if settings[tier]:
                settings[tier] = os.path.join(base, os.path.expanduser(settings[tier]))
    else:
        settings = {k: env.get(v) for k, v in KEYS.items()}
        for tier in ORDER:
            if settings[tier]:
                settings[tier] = os.path.abspath(os.path.expanduser(settings[tier]))
    if not any(settings[t] for t in ORDER):
        raise Refusal("settings_missing", "The memory tool has no settings: set MEMORY_SETTINGS, "
                      "or MEMORY_SHORT_TERM_ROOT, MEMORY_GARURA_ROOT and MEMORY_PHOENIX_ROOT.")
    settings["engine"] = settings["engine"] or "folder"
    settings["phoenix_ref"] = settings["phoenix_ref"] or "origin/main"
    settings["garura_pull_dir"] = settings["garura_pull_dir"] or ""
    settings["updates_dir"] = settings["updates_dir"] or "review/memory-updates"
    settings["citations_file"] = settings["citations_file"] or "context/citations.jsonl"
    if settings["engine"] != "folder":
        raise Refusal("settings_missing", f"Engine {settings['engine']!r} is not built; "
                      "the only engine is 'folder'.")
    return settings


# --- the folder engine ---------------------------------------------------------------

class FolderEngine:
    """Short-term and Garura memory are folders; Phoenix memory is a git repository read at
    its approved ref. Every method takes and returns paths relative to the tier's root."""

    def __init__(self, settings):
        self.s = settings

    # where things are
    def root(self, tier):
        path = self.s.get(tier)
        if not path:
            raise Refusal("tier_missing", f"{tier} memory has no setting: no folder or server "
                          "is configured for it.", tier)
        if not os.path.isdir(path):
            raise Refusal("tier_missing", f"{tier} memory cannot be reached at its setting.", tier)
        if tier == "phoenix":
            phoenix_git.version(path, self.s["phoenix_ref"])
        return path

    def version(self, tier):
        if tier == "phoenix":
            return phoenix_git.version(self.root(tier), self.s["phoenix_ref"])
        self.root(tier)
        return None

    def excluded(self, tier):
        """What a lookup in this tier never reads, as prefixes of the folder it scans.

        Inside Garura memory, the short-term folder is short-term memory, not Garura memory.
        Inside an issue's short-term memory, the memory updates are drafts waiting for a
        person (nothing in them is used until one is approved and applied), and the decision
        records are not memory (an agent never decides from its own earlier decision)."""
        if tier == "short-term":
            return (self.s["updates_dir"].strip("/") + "/", self.s["citations_file"].strip("/"))
        if tier != "garura" or not self.s.get("short-term"):
            return ()
        rel = os.path.relpath(self.s["short-term"], self.s["garura"])
        return () if rel == "." or rel.startswith("..") else (rel.replace(os.sep, "/").rstrip("/") + "/",)

    def scope(self, tier, issue):
        """The folder a lookup reads in this tier, and the prefix its paths carry."""
        root = self.root(tier)
        if tier == "short-term":
            return os.path.join(root, str(issue)), f"{issue}/"
        return root, ""

    # finding
    def files(self, tier, issue):
        if tier == "phoenix":
            return phoenix_git.files(self.root(tier), self.s["phoenix_ref"])
        folder, prefix = self.scope(tier, issue)
        skip, found = self.excluded(tier), []
        for dirpath, dirnames, names in os.walk(folder):
            dirnames[:] = sorted(d for d in dirnames if d != ".git")
            for name in sorted(names):
                rel = os.path.relpath(os.path.join(dirpath, name), folder).replace(os.sep, "/")
                if rel.startswith(skip):
                    continue
                found.append(prefix + rel)
        return found

    def grep(self, tier, issue, pattern, fixed, ignore_case):
        """(path, line, text) for every matching line, with git grep's ERE (or plain text)."""
        flags = ["-n", "-z", "-I", "-F" if fixed else "-E"] + (["-i"] if ignore_case else [])
        if tier == "phoenix":
            ref = self.s["phoenix_ref"]
            run = phoenix_git.git(self.root(tier), "grep", *flags, "-e", pattern, ref, "--")
            strip, prefix = ref + ":", ""
        else:
            folder, prefix = self.scope(tier, issue)
            if not os.path.isdir(folder):
                return []
            run = subprocess.run(["git", "-C", folder, "grep", "--no-index", *flags, "-e", pattern, "--"],
                                 capture_output=True)
            strip = ""
        if run.returncode == 1:
            return []
        if run.returncode != 0:
            raise Refusal("bad_request", f"The pattern {pattern!r} cannot be searched: "
                          f"{run.stderr.decode(errors='replace').strip()}")
        skip, hits = self.excluded(tier), []
        for record in run.stdout.decode("utf-8", errors="replace").split("\n"):
            parts = record.split("\0")
            if len(parts) != 3:
                continue
            path, line, text = parts
            path = path[len(strip):] if strip and path.startswith(strip) else path
            if path.startswith(skip) or path.startswith(".git/") or "/.git/" in path:
                continue
            hits.append((prefix + path, int(line), text))
        return hits

    def read(self, tier, path):
        """The text of one file, or None when the tier has no such file."""
        if tier == "phoenix":
            data = phoenix_git.show(self.root(tier), path, self.s["phoenix_ref"])
        else:
            full = os.path.join(self.root(tier), path)
            skip = self.excluded(tier)
            inner = path.split("/", 1)[1] if tier == "short-term" and "/" in path else path
            if inner.startswith(skip) or not os.path.isfile(full):
                return None
            with open(full, "rb") as fh:
                data = fh.read()
        return None if data is None else data.decode("utf-8", errors="replace")

    def pull(self, patterns):
        garura = os.path.join(self.root("garura"), self.s["garura_pull_dir"])
        os.makedirs(garura, exist_ok=True)
        return phoenix_git.pull(self.root("phoenix"), garura, patterns, self.s["phoenix_ref"])

    def updates(self):
        return UpdateStore(self.root("short-term"), self.s["updates_dir"])

    def citations(self):
        return CitationStore(self.root("short-term"), self.s["citations_file"])

    def garura_path(self, rel):
        """Where a piece pulled from Phoenix memory sits, as a path in Garura memory."""
        return "/".join(p for p in (self.s["garura_pull_dir"].strip("/"), rel) if p)

    def pulled(self, behind_only):
        garura = os.path.join(self.root("garura"), self.s["garura_pull_dir"])
        return phoenix_git.pulled(self.root("phoenix"), garura, behind_only, self.s["phoenix_ref"])


# --- the commands --------------------------------------------------------------------

def tiers_for(request):
    """The tiers a lookup reads, in order, and whether it stops at the first answer."""
    if request.get("tier") and request.get("every_tier"):
        raise Refusal("bad_request", "Ask for tier or every_tier, not both.")
    if request.get("issue") is None and request.get("tier") == "short-term":
        raise Refusal("bad_request", "Short-term memory is one issue's memory: a lookup without an "
                      "issue cannot ask for it.", "short-term")
    if request.get("tier"):
        return [request["tier"]], True
    order = ORDER if request.get("issue") is not None else [t for t in ORDER if t != "short-term"]
    return list(order), not request.get("every_tier")


def safe_glob(glob):
    if not SAFE_PATH.match(glob):
        raise Refusal("bad_request", f"{glob!r} is not a path inside a tier.")
    return glob_regex(glob)


def matches_glob(rx, tier, issue, path):
    """A short-term glob is matched inside the issue's folder, with or without its prefix."""
    inner = path[len(f"{issue}/"):] if tier == "short-term" else path
    return bool(rx.match(inner) or rx.match(path))


def lookup(engine, request, results_of):
    """Run results_of(tier) over the tiers in order; build looked_in and answered_by."""
    order, stop_first = tiers_for(request)
    looked_in, answered_by, results = [], None, []
    for tier in order:
        engine.root(tier)  # a tier with no setting or out of reach fails the lookup
        looked_in.append(tier)
        found = results_of(tier)
        if found and answered_by is None:
            answered_by = tier
        results += found
        if found and stop_first:
            break
    return looked_in, answered_by, results


def cmd_health(engine, request):
    tiers = []
    for tier in ORDER:
        try:
            tiers.append({"tier": tier, "reachable": True, "kind": "folder", "version": engine.version(tier)})
        except Refusal:
            tiers.append({"tier": tier, "reachable": False, "kind": "folder", "version": None})
    return ok("health", tiers=tiers)


def cmd_find(engine, request):
    issue, rx = request.get("issue"), safe_glob(request["glob"])

    def found(tier):
        version = engine.version(tier)
        return [{"tier": tier, "path": p, "version": version}
                for p in engine.files(tier, issue) if matches_glob(rx, tier, issue, p)]

    looked_in, answered_by, matches = lookup(engine, request, found)
    return ok("find", looked_in=looked_in, answered_by=answered_by, matches=matches)


def cmd_search(engine, request):
    issue = request.get("issue")
    rx = safe_glob(request["glob"]) if request.get("glob") else None

    def found(tier):
        return [{"tier": tier, "path": p, "line": n, "text": t, "fingerprint": fingerprint(t)}
                for p, n, t in engine.grep(tier, issue, request["pattern"], request.get("fixed", False),
                                           request.get("ignore_case", False))
                if rx is None or matches_glob(rx, tier, issue, p)]

    looked_in, answered_by, hits = lookup(engine, request, found)
    most = request.get("max")
    truncated = most is not None and len(hits) > most
    return ok("search", looked_in=looked_in, answered_by=answered_by,
              hits=hits[:most] if truncated else hits, truncated=truncated)


def cmd_read(engine, request):
    issue, tier, path = request.get("issue"), request["tier"], request["path"]
    if tier == "short-term" and not path.startswith(f"{issue}/"):
        raise Refusal("bad_request", f"Short-term path {path} is outside issue {issue}; "
                      "short-term memory is that issue only.", tier)
    start, end = request.get("start", 1), request.get("end")
    if end is not None and end < start:
        raise Refusal("bad_request", f"end {end} is before start {start}.", tier)
    text = engine.read(tier, path)
    if text is None:
        raise Refusal("not_found", f"{tier} memory has no file {path}.", tier)
    lines = text.split("\n")
    if lines and lines[-1] == "" and text.endswith("\n"):
        lines.pop()
    end = len(lines) if end is None else end
    if start > len(lines) or end > len(lines):
        raise Refusal("out_of_range", f"{path} has {len(lines)} lines; asked {start} to {end}.", tier)
    chunk = "\n".join(lines[start - 1:end])
    answer = ok("read", tier=tier, path=path, start=start, end=end, text=chunk,
                fingerprint=fingerprint(chunk), version=engine.version(tier))
    if tier == "phoenix":
        # used, so saved: the next lookup answers from Garura memory
        saved = engine.pull([path])[0]
        if saved["ok"]:
            answer["saved_to"] = {"tier": "garura", "path": engine.garura_path(path)}
        elif saved["error"]["code"] == "would_overwrite":
            answer["not_saved"] = saved["error"]["message"]
        else:
            return saved | {"command": "read"}
    return answer


def cmd_pull(engine, request):
    return engine.pull([request["path"]])


def cmd_pulled(engine, request):
    return engine.pulled(request.get("behind", False))


def cmd_propose(engine, request):
    return ok("propose", update=engine.updates().propose(request))


def cmd_updates(engine, request):
    return ok("updates", updates=engine.updates().list(request.get("status")))


def cmd_decide(engine, request):
    return ok("decide", update=engine.updates().decide(request))


def cmd_apply(engine, request):
    update, written = engine.updates().apply(request)
    return ok("apply", update=update, written=written)


def cmd_cite(engine, request):
    citation_id, stored = engine.citations().cite(request, engine, engine.updates())
    return ok("cite", citation_id=citation_id, stored=stored)


def cmd_citations(engine, request):
    records, problems = engine.citations().citations(request, engine)
    return ok("citations", records=records, problems=problems)


COMMANDS = {"health": cmd_health, "find": cmd_find, "search": cmd_search, "read": cmd_read,
            "pull": cmd_pull, "pulled": cmd_pulled, "propose": cmd_propose, "updates": cmd_updates,
            "decide": cmd_decide, "apply": cmd_apply, "cite": cmd_cite, "citations": cmd_citations}


def check_request(command, request):
    """Refuse any request the contract would refuse, before the tool touches memory."""
    schema = CONTRACT["commands"][command]["request"]
    problems = check_contract.validate(request, schema, CONTRACT)
    if problems:
        raise Refusal("bad_request", "The request does not match the contract: " + "; ".join(problems))


def run(command, request, env=None):
    """Answer one request. Returns the list of answers (pull may give several)."""
    try:
        check_request(command, request)
        engine = FolderEngine(load_settings(env))
        answers = COMMANDS[command](engine, request)
    except Refusal as r:
        answers = error(command, r)
    except OSError as exc:
        # Garura memory could not be written (a pull, or saving a used Phoenix file)
        answers = error(command, Refusal("tier_missing", f"Garura memory cannot be written: {exc}.", "garura"))
    return answers if isinstance(answers, list) else [answers]


# --- the command line ----------------------------------------------------------------

class BadFlags(Exception):
    """A command line the tool cannot read; answered as bad_request, never a bare usage error."""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise BadFlags(message)


def parse(argv):
    ap = Parser(description=__doc__.splitlines()[1])
    sub = ap.add_subparsers(dest="command", required=True)
    for name in COMMANDS:
        p = sub.add_parser(name)
        p.add_argument("--request", help="the whole request as one JSON object")
        if name in ("find", "search", "read"):
            p.add_argument("--issue", type=int)
        if name in ("find", "search"):
            p.add_argument("--glob")
            p.add_argument("--tier")
            p.add_argument("--every-tier", dest="every_tier", action="store_true", default=None)
        if name == "search":
            p.add_argument("--pattern")
            p.add_argument("--fixed", action="store_true", default=None)
            p.add_argument("--ignore-case", dest="ignore_case", action="store_true", default=None)
            p.add_argument("--max", type=int)
        if name == "read":
            p.add_argument("--tier")
            p.add_argument("--path")
            p.add_argument("--start", type=int)
            p.add_argument("--end", type=int)
        if name == "pull":
            p.add_argument("patterns", nargs="*")
            p.add_argument("--path")
        if name == "pulled":
            p.add_argument("--behind", action="store_true", default=None)
        if name == "updates":
            p.add_argument("--status")
        if name == "apply":
            p.add_argument("--id")
        if name == "citations":
            p.add_argument("--issue", type=int)
            p.add_argument("--play")
            p.add_argument("--check", action="store_true", default=None)
    for name, p in sub.choices.items():
        p.__class__ = Parser
    ns = ap.parse_args(argv)
    if ns.request:
        try:
            request = json.loads(ns.request)
        except ValueError as exc:
            raise BadFlags(f"--request is not one JSON object: {exc}") from exc
        if not isinstance(request, dict):
            raise BadFlags("--request is not one JSON object.")
    else:
        request = {k: v for k, v in vars(ns).items() if k not in ("command", "request") and v not in (None, [])}
    return ns.command, request


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        command, request = parse(argv)
        if command == "pull" and "patterns" in request:
            # the command line's list is one contract request ({path}) per path
            requests = [{"path": p} for p in request.pop("patterns")] + ([request] if request else [])
            answers = [a for r in requests for a in run("pull", r)]
            for a in answers:
                print(json.dumps(a))
            return 0 if all(a["ok"] for a in answers) else 1
    except BadFlags as exc:
        command = argv[0] if argv and argv[0] in COMMANDS else None
        if command is None:
            print(f"memory.py: {exc}. Commands: {', '.join(COMMANDS)}.", file=sys.stderr)
            return 2
        print(json.dumps(error(command, Refusal("bad_request", str(exc)))))
        return 1
    answers = run(command, request)
    for a in answers:
        print(json.dumps(a))
    return 0 if all(a["ok"] for a in answers) else 1


if __name__ == "__main__":
    sys.exit(main())
