#!/usr/bin/env python3
"""Run the structure check on every draft page of this capability and keep the results.

The capability is checked at both stages: the detailed stage the brief named, and the
directional stage its approved shape (ship-every-change, detail: directional in the spine) uses.
"""
import json, subprocess, sys, datetime
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
D = ".garura/project/issues/1021/context/bi-9-capability-2/drafts/product-os/software-delivery-planning/run-plays-as-loops"
SHAPE = ".garura/product/product-os/software-delivery-planning/ship-every-change/capability.md"
runs = [(f"{D}/capability.md", ["--kind", "capability", "--stage", "detailed"]),
        (f"{D}/capability.md", ["--kind", "capability", "--stage", "directional"]),
        (SHAPE, ["--kind", "capability", "--stage", "detailed"]),
        (SHAPE, ["--kind", "capability", "--stage", "directional"])]
for fn in ("fn-run-loop", "fn-check-loop-result", "fn-brief-open-points", "fn-show-run-status", "fn-loop-per-transition"):
    runs.append((f"{D}/{fn}/feature.md", ["--kind", "feature", "--stage", "detailed"]))
results = []
for doc, args in runs:
    out = subprocess.run([sys.executable, LINT, "--doc", doc, *args], capture_output=True, text=True)
    d = json.loads(out.stdout)
    results.append({"doc": doc, "args": args, "ok": d["ok"], "errors": d["errors"], "warnings": d["warnings"],
                    "note": "the approved shape page, for comparison" if doc == SHAPE else ""})
rec = {"checked_on": datetime.date.today().isoformat(), "tool": LINT,
       "first_run": "fn-show-run-status failed once on one short label bullet ('What it holds:'); it was written out and the check run again",
       "results": results}
json.dump(rec, open(".garura/project/issues/1021/context/bi-9-capability-2/checks/lint.json", "w"), indent=2)
for r in results:
    print(("ok  " if r["ok"] else "FAIL"), r["args"][-1], r["doc"].split("run-plays-as-loops/")[-1] if "run-plays" in r["doc"] else r["doc"], len(r["errors"]), "errors")
