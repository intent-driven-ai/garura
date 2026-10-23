#!/usr/bin/env python3
"""
slice_check.py — the model's own checks after /shape-slice wrote the slice (C6, C9, C11).

It runs the shared grounding linter over the whole model (`lint_grounding.py --root --spine`:
the structure and link check, with the old-name guard inside it) and then checks the slices:
  - the slice this run wrote is in the spine and lists the business intent;
  - EVERY spine slice entry holds the six fields id, slug, feature_refs, vertical, intents,
    record (in any order) and no other — no status, order, effort, depends_on or domain_ref
    (ontology v10) — with record pointing to slices/<id>.yaml;
  - EVERY spine slice's record at slices/<id>.yaml follows slice.yaml v2:
        slice:   {id, slug, name, outcome, feature_refs, vertical, intents}
        surface: {id, name, persona_ref, user_action}
    each field present and not empty; slice.id, feature_refs, vertical and intents equal to
    the spine entry's; surface.name equal to the vertical. A record with no persona_ref (no
    tester) is not valid.

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
RECORD_SLICE = ["id", "slug", "name", "outcome", "feature_refs", "vertical", "intents"]
RECORD_SURFACE = ["id", "name", "persona_ref", "user_action"]


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


def _filled(value):
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, list):
        return bool(value)
    return value is not None


def record_problems(root, entry):
    sid = entry.get("id")
    rec_path = os.path.join(root, "slices", f"{sid}.yaml")
    if not os.path.isfile(rec_path):
        return [f"slice '{sid}' has no record at slices/{sid}.yaml"]
    with open(rec_path, encoding="utf-8") as fh:
        rec = yaml.safe_load(fh) or {}
    if not isinstance(rec, dict):
        return [f"slice '{sid}' record is not a YAML mapping"]
    problems = []
    body = rec.get("slice") if isinstance(rec.get("slice"), dict) else {}
    for key in RECORD_SLICE:
        if not _filled(body.get(key)):
            problems.append(f"slice '{sid}' record has no slice.{key}")
    for key in ("id", "feature_refs", "vertical", "intents"):
        if _filled(body.get(key)) and body.get(key) != entry.get(key):
            problems.append(f"slice '{sid}' record slice.{key} is {body.get(key)!r}, not the "
                            f"spine entry's {entry.get(key)!r}")
    surface = rec.get("surface")
    if not isinstance(surface, dict):
        problems.append(f"slice '{sid}' record does not hold exactly one surface (top-level "
                        "`surface`, slice.yaml v2)")
        return problems
    for key in RECORD_SURFACE:
        if not _filled(surface.get(key)):
            what = " (no tester)" if key == "persona_ref" else ""
            problems.append(f"slice '{sid}' record surface has no {key}{what}")
    if _filled(surface.get("name")) and surface.get("name") != entry.get("vertical"):
        problems.append(f"slice '{sid}' surface '{surface.get('name')}' is not its vertical "
                        f"'{entry.get('vertical')}'")
    return problems


def entry_problems(entry):
    sid = entry.get("id")
    problems = []
    keys = list(entry)
    if set(keys) != set(SPINE_FIELDS) or len(keys) != len(SPINE_FIELDS):
        problems.append(f"slice '{sid}' spine entry holds {keys}, not exactly the six fields "
                        f"{SPINE_FIELDS}")
    if entry.get("record") != f"slices/{sid}.yaml":
        problems.append(f"slice '{sid}' record pointer is {entry.get('record')!r}, "
                        f"not 'slices/{sid}.yaml'")
    return problems


def slice_problems(root, spine_path, sid, intent):
    with open(spine_path, encoding="utf-8") as fh:
        spine = yaml.safe_load(fh) or {}
    entries = [s for s in spine.get("slices") or [] if isinstance(s, dict)]
    entry = next((s for s in entries if s.get("id") == sid), None)
    if entry is None:
        return [f"slice '{sid}' is not in the spine"]
    problems = []
    if intent not in (entry.get("intents") or []):
        problems.append(f"slice '{sid}' does not list business intent '{intent}'")
    for e in entries:
        problems += entry_problems(e)
        problems += record_problems(root, e)
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
