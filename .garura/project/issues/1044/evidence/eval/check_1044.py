#!/usr/bin/env python3
"""
check_1044.py — the acceptance check of #1044 (the ADR 066 rename). It tests the issue's
"Done when" and nothing else. Read only: it reads the repository, runs the old-name check and
the linter, and reads the five closed issues through `gh` (no write anywhere).

    python3 .garura/project/issues/1044/evidence/eval/check_1044.py [--root .] [--no-network]

Exit 0 when every check passes, 1 when any fails (each is listed), 2 when it cannot run.
Written before the build; it must fail on main and pass after the rename.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import yaml

RENAMES = {  # ADR 066, .garura/project/issues/1021/context/names.md
    "plays": {
        "discover-intent": "specify-intent", "discover-domains": "specify-domains",
        "discover-capabilities": "specify-capabilities", "edit-ontology": "specify-ontology",
        "shape-slice": "design-slice", "shape-eval": "design-eval", "record-decision": "design-adr",
        "shape-ux-lens": "design-surface", "shape-run-lens": "design-env",
        "shape-architecture-lens": "design-architecture", "shape-quality-lens": "design-quality",
        "shape-agentic-lens": "design-agentic",
        "build-epic": "build-work", "fix-bug": "fix-work", "refactor-code": "refactor-work",
        "create-play": "build-play", "edit-play": "fix-play", "create-loop": "build-loop",
        "edit-loop": "fix-loop",
        "check-change": "validate-work", "validate-epic": "validate-slice", "release-epic": "validate-uat",
        "update-plan": "reshape-plan", "show-plan": "view-plan", "list-focus-issues": "list-issues",
        "start-change": "start-work", "commit-change": "commit-work", "propose-change": "review-work",
        "merge-change": "merge-work",
    },
    "loops": {"complete-discovery": "loop-product-spec"},
}
CLOSED = [736, 742, 743, 744, 745]
LINE = "> **Replaced by ADR 066 (2026-11-03); the rename is #1044.**"
OLDER_ADRS = ["028", "029", "038", "045", "046", "053"]
PHOENIX = os.path.expanduser("~/.phoenix/core/memory/standards/rules")
RULES = "core/components/memory/standards/rules"

results = []


def check(label, ok, detail=""):
    results.append({"check": label, "ok": bool(ok), "detail": detail})


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--no-network", action="store_true")
    ns = ap.parse_args()
    root = ns.root
    count = sum(len(v) for v in RENAMES.values())
    check("the list holds 30 renames", count == 30, f"{count}")

    # 1. Each part moved: the old folder is gone, the new one is there with its name and ICE.
    for kind, pairs in RENAMES.items():
        for old, new in pairs.items():
            old_dir = os.path.join(root, "core/components", kind, old)
            new_dir = os.path.join(root, "core/components", kind, new)
            skill = os.path.join(new_dir, "SKILL.md")
            ok = not os.path.exists(old_dir) and os.path.isfile(skill)
            name_ok = ok and re.search(rf"^name:\s*{re.escape(new)}\s*$", read(root, os.path.relpath(skill, root)), re.M)
            check(f"{kind}/{old} is now {kind}/{new}", ok and name_ok)
            ice = os.path.join(new_dir, "reference", "ice.md")
            if os.path.isfile(ice):
                text = read(root, os.path.relpath(ice, root))
                stale = re.search(rf"(?<![\w-]){re.escape(old)}(?![\w-])", text)
                check(f"{new}'s ICE names no old name of its own", not stale)

    # 2. The rename map holds the 30 pairs, and no entry still points at a renamed name.
    rmap = yaml.safe_load(read(root, f"{RULES}/rename-map.yaml")) or {}
    for kind, pairs in RENAMES.items():
        have = rmap.get(kind) or {}
        missing = [o for o, n in pairs.items() if have.get(o) != n]
        check(f"the rename map has every {kind} pair", not missing, ", ".join(missing))
        stale = [o for o, n in have.items() if n in pairs]
        check(f"no {kind} entry in the map still points at an old name", not stale, ", ".join(stale))

    # 3. The old-name check exits 0.
    r = subprocess.run([sys.executable, "core/tools/naming/check_old_names.py", "--root", root],
                       cwd=root, capture_output=True, text=True)
    check("the old-name check exits 0", r.returncode == 0, r.stdout[-400:] if r.returncode else "")

    # 4. The linter reports no naming error, run from the repository root.
    r = subprocess.run(["node", "core/tools/lint-components/index.js", "--target", "core/components"],
                       cwd=root, capture_output=True, text=True)
    try:
        violations = json.loads(r.stdout).get("violations", [])
        naming = [v for v in violations if v.get("rule", "").startswith("naming")]
        check("the linter reports no naming error", not naming,
              "; ".join(f"{v['file']}: {v['message']}" for v in naming[:5]))
    except json.JSONDecodeError:
        check("the linter reports no naming error", False, "the linter's output is not JSON")

    # 5. Under the new rules, loop-product-spec passes and a play named exactly a built-in fails.
    js = ("const {checkName}=require('./core/tools/lint-components/lib/rules/naming');"
          "const yaml=require('./core/tools/lint-components/node_modules/js-yaml');"
          "const fs=require('fs');const std=yaml.load(fs.readFileSync("
          f"'{RULES}/naming.yaml','utf8'));"
          "const r=(t,n)=>checkName({type:t,name:n,file:'x'},std).map(v=>v.rule);"
          "console.log(JSON.stringify({loop:r('loop','loop-product-spec'),builtin:r('play','review'),"
          "prefix:r('play','review-work'),env:r('play','design-env')}));")
    r = subprocess.run(["node", "-e", js], cwd=root, capture_output=True, text=True)
    try:
        got = json.loads(r.stdout)
        check("a loop named loop-product-spec passes", got["loop"] == [], str(got["loop"]))
        check("a play named exactly a built-in command fails", "naming-reserved" in got["builtin"], str(got["builtin"]))
        check("a play that starts with a built-in command passes", got["prefix"] == [], str(got["prefix"]))
        check("env is an allowed short word", got["env"] == [], str(got["env"]))
    except (json.JSONDecodeError, KeyError):
        check("the new naming rules can be run", False, (r.stderr or r.stdout)[-300:])

    # 6. The phase table in naming.md names the second phase Spec.
    md = read(root, f"{RULES}/naming.md")
    check("naming.md's phase table says Product → Spec and Spec → Design",
          "Product → Spec" in md and "Spec → Design" in md and "→ Intent" not in md and "Intent →" not in md)

    # 7. Phoenix memory's copies match the source.
    for name in ("naming.md", "naming.yaml"):
        src = read(root, f"{RULES}/{name}")
        p = os.path.join(PHOENIX, name)
        same = os.path.isfile(p) and open(p, encoding="utf-8").read() == src
        check(f"Phoenix memory's {name} matches the source", same)

    # 8. ADR 066 names this issue; the index shows ADR 066 beside each record it changes.
    adr = [f for f in os.listdir(os.path.join(root, "docs/adr")) if f.startswith("066-")]
    check("ADR 066 names #1044", adr and "#1044" in read(root, f"docs/adr/{adr[0]}"))
    index = read(root, "docs/adr/_index.md")
    for n in OLDER_ADRS:
        row = next((ln for ln in index.splitlines() if ln.startswith(f"| [{n}]")), "")
        check(f"the ADR index shows ADR 066 beside ADR {n}", "066" in row.split("|")[3] if row.count("|") > 4 else False, row[:160])

    # 9. The five closed issues carry their line.
    if not ns.no_network:
        for n in CLOSED:
            r = subprocess.run(["gh", "issue", "view", str(n), "--repo", "intent-driven-ai/garura",
                                "--json", "body,state"], capture_output=True, text=True)
            try:
                d = json.loads(r.stdout)
                check(f"#{n} starts with the line and is still closed",
                      d["body"].startswith(LINE) and d["state"] == "CLOSED")
            except (json.JSONDecodeError, KeyError):
                check(f"#{n} can be read", False, r.stderr[-200:])

    failed = [x for x in results if not x["ok"]]
    print(json.dumps({"passed": len(results) - len(failed), "failed": len(failed),
                      "failures": failed}, indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, yaml.YAMLError) as exc:
        print(json.dumps({"error": str(exc)}))
        sys.exit(2)
