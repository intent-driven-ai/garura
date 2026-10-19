#!/usr/bin/env python3
"""#661 item 10 — list every memory path left in #661's scope, and find none.

Scope: /intent, /vision, /understand (SKILL.md and reference/ice.md), their two agents and
the skills those agents hand memory to, template-manager, judge-grounding, the shared close,
and every play's close block. A memory path is a place in a memory tier named by its folder
(the tool, never a path, finds memory — ADR 035, ADR 039). A line that only forbids one
(for example "never use the old router (`kb.py`)") is not a read.
Exit 0 when none is found, 1 otherwise.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(ROOT, "core", "components")):
    ROOT = os.path.dirname(ROOT)
C = os.path.join(ROOT, "core", "components")

PATTERNS = [
    r"<memory>", r"\{memory\}", r"\$\{?ltm_project_target", r"ltm\.project-target",
    r"~/\.garura/core/memory", r"~/\.garura/phoenix-memory", r"~/\.phoenix/core/memory/\S",
    r"\.garura/core/memory/\S", r"core/components/memory/", r"kb\.py", r"\$KB\b", r"\{KB\}",
    r"\.pageindex", r"ltm_context", r"\$\(cat \"(?!\$\{templates\})[^)]*standards/",  # ${templates} is the short-term copy
]
FORBIDS = re.compile(r"\b(never|not|no longer|forbid|instead of)\b", re.I)

def scope():
    files = []
    for play in ("intent", "vision", "understand"):
        files += [os.path.join(C, "plays", play, "SKILL.md"), os.path.join(C, "plays", play, "reference", "ice.md")]
    for agent in ("business-intent-keeper", "product-os-keeper", "template-manager"):
        files.append(os.path.join(C, "agents", agent + ".md"))
    for skill in ("author-business-intent", "author-vision-seed", "enrich-capability-ice", "search-kb",
                  "kb-search", "propose-kb-node", "judge-grounding"):
        files.append(os.path.join(C, "skills", skill, "SKILL.md"))
    files.append(os.path.join(C, "plays", "_shared", "play-close.md"))
    return files

def close_blocks():
    opener, closer = "# --- Standard Play Close", "# --- end Standard Play Close ---"
    for play in sorted(os.listdir(os.path.join(C, "plays"))):
        f = os.path.join(C, "plays", play, "SKILL.md")
        if os.path.isfile(f):
            text = open(f, encoding="utf-8").read()
            a, b = text.find(opener), text.find(closer)
            if a >= 0 and b > a:
                start = text[:a].count("\n") + 1
                yield f, start, text[a:b]

def scan(path, text, first_line=1):
    hits = []
    for n, line in enumerate(text.split("\n"), first_line):
        for p in PATTERNS:
            if re.search(p, line) and not FORBIDS.search(line):
                hits.append((os.path.relpath(path, ROOT), n, p, line.strip()[:140]))
    return hits

hits, checked = [], 0
for f in scope():
    checked += 1
    hits += scan(f, open(f, encoding="utf-8").read())
closes = 0
for f, start, block in close_blocks():
    closes += 1
    hits += scan(f, block, start)
for h in hits:
    print("%s:%d  [%s]  %s" % h)
print(f"checked {checked} files and {closes} play closes; memory paths found: {len(hits)}")
sys.exit(1 if hits else 0)
