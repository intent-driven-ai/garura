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
    open(path, "w").write(text)


def main():
    with tempfile.TemporaryDirectory() as root:
        subprocess.run(["git", "init", "-q"], cwd=root)
        write(root, co.MAP, yaml.safe_dump({"plays": {"vision": "discover-domains", "shape": "shape-scope"},
                                            "loops": {"discovery": "complete-discovery"},
                                            "skills": {"kb-search": "find-architecture-learnings"},
                                            "agents": {"env-operator": "environment-operator"}}))
        write(root, "core/components/plays/vision/SKILL.md", "---\nname: vision\n---\nRun /shape next.\n")
        write(root, "core/components/plays/shape/SKILL.md", "---\nname: shape\n---\nThen /garura:vision.\n")
        write(root, "core/components/loops/discovery/SKILL.md", "---\nname: discovery\n---\nRuns /vision.\n")
        write(root, "core/components/skills/kb-search/SKILL.md", "---\nname: kb-search\n---\nx\n")
        write(root, "core/components/agents/env-operator.md", "---\nname: env-operator\n---\nUses kb-search.\n")
        write(root, "docs/guide.md", "Run `/vision`, then the `shape` play. A good vision matters. See docs/adr/006.\n"
                                     "Path: core/components/plays/vision/SKILL.md. Lens quality stays.\n")
        write(root, "core/x.py", 'play = "vision"\nLENS = ("quality", "run")\nkey = "shape"\n')
        write(root, "docs/adr/006-naming.md", "The /vision play.\n")
        write(root, "CHANGELOG.md", "/vision shipped.\n")
        subprocess.run(["git", "add", "-A"], cwd=root)
        subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x"], cwd=root)

        before = co.find(root, co.load_map(root), ["plays", "loops", "skills", "agents"])
        files_hit = {h["file"] for h in before}
        check("today: the check finds the old names", len(before) >= 10)
        check("a plain English 'vision' in prose is not flagged",
              not any(h["file"] == "docs/guide.md" and h["line"] == 1 and h["old"] == "vision" and h.get("x") for h in before))
        check("a lens word in code is not flagged", not any(h["file"] == "core/x.py" and h["line"] == 2 for h in before))
        check("a dict key 'shape' in code is not flagged", not any(h["file"] == "core/x.py" and h["line"] == 3 for h in before))
        check("past records are not searched", "docs/adr/006-naming.md" not in files_hit and "CHANGELOG.md" not in files_hit)

        ar.main(["--root", root])
        after = co.find(root, co.load_map(root), ["plays", "loops", "skills", "agents"])
        check("after the rename the check finds nothing", after == [])
        check("folders moved", os.path.isdir(os.path.join(root, "core/components/plays/discover-domains"))
              and not os.path.exists(os.path.join(root, "core/components/plays/vision")))
        check("agent file moved", os.path.isfile(os.path.join(root, "core/components/agents/environment-operator.md")))
        check("name line updated", "name: discover-domains" in open(os.path.join(root, "core/components/plays/discover-domains/SKILL.md")).read())
        guide = open(os.path.join(root, "docs/guide.md")).read()
        check("commands and paths rewritten", "`/discover-domains`" in guide and "plays/discover-domains/SKILL.md" in guide
              and "`shape-scope` play" in guide)
        check("prose words and lens words kept", "A good vision matters" in guide and "Lens quality stays" in guide)
        check("docs/adr path kept", "docs/adr/006" in guide)
        code = open(os.path.join(root, "core/x.py")).read()
        check("play field rewritten, lens and key kept", 'play = "discover-domains"' in code and '("quality", "run")' in code and 'key = "shape"' in code)
        check("/shape-scope not double-rewritten", "/shape-scope" in open(os.path.join(root, "core/components/plays/discover-domains/SKILL.md")).read())
        check("past records kept their old words", "/vision" in open(os.path.join(root, "CHANGELOG.md")).read()
              and "/vision" in open(os.path.join(root, "docs/adr/006-naming.md")).read())
        ar.main(["--root", root])
        check("a second run changes nothing", co.find(root, co.load_map(root), ["plays"]) == [])
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
