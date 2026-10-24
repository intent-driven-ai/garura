#!/usr/bin/env python3
"""test_naming_tools.py — the old-name check and the rename tool on a scratch repo (#741, #743).

    python3 core/tools/naming/test_naming_tools.py
"""
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_renames as ar  # noqa: E402
import check_old_names as co  # noqa: E402

PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


def read(root, rel):
    with open(os.path.join(root, rel)) as fh:
        return fh.read()


RENAME_MAP = {"plays": {"vision": "discover-domains", "grill": "shape-slice"},
              "loops": {"discovery": "complete-discovery"},
              "skills": {"kb-search": "find-architecture-learnings"},
              "agents": {"env-operator": "environment-operator"}}

ADR_TEXT = "The /vision play.\n"
SEED = {
    "core/components/plays/vision/SKILL.md": "---\nname: vision\n---\nRun /grill next.\n",
    "core/components/plays/grill/SKILL.md": "---\nname: grill\n---\nThen /garura:vision.\n",
    "core/components/loops/discovery/SKILL.md": "---\nname: discovery\n---\nRuns /vision.\n",
    "core/components/skills/kb-search/SKILL.md": "---\nname: kb-search\n---\nx\n",
    "core/components/agents/env-operator.md": "---\nname: env-operator\n---\nUses kb-search.\n",
    "docs/guide.md": "Run `/vision`, then the `grill` play. A good vision matters. See docs/adr/006.\n"
                     "Path: core/components/plays/vision/SKILL.md. Lens quality stays.\n",
    "core/x.py": 'play = "vision"\nLENS = ("quality", "run")\nkey = "grill"\n',
    "docs/adr/006-naming.md": ADR_TEXT,
    "docs/adr/046-one-naming-standard.md": ADR_TEXT,
    "docs/adr/047-the-ice.md": ADR_TEXT,
    "docs/adr/048-two-layers.md": ADR_TEXT,
    "docs/adr/049-a-later-decision.md": ADR_TEXT,
    "docs/adr/053-a-quoting-decision.md": ADR_TEXT,
    "docs/adr/054-a-later-decision.md": ADR_TEXT,
    "docs/adr/SUPERSEDED-046-old-naming.md": ADR_TEXT,
    "docs/adr/SUPERSEDED-047-old-ice.md": ADR_TEXT,
    "CHANGELOG.md": "/vision shipped.\n",
}
KINDS = ["plays", "loops", "skills", "agents"]


def seed_repo(root):
    """A scratch repository that holds old names in every place the check reads or skips."""
    subprocess.run(["git", "init", "-q"], cwd=root)
    write(root, co.MAP, yaml.safe_dump(RENAME_MAP))
    for rel, text in SEED.items():
        write(root, rel, text)
    subprocess.run(["git", "add", "-A"], cwd=root)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"], cwd=root)


def hit_at(hits, file, line):
    return any(h["file"] == file and h["line"] == line for h in hits)


def check_before(root):
    """What the old-name check finds, and what it skips, before the rename."""
    before = co.find(root, co.load_map(root), KINDS)
    hit = {h["file"] for h in before}
    check("today: the check finds the old names", len(before) >= 10)
    prose = [h for h in before if h["old"] == "vision" and h.get("x")]
    check("a plain English 'vision' in prose is not flagged", not hit_at(prose, "docs/guide.md", 1))
    check("a lens word in code is not flagged", not hit_at(before, "core/x.py", 2))
    check("a dict key 'grill' in code is not flagged", not hit_at(before, "core/x.py", 3))
    check("past records are not searched", not {"docs/adr/006-naming.md", "CHANGELOG.md"} & hit)
    check("the rename ADRs 046 and 048 are not searched",
          not {"docs/adr/046-one-naming-standard.md", "docs/adr/048-two-layers.md"} & hit)
    check("ADR 047 is searched", "docs/adr/047-the-ice.md" in hit)
    check("ADR 049 is searched", "docs/adr/049-a-later-decision.md" in hit)
    check("ADR 053, which quotes old names, is not searched", "docs/adr/053-a-quoting-decision.md" not in hit)
    check("a later ADR 054 is searched", "docs/adr/054-a-later-decision.md" in hit)
    check("a superseded rename ADR 046 is not searched", "docs/adr/SUPERSEDED-046-old-naming.md" not in hit)
    check("a superseded ADR 047 is searched", "docs/adr/SUPERSEDED-047-old-ice.md" in hit)


def check_after(root):
    """What the rename tool changed, and what it kept."""
    check("after the rename the check finds nothing", co.find(root, co.load_map(root), KINDS) == [])
    check("folders moved", os.path.isdir(os.path.join(root, "core/components/plays/discover-domains"))
          and not os.path.exists(os.path.join(root, "core/components/plays/vision")))
    check("agent file moved", os.path.isfile(os.path.join(root, "core/components/agents/environment-operator.md")))
    play = read(root, "core/components/plays/discover-domains/SKILL.md")
    check("name line updated", "name: discover-domains" in play)
    check("/shape-slice not double-rewritten", "/shape-slice" in play)
    guide = read(root, "docs/guide.md")
    check("commands and paths rewritten", all(w in guide for w in (
        "`/discover-domains`", "plays/discover-domains/SKILL.md", "`shape-slice` play")))
    check("prose words and lens words kept", "A good vision matters" in guide and "Lens quality stays" in guide)
    check("docs/adr path kept", "docs/adr/006" in guide)
    code = read(root, "core/x.py")
    check("play field rewritten, lens and key kept",
          all(w in code for w in ('play = "discover-domains"', '("quality", "run")', 'key = "grill"')))
    check("past records kept their old words",
          "/vision" in read(root, "CHANGELOG.md") and "/vision" in read(root, "docs/adr/006-naming.md"))


def main():
    with tempfile.TemporaryDirectory() as root:
        seed_repo(root)
        check_before(root)
        ar.main(["--root", root])
        check_after(root)
        ar.main(["--root", root])
        check("a second run changes nothing", co.find(root, co.load_map(root), ["plays"]) == [])
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
