#!/usr/bin/env python3
"""
apply_renames.py — move every component to its new name and update every reference (#743-#746).

Reads core/components/memory/standards/rules/rename-map.yaml. For each old -> new name it
(1) moves the component with `git mv` (plays/<old>/, loops/<old>/, skills/<old>/,
agents/<old>.md), (2) sets the `name:` line in the moved component, and (3) rewrites every
reference the old-name check finds — the same patterns, so the check passes after this runs.

    python3 core/tools/naming/apply_renames.py [--root .] [--kind plays|loops|skills|agents] [--dry-run]

Names and references only: no behaviour changes. Past records (.garura/, CHANGELOG.md, the ADRs
before ADR 046) keep their old words. Idempotent: a second run finds nothing to move or rewrite.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_old_names as co  # noqa: E402

COMPONENTS = "core/components"


def move(root, kind, old, new, dry):
    if kind == "agents":
        src, dst = f"{COMPONENTS}/agents/{old}.md", f"{COMPONENTS}/agents/{new}.md"
    else:
        src, dst = f"{COMPONENTS}/{kind}/{old}", f"{COMPONENTS}/{kind}/{new}"
    if not os.path.exists(os.path.join(root, src)) or os.path.exists(os.path.join(root, dst)):
        return None
    if not dry:
        for attempt in range(8):  # the repo's index.lock flickers; retry the move
            if subprocess.run(["git", "mv", src, dst], cwd=root, capture_output=True).returncode == 0:
                break
            time.sleep(1.5)
        else:
            raise RuntimeError(f"git mv {src} {dst} failed")
        main = os.path.join(root, dst if kind == "agents" else f"{dst}/SKILL.md")
        if os.path.isfile(main):
            text = open(main, encoding="utf-8").read()
            text = re.sub(rf"^(name:\s*)(?:garura:)?{re.escape(old)}\s*$", rf"\g<1>{new}", text, count=1, flags=re.M)
            open(main, "w", encoding="utf-8").write(text)
    return f"{src} -> {dst}"


def rewrite(root, rename, kinds, dry):
    compiled = []
    for kind in kinds:
        for old, new in sorted(rename[kind].items(), key=lambda kv: -len(kv[0])):
            compiled += [(p, new) for p in co.patterns(old, kind)]
    changed = {}
    for rel in co.files(root):
        if rel in co.SKIP_FILES or co.is_past_record(rel):
            continue
        path = os.path.join(root, rel)
        try:
            text = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        out, n = text, 0
        here = compiled
        if co.is_loop_file(rel) and "plays" in kinds:
            here = compiled + [(p, new) for old, new in sorted(rename["plays"].items(), key=lambda kv: -len(kv[0]))
                               for p in co.loop_patterns(old)]
        for p, new in here:
            out, k = p.subn(lambda m, new=new: m.group(0)[:m.start("n") - m.start(0)] + new
                            + m.group(0)[m.end("n") - m.start(0):], out)
            n += k
        if n:
            changed[rel] = n
            if not dry:
                open(path, "w", encoding="utf-8").write(out)
    return changed


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--kind", choices=["plays", "loops", "skills", "agents"], action="append")
    ap.add_argument("--dry-run", action="store_true")
    ns = ap.parse_args(argv)
    rename = co.load_map(ns.root)
    kinds = ns.kind or ["plays", "loops", "skills", "agents"]
    moved = [m for kind in kinds for old, new in rename[kind].items()
             if (m := move(ns.root, kind, old, new, ns.dry_run))]
    changed = rewrite(ns.root, rename, kinds, ns.dry_run)
    print(json.dumps({"moved": len(moved), "files_changed": len(changed),
                      "references": sum(changed.values()), "dry_run": ns.dry_run}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
