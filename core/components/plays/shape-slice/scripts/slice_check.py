#!/usr/bin/env python3
"""
slice_check.py — the model's own checks after /shape-slice wrote the slice (C6, C9, C11).

It runs the shared grounding linter over the whole model (`lint_grounding.py --root --spine`:
the structure and link check, with the old-name guard inside it) and then checks the one
slice this run wrote:
  - the spine entry is there and holds exactly id, slug, feature_refs, vertical, intents,
    record, with record pointing to slices/<id>.yaml;
  - it lists the business intent;
  - its record at slices/<id>.yaml holds one surface, with a name equal to the vertical and
    a persona_ref (the person who tests it).

    python3 slice_check.py --root <product-os dir> --spine <_spine.yaml> \
        --slice-id <id> --intent <bi-id> --out <slice-check.json>

Writes {"valid": bool, "lint": {...}, "problems": [...]}. `valid` is true only when the
linter reads ok and the slice has no problem. Exit 0 valid, 1 not valid, 2 usage error.
Files on disk only; no git, no network.
"""

import argparse
import json
import os
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("slice_check.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE_FIELDS = ["id", "slug", "feature_refs", "vertical", "intents", "record"]


def lint(root, spine):
    p = subprocess.run([sys.executable, os.path.join(HERE, "lint_grounding.py"),
                        "--root", root, "--spine", spine], capture_output=True, text=True)
    try:
        report = json.loads(p.stdout)
    except json.JSONDecodeError:
        report = {"ok": False, "errors": [p.stderr.strip() or "the linter gave no report"]}
    if p.returncode == 2:
        report["ok"] = False
        report.setdefault("errors", []).append(p.stderr.strip() or "the linter stopped")
    return report


def slice_problems(root, spine_path, sid, intent):
    with open(spine_path, encoding="utf-8") as fh:
        spine = yaml.safe_load(fh) or {}
    entry = next((s for s in spine.get("slices") or [] if isinstance(s, dict) and s.get("id") == sid), None)
    if entry is None:
        return [f"slice '{sid}' is not in the spine"]
    problems = []
    if list(entry) != SPINE_FIELDS:
        problems.append(f"slice '{sid}' spine entry holds {list(entry)}, not exactly {SPINE_FIELDS}")
    if entry.get("record") != f"slices/{sid}.yaml":
        problems.append(f"slice '{sid}' record pointer is {entry.get('record')!r}, "
                        f"not 'slices/{sid}.yaml'")
    if intent not in (entry.get("intents") or []):
        problems.append(f"slice '{sid}' does not list business intent '{intent}'")
    rec_path = os.path.join(root, "slices", f"{sid}.yaml")
    if not os.path.isfile(rec_path):
        return problems + [f"slice '{sid}' has no record at slices/{sid}.yaml"]
    with open(rec_path, encoding="utf-8") as fh:
        rec = (yaml.safe_load(fh) or {}).get("slice") or {}
    surface = rec.get("surface")
    if not isinstance(surface, dict):
        problems.append(f"slice '{sid}' record does not hold exactly one surface")
    else:
        if surface.get("name") != entry.get("vertical"):
            problems.append(f"slice '{sid}' surface '{surface.get('name')}' is not its vertical "
                            f"'{entry.get('vertical')}'")
        if not surface.get("persona_ref"):
            problems.append(f"slice '{sid}' surface names no persona_ref (no tester)")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the model after the slice is written.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--spine", required=True)
    ap.add_argument("--slice-id", required=True)
    ap.add_argument("--intent", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if not os.path.isfile(args.spine):
        sys.stderr.write(f"slice_check.py: spine not found: {args.spine}\n")
        return 2
    report = lint(args.root, args.spine)
    try:
        problems = slice_problems(args.root, args.spine, args.slice_id, args.intent)
    except (OSError, yaml.YAMLError) as exc:
        problems = [f"cannot read the slice: {exc}"]
    result = {"valid": bool(report.get("ok")) and not problems, "lint": report, "problems": problems}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({"valid": result["valid"], "lint_errors": len(report.get("errors") or []),
                      "problems": problems}, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
