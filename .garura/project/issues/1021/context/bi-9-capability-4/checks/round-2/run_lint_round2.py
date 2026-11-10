#!/usr/bin/env python3
"""Run the structure check on each new or changed page of one BI-9 capability folder (round 2).

Run from the repository root:
    python3 -B <run>/checks/round-2/run_lint_round2.py --run <run> --cap <capability folder> \
        --feature <page> [<page> ...] [--capability <page>]
Each feature page is checked with --kind feature --stage detailed. A changed capability page is
checked at both stages, as the earlier round did, because its approved shape is the directional one.
Writes <run>/checks/round-2/lint.json.
"""
import argparse, datetime, json, os, subprocess, sys

LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
ap = argparse.ArgumentParser()
ap.add_argument("--run", required=True)
ap.add_argument("--cap", required=True)
ap.add_argument("--feature", nargs="*", default=[])
ap.add_argument("--capability", default=None)
a = ap.parse_args()
base = os.path.join(a.run, "drafts", "product-os", "software-delivery-planning", a.cap)
runs = [(p, ["--kind", "feature", "--stage", "detailed"]) for p in a.feature]
if a.capability:
    runs += [(a.capability, ["--kind", "capability", "--stage", s]) for s in ("detailed", "directional")]
results = []
for rel, args in runs:
    out = subprocess.run([sys.executable, LINT, "--doc", os.path.join(base, rel), *args], capture_output=True, text=True)
    d = json.loads(out.stdout)
    results.append({"doc": rel, "args": args, "ok": d["ok"], "errors": d["errors"], "warnings": d["warnings"]})
    print(("ok  " if d["ok"] else "FAIL"), " ".join(args), rel, len(d["errors"]), "errors", len(d["warnings"]), "warnings")
json.dump({"checked_on": datetime.date.today().isoformat(), "tool": LINT, "results": results},
          open(os.path.join(a.run, "checks", "round-2", "lint.json"), "w"), indent=2)
