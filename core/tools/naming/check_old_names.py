#!/usr/bin/env python3
"""
check_old_names.py — is any old component name still used? (#741, harness standard, ADR 046)

Reads core/components/memory/standards/rules/rename-map.yaml and searches the repo for
every old name where it can only mean the component:

  a name with a "-" in it (kb-search, review-change)  — anywhere, as a whole token
  any old name                                        — as a command (/vision, /garura:vision),
                                                        a component path (plays/vision/,
                                                        skills/kb-search/), a play field
                                                        (play="vision", --play vision), or
                                                        "`vision` play" in prose

A one-word old name (vision, run, quality) is an everyday word, so plain prose is not
searched for it. Past records keep their old words and are not searched: .garura/,
CHANGELOG.md, the ADRs before ADR 046, and ADR 046 and ADR 048 (they record the renames).

    python3 core/tools/naming/check_old_names.py [--root .] [--kind plays|skills|loops|agents] \
        [--out report.json]

Exit 0 when no old name is left, 1 when some are (the report lists each one with file and
line), 2 when the map cannot be read. Read only: no git, no network, no LLM.
"""
import argparse
import json
import os
import re
import sys

import yaml

MAP = "core/components/memory/standards/rules/rename-map.yaml"
SEARCH = ["core", "docs", "installer", "CLAUDE.md", "README.md", "AGENTS.md"]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".garura"}
SKIP_FILES = {MAP, "core/components/memory/standards/rules/naming.yaml",
              "core/tools/naming/check_old_names.py", "core/tools/naming/apply_renames.py",
              "core/tools/naming/test_naming_tools.py", "CHANGELOG.md",
              "core/components/memory/standards/rules/naming.md", "core/tools/lint-components/test/naming.test.js",
              "core/tools/lint-components/package.json", "core/tools/lint-components/package-lock.json",
              "docs/adr/_index.md", "docs/agentic-methodology/tools/lint-components.md",
              "core/components/plays/install-garura/scripts/test_install.py"}  # sets up old-name folders on purpose
TEXT = (".md", ".py", ".js", ".yaml", ".yml", ".json", ".sh", ".txt", ".toml")
FIRST_RENAME_ADR = 46
RENAME_ADRS = {46, 48}  # they record the renames, so they name the old names on purpose
# ADRs that quote an older ADR word for word, old names included. ADR 053 quotes ADR 033's
# "`/intent` and `/adr` run by hand". ADR 059 quotes the old names of the plays and the loop it
# found left behind, as the defect it records. An accepted ADR is not edited (only a forward
# pointer may be added), so the check does not search these.
QUOTING_ADRS = {53, 59}
# Files whose keys are play or loop names (the next-step map, the config).
KEYED_FILES = {"core/components/memory/standards/rules/pipeline-next.md", "core/config.yaml"}


def load_map(root):
    with open(os.path.join(root, MAP), encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return {kind: dict(data.get(kind) or {}) for kind in ("plays", "loops", "skills", "agents")}


def is_past_record(rel):
    m = re.match(r"docs/adr/(?:SUPERSEDED-)?(\d{3})-", rel)
    if not m:
        return False
    number = int(m.group(1))
    return number < FIRST_RENAME_ADR or number in RENAME_ADRS or number in QUOTING_ADRS


def patterns(old, kind):
    """Regexes that match `old` only where it names the component. The name sits in group "n"."""
    o = re.escape(old)
    folder = {"plays": "plays", "loops": "loops", "skills": "skills", "agents": "agents"}[kind]
    pats = [
        rf"(?:^|(?<=[\s`(\"'|\[]))/(?:garura:)?(?P<n>{o})(?![\w/-])",       # /vision, /garura:vision
        rf"\b{folder}/(?P<n>{o})(?=[/.\s`'\")]|$)",                         # plays/vision/, agents/env-operator.md
        rf"\bplay[\"']?\s*[:=,]\s*[\"'](?P<n>{o})(?=[\"'])",                # play="vision", "play": "vision"
        rf"--play[\"']?,?\s+[\"']?(?P<n>{o})(?=[\"'\s]|$)",                  # --play vision
        rf"`(?P<n>{o})`(?=\s+(?:play|plays|loop|skill|skills)\b)",           # `vision` play
    ]
    pats.append(rf"(?<=plays=)(?:[\w-]+,)*(?P<n>{o})(?=[,\s;]|$)")                    # plays=intent,vision
    pats.append(rf"(?<=plays=)[\w,-]*,(?P<n>{o})(?=[,\s;]|$)")
    pats.append(rf"\bloops\.(?P<n>{o})\.")                                          # loops.discovery.runner
    if "-" in old:
        pats.append(rf"(?<![\w-])(?<!tools/)(?P<n>{o})(?![\w-])")                     # kb-search anywhere
    return [re.compile(p, re.M) for p in pats]


def is_loop_file(rel):
    return rel.startswith("core/components/loops/") or "/compiled-loop-example/" in rel


def loop_patterns(old):
    """Inside a loop, a play is named in its step owner, input and answer paths, done and
    question files, and its table cells — places where the word can only mean the play."""
    o = re.escape(old)
    return [re.compile(p, re.M) for p in (
        rf"`(?P<n>{o})`",                                   # Owner: `intent`, R5 for `intent`
        rf"\b(?:inputs|answers)\.(?P<n>{o})\.",              # inputs.intent.statement
        rf"(?<![\w-])(?P<n>{o})-done\.json",                  # intent-done.json
        rf"\bopen-(?P<n>{o})\.json",                          # open-vision.json
        rf"\|\s*\d+\s*\|\s*(?P<n>{o})\s*\|",                    # | 1 | intent |
        rf"\|\s*plays\s*\|[^|\n]*?(?<![\w-])(?P<n>{o})(?![\w-])",  # | plays | intent, vision |
    )]


def files(root):
    for top in SEARCH:
        path = os.path.join(root, top)
        if os.path.isfile(path):
            yield top
            continue
        for d, dirs, names in os.walk(path):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for n in names:
                if n.endswith(TEXT):
                    yield os.path.relpath(os.path.join(d, n), root)


def find(root, rename, kinds):
    hits = []
    compiled = [(kind, old, new, patterns(old, kind)) for kind in kinds for old, new in rename[kind].items()]
    for rel in files(root):
        if rel in SKIP_FILES or is_past_record(rel):
            continue
        try:
            text = open(os.path.join(root, rel), encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        keyed = rel in KEYED_FILES
        in_loop = is_loop_file(rel)
        for kind, old, new, pats in compiled:
            extra = [re.compile(rf"^(?:\s+)(?P<n>{re.escape(old)})(?=:\s)", re.M),
                     re.compile(rf"command:\s*(?P<n>{re.escape(old)})(?=\s*,)")] if keyed and kind in ("plays", "loops") else []
            if in_loop and kind == "plays":
                extra += loop_patterns(old)
            for p in pats + extra:
                for m in p.finditer(text):
                    line = text.count("\n", 0, m.start("n")) + 1
                    hits.append({"file": rel, "line": line, "kind": kind, "old": old, "new": new})
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--kind", choices=["plays", "loops", "skills", "agents"], action="append")
    ap.add_argument("--out")
    ns = ap.parse_args(argv)
    try:
        rename = load_map(ns.root)
    except (OSError, yaml.YAMLError) as exc:
        print(json.dumps({"error": f"cannot read {MAP}: {exc}"}))
        return 2
    kinds = ns.kind or ["plays", "loops", "skills", "agents"]
    hits = find(ns.root, rename, kinds)
    by_old = {}
    for h in hits:
        by_old[h["old"]] = by_old.get(h["old"], 0) + 1
    report = {"ok": not hits, "hits": len(hits), "old_names_left": len(by_old), "by_old_name": by_old,
              "first": hits[:40]}
    out = json.dumps(report, indent=2)
    if ns.out:
        with open(ns.out, "w", encoding="utf-8") as fh:
            json.dump({**report, "all": hits}, fh, indent=2)
    print(out)
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
