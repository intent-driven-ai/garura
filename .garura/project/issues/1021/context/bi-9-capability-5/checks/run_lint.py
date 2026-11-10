#!/usr/bin/env python3
"""Run the grounding structure check on each draft page and keep the results.

Run from the repository root:
    python3 -B <run>/checks/run_lint.py <run>
The capability page is checked with --stage directional, as the approved Argus page
(review-agent-work/capability.md) was; each feature page with --stage detailed.
Writes <run>/checks/lint.json. Exit 1 when any page fails.
"""
import json, os, subprocess, sys

run = sys.argv[1]
cap = os.path.join(run, "drafts", "product-os", "software-delivery-planning", "give-every-gate-a-way-past")
tool = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
jobs = [(os.path.join(cap, "capability.md"), "capability", "directional")]
jobs += [(os.path.join(cap, fn, "feature.md"), "feature", "detailed") for fn in sorted(os.listdir(cap)) if fn.startswith("fn-")]
results = []
for doc, kind, stage in jobs:
    p = subprocess.run(["python3", tool, "--doc", doc, "--kind", kind, "--stage", stage], capture_output=True, text=True)
    out = json.loads(p.stdout)
    results.append({"doc": doc, "args": ["--kind", kind, "--stage", stage], "exit": p.returncode,
                    "ok": out["ok"], "errors": out["errors"], "warnings": out["warnings"]})
    print(os.path.relpath(doc, cap), kind, stage, "ok" if out["ok"] else "FAIL", out["errors"], out["warnings"])
json.dump({"checked_on": "2026-11-10", "tool": tool,
           "note": "The capability page copies the approved shape of review-agent-work/capability.md: '## Directional intent' "
                   "with the detailed parts as '###' sections, so it is checked with --stage directional, as the BI-8 Argus page was. "
                   "Each feature page is checked with --stage detailed.",
           "results": results}, open(os.path.join(run, "checks", "lint.json"), "w"), indent=2)
sys.exit(0 if all(r["ok"] for r in results) else 1)
